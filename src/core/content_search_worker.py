# -*- coding: utf-8 -*-
"""
Content Search Worker - 非同期コンテンツ検索ワーカー
"""
from typing import List, Dict, Any, Optional
from PySide6.QtCore import QThread, Signal, QObject

from src.core.content_searcher import ContentSearcher
from src.core.search_result import SearchResults, SearchOptions
from src.core.logger import get_logger

logger = get_logger(__name__)


class ContentSearchWorker(QThread):
    """非同期コンテンツ検索ワーカー"""

    # シグナル定義
    progress_updated = Signal(float, str)  # progress%, status_message
    search_completed = Signal(object)  # SearchResults
    search_failed = Signal(str)  # error_message

    def __init__(
        self,
        search_paths: List[str],
        options: SearchOptions,
        parent: Optional[QObject] = None,
    ):
        super().__init__(parent)
        self.search_paths = search_paths
        self.options = options
        self.searcher = ContentSearcher()
        self._is_running = False

    def run(self):
        """検索を実行"""
        self._is_running = True

        try:
            # 進捗コールバック
            def progress_callback(progress: float, message: str):
                if self._is_running:
                    self.progress_updated.emit(progress, message)

            # 検索実行
            results = self.searcher.search(
                self.search_paths, self.options, progress_callback
            )

            if self._is_running:
                if results.has_error():
                    self.search_failed.emit(results.error_message)
                else:
                    self.search_completed.emit(results)

        except Exception as e:
            error_message = f"検索エラー: {str(e)}"
            logger.error(error_message)
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            self.search_failed.emit(error_message)

    def stop(self):
        """検索を停止"""
        self._is_running = False
        self.searcher.cancel()


class ContentSearchManager(QObject):
    """コンテンツ検索マネージャー"""

    # シグナル定義
    search_started = Signal()
    search_progress = Signal(float, str)  # progress%, message
    search_completed = Signal(object)  # SearchResults
    search_failed = Signal(str)  # error_message

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.worker: Optional[ContentSearchWorker] = None
        self._search_paths: List[str] = []

    def set_search_paths(self, paths: List[str]) -> None:
        """検索対象パスを設定"""
        self._search_paths = paths

    def is_searching(self) -> bool:
        """検索中かどうか"""
        return self.worker is not None and self.worker.isRunning()

    def start_search(self, options: SearchOptions) -> bool:
        """検索を開始"""
        if self.is_searching():
            logger.warning("検索は既に実行中です")
            return False

        if not self._search_paths:
            self.search_failed.emit("検索パスが設定されていません")
            return False

        # ワーカーを作成
        self.worker = ContentSearchWorker(self._search_paths, options)

        # シグナル接続
        self.worker.progress_updated.connect(self.search_progress)
        self.worker.search_completed.connect(self._on_search_completed)
        self.worker.search_failed.connect(self.search_failed)
        self.worker.finished.connect(self._on_worker_finished)

        # ワーカー開始
        self.worker.start()
        self.search_started.emit()

        logger.info(f"検索開始: '{options.query}' in {len(self._search_paths)} paths")
        return True

    def cancel_search(self) -> None:
        """検索をキャンセル"""
        if self.worker and self.worker.isRunning():
            logger.info("検索キャンセル要求")
            self.worker.stop()

    def _on_search_completed(self, results: SearchResults) -> None:
        """検索完了時の処理"""
        logger.info(
            f"検索完了: {results.total_matches}件 ({results.file_count}ファイル) "
            f"in {results.search_time:.2f}秒"
        )
        self.search_completed.emit(results)

    def _on_worker_finished(self) -> None:
        """ワーカー終了時の処理"""
        if self.worker:
            self.worker.deleteLater()
            self.worker = None
