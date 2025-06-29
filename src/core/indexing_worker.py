# -*- coding: utf-8 -*-
"""
Indexing Worker - 非同期インデックス構築ワーカー
"""
from typing import List, Tuple, Dict, Any
from PySide6.QtCore import QThread, Signal, QObject

from src.core.file_indexer import FileIndexer


class IndexingWorker(QThread):
    """非同期インデックス構築ワーカー"""
    
    # シグナル定義
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
    
    def run(self):
        """メインの実行ループ"""
        self._is_running = True
        
        try:
            # インデックスを初期化
            self.indexer = FileIndexer()
            
            if self.rebuild_all:
                self.indexer.clear_index()
                self.progress_updated.emit(0, "インデックスをクリアしました")
            
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
                    f"インデックス中: {workspace_name}"
                )
                
                # プログレスコールバック関数
                def progress_callback(progress: float, message: str):
                    if self._is_running:
                        # ワークスペース内のプログレス + 全体のプログレス
                        overall_progress = ((i + progress / 100) / total_workspaces) * 100
                        self.progress_updated.emit(overall_progress, message)
                
                # ワークスペースをインデックス
                files_count, folders_count = self.indexer.add_workspace_files(
                    workspace_name, workspace_path, progress_callback
                )
                
                total_files += files_count
                total_folders += folders_count
                
                self.workspace_completed.emit(workspace_name, files_count, folders_count)
            
            if self._is_running:
                # インデックスを保存
                self.progress_updated.emit(95, "インデックスを保存中...")
                self.indexer.save_index()
                
                # 完了通知
                stats = self.indexer.get_stats()
                self.progress_updated.emit(100, "インデックス構築完了")
                self.indexing_completed.emit(stats)
            
        except Exception as e:
            error_message = f"インデックス構築エラー: {str(e)}"
            print(error_message)
            self.indexing_failed.emit(error_message)
    
    def stop(self):
        """インデックス構築を停止"""
        self._is_running = False


class IndexingManager(QObject):
    """インデックス管理クラス"""
    
    # シグナル定義
    indexing_started = Signal()
    indexing_progress = Signal(float, str)  # progress%, message
    indexing_completed = Signal(dict)  # stats
    indexing_failed = Signal(str)  # error_message
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.indexer = FileIndexer()  # メインスレッド用のインデックス
    
    def is_indexing(self) -> bool:
        """インデックス中かどうか"""
        return self.worker is not None and self.worker.isRunning()
    
    def start_indexing(self, workspaces: List[Dict[str, str]], rebuild_all: bool = False):
        """インデックス構築を開始"""
        if self.is_indexing():
            return False
        
        self.worker = IndexingWorker(workspaces, rebuild_all)
        
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
        # メインスレッドのインデックスを再読み込み
        self.indexer.load_index()
        self.indexing_completed.emit(stats)
    
    def _on_worker_finished(self):
        """ワーカー終了時の処理"""
        if self.worker:
            self.worker.deleteLater()
            self.worker = None
    
    def get_indexer(self) -> FileIndexer:
        """インデックスを取得"""
        return self.indexer
    
    def reload_index(self) -> bool:
        """インデックスを再読み込み"""
        return self.indexer.load_index()
    
    def get_stats(self) -> Dict[str, Any]:
        """統計情報を取得"""
        return self.indexer.get_stats()
    
    def check_indexing_needed(self, workspaces: List[Dict[str, str]]) -> bool:
        """インデックスが必要かどうかをチェック"""
        return len(self.indexer.needs_workspace_indexing(workspaces)) > 0
    
    def start_smart_indexing(self, workspaces: List[Dict[str, str]]) -> bool:
        """必要な場合のみインデックス構築を開始"""
        if self.is_indexing():
            return False
        
        # インデックスが必要なワークスペースのみを取得
        workspaces_to_index = self.indexer.needs_workspace_indexing(workspaces)
        
        if not workspaces_to_index:
            # インデックス不要の場合
            return False
        
        # 必要なワークスペースのみインデックス構築
        rebuild_all = len(workspaces_to_index) == len(workspaces)
        return self.start_indexing(workspaces_to_index, rebuild_all)