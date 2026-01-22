# -*- coding: utf-8 -*-
"""
Content Search Panel - VSCodeライクなコンテンツ検索パネル
"""
import os
from typing import Optional, List
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QComboBox,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QTextEdit,
    QSplitter,
    QFrame,
    QSizePolicy,
    QAbstractItemView,
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor, QBrush, QFont

from src.core.ui_strings import tr
from src.core.search_result import SearchResults, SearchOptions, FileSearchResult, SearchMatch
from src.core.content_search_worker import ContentSearchManager
from src.core.logger import get_logger

logger = get_logger(__name__)


class ContentSearchPanel(QWidget):
    """コンテンツ検索パネル"""

    # シグナル
    file_selected = Signal(str, int)  # file_path, line_number
    search_started = Signal()
    search_completed = Signal(int, int, float)  # matches, files, time

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.search_manager = ContentSearchManager(self)
        self.current_results: Optional[SearchResults] = None
        self._search_paths: List[str] = []

        # 検索遅延用タイマー
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._execute_search)
        self.search_delay = 500  # 500ms

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """UIを初期化"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(4)

        # 検索入力セクション
        search_input_layout = QHBoxLayout()
        search_input_layout.setSpacing(4)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(tr("content_search_placeholder"))
        self.search_input.returnPressed.connect(self._on_search_requested)
        search_input_layout.addWidget(self.search_input)

        self.search_button = QPushButton(tr("button_search"))
        self.search_button.clicked.connect(self._on_search_requested)
        self.search_button.setFixedWidth(60)
        search_input_layout.addWidget(self.search_button)

        main_layout.addLayout(search_input_layout)

        # オプションセクション
        options_layout = QHBoxLayout()
        options_layout.setSpacing(8)

        self.case_sensitive_cb = QCheckBox(tr("content_search_case_sensitive"))
        self.case_sensitive_cb.setToolTip(tr("content_search_case_sensitive_tooltip"))
        options_layout.addWidget(self.case_sensitive_cb)

        self.regex_cb = QCheckBox(tr("content_search_regex"))
        self.regex_cb.setToolTip(tr("content_search_regex_tooltip"))
        options_layout.addWidget(self.regex_cb)

        self.word_match_cb = QCheckBox(tr("content_search_word_match"))
        self.word_match_cb.setToolTip(tr("content_search_word_match_tooltip"))
        options_layout.addWidget(self.word_match_cb)

        options_layout.addStretch()
        main_layout.addLayout(options_layout)

        # フィルターセクション
        filter_frame = QFrame()
        filter_frame.setFrameShape(QFrame.StyledPanel)
        filter_layout = QVBoxLayout(filter_frame)
        filter_layout.setContentsMargins(4, 4, 4, 4)
        filter_layout.setSpacing(2)

        # ファイルパターン
        include_layout = QHBoxLayout()
        include_label = QLabel(tr("content_search_include_files"))
        include_label.setFixedWidth(60)
        include_layout.addWidget(include_label)

        self.include_combo = QComboBox()
        self.include_combo.setEditable(True)
        self.include_combo.addItems(["", "*.py", "*.js,*.ts", "*.cpp,*.h", "*.java"])
        self.include_combo.setToolTip(tr("content_search_include_tooltip"))
        include_layout.addWidget(self.include_combo)
        filter_layout.addLayout(include_layout)

        # 除外パターン
        exclude_layout = QHBoxLayout()
        exclude_label = QLabel(tr("content_search_exclude_files"))
        exclude_label.setFixedWidth(60)
        exclude_layout.addWidget(exclude_label)

        self.exclude_combo = QComboBox()
        self.exclude_combo.setEditable(True)
        self.exclude_combo.addItems(
            ["", "node_modules,__pycache__", "*.min.js", "build,dist"]
        )
        self.exclude_combo.setToolTip(tr("content_search_exclude_tooltip"))
        exclude_layout.addWidget(self.exclude_combo)
        filter_layout.addLayout(exclude_layout)

        main_layout.addWidget(filter_frame)

        # 結果サマリー
        self.result_summary = QLabel(tr("content_search_ready"))
        self.result_summary.setStyleSheet("color: gray;")
        main_layout.addWidget(self.result_summary)

        # スプリッター（結果ツリー + プレビュー）
        splitter = QSplitter(Qt.Vertical)

        # 結果ツリー
        self.result_tree = QTreeWidget()
        self.result_tree.setHeaderHidden(True)
        self.result_tree.setIndentation(16)
        self.result_tree.itemClicked.connect(self._on_item_clicked)
        self.result_tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.result_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.result_tree.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        splitter.addWidget(self.result_tree)

        # プレビューエリア
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMinimumHeight(100)
        self.preview_text.setPlaceholderText(tr("content_search_preview_placeholder"))
        # 等幅フォント
        preview_font = QFont("Consolas", 9)
        preview_font.setStyleHint(QFont.Monospace)
        self.preview_text.setFont(preview_font)
        splitter.addWidget(self.preview_text)

        # スプリッターの初期比率
        splitter.setSizes([300, 150])

        main_layout.addWidget(splitter)

    def _connect_signals(self):
        """シグナルを接続"""
        self.search_manager.search_started.connect(self._on_search_started)
        self.search_manager.search_progress.connect(self._on_search_progress)
        self.search_manager.search_completed.connect(self._on_search_completed)
        self.search_manager.search_failed.connect(self._on_search_failed)

    def set_search_paths(self, paths: List[str]) -> None:
        """検索対象パスを設定"""
        self._search_paths = paths
        self.search_manager.set_search_paths(paths)

    def _on_search_requested(self) -> None:
        """検索リクエスト"""
        query = self.search_input.text().strip()
        if not query:
            return

        # 検索中なら前回をキャンセル
        if self.search_manager.is_searching():
            self.search_manager.cancel_search()

        # タイマーをリセットして遅延検索
        self.search_timer.stop()
        self.search_timer.start(100)  # 即時に近い遅延

    def _execute_search(self) -> None:
        """検索を実行"""
        query = self.search_input.text().strip()
        if not query:
            return

        if not self._search_paths:
            self.result_summary.setText(tr("content_search_no_workspace"))
            self.result_summary.setStyleSheet("color: orange;")
            return

        # オプションを構築
        options = SearchOptions(
            query=query,
            is_regex=self.regex_cb.isChecked(),
            is_case_sensitive=self.case_sensitive_cb.isChecked(),
            is_word_match=self.word_match_cb.isChecked(),
            include_patterns=self._parse_patterns(self.include_combo.currentText()),
            exclude_patterns=self._parse_patterns(self.exclude_combo.currentText()),
            context_lines=2,
            max_results=1000,
        )

        # 検索開始
        self.search_manager.start_search(options)

    def _parse_patterns(self, text: str) -> List[str]:
        """カンマ区切りのパターンをリストに変換"""
        if not text:
            return []
        return [p.strip() for p in text.split(",") if p.strip()]

    def _on_search_started(self) -> None:
        """検索開始時"""
        self.result_summary.setText(tr("content_search_searching"))
        self.result_summary.setStyleSheet("color: blue;")
        self.search_button.setEnabled(False)
        self.result_tree.clear()
        self.preview_text.clear()
        self.search_started.emit()

    def _on_search_progress(self, progress: float, message: str) -> None:
        """検索進捗"""
        self.result_summary.setText(f"{message} ({progress:.0f}%)")

    def _on_search_completed(self, results: SearchResults) -> None:
        """検索完了時"""
        self.current_results = results
        self.search_button.setEnabled(True)

        # サマリーを更新
        summary = tr(
            "content_search_result_summary",
            matches=results.total_matches,
            files=results.file_count,
            time=f"{results.search_time:.2f}",
        )
        if results.truncated:
            summary += " " + tr("content_search_truncated")

        self.result_summary.setText(summary)
        self.result_summary.setStyleSheet("color: green;" if results.total_matches > 0 else "color: gray;")

        # 結果ツリーを構築
        self._populate_result_tree(results)

        self.search_completed.emit(
            results.total_matches, results.file_count, results.search_time
        )

    def _on_search_failed(self, error_message: str) -> None:
        """検索失敗時"""
        self.search_button.setEnabled(True)
        self.result_summary.setText(f"Error: {error_message}")
        self.result_summary.setStyleSheet("color: red;")

    def _populate_result_tree(self, results: SearchResults) -> None:
        """結果ツリーを構築"""
        self.result_tree.clear()

        for file_result in results.file_results:
            # ファイルノード
            file_item = QTreeWidgetItem(self.result_tree)
            file_item.setText(
                0, f"{file_result.relative_path} ({file_result.match_count})"
            )
            file_item.setData(0, Qt.UserRole, {
                "type": "file",
                "path": file_result.file_path,
                "relative_path": file_result.relative_path,
            })
            file_item.setExpanded(True)

            # マッチノード
            for match in file_result.matches:
                match_item = QTreeWidgetItem(file_item)
                # 行番号とマッチした行を表示（切り詰め）
                line_preview = match.line_content[:80]
                if len(match.line_content) > 80:
                    line_preview += "..."
                match_item.setText(0, f"  {match.line_number}: {line_preview.strip()}")
                match_item.setData(0, Qt.UserRole, {
                    "type": "match",
                    "path": file_result.file_path,
                    "relative_path": file_result.relative_path,
                    "line_number": match.line_number,
                    "match": match,
                })

    def _on_item_clicked(self, item: QTreeWidgetItem, _column: int) -> None:
        """アイテムクリック時"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return

        if data["type"] == "match":
            match: SearchMatch = data["match"]
            self._show_preview(data["path"], match)
            self.file_selected.emit(data["path"], match.line_number)

    def _on_item_double_clicked(self, item: QTreeWidgetItem, _column: int) -> None:
        """アイテムダブルクリック時"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return

        if data["type"] == "match":
            self.file_selected.emit(data["path"], data["line_number"])
        elif data["type"] == "file":
            # ファイルノードをダブルクリックした場合は展開/折りたたみ
            item.setExpanded(not item.isExpanded())

    def _show_preview(self, file_path: str, match: SearchMatch) -> None:
        """プレビューを表示"""
        self.preview_text.clear()

        # コンテキストと共に表示
        lines = []

        # 前のコンテキスト
        start_line = match.line_number - len(match.context_before)
        for i, line in enumerate(match.context_before):
            lines.append((start_line + i, line, False))

        # マッチ行
        lines.append((match.line_number, match.line_content, True))

        # 後のコンテキスト
        for i, line in enumerate(match.context_after):
            lines.append((match.line_number + 1 + i, line, False))

        # テキストを構築
        cursor = self.preview_text.textCursor()

        # ファイルパス表示
        path_format = QTextCharFormat()
        path_format.setForeground(QBrush(QColor("#0066cc")))
        path_format.setFontWeight(QFont.Bold)
        cursor.setCharFormat(path_format)
        cursor.insertText(f"{file_path}\n\n")

        # 行を表示
        normal_format = QTextCharFormat()
        normal_format.setForeground(QBrush(QColor("#888888")))

        match_line_format = QTextCharFormat()
        match_line_format.setForeground(QBrush(QColor("#000000")))

        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QBrush(QColor("#ffff00")))
        highlight_format.setForeground(QBrush(QColor("#000000")))

        for line_num, line_content, is_match in lines:
            # 行番号
            cursor.setCharFormat(normal_format)
            cursor.insertText(f"{line_num:4d}: ")

            if is_match:
                # マッチ行：ハイライト付き
                before_match = line_content[: match.match_start]
                match_text = line_content[match.match_start : match.match_end]
                after_match = line_content[match.match_end :]

                cursor.setCharFormat(match_line_format)
                cursor.insertText(before_match)

                cursor.setCharFormat(highlight_format)
                cursor.insertText(match_text)

                cursor.setCharFormat(match_line_format)
                cursor.insertText(after_match + "\n")
            else:
                # コンテキスト行
                cursor.setCharFormat(normal_format)
                cursor.insertText(line_content + "\n")

        self.preview_text.setTextCursor(cursor)

    def cancel_search(self) -> None:
        """検索をキャンセル"""
        self.search_manager.cancel_search()

    def update_language(self) -> None:
        """言語変更時にUIを更新"""
        self.search_input.setPlaceholderText(tr("content_search_placeholder"))
        self.search_button.setText(tr("button_search"))
        self.case_sensitive_cb.setText(tr("content_search_case_sensitive"))
        self.case_sensitive_cb.setToolTip(tr("content_search_case_sensitive_tooltip"))
        self.regex_cb.setText(tr("content_search_regex"))
        self.regex_cb.setToolTip(tr("content_search_regex_tooltip"))
        self.word_match_cb.setText(tr("content_search_word_match"))
        self.word_match_cb.setToolTip(tr("content_search_word_match_tooltip"))
        self.include_combo.setToolTip(tr("content_search_include_tooltip"))
        self.exclude_combo.setToolTip(tr("content_search_exclude_tooltip"))
        self.preview_text.setPlaceholderText(tr("content_search_preview_placeholder"))

        # 結果がない場合のみサマリーを更新
        if self.current_results is None:
            self.result_summary.setText(tr("content_search_ready"))

    def focus_search_input(self) -> None:
        """検索入力にフォーカス"""
        self.search_input.setFocus()
        self.search_input.selectAll()
