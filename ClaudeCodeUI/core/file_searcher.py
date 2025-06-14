# -*- coding: utf-8 -*-
"""
File Searcher - @ file search functionality
"""
import os
import re
from typing import List, Dict, Tuple, Optional
from core.workspace_manager import WorkspaceManager


class FileSearcher:
    """ファイル検索機能を提供するクラス"""
    
    def __init__(self, workspace_manager: WorkspaceManager):
        self.workspace_manager = workspace_manager
        self.max_results = 10
    
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
        Search files and folders by name
        """
        if not query:
            return []
        
        # Search for both files and folders matching the query
        results = self.workspace_manager.search_files_and_folders(query)
        
        # Score the results
        scored_results = []
        for item_info in results:
            score = self._calculate_relevance_score(query, item_info)
            scored_results.append((score, item_info))
        
        # Sort by score (folders get slight priority boost)
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        # 上位結果を返す
        return [result[1] for result in scored_results[:self.max_results]]
    
    def _calculate_relevance_score(self, query: str, item_info: Dict[str, str]) -> float:
        """ファイル・フォルダの関連性スコアを計算"""
        score = 0.0
        query_lower = query.lower()
        item_name = item_info['name'].lower()
        relative_path = item_info['relative_path'].lower()
        item_type = item_info.get('type', 'file')
        
        # フォルダの場合は少しボーナス点を与える
        if item_type == 'folder':
            score += 5
        
        # 完全一致
        if query_lower == item_name:
            score += 100
        
        # ファイルの場合は拡張子なしでの一致もチェック
        if item_type == 'file':
            name_without_ext = os.path.splitext(item_name)[0]
            if query_lower == name_without_ext:
                score += 95
        
        # 名前の開始位置での一致
        if item_name.startswith(query_lower):
            score += 80
        
        # 名前に含まれる
        if query_lower in item_name:
            score += 60
        
        # パスに含まれる
        if query_lower in relative_path:
            score += 40
        
        # 部分一致（単語境界）
        if re.search(r'\b' + re.escape(query_lower), item_name):
            score += 30
        
        # 深さによる調整（浅い方が高スコア）
        depth = relative_path.count('/')
        score -= depth * 5
        
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
        """部分的なファイル名から補完候補を取得"""
        if not partial_filename:
            return []
        
        matches = self.search_files_by_name(partial_filename)
        suggestions = []
        
        for file_info in matches:
            # ファイル名（拡張子なし）
            name_without_ext = os.path.splitext(file_info['name'])[0]
            if name_without_ext not in suggestions:
                suggestions.append(name_without_ext)
            
            # ファイル名（拡張子込み）
            if file_info['name'] not in suggestions:
                suggestions.append(file_info['name'])
        
        return suggestions[:5]  # 上位5件