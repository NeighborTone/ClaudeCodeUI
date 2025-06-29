# -*- coding: utf-8 -*-
"""
Indexing Adapter - 新しいSQLiteインデックスシステムと既存システムの統合アダプター
"""
import os
from typing import List, Dict, Any, Optional
from PySide6.QtCore import QObject, Signal

from src.core.settings import SettingsManager
from src.core.sqlite_indexer import SQLiteIndexer
from src.core.sqlite_indexing_worker import SQLiteIndexingManager
from src.core.fast_sqlite_searcher import FastSQLiteSearcher
from src.core.file_indexer import FileIndexer
from src.core.indexing_worker import IndexingManager
from src.core.fast_file_searcher import FastFileSearcher


class IndexingAdapter(QObject):
    """
    新旧インデックスシステムの統合アダプター
    設定に基づいてSQLiteシステムまたは従来システムを使用
    """
    
    # シグナル定義（統一インターフェース）
    indexing_started = Signal()
    indexing_progress = Signal(float, str)
    indexing_completed = Signal(dict)
    indexing_failed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.settings_manager = SettingsManager()
        self.use_sqlite = self._should_use_sqlite()
        
        # 使用するシステムを初期化
        if self.use_sqlite:
            print("🚀 高速SQLiteインデックスシステムを使用")
            self.indexing_manager = SQLiteIndexingManager(self)
            self.searcher = FastSQLiteSearcher(self.indexing_manager.get_indexer())
        else:
            print("📂 従来のTrieインデックスシステムを使用")
            self.indexing_manager = IndexingManager(self)
            self.searcher = FastFileSearcher(self.indexing_manager.get_indexer())
        
        # シグナルの統一
        self.indexing_manager.indexing_started.connect(self.indexing_started)
        self.indexing_manager.indexing_progress.connect(self.indexing_progress)
        self.indexing_manager.indexing_completed.connect(self.indexing_completed)
        self.indexing_manager.indexing_failed.connect(self.indexing_failed)
    
    def _should_use_sqlite(self) -> bool:
        """SQLiteシステムを使用するかどうかを判定"""
        # 設定ファイルから判定（デフォルトはTrue）
        use_sqlite = self.settings_manager.get('indexing.use_sqlite', True)
        
        # 環境変数での強制指定も可能
        env_force = os.environ.get('CLAUDE_UI_USE_SQLITE', '').lower()
        if env_force in ('true', '1', 'yes'):
            return True
        elif env_force in ('false', '0', 'no'):
            return False
        
        return use_sqlite
    
    def get_indexer(self):
        """アクティブなインデックスを取得（統一インターフェース）"""
        return self.indexing_manager.get_indexer()
    
    def get_searcher(self):
        """アクティブな検索システムを取得"""
        return self.searcher
    
    def is_indexing(self) -> bool:
        """インデックス中かどうか"""
        return self.indexing_manager.is_indexing()
    
    def start_indexing(self, workspaces: List[Dict[str, str]], rebuild_all: bool = False) -> bool:
        """インデックス構築を開始"""
        return self.indexing_manager.start_indexing(workspaces, rebuild_all)
    
    def start_smart_indexing(self, workspaces: List[Dict[str, str]]) -> bool:
        """必要な場合のみインデックス構築を開始"""
        return self.indexing_manager.start_smart_indexing(workspaces)
    
    def check_indexing_needed(self, workspaces: List[Dict[str, str]]) -> bool:
        """インデックスが必要かどうかをチェック"""
        return self.indexing_manager.check_indexing_needed(workspaces)
    
    def get_stats(self) -> Dict[str, Any]:
        """統計情報を取得"""
        stats = self.indexing_manager.get_stats()
        stats['system_type'] = 'SQLite' if self.use_sqlite else 'Trie'
        return stats
    
    def clear_index(self):
        """インデックスをクリア"""
        if hasattr(self.indexing_manager, 'clear_index'):
            self.indexing_manager.clear_index()
    
    def force_rebuild(self, workspaces: List[Dict[str, str]]) -> bool:
        """強制的にインデックスを再構築"""
        if hasattr(self.indexing_manager, 'force_rebuild'):
            return self.indexing_manager.force_rebuild(workspaces)
        else:
            return self.start_indexing(workspaces, rebuild_all=True)
    
    def close(self):
        """リソースのクリーンアップ"""
        if hasattr(self.indexing_manager, 'close'):
            self.indexing_manager.close()


class AdaptiveFileSearcher:
    """
    新旧ファイル検索システムの統合アダプター
    既存のFastFileSearcherインターフェースを維持
    """
    
    def __init__(self, indexing_adapter: IndexingAdapter):
        self.indexing_adapter = indexing_adapter
        self.searcher = indexing_adapter.get_searcher()
    
    def extract_file_mentions(self, text: str) -> List:
        """テキストから@ファイル名の部分を抽出"""
        return self.searcher.extract_file_mentions(text)
    
    def search_files_by_name(self, query: str) -> List[Dict[str, str]]:
        """ファイル・フォルダを名前で検索"""
        return self.searcher.search_files_by_name(query)
    
    def get_file_content_preview(self, file_path: str, max_lines: int = 10) -> str:
        """ファイルの内容のプレビューを取得"""
        return self.searcher.get_file_content_preview(file_path, max_lines)
    
    def resolve_file_mentions(self, text: str) -> Dict[str, List[Dict[str, str]]]:
        """テキスト内の@ファイル名をすべて解決"""
        return self.searcher.resolve_file_mentions(text)
    
    def replace_file_mentions_with_content(self, text: str, selected_files: Dict[str, str]) -> str:
        """@ファイル名をファイルの内容に置換"""
        return self.searcher.replace_file_mentions_with_content(text, selected_files)
    
    def get_completion_suggestions(self, partial_filename: str) -> List[str]:
        """部分的なファイル名から補完候補を取得"""
        return self.searcher.get_completion_suggestions(partial_filename)
    
    def get_stats(self) -> Dict[str, Any]:
        """検索統計情報を取得"""
        return self.searcher.get_stats()
    
    def get_quick_suggestions(self, partial_filename: str) -> List[Dict[str, str]]:
        """クイック補完候補を取得（SQLiteシステムのみ）"""
        if hasattr(self.searcher, 'get_quick_suggestions'):
            return self.searcher.get_quick_suggestions(partial_filename)
        else:
            # 従来システムの場合は基本的な候補を返す
            suggestions = self.get_completion_suggestions(partial_filename)
            return [{'name': name, 'display_name': name, 'type': 'file'} for name in suggestions]
    
    def set_max_results(self, max_results: int):
        """最大結果数を設定（SQLiteシステムのみ）"""
        if hasattr(self.searcher, 'set_max_results'):
            self.searcher.set_max_results(max_results)
    
    def clear_cache(self):
        """キャッシュをクリア（SQLiteシステムのみ）"""
        if hasattr(self.searcher, 'clear_cache'):
            self.searcher.clear_cache()


def create_indexing_system(parent=None) -> tuple:
    """
    適切なインデックスシステムを作成して返す
    Returns: (IndexingAdapter, AdaptiveFileSearcher)
    """
    indexing_adapter = IndexingAdapter(parent)
    file_searcher = AdaptiveFileSearcher(indexing_adapter)
    
    return indexing_adapter, file_searcher


def migrate_old_index_to_sqlite():
    """
    従来のJSONインデックスをSQLiteに移行
    """
    try:
        old_index_file = "saved/file_index.json"
        if not os.path.exists(old_index_file):
            print("移行対象の古いインデックスが見つかりません")
            return
        
        print("🔄 古いインデックスをSQLiteに移行中...")
        
        # 古いインデックスを読み込み
        old_indexer = FileIndexer()
        old_stats = old_indexer.get_stats()
        
        if old_stats['total_entries'] == 0:
            print("移行対象のデータがありません")
            return
        
        # 新しいSQLiteインデックスを作成
        sqlite_indexer = SQLiteIndexer()
        sqlite_indexer.clear_index()
        
        # ワークスペース情報を移行
        for workspace_path, workspace_info in old_indexer.workspaces.items():
            workspace_name = workspace_info['name']
            
            print(f"ワークスペース移行中: {workspace_name}")
            
            # ファイルエントリを移行（簡単なバッチ処理）
            file_entries = []
            for entry in old_indexer.entries_by_path.values():
                if entry.workspace == workspace_name:
                    file_entries.append((
                        entry.path_hash if hasattr(entry, 'path_hash') else "",
                        entry.name, entry.path, entry.relative_path,
                        entry.workspace, entry.type, entry.size,
                        entry.modified_time, entry.extension,
                        sqlite_indexer.extension_priorities.get(entry.extension, 30)
                    ))
            
            if file_entries:
                sqlite_indexer._insert_batch(file_entries)
        
        # 移行完了
        new_stats = sqlite_indexer.get_stats()
        print(f"✅ 移行完了: {new_stats['total_entries']}エントリ")
        
        # 古いインデックスファイルをバックアップ
        backup_file = old_index_file + ".backup"
        if os.path.exists(old_index_file):
            os.rename(old_index_file, backup_file)
            print(f"古いインデックスを {backup_file} にバックアップしました")
        
        sqlite_indexer.close()
        
    except Exception as e:
        print(f"インデックス移行エラー: {e}")
        import traceback
        traceback.print_exc()