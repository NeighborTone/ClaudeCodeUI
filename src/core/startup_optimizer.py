# -*- coding: utf-8 -*-
"""
Startup Optimizer - アプリケーション起動時の最適化
"""
import time
import os
from typing import List, Dict, Optional, Callable
from PySide6.QtCore import QObject, Signal, QTimer

from src.core.settings import SettingsManager
from src.core.workspace_manager import WorkspaceManager
from src.core.indexing_adapter import IndexingAdapter


class StartupOptimizer(QObject):
    """アプリケーション起動時の最適化クラス"""
    
    # シグナル定義
    startup_completed = Signal()
    index_check_completed = Signal(bool)  # インデックスが最新かどうか
    background_indexing_started = Signal()
    background_indexing_completed = Signal()
    
    def __init__(self, settings_manager: SettingsManager, 
                 workspace_manager: WorkspaceManager,
                 indexing_adapter: IndexingAdapter,
                 parent=None):
        super().__init__(parent)
        
        self.settings_manager = settings_manager
        self.workspace_manager = workspace_manager
        self.indexing_adapter = indexing_adapter
        
        # 起動時の設定
        self.auto_index_on_startup = self.settings_manager.get('indexing.auto_index_on_startup', True)
        self.startup_completed_emitted = False
    
    def optimize_startup(self, progress_callback: Optional[Callable] = None):
        """起動時の最適化を実行"""
        start_time = time.time()
        
        if progress_callback:
            progress_callback(10, "起動時最適化開始...")
        
        # 1. 設定とワークスペースの高速読み込み
        if progress_callback:
            progress_callback(20, "設定とワークスペースを読み込み中...")
        
        workspaces = self.workspace_manager.get_workspaces()
        
        # 2. インデックスの妥当性を高速チェック
        if progress_callback:
            progress_callback(40, "インデックスの妥当性をチェック中...")
        
        index_valid = self._fast_index_check(workspaces)
        
        if progress_callback:
            progress_callback(60, "インデックスチェック完了")
        
        # 3. インデックスが無効な場合の処理
        if not index_valid and self.auto_index_on_startup:
            if progress_callback:
                progress_callback(70, "インデックス更新が必要です...")
            
            # バックグラウンドでインデックス構築を開始
            self._start_background_indexing(workspaces)
        else:
            if progress_callback:
                progress_callback(90, "インデックスは最新です")
        
        # 4. 起動完了
        startup_time = time.time() - start_time
        
        if progress_callback:
            progress_callback(100, f"起動完了 ({startup_time:.2f}秒)")
        
        # 少し遅延させて起動完了シグナルを発行
        QTimer.singleShot(100, self._emit_startup_completed)
        
        self.index_check_completed.emit(index_valid)
        
        return {
            'startup_time': startup_time,
            'index_valid': index_valid,
            'workspaces_count': len(workspaces)
        }
    
    def _fast_index_check(self, workspaces: List[Dict[str, str]]) -> bool:
        """高速インデックス妥当性チェック"""
        try:
            # SQLiteベースの場合は非常に高速
            if hasattr(self.indexing_adapter.indexing_manager, 'get_indexer'):
                indexer = self.indexing_adapter.indexing_manager.get_indexer()
                
                # SQLiteIndexerの場合
                if hasattr(indexer, 'is_index_valid_for_workspaces'):
                    return indexer.is_index_valid_for_workspaces(workspaces, debug=False)
                # 従来のFileIndexerの場合
                elif hasattr(indexer, 'is_index_valid_for_workspaces'):
                    return indexer.is_index_valid_for_workspaces(workspaces, debug=False)
            
            return False
            
        except Exception as e:
            print(f"インデックスチェックエラー: {e}")
            return False
    
    def _start_background_indexing(self, workspaces: List[Dict[str, str]]):
        """バックグラウンドでインデックス構築を開始"""
        print("🔄 バックグラウンドインデックス構築を開始")
        
        self.background_indexing_started.emit()
        
        # インデックス構築の進行状況を監視
        self.indexing_adapter.indexing_completed.connect(self._on_background_indexing_completed)
        self.indexing_adapter.indexing_failed.connect(self._on_background_indexing_failed)
        
        # スマートインデックス構築を開始
        success = self.indexing_adapter.start_smart_indexing(workspaces)
        
        if not success:
            print("バックグラウンドインデックス構築は不要でした")
            self._on_background_indexing_completed({'message': 'not_needed'})
    
    def _on_background_indexing_completed(self, stats: Dict):
        """バックグラウンドインデックス構築完了"""
        print(f"✅ バックグラウンドインデックス構築完了: {stats}")
        self.background_indexing_completed.emit()
        
        # シグナル接続を解除
        self.indexing_adapter.indexing_completed.disconnect(self._on_background_indexing_completed)
        if hasattr(self.indexing_adapter, 'indexing_failed'):
            try:
                self.indexing_adapter.indexing_failed.disconnect(self._on_background_indexing_failed)
            except:
                pass
    
    def _on_background_indexing_failed(self, error_message: str):
        """バックグラウンドインデックス構築失敗"""
        print(f"❌ バックグラウンドインデックス構築失敗: {error_message}")
        
        # シグナル接続を解除
        try:
            self.indexing_adapter.indexing_completed.disconnect(self._on_background_indexing_completed)
            self.indexing_adapter.indexing_failed.disconnect(self._on_background_indexing_failed)
        except:
            pass
    
    def _emit_startup_completed(self):
        """起動完了シグナルを発行"""
        if not self.startup_completed_emitted:
            self.startup_completed_emitted = True
            self.startup_completed.emit()
    
    def get_startup_stats(self) -> Dict[str, any]:
        """起動統計情報を取得"""
        try:
            stats = self.indexing_adapter.get_stats()
            stats['auto_index_enabled'] = self.auto_index_on_startup
            stats['system_type'] = 'SQLite' if hasattr(self.indexing_adapter.indexing_manager.get_indexer(), 'connection') else 'Trie'
            return stats
        except Exception as e:
            print(f"起動統計取得エラー: {e}")
            return {'error': str(e)}
    
    def force_reindex(self, workspaces: List[Dict[str, str]]) -> bool:
        """強制的にインデックスを再構築"""
        if hasattr(self.indexing_adapter, 'force_rebuild'):
            return self.indexing_adapter.force_rebuild(workspaces)
        else:
            return self.indexing_adapter.start_indexing(workspaces, rebuild_all=True)
    
    def is_indexing_in_background(self) -> bool:
        """バックグラウンドでインデックス構築中かどうか"""
        return self.indexing_adapter.is_indexing()
    
    def set_auto_index_on_startup(self, enabled: bool):
        """起動時自動インデックスの有効/無効を設定"""
        self.auto_index_on_startup = enabled
        self.settings_manager.set('indexing.auto_index_on_startup', enabled)
        self.settings_manager.save_settings()


class FastStartupManager:
    """高速起動管理クラス"""
    
    @staticmethod
    def create_startup_optimizer(settings_manager: SettingsManager,
                                workspace_manager: WorkspaceManager,
                                indexing_adapter: IndexingAdapter,
                                parent=None) -> StartupOptimizer:
        """起動最適化システムを作成"""
        return StartupOptimizer(
            settings_manager, workspace_manager, indexing_adapter, parent
        )
    
    @staticmethod
    def optimize_system_settings():
        """システム設定の最適化"""
        # 環境変数でPythonの最適化を有効化
        os.environ['PYTHONOPTIMIZE'] = '1'
        
        # SQLiteの最適化設定
        os.environ['SQLITE_ENABLE_FTS5'] = '1'
        
        print("⚡ システム設定を最適化しました")
    
    @staticmethod
    def get_system_info() -> Dict[str, any]:
        """システム情報を取得"""
        import platform
        import sys
        
        return {
            'platform': platform.system(),
            'python_version': sys.version,
            'optimization_enabled': os.environ.get('PYTHONOPTIMIZE', '0') == '1',
            'sqlite_fts5_enabled': os.environ.get('SQLITE_ENABLE_FTS5', '0') == '1'
        }