# -*- coding: utf-8 -*-
"""
Prompt History Manager - プロンプト履歴の管理
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from PySide6.QtCore import QObject, Signal


class PromptHistoryManager(QObject):
    """プロンプト履歴を管理するクラス"""
    
    history_updated = Signal()  # 履歴が更新されたときのシグナル
    
    def __init__(self, max_history: int = 100):
        """
        初期化
        
        Args:
            max_history: 保存する履歴の最大数（デフォルト: 100）
        """
        super().__init__()
        self.max_history = max_history
        self.history_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'saved',
            'prompt_history.json'
        )
        self.history: List[Dict] = []
        self._ensure_saved_directory()
        self._load_history()
    
    def _ensure_saved_directory(self):
        """savedディレクトリが存在することを確認"""
        saved_dir = os.path.dirname(self.history_file)
        if not os.path.exists(saved_dir):
            os.makedirs(saved_dir, exist_ok=True)
    
    def _load_history(self):
        """履歴をファイルから読み込む"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get('history', [])
                    # 最大数を超えている場合は古いものから削除
                    if len(self.history) > self.max_history:
                        self.history = self.history[-self.max_history:]
            except Exception as e:
                print(f"Failed to load prompt history: {e}")
                self.history = []
        else:
            self.history = []
    
    def _save_history(self):
        """履歴をファイルに保存"""
        try:
            data = {
                'version': '1.0',
                'history': self.history
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save prompt history: {e}")
    
    def add_prompt(self, prompt: str, thinking_level: str = "", 
                   pre_template: str = "", post_template: str = ""):
        """
        プロンプトを履歴に追加
        
        Args:
            prompt: プロンプト本文
            thinking_level: 思考レベル
            pre_template: 事前テンプレート
            post_template: 事後テンプレート
        """
        # プロンプトの最初の行をタイトルとして使用（最大50文字）
        lines = prompt.strip().split('\n')
        title = lines[0][:50] + ('...' if len(lines[0]) > 50 else '')
        
        # 履歴エントリを作成
        entry = {
            'id': datetime.now().isoformat(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'title': title,
            'prompt': prompt,
            'thinking_level': thinking_level,
            'pre_template': pre_template,
            'post_template': post_template
        }
        
        # 履歴に追加
        self.history.append(entry)
        
        # 最大数を超えた場合は古いものを削除
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        # 保存
        self._save_history()
        self.history_updated.emit()
    
    def get_history(self) -> List[Dict]:
        """
        履歴を取得
        
        Returns:
            履歴のリスト（新しい順）
        """
        return list(reversed(self.history))
    
    def get_prompt_by_id(self, prompt_id: str) -> Optional[Dict]:
        """
        IDでプロンプトを取得
        
        Args:
            prompt_id: プロンプトID
            
        Returns:
            プロンプト情報、見つからない場合はNone
        """
        for entry in self.history:
            if entry.get('id') == prompt_id:
                return entry
        return None
    
    def delete_prompt(self, prompt_id: str):
        """
        プロンプトを削除
        
        Args:
            prompt_id: 削除するプロンプトのID
        """
        self.history = [entry for entry in self.history if entry.get('id') != prompt_id]
        self._save_history()
        self.history_updated.emit()
    
    def clear_history(self):
        """履歴をすべてクリア"""
        self.history = []
        self._save_history()
        self.history_updated.emit()
    
    def search_history(self, query: str) -> List[Dict]:
        """
        履歴を検索
        
        Args:
            query: 検索クエリ
            
        Returns:
            マッチした履歴のリスト（新しい順）
        """
        query_lower = query.lower()
        results = []
        
        for entry in self.history:
            # タイトルまたはプロンプト本文に検索クエリが含まれているかチェック
            if (query_lower in entry.get('title', '').lower() or
                query_lower in entry.get('prompt', '').lower()):
                results.append(entry)
        
        return list(reversed(results))


# グローバルインスタンス
_prompt_history_manager = None


def get_prompt_history_manager() -> PromptHistoryManager:
    """プロンプト履歴マネージャーのインスタンスを取得"""
    global _prompt_history_manager
    if _prompt_history_manager is None:
        _prompt_history_manager = PromptHistoryManager()
    return _prompt_history_manager