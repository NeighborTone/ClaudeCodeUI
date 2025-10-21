# -*- coding: utf-8 -*-
"""
SQLite File Indexer - High-performance SQLite-based file search indexing system
"""
import os
import sqlite3
import json
import time
import threading
from typing import Dict, List, Set, Optional, Tuple, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict
import hashlib

from src.core.sqlite_persistent_connection import SQLitePersistentConnection
from src.core.logger import logger


@dataclass
class FileEntry:
    """ファイル・フォルダエントリ"""
    name: str
    path: str
    relative_path: str
    workspace: str
    type: str  # 'file' or 'folder'
    size: int
    modified_time: float
    extension: str
    path_hash: str = ""  # パスのハッシュ値（主キー用）
    
    def __post_init__(self):
        if not self.path_hash:
            self.path_hash = hashlib.md5(self.path.encode('utf-8')).hexdigest()


class SQLiteIndexer:
    """高性能SQLiteベースファイル検索インデックスシステム"""

    INDEX_VERSION = "2.0.0"
    INDEX_FILE = "saved/file_index.db"

    # クエリ定数（プリペアドステートメントの基礎）
    QUERY_PREFIX_SEARCH_LIKE = """
        SELECT * FROM file_entries
        WHERE name LIKE ? OR relative_path LIKE ?
        ORDER BY CASE WHEN type = 'folder' THEN 0 ELSE 1 END,
                 priority DESC,
                 length(name)
        LIMIT ?
    """

    QUERY_FTS5_SEARCH = """
        SELECT fe.* FROM file_entries fe
        JOIN file_search fs ON fe.rowid = fs.rowid
        WHERE file_search MATCH ?
        ORDER BY CASE WHEN fe.type = 'folder' THEN 0 ELSE 1 END,
                 fe.priority DESC,
                 length(fe.name)
        LIMIT ?
    """

    QUERY_LIKE_SEARCH = """
        SELECT * FROM file_entries
        WHERE (name LIKE ? OR relative_path LIKE ?)
        ORDER BY CASE WHEN type = 'folder' THEN 0 ELSE 1 END,
                 priority DESC,
                 length(name)
        LIMIT ?
    """

    def __init__(self):
        self.db_path = self.INDEX_FILE
        self._connection_manager = SQLitePersistentConnection()
        self.connection = None
        self._lock = threading.RLock()

        # プリペアドステートメントキャッシュ
        self._prepared_statements = {}

        # ファイル拡張子の優先度設定
        self.extension_priorities = {
            # ソースファイル（最高優先度）- C++とC#を最優先
            '.cpp': 110, '.c': 110, '.h': 110, '.hpp': 110, '.cxx': 110, '.hxx': 110,
            '.cs': 105,  # C#を第二優先
            '.py': 100, 
            '.js': 90, '.ts': 90, '.jsx': 90, '.tsx': 90,
            '.java': 85, '.go': 85, '.rs': 85,
            '.php': 80, '.rb': 80, '.swift': 80, '.kt': 80,
            
            # 設定・データファイル（高優先度）
            '.json': 70, '.yaml': 70, '.yml': 70, '.xml': 70,
            '.toml': 70, '.ini': 65, '.conf': 65, '.cfg': 65,
            '.csv': 60, '.txt': 60, '.md': 60, '.rst': 60,
            
            # ビルドファイル（中優先度）
            '.cmake': 50, '.make': 50, '.gradle': 50,
            '.sln': 50, '.vcxproj': 50, '.pro': 50,
            
            # 画像・メディアファイル（低優先度）
            '.png': 20, '.jpg': 20, '.jpeg': 20, '.gif': 20,
            '.wav': 10, '.mp3': 10, '.mp4': 10, '.avi': 10,
        }
        
        # 除外するディレクトリ
        self.excluded_dirs = {
            'node_modules', '__pycache__', 'Binaries', 'Intermediate',
            'Saved', 'DerivedDataCache', '.vs', 'obj', 'bin', '.git',
            '.svn', '.hg', 'build', 'dist', 'out'
        }
        
        # 除外するファイル拡張子
        self.excluded_extensions = {
            '.exe', '.dll', '.so', '.dylib', '.lib', '.a', '.o', '.obj',
            '.class', '.jar', '.war', '.pdb', '.idb', '.tmp', '.temp',
            '.log', '.cache', '.lock'
        }
        
        self._initialize_database()
    
    def _initialize_database(self):
        """データベースを初期化"""
        try:
            # ディレクトリを作成
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            with self._lock:
                self.connection = self._connection_manager.connect(self.db_path)
                
                # テーブル作成
                self._create_tables()
                
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def _get_prepared_stmt(self, query_name: str) -> str:
        """
        プリペアドステートメント（クエリ文字列）を取得

        Python sqlite3ではプリペアドステートメントを明示的にキャッシュできないため、
        クエリ文字列の参照を一元管理することで、コードの重複を削減し保守性を向上させる。

        Args:
            query_name: クエリ名（'prefix_search_like', 'fts5_search', 'like_search'）

        Returns:
            クエリ文字列
        """
        query_map = {
            'prefix_search_like': self.QUERY_PREFIX_SEARCH_LIKE,
            'fts5_search': self.QUERY_FTS5_SEARCH,
            'like_search': self.QUERY_LIKE_SEARCH,
        }

        if query_name not in query_map:
            logger.warning(f"Unknown query name: {query_name}")
            return ""

        return query_map[query_name]

    def _execute_search_query(
        self,
        query_type: str,
        params: tuple,
        use_fts5: bool = True,
        fallback_to_like: bool = True
    ) -> List[Dict]:
        """
        統一的なクエリ実行ヘルパーメソッド

        FTS5とLIKEの両方をサポートし、エラーハンドリングを一元化する。

        Args:
            query_type: クエリタイプ（'fts5_search', 'like_search', 'prefix_search_like'）
            params: クエリパラメータ
            use_fts5: FTS5を使用するかどうか（デフォルト: True）
            fallback_to_like: FTS5エラー時にLIKEにフォールバックするかどうか（デフォルト: True）

        Returns:
            クエリ結果のリスト（辞書形式）
        """
        results = []

        try:
            # クエリを取得
            query = self._get_prepared_stmt(query_type)
            if not query:
                logger.warning(f"Invalid query type: {query_type}")
                return results

            # クエリを実行
            cursor = self.connection.execute(query, params)

            # 結果を収集
            for row in cursor:
                results.append(dict(row))

        except Exception as e:
            # FTS5エラーの場合
            if "fts5" in str(e).lower() or "no such column" in str(e).lower():
                logger.debug(f"FTS5 search error: {e}")

                # LIKEフォールバックが有効な場合
                if fallback_to_like and query_type == 'fts5_search':
                    logger.debug("Falling back to LIKE search")
                    # LIKEにフォールバックするのは呼び出し元の責任
                    pass
            else:
                # その他のエラー
                logger.error(f"Query execution error ({query_type}): {e}")

        return results

    def _execute_fts5_search_safe(
        self,
        query_string: str,
        max_results: int,
        existing_paths: Optional[Set[str]] = None
    ) -> List[Dict]:
        """
        FTS5検索を安全に実行（エラーハンドリング付き）

        Args:
            query_string: FTS5クエリ文字列（エスケープ済み）
            max_results: 最大結果数
            existing_paths: 既存のパスセット（重複除去用、オプション）

        Returns:
            クエリ結果のリスト（辞書形式）
        """
        results = []

        if not query_string:
            return results

        try:
            # FTS5クエリをエスケープ
            escaped_query = self._escape_fts5_query(query_string)

            if not escaped_query:
                logger.debug("FTS5 query escaping failed")
                return results

            # FTS5検索を実行
            query_results = self._execute_search_query(
                'fts5_search',
                (escaped_query, max_results),
                use_fts5=True,
                fallback_to_like=False
            )

            # 重複除去（必要に応じて）
            if existing_paths is not None:
                for row in query_results:
                    if row['path'] not in existing_paths:
                        existing_paths.add(row['path'])
                        results.append(row)
            else:
                results = query_results

        except Exception as e:
            logger.debug(f"FTS5 safe search error: {e}")

        return results

    def _create_tables(self):
        """必要なテーブルを作成"""
        with self.connection:
            # メタデータテーブル
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            
            # ワークスペーステーブル
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS workspaces (
                    path TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    files_count INTEGER DEFAULT 0,
                    folders_count INTEGER DEFAULT 0,
                    last_indexed REAL DEFAULT 0
                )
            """)
            
            # ファイルエントリテーブル
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS file_entries (
                    path_hash TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    path TEXT UNIQUE NOT NULL,
                    relative_path TEXT NOT NULL,
                    workspace TEXT NOT NULL,
                    type TEXT NOT NULL,
                    size INTEGER DEFAULT 0,
                    modified_time REAL DEFAULT 0,
                    extension TEXT DEFAULT '',
                    priority INTEGER DEFAULT 0
                )
            """)
            
            # FTS5仮想テーブル（高速全文検索用）
            self.connection.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS file_search USING fts5(
                    name,
                    path,
                    relative_path,
                    extension,
                    workspace,
                    content=file_entries,
                    content_rowid=rowid
                )
            """)
            
            # インデックス作成
            self.connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_extension ON file_entries(extension)
            """)
            self.connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_workspace ON file_entries(workspace)
            """)
            self.connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_type ON file_entries(type)
            """)
            self.connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_priority ON file_entries(priority DESC)
            """)
            
            # バージョン情報を保存
            self.connection.execute("""
                INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)
            """, ("version", self.INDEX_VERSION))
    
    def search_by_prefix(self, prefix: str, max_results: int = 50) -> List[FileEntry]:
        """前方一致検索（SQLite FTS5使用 - クエリ実行一本化版）"""
        if not prefix:
            return []

        try:
            with self._lock:
                # 1. LIKE検索を実行（前方一致）
                like_results = self._execute_search_query(
                    'prefix_search_like',
                    (f"{prefix}%", f"%{prefix}%", max_results)
                )

                # 2. FTS5検索を実行（エラーハンドリング付き）
                existing_paths = set(row['path'] for row in like_results)
                fts5_results = []

                if len(like_results) < max_results:
                    fts5_results = self._execute_fts5_search_safe(
                        prefix,
                        max_results - len(like_results),
                        existing_paths
                    )

                # 3. 結果を統合
                all_rows = like_results + fts5_results

                # 4. FileEntryオブジェクトに変換
                file_entries = []
                for row in all_rows[:max_results]:
                    entry = FileEntry(
                        name=row['name'],
                        path=row['path'],
                        relative_path=row['relative_path'],
                        workspace=row['workspace'],
                        type=row['type'],
                        size=row['size'],
                        modified_time=row['modified_time'],
                        extension=row['extension'],
                        path_hash=row['path_hash']
                    )
                    file_entries.append(entry)

                return file_entries

        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def search_fuzzy(self, query: str, max_results: int = 50) -> List[FileEntry]:
        """ファジー検索（部分一致を含む） - クエリ実行一本化版"""
        if not query:
            return []

        try:
            with self._lock:
                all_results = []
                seen_paths = set()

                # 1. FTS5検索を実行（エラーハンドリング付き）
                fts5_results = self._execute_fts5_search_safe(
                    query,
                    max_results,
                    seen_paths
                )

                # 2. FTS5結果をFileEntryオブジェクトに変換
                for row in fts5_results:
                    entry = FileEntry(
                        name=row['name'],
                        path=row['path'],
                        relative_path=row['relative_path'],
                        workspace=row['workspace'],
                        type=row['type'],
                        size=row['size'],
                        modified_time=row['modified_time'],
                        extension=row['extension'],
                        path_hash=row['path_hash']
                    )
                    all_results.append(entry)

                # 3. FTS5で十分な結果が得られなかった場合、LIKE検索で補完
                if len(all_results) < max_results:
                    like_results = self._search_with_like(query, max_results - len(all_results), seen_paths)
                    all_results.extend(like_results)

                return all_results

        except Exception as e:
            logger.error(f"Fuzzy search error: {e}")
            return []
    
    def add_workspace_files(self, workspace_name: str, workspace_path: str, 
                          progress_callback: Optional[Callable] = None) -> Tuple[int, int]:
        """ワークスペースのファイルをインデックスに追加（高速化版）"""
        if not os.path.exists(workspace_path):
            return 0, 0
        
        files_count = 0
        folders_count = 0
        processed_count = 0
        
        # バッチ処理用のリスト
        file_entries = []
        batch_size = 1000
        
        try:
            with self._lock:
                # 既存のワークスペースエントリを削除
                self.connection.execute("""
                    DELETE FROM file_entries WHERE workspace = ?
                """, (workspace_name,))
                
                # まず総ファイル数を概算
                estimated_total = self._estimate_file_count(workspace_path)
                
                for root, dirs, files in os.walk(workspace_path):
                    # 除外ディレクトリをフィルタ
                    dirs[:] = [d for d in dirs if not d.startswith('.') or d == '.claude']
                    dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
                    
                    # フォルダを追加
                    for dir_name in dirs:
                        dir_path = os.path.join(root, dir_name)

                        try:
                            # パスの相対化を試行
                            try:
                                relative_path = os.path.relpath(dir_path, workspace_path)
                            except (ValueError, OSError) as e:
                                # 異なるドライブや特殊パスの場合はスキップ
                                logger.debug(f"Skipping folder with invalid path: {dir_path} ({e})")
                                continue

                            stat = os.stat(dir_path)
                            priority = 80  # フォルダの基本優先度（ファイルより高い優先度）

                            file_entries.append((
                                hashlib.md5(dir_path.encode('utf-8')).hexdigest(),
                                dir_name, dir_path, relative_path, workspace_name,
                                'folder', 0, stat.st_mtime, '', priority
                            ))

                            folders_count += 1

                        except (OSError, PermissionError):
                            continue
                    
                    # ファイルを追加
                    for file_name in files:
                        if file_name.startswith('.'):
                            continue

                        file_path = os.path.join(root, file_name)

                        # パスの相対化を試行
                        try:
                            relative_path = os.path.relpath(file_path, workspace_path)
                        except (ValueError, OSError) as e:
                            # 異なるドライブや特殊パスの場合はスキップ
                            logger.debug(f"Skipping file with invalid path: {file_path} ({e})")
                            continue

                        file_ext = os.path.splitext(file_name)[1].lower()

                        # 除外拡張子をスキップ
                        if file_ext in self.excluded_extensions:
                            continue

                        try:
                            stat = os.stat(file_path)

                            # 大きすぎるファイルをスキップ（100MB以上）
                            if stat.st_size > 100 * 1024 * 1024:
                                continue

                            priority = self.extension_priorities.get(file_ext, 30)

                            file_entries.append((
                                hashlib.md5(file_path.encode('utf-8')).hexdigest(),
                                file_name, file_path, relative_path, workspace_name,
                                'file', stat.st_size, stat.st_mtime, file_ext, priority
                            ))

                            files_count += 1

                        except (OSError, PermissionError):
                            continue
                        
                        processed_count += 1
                        
                        # バッチ処理
                        if len(file_entries) >= batch_size:
                            self._insert_batch(file_entries)
                            file_entries.clear()
                        
                        if progress_callback and processed_count % 100 == 0:
                            progress = min(processed_count / max(estimated_total, 1) * 100, 100)
                            progress_callback(progress, f"Indexing: {file_name}")
                
                # 残りのエントリを挿入
                if file_entries:
                    self._insert_batch(file_entries)
                
                # ワークスペース情報を保存
                self.connection.execute("""
                    INSERT OR REPLACE INTO workspaces 
                    (path, name, files_count, folders_count, last_indexed)
                    VALUES (?, ?, ?, ?, ?)
                """, (workspace_path, workspace_name, files_count, folders_count, time.time()))
                
                # Update FTS5 index
                self.connection.execute("INSERT INTO file_search(file_search) VALUES('rebuild')")
                
                self.connection.commit()
                
        except Exception as e:
            logger.error(f"Workspace addition error: {e}")
            self.connection.rollback()
        
        return files_count, folders_count
    
    def _insert_batch(self, file_entries: List[Tuple]):
        """バッチでファイルエントリを挿入"""
        self.connection.executemany("""
            INSERT OR REPLACE INTO file_entries 
            (path_hash, name, path, relative_path, workspace, type, size, modified_time, extension, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, file_entries)
    
    def _estimate_file_count(self, workspace_path: str) -> int:
        """ファイル数を概算（高速化のため深さ制限あり）"""
        count = 0
        max_depth = 3
        
        for root, dirs, files in os.walk(workspace_path):
            depth = root[len(workspace_path):].count(os.sep)
            if depth >= max_depth:
                dirs[:] = []
                continue
            
            dirs[:] = [d for d in dirs if not d.startswith('.') or d == '.claude']
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            count += len([f for f in files if not f.startswith('.')])
            
            if count > 50000:
                return 50000
        
        return max(count * 4, 1000)
    
    def remove_workspace(self, workspace_path: str) -> None:
        """ワークスペースをインデックスから削除"""
        try:
            with self._lock:
                # ワークスペース情報を取得
                cursor = self.connection.execute("""
                    SELECT name FROM workspaces WHERE path = ?
                """, (workspace_path,))
                row = cursor.fetchone()
                
                if row:
                    workspace_name = row['name']
                    
                    # ファイルエントリを削除
                    self.connection.execute("""
                        DELETE FROM file_entries WHERE workspace = ?
                    """, (workspace_name,))
                    
                    # ワークスペース情報を削除
                    self.connection.execute("""
                        DELETE FROM workspaces WHERE path = ?
                    """, (workspace_path,))
                    
                    # Update FTS5 index
                    self.connection.execute("INSERT INTO file_search(file_search) VALUES('rebuild')")
                    
                    self.connection.commit()
                    
        except Exception as e:
            logger.error(f"Workspace deletion error: {e}")
    
    def clear_index(self) -> None:
        """インデックスをクリア"""
        try:
            with self._lock:
                self.connection.execute("DELETE FROM file_entries")
                self.connection.execute("DELETE FROM workspaces")
                self.connection.execute("INSERT INTO file_search(file_search) VALUES('rebuild')")
                self.connection.commit()
                
        except Exception as e:
            logger.error(f"Index clear error: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """インデックス統計情報を取得"""
        try:
            with self._lock:
                cursor = self.connection.execute("""
                    SELECT 
                        COUNT(*) as total_entries,
                        COUNT(CASE WHEN type = 'file' THEN 1 END) as files,
                        COUNT(CASE WHEN type = 'folder' THEN 1 END) as folders,
                        COUNT(DISTINCT workspace) as workspaces,
                        COUNT(DISTINCT extension) as extensions
                    FROM file_entries
                """)
                row = cursor.fetchone()
                
                # 最終更新時刻を取得
                cursor = self.connection.execute("""
                    SELECT MAX(last_indexed) as last_updated FROM workspaces
                """)
                time_row = cursor.fetchone()
                
                return {
                    "total_entries": row['total_entries'] if row else 0,
                    "files": row['files'] if row else 0,
                    "folders": row['folders'] if row else 0,
                    "workspaces": row['workspaces'] if row else 0,
                    "extensions": row['extensions'] if row else 0,
                    "last_updated": time_row['last_updated'] if time_row and time_row['last_updated'] else 0
                }
                
        except Exception as e:
            logger.error(f"Statistics retrieval error: {e}")
            return {
                "total_entries": 0, "files": 0, "folders": 0,
                "workspaces": 0, "extensions": 0, "last_updated": 0
            }
    
    def is_index_valid_for_workspaces(self, workspace_list: List[Dict[str, str]], debug: bool = False) -> bool:
        """指定されたワークスペースリストに対してインデックスが有効かどうかをチェック"""
        try:
            with self._lock:
                # 現在のワークスペースパスを取得
                cursor = self.connection.execute("SELECT path FROM workspaces")
                indexed_paths = set(row['path'] for row in cursor)
                
                current_paths = set(ws['path'] for ws in workspace_list)
                
                # ワークスペースが一致するかチェック
                if current_paths != indexed_paths:
                    if debug:
                        logger.debug(f"ワークスペース不一致")
                        logger.debug(f"  現在: {current_paths}")
                        logger.debug(f"  インデックス: {indexed_paths}")
                    return False
                
                if debug:
                    logger.debug("インデックス有効性チェック完了 - 有効")
                return True
                
        except Exception as e:
            if debug:
                logger.debug(f"インデックス妥当性チェックエラー: {e}")
            return False
    
    def needs_workspace_indexing(self, workspace_list: List[Dict[str, str]], debug: bool = False) -> List[Dict[str, str]]:
        """インデックスが必要なワークスペースのリストを返す"""
        if not self.is_index_valid_for_workspaces(workspace_list, debug):
            if debug:
                logger.debug("インデックス全体が無効 - 全ワークスペースを再構築")
            return workspace_list
        
        # SQLiteベースでは基本的に増分更新は複雑なので、簡単な存在チェックのみ
        workspaces_to_index = []
        
        try:
            with self._lock:
                for workspace in workspace_list:
                    workspace_path = workspace['path']
                    
                    cursor = self.connection.execute("""
                        SELECT files_count FROM workspaces WHERE path = ?
                    """, (workspace_path,))
                    row = cursor.fetchone()
                    
                    if not row:
                        if debug:
                            logger.debug(f"新しいワークスペース: {workspace_path}")
                        workspaces_to_index.append(workspace)
                        
        except Exception as e:
            if debug:
                logger.debug(f"ワークスペースチェックエラー: {e}")
            return workspace_list
        
        if debug:
            logger.debug(f"再インデックスが必要なワークスペース: {len(workspaces_to_index)}個")
        return workspaces_to_index
    
    def _escape_fts5_query(self, query: str) -> Optional[str]:
        """
        FTS5クエリの特殊文字を適切にエスケープ

        FTS5は以下の特殊文字を認識:
        - " (ダブルクォート): フレーズ検索
        - * (アスタリスク): ワイルドカード
        - AND, OR, NOT: 論理演算子

        戦略:
        1. 空文字列や無効な入力はNoneを返す
        2. ダブルクォートをエスケープ（""に置換）
        3. クエリ全体をダブルクォートで囲む
        4. 前方一致検索のための*を追加

        Returns:
            エスケープされたFTS5クエリ文字列、または無効な場合はNone
        """
        # 空文字列チェック
        if not query or not query.strip():
            return None

        # クエリをトリム
        query = query.strip()

        # 非常に長いクエリは拒否（パフォーマンス保護）
        if len(query) > 200:
            return None

        # FTS5予約語のチェック（大文字小文字を区別しない）
        fts5_keywords = ['AND', 'OR', 'NOT', 'NEAR']
        if query.upper() in fts5_keywords:
            # 予約語の場合はダブルクォートで囲む
            return f'"{query}"*'

        # ダブルクォートをエスケープ（" -> ""）
        escaped_query = query.replace('"', '""')

        # FTS5フレーズ検索構文: "query"*
        # ダブルクォートで囲むことで特殊文字を含む検索が可能
        # 末尾の*は前方一致を意味する
        return f'"{escaped_query}"*'
    
    def _search_with_like(self, query: str, max_results: int, seen_paths: set) -> List[FileEntry]:
        """
        LIKE演算子を使用したフォールバック検索 - プリペアドステートメント活用版
        """
        results = []

        try:
            # 複数の検索パターンを試行
            search_patterns = [
                f'{query}%',      # 前方一致
                f'%{query}%',     # 部分一致
                f'%{query}',      # 後方一致
            ]

            # プリペアドステートメントとして定義されたクエリを使用
            sql_query = self._get_prepared_stmt('like_search')

            for pattern in search_patterns:
                if len(results) >= max_results:
                    break

                cursor = self.connection.execute(
                    sql_query,
                    (pattern, pattern, max_results - len(results))
                )

                for row in cursor:
                    if row['path'] not in seen_paths and len(results) < max_results:
                        seen_paths.add(row['path'])
                        entry = FileEntry(
                            name=row['name'],
                            path=row['path'],
                            relative_path=row['relative_path'],
                            workspace=row['workspace'],
                            type=row['type'],
                            size=row['size'],
                            modified_time=row['modified_time'],
                            extension=row['extension'],
                            path_hash=row['path_hash']
                        )
                        results.append(entry)
            
        except Exception as e:
            logger.debug(f"LIKE検索エラー: {e}")
        
        return results
    
    def get_all_entries(self, entry_type: Optional[str] = None, extensions: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        全エントリ（ファイル/フォルダ）をSQLiteから取得

        Args:
            entry_type: エントリタイプ ('file', 'folder', またはNoneで全て)
            extensions: ファイル拡張子フィルタ（Noneの場合はフィルタなし）

        Returns:
            辞書形式のエントリリスト
        """
        results = []

        try:
            with self._lock:
                # クエリ構築
                query = "SELECT * FROM file_entries"
                params = []
                conditions = []

                # タイプフィルタ
                if entry_type:
                    conditions.append("type = ?")
                    params.append(entry_type)

                # 拡張子フィルタ
                if extensions:
                    placeholders = ','.join(['?' for _ in extensions])
                    conditions.append(f"extension IN ({placeholders})")
                    params.extend(extensions)

                # WHERE句を追加
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                # ORDER BY
                query += " ORDER BY CASE WHEN type = 'folder' THEN 0 ELSE 1 END, priority DESC, name"

                # 実行
                cursor = self.connection.execute(query, params)

                # 結果を収集（WorkspaceManagerとの互換性のため、キー名を調整）
                for row in cursor:
                    results.append({
                        'name': row['name'],
                        'path': row['path'],
                        'relative_path': row['relative_path'],
                        'workspace': row['workspace'],
                        'type': row['type'],
                        'size': row['size'],
                        'modified_time': row['modified_time'],
                        'extension': row['extension']
                    })

                logger.debug(f"get_all_entries: Retrieved {len(results)} entries (type={entry_type})")

        except Exception as e:
            logger.error(f"get_all_entries error: {e}")

        return results

    def close(self):
        """データベース接続を閉じる（持続的接続なので実際には閉じない）"""
        # プリペアドステートメントキャッシュをクリア
        self._prepared_statements.clear()

        # 持続的接続を使用しているため、実際には閉じない
        # 接続マネージャーが管理している
        pass