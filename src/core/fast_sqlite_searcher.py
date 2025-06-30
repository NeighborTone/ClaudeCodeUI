# -*- coding: utf-8 -*-
"""
Fast SQLite File Searcher - 高速SQLiteベースファイル検索
"""
import os
import re
import time
from typing import List, Dict, Tuple, Optional
from functools import lru_cache
from collections import OrderedDict

from src.core.sqlite_indexer import SQLiteIndexer, FileEntry
from src.core.path_converter import PathConverter
from src.core.logger import get_logger


class FastSQLiteSearcher:
    """高速SQLiteベースファイル検索クラス"""
    
    def __init__(self, sqlite_indexer: SQLiteIndexer):
        self.sqlite_indexer = sqlite_indexer
        self.max_results = 30  # オートコンプリート候補数上限を30に設定
        self._search_cache = OrderedDict()  # LRUキャッシュ
        self._cache_max_size = 100
        self._cache_ttl = 300  # 5分間のTTL
        self.logger = get_logger(__name__)
    
    def extract_file_mentions(self, text: str) -> List[Tuple[int, int, str]]:
        """
        テキストから@ファイル名の部分を抽出
        Returns: [(start_pos, end_pos, filename), ...]
        """
        mentions = []
        pattern = r'@([^\s@]+)'
        
        for match in re.finditer(pattern, text):
            start_pos = match.start()
            end_pos = match.end()
            filename = match.group(1)
            mentions.append((start_pos, end_pos, filename))
        
        return mentions
    
    def search_files_by_name(self, query: str) -> List[Dict[str, str]]:
        """
        ファイル・フォルダを名前で検索（高速SQLite検索使用）
        """
        if not query:
            return []
        
        # キャッシュをチェック
        cache_key = f"search_{query}_{self.max_results}"
        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            return cached_result
        
        start_time = time.time()
        
        # 前方一致検索を実行
        entries = self.sqlite_indexer.search_by_prefix(query, self.max_results)
        
        # 結果が少ない場合は部分一致検索も実行
        if len(entries) < self.max_results // 2:
            try:
                fuzzy_entries = self.sqlite_indexer.search_fuzzy(query, self.max_results - len(entries))
                
                # 重複を除去してマージ
                existing_paths = set(entry.path for entry in entries)
                for fuzzy_entry in fuzzy_entries:
                    if fuzzy_entry.path not in existing_paths:
                        entries.append(fuzzy_entry)
                        existing_paths.add(fuzzy_entry.path)
                        if len(entries) >= self.max_results:
                            break
            except AttributeError:
                # search_fuzzyメソッドが存在しない場合はスキップ
                pass
        
        # スコアリングして並び替え
        scored_entries = []
        for entry in entries:
            score = self._calculate_relevance_score(query, entry)
            scored_entries.append((score, entry))
        
        # スコア順でソート
        scored_entries.sort(key=lambda x: x[0], reverse=True)
        
        # 結果を従来の形式に変換
        results = []
        folders_count = 0
        files_count = 0
        
        for score, entry in scored_entries[:self.max_results]:
            result = {
                'name': entry.name,
                'path': entry.path,
                'relative_path': entry.relative_path,
                'workspace': entry.workspace,
                'type': entry.type,
                'score': score  # デバッグ用スコア
            }
            results.append(result)
            
            if entry.type == 'folder':
                folders_count += 1
            else:
                files_count += 1
        
        search_time = time.time() - start_time
        
        # 結果をキャッシュ
        self._add_to_cache(cache_key, results)
        
        return results
    
    def search_files_only_by_name(self, query: str) -> List[Dict[str, str]]:
        """
        ファイルのみを名前で検索（$ パターン用）
        """
        if not query:
            return []
        
        # 全件検索してからフィルタリング
        all_results = self.search_files_by_name(query)
        
        # ファイルのみをフィルタリング
        files_only = [result for result in all_results if result.get('type') == 'file']
        
        return files_only
    
    def search_folders_only_by_name(self, query: str) -> List[Dict[str, str]]:
        """
        フォルダのみを名前で検索（# パターン用）
        """
        if not query:
            return []
        
        # 全件検索してからフィルタリング
        all_results = self.search_files_by_name(query)
        
        # フォルダのみをフィルタリング
        folders_only = [result for result in all_results if result.get('type') == 'folder']
        
        return folders_only
    
    def _calculate_relevance_score(self, query: str, entry: FileEntry) -> float:
        """関連度スコア計算（改良版）"""
        score = 0.0
        query_lower = query.lower()
        name_lower = entry.name.lower()
        relative_path_lower = entry.relative_path.lower()
        
        # 基本スコア（拡張子の優先度）
        base_score = self.sqlite_indexer.extension_priorities.get(entry.extension, 30)
        score += base_score / 10  # 基本スコアを調整
        
        # フォルダの場合は高優先度ボーナス（ファイルと同等以上にする）
        if entry.type == 'folder':
            score += 50  # フォルダに大幅なボーナス点を与える
        
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
                score += 20
            elif entry.size > 10000000:  # 10MB以上は少し減点
                score -= 30
        
        # 深さによる調整（浅い方が高スコア）
        depth = relative_path_lower.count('/')
        score -= depth * 5
        
        # 最近更新されたファイルを優先
        days_old = (time.time() - entry.modified_time) / (24 * 3600)
        if days_old < 7:
            score += 30
        elif days_old < 30:
            score += 15
        
        # 文字列の長さでの調整（短い名前を優先）
        score -= len(entry.name) * 0.1
        
        return score
    
    def get_file_content_preview(self, file_path: str, max_lines: int = 10) -> str:
        """ファイルの内容のプレビューを取得"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        lines.append("...")
                        break
                    lines.append(line.rstrip())
                return '\n'.join(lines)
        except Exception as e:
            return f"ファイル読み込みエラー: {e}"
    
    def resolve_file_mentions(self, text: str) -> Dict[str, List[Dict[str, str]]]:
        """
        テキスト内の@ファイル名をすべて解決
        Returns: {filename: [matching_files], ...}
        """
        mentions = self.extract_file_mentions(text)
        resolved = {}
        
        for _, _, filename in mentions:
            if filename not in resolved:
                matches = self.search_files_by_name(filename)
                resolved[filename] = matches
        
        return resolved
    
    def replace_file_mentions_with_content(self, text: str, selected_files: Dict[str, str]) -> str:
        """
        @ファイル名をファイルの内容に置換
        selected_files: {filename: selected_file_path}
        """
        mentions = self.extract_file_mentions(text)
        
        # 後ろから置換（位置がずれないように）
        for start_pos, end_pos, filename in reversed(mentions):
            if filename in selected_files:
                file_path = selected_files[filename]
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()
                    
                    replacement = f"ファイル: {os.path.basename(file_path)}\n```\n{file_content}\n```"
                    text = text[:start_pos] + replacement + text[end_pos:]
                except Exception as e:
                    replacement = f"[ファイル読み込みエラー: {filename} - {e}]"
                    text = text[:start_pos] + replacement + text[end_pos:]
        
        return text
    
    def get_completion_suggestions(self, partial_filename: str) -> List[str]:
        """部分的なファイル名から補完候補を取得（高速化版）"""
        if not partial_filename:
            return []
        
        # キャッシュをチェック
        cache_key = f"completion_{partial_filename}"
        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            return cached_result
        
        matches = self.search_files_by_name(partial_filename)
        suggestions = []
        
        for file_info in matches[:10]:  # 上位10件
            # ファイル名（拡張子なし）
            name_without_ext = os.path.splitext(file_info['name'])[0]
            if name_without_ext not in suggestions:
                suggestions.append(name_without_ext)
            
            # ファイル名（拡張子込み）
            if file_info['name'] not in suggestions:
                suggestions.append(file_info['name'])
        
        # 結果をキャッシュ
        self._add_to_cache(cache_key, suggestions[:8])
        
        return suggestions[:8]  # 上位8件
    
    def get_quick_suggestions(self, partial_filename: str) -> List[Dict[str, str]]:
        """
        クイック補完候補を取得（UIで使用）
        より詳細な情報を返す
        """
        if not partial_filename:
            return []
        
        matches = self.search_files_by_name(partial_filename)
        
        suggestions = []
        for match in matches[:10]:
            suggestion = {
                'name': match['name'],
                'relative_path': match['relative_path'],
                'type': match['type'],
                'workspace': match['workspace'],
                'display_name': self._get_display_name(match)
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _get_display_name(self, file_info: Dict[str, str]) -> str:
        """表示用の名前を生成"""
        name = file_info['name']
        relative_path = file_info['relative_path']
        
        # ディレクトリ構造を含む表示名
        if '/' in relative_path:
            parent_dir = os.path.dirname(relative_path)
            return f"{name} ({parent_dir})"
        else:
            return name
    
    def get_stats(self) -> Dict[str, any]:
        """検索統計情報を取得"""
        stats = self.sqlite_indexer.get_stats()
        stats['cache_size'] = len(self._search_cache)
        return stats
    
    def _get_from_cache(self, cache_key: str) -> Optional[List]:
        """LRUキャッシュから取得"""
        if cache_key in self._search_cache:
            result, timestamp = self._search_cache[cache_key]
            if time.time() - timestamp < self._cache_ttl:
                # LRU: アクセスされたアイテムを最後に移動
                self._search_cache.move_to_end(cache_key)
                return result
            else:
                # 期限切れのエントリを削除
                del self._search_cache[cache_key]
        return None
    
    def _add_to_cache(self, cache_key: str, result: List):
        """LRUキャッシュに追加"""
        # キャッシュサイズの制限（LRU方式）
        if len(self._search_cache) >= self._cache_max_size:
            # 最も古いエントリ（first item）を削除
            self._search_cache.popitem(last=False)
        
        # 新しいエントリを最後に追加
        self._search_cache[cache_key] = (result, time.time())
    
    def search_fuzzy(self, query: str, max_results: int = None) -> List[Dict[str, str]]:
        """
        ファジー検索（部分一致検索）
        SQLiteIndexerのsearch_fuzzyメソッドを使用するか、代替実装を提供
        """
        if max_results is None:
            max_results = self.max_results
        
        # SQLiteIndexerにsearch_fuzzyメソッドがある場合はそれを使用
        if hasattr(self.sqlite_indexer, 'search_fuzzy'):
            entries = self.sqlite_indexer.search_fuzzy(query, max_results)
        else:
            # フォールバック: 部分一致検索を実装
            entries = self._fallback_fuzzy_search(query, max_results)
        
        # 結果を従来の形式に変換
        results = []
        for entry in entries:
            result = {
                'name': entry.name,
                'path': entry.path,
                'relative_path': entry.relative_path,
                'workspace': entry.workspace,
                'type': entry.type
            }
            results.append(result)
        
        return results
    
    def _fallback_fuzzy_search(self, query: str, max_results: int) -> List:
        """
        フォールバック: 部分一致検索の実装
        """
        try:
            with self.sqlite_indexer._lock:
                cursor = self.sqlite_indexer.connection.execute("""
                    SELECT * FROM file_entries
                    WHERE name LIKE ? OR relative_path LIKE ?
                    ORDER BY CASE WHEN type = 'folder' THEN 0 ELSE 1 END,
                             priority DESC,
                             length(name)
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", max_results))
                
                from src.core.sqlite_indexer import FileEntry
                entries = []
                for row in cursor:
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
                    entries.append(entry)
                
                return entries
                
        except Exception as e:
            self.logger.error(f"Fallback fuzzy search error: {e}")
            return []
    
    def clear_cache(self):
        """キャッシュをクリア"""
        self._search_cache.clear()
    
    def set_max_results(self, max_results: int):
        """最大結果数を設定"""
        self.max_results = max_results
        self.clear_cache()  # キャッシュをクリアして新しい設定を反映