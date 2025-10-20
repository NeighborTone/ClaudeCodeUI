# -*- coding: utf-8 -*-
"""
SQLite Indexing Worker - High-performance SQLite-based asynchronous index building worker
"""
import time
from typing import List, Tuple, Dict, Any
from PySide6.QtCore import QThread, Signal, QObject

from src.core.sqlite_indexer import SQLiteIndexer
from src.core.logger import get_logger


class SQLiteIndexingWorker(QThread):
    """High-performance SQLite-based asynchronous index building worker"""
    
    # Signal definitions
    progress_updated = Signal(float, str)  # progress%, status_message
    workspace_completed = Signal(str, int, int)  # workspace_name, files_count, folders_count
    indexing_completed = Signal(dict)  # stats
    indexing_failed = Signal(str)  # error_message
    
    def __init__(self, workspaces: List[Dict[str, str]], rebuild_all: bool = False):
        super().__init__()
        self.workspaces = workspaces
        self.rebuild_all = rebuild_all
        self.indexer = None
        self._is_running = False
        self.logger = get_logger(__name__)
    
    def run(self):
        """メインの実行ループ"""
        self._is_running = True
        
        try:
            # SQLiteインデックスを初期化
            self.indexer = SQLiteIndexer()
            
            if self.rebuild_all:
                self.indexer.clear_index()
                self.progress_updated.emit(0, "Index cleared")
            
            total_workspaces = len(self.workspaces)
            total_files = 0
            total_folders = 0
            
            # 各ワークスペースをインデックス
            for i, workspace in enumerate(self.workspaces):
                if not self._is_running:
                    break
                
                workspace_name = workspace['name']
                workspace_path = workspace['path']
                
                self.progress_updated.emit(
                    (i / total_workspaces) * 100,
                    f"Indexing: {workspace_name}"
                )
                
                # プログレスコールバック関数
                def progress_callback(progress: float, message: str):
                    if self._is_running:
                        # ワークスペース内のプログレス + 全体のプログレス
                        overall_progress = ((i + progress / 100) / total_workspaces) * 90  # 90%まで
                        self.progress_updated.emit(overall_progress, message)
                
                # ワークスペースをインデックス（SQLite版）
                start_time = time.time()
                files_count, folders_count = self.indexer.add_workspace_files(
                    workspace_name, workspace_path, progress_callback
                )
                end_time = time.time()
                
                total_files += files_count
                total_folders += folders_count
                
                self.logger.info(f"Workspace '{workspace_name}' index completed: "
                                  f"{files_count} files, {folders_count} folders ({end_time - start_time:.2f}s)")
                
                self.workspace_completed.emit(workspace_name, files_count, folders_count)
            
            if self._is_running:
                # 最終処理
                self.progress_updated.emit(95, "Optimizing index...")
                
                # SQLiteインデックスの最適化
                self._optimize_database()
                
                # 完了通知
                stats = self.indexer.get_stats()
                stats['total_files_indexed'] = total_files
                stats['total_folders_indexed'] = total_folders
                
                self.progress_updated.emit(100, "Index build completed")
                self.indexing_completed.emit(stats)
            
        except Exception as e:
            error_message = f"SQLite index build error: {str(e)}"
            self.logger.error(error_message)
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            self.indexing_failed.emit(error_message)
        finally:
            # リソースのクリーンアップは行わない（メインスレッドで引き続き使用するため）
            pass
    
    def _optimize_database(self):
        """データベースの最適化を実行"""
        try:
            with self.indexer._lock:
                # VACUUM（データベースの最適化）
                self.indexer.connection.execute("VACUUM")
                
                # ANALYZE（統計情報の更新）
                self.indexer.connection.execute("ANALYZE")
                
                # WALファイルのチェックポイント
                self.indexer.connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
                
                self.indexer.connection.commit()
                self.logger.info("Database optimization completed")
                
        except Exception as e:
            self.logger.error(f"Database optimization error: {e}")
    
    def stop(self):
        """インデックス構築を停止"""
        self._is_running = False


class SQLiteIndexingManager(QObject):
    """SQLite index management class"""

    # Signal definitions
    indexing_started = Signal()
    indexing_progress = Signal(float, str)  # progress%, message
    indexing_completed = Signal(dict)  # stats
    indexing_failed = Signal(str)  # error_message

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.indexer = SQLiteIndexer()  # メインスレッド用のインデックス
        self.logger = get_logger(__name__)  # ロガーを初期化
    
    def is_indexing(self) -> bool:
        """インデックス中かどうか"""
        return self.worker is not None and self.worker.isRunning()
    
    def start_indexing(self, workspaces: List[Dict[str, str]], rebuild_all: bool = False):
        """インデックス構築を開始"""
        if self.is_indexing():
            return False
        
        self.worker = SQLiteIndexingWorker(workspaces, rebuild_all)
        
        # シグナル接続
        self.worker.progress_updated.connect(self.indexing_progress)
        self.worker.indexing_completed.connect(self._on_indexing_completed)
        self.worker.indexing_failed.connect(self.indexing_failed)
        self.worker.finished.connect(self._on_worker_finished)
        
        # ワーカー開始
        self.worker.start()
        self.indexing_started.emit()
        
        return True
    
    def _on_indexing_completed(self, stats: dict):
        """インデックス完了時の処理"""
        # メインスレッドのインデックスを再初期化（新しいインスタンス作成）
        self.indexer.close()
        self.indexer = SQLiteIndexer()
        
        self.indexing_completed.emit(stats)
    
    def _on_worker_finished(self):
        """ワーカー終了時の処理"""
        if self.worker:
            self.worker.deleteLater()
            self.worker = None
    
    def get_indexer(self) -> SQLiteIndexer:
        """インデックスを取得"""
        return self.indexer
    
    def get_stats(self) -> Dict[str, Any]:
        """統計情報を取得"""
        return self.indexer.get_stats()
    
    def check_indexing_needed(self, workspaces: List[Dict[str, str]]) -> bool:
        """インデックスが必要かどうかをチェック"""
        needed_workspaces = self.indexer.needs_workspace_indexing(workspaces, debug=False)
        return len(needed_workspaces) > 0
    
    def start_smart_indexing(self, workspaces: List[Dict[str, str]]) -> bool:
        """必要な場合のみインデックス構築を開始"""
        if self.is_indexing():
            return False
        
        # インデックスが必要なワークスペースのみを取得
        workspaces_to_index = self.indexer.needs_workspace_indexing(workspaces, debug=True)
        
        if not workspaces_to_index:
            # インデックス不要の場合
            self.logger.info("Index build not required - using existing index")
            return False
        
        self.logger.info(f"Index build started: {len(workspaces_to_index)} workspaces")
        
        # 必要なワークスペースのみインデックス構築
        rebuild_all = len(workspaces_to_index) == len(workspaces)
        return self.start_indexing(workspaces_to_index, rebuild_all)
    
    def force_rebuild(self, workspaces: List[Dict[str, str]]) -> bool:
        """強制的にインデックスを再構築"""
        return self.start_indexing(workspaces, rebuild_all=True)
    
    def clear_index(self):
        """インデックスをクリア"""
        if not self.is_indexing():
            self.indexer.clear_index()
    
    def close(self):
        """リソースのクリーンアップ"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(5000)  # 5秒まで待機
        
        if self.indexer:
            self.indexer.close()