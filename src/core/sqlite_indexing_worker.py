# -*- coding: utf-8 -*-
"""
SQLite Indexing Worker - 高速SQLiteベース非同期インデックス構築ワーカー
"""
import time
from typing import List, Tuple, Dict, Any
from PySide6.QtCore import QThread, Signal, QObject

from src.core.sqlite_indexer import SQLiteIndexer


class SQLiteIndexingWorker(QThread):
    """高速SQLiteベース非同期インデックス構築ワーカー"""
    
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
            # SQLiteインデックスを初期化
            self.indexer = SQLiteIndexer()
            
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
                
                print(f"ワークスペース '{workspace_name}' インデックス完了: "
                      f"{files_count}ファイル, {folders_count}フォルダ ({end_time - start_time:.2f}秒)")
                
                self.workspace_completed.emit(workspace_name, files_count, folders_count)
            
            if self._is_running:
                # 最終処理
                self.progress_updated.emit(95, "インデックス最適化中...")
                
                # SQLiteインデックスの最適化
                self._optimize_database()
                
                # 完了通知
                stats = self.indexer.get_stats()
                stats['total_files_indexed'] = total_files
                stats['total_folders_indexed'] = total_folders
                
                self.progress_updated.emit(100, "インデックス構築完了")
                self.indexing_completed.emit(stats)
            
        except Exception as e:
            error_message = f"SQLiteインデックス構築エラー: {str(e)}"
            print(error_message)
            import traceback
            traceback.print_exc()
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
                print("データベース最適化完了")
                
        except Exception as e:
            print(f"データベース最適化エラー: {e}")
    
    def stop(self):
        """インデックス構築を停止"""
        self._is_running = False


class SQLiteIndexingManager(QObject):
    """SQLiteインデックス管理クラス"""
    
    # シグナル定義
    indexing_started = Signal()
    indexing_progress = Signal(float, str)  # progress%, message
    indexing_completed = Signal(dict)  # stats
    indexing_failed = Signal(str)  # error_message
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.indexer = SQLiteIndexer()  # メインスレッド用のインデックス
    
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
            print("インデックス構築不要 - 既存のインデックスを使用")
            return False
        
        print(f"インデックス構築開始: {len(workspaces_to_index)}個のワークスペース")
        
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