# -*- coding: utf-8 -*-
"""
File Indexer - High-performance file search indexing system
"""
import os
import json
import time
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict


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
    
    def __hash__(self):
        """ハッシュ値を計算（pathで一意性を保証）"""
        return hash(self.path)
    
    def __eq__(self, other):
        """等価性をチェック（pathで比較）"""
        if not isinstance(other, FileEntry):
            return False
        return self.path == other.path


class TrieNode:
    """Trie構造のノード"""
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.entries: List[FileEntry] = []
        self.is_end_word = False


class FileIndexer:
    """高性能ファイル検索インデックスシステム"""
    
    INDEX_VERSION = "1.0.0"
    INDEX_FILE = "saved/file_index.json"
    
    def __init__(self):
        self.trie_root = TrieNode()
        self.entries_by_path: Dict[str, FileEntry] = {}
        self.entries_by_extension: Dict[str, List[FileEntry]] = defaultdict(list)
        self.workspaces: Dict[str, Dict[str, Any]] = {}
        self.index_metadata = {
            "version": self.INDEX_VERSION,
            "last_updated": 0,
            "total_files": 0,
            "total_folders": 0
        }
        
        # ファイル拡張子の優先度設定
        self.extension_priorities = {
            # ソースファイル（最高優先度）
            '.py': 100, '.cpp': 95, '.c': 95, '.h': 95, '.hpp': 95,
            '.js': 90, '.ts': 90, '.jsx': 90, '.tsx': 90,
            '.java': 85, '.cs': 85, '.go': 85, '.rs': 85,
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
        
        self.load_index()
    
    def add_entry_to_trie(self, entry: FileEntry) -> None:
        """Trieにエントリを追加"""
        # ファイル名でインデックス
        self._add_string_to_trie(entry.name.lower(), entry)
        
        # 拡張子なしのファイル名でもインデックス（ファイルの場合）
        if entry.type == 'file' and '.' in entry.name:
            name_without_ext = os.path.splitext(entry.name)[0].lower()
            if name_without_ext:
                self._add_string_to_trie(name_without_ext, entry)
        
        # パスの各部分でもインデックス
        path_parts = entry.relative_path.lower().split('/')
        for part in path_parts:
            if part and part != entry.name.lower():
                self._add_string_to_trie(part, entry)
    
    def _add_string_to_trie(self, string: str, entry: FileEntry) -> None:
        """文字列をTrieに追加"""
        if not string:
            return
            
        node = self.trie_root
        for char in string:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.entries.append(entry)
        
        node.is_end_word = True
    
    def search_by_prefix(self, prefix: str, max_results: int = 50) -> List[FileEntry]:
        """前方一致検索"""
        if not prefix:
            return []
        
        prefix_lower = prefix.lower()
        node = self.trie_root
        
        # プレフィックスまでのノードを辿る
        for char in prefix_lower:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # 見つかったエントリを収集
        entries = set()
        self._collect_entries(node, entries, max_results * 2)  # 重複除去のため多めに取得
        
        # 重複除去とスコアリング
        unique_entries = {}
        for entry in entries:
            if entry.path not in unique_entries:
                unique_entries[entry.path] = entry
        
        # スコアリングして上位結果を返す
        scored_entries = []
        for entry in unique_entries.values():
            score = self._calculate_relevance_score(prefix, entry)
            scored_entries.append((score, entry))
        
        # スコア順でソート
        scored_entries.sort(key=lambda x: x[0], reverse=True)
        
        return [entry for _, entry in scored_entries[:max_results]]
    
    def _collect_entries(self, node: TrieNode, entries: Set[FileEntry], max_count: int) -> None:
        """ノード以下のエントリを再帰的に収集"""
        if len(entries) >= max_count:
            return
        
        entries.update(node.entries)
        
        for child in node.children.values():
            if len(entries) >= max_count:
                break
            self._collect_entries(child, entries, max_count)
    
    def _calculate_relevance_score(self, query: str, entry: FileEntry) -> float:
        """関連度スコア計算"""
        score = 0.0
        query_lower = query.lower()
        name_lower = entry.name.lower()
        relative_path_lower = entry.relative_path.lower()
        
        # フォルダの場合は少しボーナス点
        if entry.type == 'folder':
            score += 5
        
        # 拡張子による基本スコア
        base_score = self.extension_priorities.get(entry.extension, 30)
        score += base_score
        
        # 完全一致（最高スコア）
        if query_lower == name_lower:
            score += 1000
        
        # 拡張子なしでの完全一致
        if entry.type == 'file' and '.' in entry.name:
            name_without_ext = os.path.splitext(name_lower)[0]
            if query_lower == name_without_ext:
                score += 950
        
        # 名前の開始位置での一致
        if name_lower.startswith(query_lower):
            score += 500
        
        # 単語境界での一致
        if query_lower in name_lower:
            # 単語の境界でのマッチング
            import re
            if re.search(r'\b' + re.escape(query_lower), name_lower):
                score += 300
            else:
                score += 200
        
        # パスに含まれる
        if query_lower in relative_path_lower:
            score += 100
        
        # ファイルサイズ（適度なサイズを優先）
        if entry.type == 'file':
            if 1000 < entry.size < 1000000:  # 1KB - 1MB
                score += 10
            elif entry.size > 10000000:  # 10MB以上は少し減点
                score -= 20
        
        # 深さによる調整（浅い方が高スコア）
        depth = relative_path_lower.count('/')
        score -= depth * 3
        
        # 最近更新されたファイルを優先
        days_old = (time.time() - entry.modified_time) / (24 * 3600)
        if days_old < 7:
            score += 20
        elif days_old < 30:
            score += 10
        
        return score
    
    def add_workspace_files(self, workspace_name: str, workspace_path: str, 
                          progress_callback=None) -> Tuple[int, int]:
        """ワークスペースのファイルをインデックスに追加"""
        if not os.path.exists(workspace_path):
            return 0, 0
        
        files_count = 0
        folders_count = 0
        processed_count = 0
        
        # まず総ファイル数を概算（プログレス表示用）
        estimated_total = self._estimate_file_count(workspace_path)
        
        for root, dirs, files in os.walk(workspace_path):
            # 除外ディレクトリをフィルタ
            dirs[:] = [d for d in dirs if not d.startswith('.') or d == '.claude']
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            # フォルダを追加
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                relative_path = os.path.relpath(dir_path, workspace_path)
                
                try:
                    stat = os.stat(dir_path)
                    entry = FileEntry(
                        name=dir_name,
                        path=dir_path,
                        relative_path=relative_path,
                        workspace=workspace_name,
                        type='folder',
                        size=0,
                        modified_time=stat.st_mtime,
                        extension=''
                    )
                    
                    self.add_entry_to_trie(entry)
                    self.entries_by_path[dir_path] = entry
                    folders_count += 1
                    
                except (OSError, PermissionError):
                    continue
            
            # ファイルを追加
            for file_name in files:
                if file_name.startswith('.'):
                    continue
                
                file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(file_path, workspace_path)
                file_ext = os.path.splitext(file_name)[1].lower()
                
                # 除外拡張子をスキップ
                if file_ext in self.excluded_extensions:
                    continue
                
                try:
                    stat = os.stat(file_path)
                    
                    # 大きすぎるファイルをスキップ（100MB以上）
                    if stat.st_size > 100 * 1024 * 1024:
                        continue
                    
                    entry = FileEntry(
                        name=file_name,
                        path=file_path,
                        relative_path=relative_path,
                        workspace=workspace_name,
                        type='file',
                        size=stat.st_size,
                        modified_time=stat.st_mtime,
                        extension=file_ext
                    )
                    
                    self.add_entry_to_trie(entry)
                    self.entries_by_path[file_path] = entry
                    self.entries_by_extension[file_ext].append(entry)
                    files_count += 1
                    
                except (OSError, PermissionError):
                    continue
                
                processed_count += 1
                if progress_callback and processed_count % 100 == 0:
                    progress = min(processed_count / max(estimated_total, 1) * 100, 100)
                    progress_callback(progress, f"Indexing: {file_name}")
        
        # ワークスペース情報を保存
        self.workspaces[workspace_path] = {
            'name': workspace_name,
            'path': workspace_path,
            'files_count': files_count,
            'folders_count': folders_count,
            'last_indexed': time.time()
        }
        
        return files_count, folders_count
    
    def _estimate_file_count(self, workspace_path: str) -> int:
        """ファイル数を概算（高速化のため深さ制限あり）"""
        count = 0
        max_depth = 3
        
        for root, dirs, files in os.walk(workspace_path):
            depth = root[len(workspace_path):].count(os.sep)
            if depth >= max_depth:
                dirs[:] = []  # それ以上深く行かない
                continue
            
            dirs[:] = [d for d in dirs if not d.startswith('.') or d == '.claude']
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            count += len([f for f in files if not f.startswith('.')])
            
            if count > 50000:  # 概算なので上限を設ける
                return 50000
        
        return max(count * 4, 1000)  # 深い階層を考慮して係数をかける
    
    def remove_workspace(self, workspace_path: str) -> None:
        """ワークスペースをインデックスから削除"""
        if workspace_path in self.workspaces:
            del self.workspaces[workspace_path]
        
        # エントリを削除（効率的ではないが、完全再構築を避けるため）
        paths_to_remove = [
            path for path, entry in self.entries_by_path.items()
            if entry.path.startswith(workspace_path)
        ]
        
        for path in paths_to_remove:
            entry = self.entries_by_path[path]
            if entry.extension in self.entries_by_extension:
                self.entries_by_extension[entry.extension] = [
                    e for e in self.entries_by_extension[entry.extension]
                    if e.path != path
                ]
            del self.entries_by_path[path]
        
        # Trieの完全再構築（効率的ではないが確実）
        self._rebuild_trie()
    
    def _rebuild_trie(self) -> None:
        """Trieを完全再構築"""
        self.trie_root = TrieNode()
        for entry in self.entries_by_path.values():
            self.add_entry_to_trie(entry)
    
    def clear_index(self) -> None:
        """インデックスをクリア"""
        self.trie_root = TrieNode()
        self.entries_by_path.clear()
        self.entries_by_extension.clear()
        self.workspaces.clear()
        self.index_metadata = {
            "version": self.INDEX_VERSION,
            "last_updated": 0,
            "total_files": 0,
            "total_folders": 0
        }
    
    def save_index(self) -> None:
        """インデックスを永続化"""
        try:
            # ディレクトリを作成
            os.makedirs(os.path.dirname(self.INDEX_FILE), exist_ok=True)
            
            # メタデータを更新
            self.index_metadata.update({
                "last_updated": time.time(),
                "total_files": sum(1 for e in self.entries_by_path.values() if e.type == 'file'),
                "total_folders": sum(1 for e in self.entries_by_path.values() if e.type == 'folder')
            })
            
            # データ準備
            data = {
                "metadata": self.index_metadata,
                "workspaces": self.workspaces,
                "entries": [asdict(entry) for entry in self.entries_by_path.values()]
            }
            
            # JSON保存
            with open(self.INDEX_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"インデックス保存エラー: {e}")
    
    def load_index(self) -> bool:
        """インデックスを読み込み"""
        try:
            if not os.path.exists(self.INDEX_FILE):
                return False
            
            with open(self.INDEX_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # バージョンチェック
            if data.get("metadata", {}).get("version") != self.INDEX_VERSION:
                print("インデックスバージョンが異なるため、再構築が必要です")
                return False
            
            self.index_metadata = data.get("metadata", {})
            self.workspaces = data.get("workspaces", {})
            
            # エントリを復元
            entries_data = data.get("entries", [])
            for entry_dict in entries_data:
                entry = FileEntry(**entry_dict)
                self.entries_by_path[entry.path] = entry
                self.entries_by_extension[entry.extension].append(entry)
                self.add_entry_to_trie(entry)
            
            print(f"インデックス読み込み完了: {len(self.entries_by_path)} エントリ")
            return True
            
        except Exception as e:
            print(f"インデックス読み込みエラー: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """インデックス統計情報を取得"""
        file_count = sum(1 for e in self.entries_by_path.values() if e.type == 'file')
        folder_count = sum(1 for e in self.entries_by_path.values() if e.type == 'folder')
        
        return {
            "total_entries": len(self.entries_by_path),
            "files": file_count,
            "folders": folder_count,
            "workspaces": len(self.workspaces),
            "last_updated": self.index_metadata.get("last_updated", 0),
            "extensions": len(self.entries_by_extension)
        }
    
    def is_index_valid_for_workspaces(self, workspace_list: List[Dict[str, str]]) -> bool:
        """指定されたワークスペースリストに対してインデックスが有効かどうかをチェック"""
        if not self.entries_by_path:
            # インデックスが空の場合は無効
            return False
        
        # ワークスペースパスのセットを作成
        current_workspace_paths = set(ws['path'] for ws in workspace_list)
        indexed_workspace_paths = set(self.workspaces.keys())
        
        # ワークスペースが一致しない場合は無効
        if current_workspace_paths != indexed_workspace_paths:
            return False
        
        # 各ワークスペースが存在し、大きな変更がないかチェック
        for workspace in workspace_list:
            workspace_path = workspace['path']
            
            # ワークスペースディレクトリが存在するかチェック
            if not os.path.exists(workspace_path):
                return False
            
            # インデックスされたワークスペース情報を取得
            if workspace_path not in self.workspaces:
                return False
        
        # 最後の更新から24時間以内であれば有効とみなす
        last_updated = self.index_metadata.get("last_updated", 0)
        if last_updated == 0:
            return False
        
        current_time = time.time()
        hours_since_update = (current_time - last_updated) / 3600
        
        # 24時間以内なら有効
        return hours_since_update < 24
    
    def needs_workspace_indexing(self, workspace_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """インデックスが必要なワークスペースのリストを返す"""
        if not self.is_index_valid_for_workspaces(workspace_list):
            # インデックス全体が無効な場合は全ワークスペースを返す
            return workspace_list
        
        # 部分的な更新が必要なワークスペースをチェック
        workspaces_to_index = []
        
        for workspace in workspace_list:
            workspace_path = workspace['path']
            
            # 新しいワークスペースかチェック
            if workspace_path not in self.workspaces:
                workspaces_to_index.append(workspace)
                continue
            
            # ワークスペース内のファイル数が大きく変わっていないかチェック
            try:
                # 簡単なファイル数チェック（詳細なチェックはしない）
                current_file_count = 0
                for root, dirs, files in os.walk(workspace_path):
                    # 除外ディレクトリをスキップ
                    dirs[:] = [d for d in dirs if (not d.startswith('.') or d == '.claude') and d not in self.excluded_dirs]
                    current_file_count += len([f for f in files if not f.startswith('.')])
                    
                    # 100件以上カウントしたら打ち切り（概算で十分）
                    if current_file_count > 100:
                        break
                
                indexed_info = self.workspaces[workspace_path]
                indexed_file_count = indexed_info.get('files_count', 0)
                
                # ファイル数が大きく変わっている場合（50%以上の差）
                if abs(current_file_count - indexed_file_count) > max(indexed_file_count * 0.5, 10):
                    workspaces_to_index.append(workspace)
                    
            except Exception:
                # エラーが発生した場合は安全のため再インデックス
                workspaces_to_index.append(workspace)
        
        return workspaces_to_index