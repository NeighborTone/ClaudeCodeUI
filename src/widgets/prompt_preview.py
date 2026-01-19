# -*- coding: utf-8 -*-
"""
Prompt Preview Widget - プロンプトプレビューウィジェット
リアルタイムで最終プロンプトをプレビュー表示
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QLabel, QFrame)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QFont

from src.core.template_manager import get_template_manager
from src.core.ui_strings import tr


class PromptPreviewWidget(QWidget):
    """プロンプトプレビューウィジェット"""
    
    # シグナル: プレビュー内容が変更された時に最終プロンプトを送信
    prompt_content_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.template_manager = get_template_manager()
        self.setup_ui()
        
        # 更新遅延タイマー（リアルタイム更新のパフォーマンス最適化）
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._update_preview)
        self.update_timer.setInterval(100)  # 100ms遅延
        
        # 現在の値を保持
        self.current_pre_template = ""
        self.current_main_content = ""
        self.current_post_template = ""
        
        # UIをセットアップしてから初期プレビューを設定
        QTimer.singleShot(0, self._update_preview)
    
    def setup_ui(self):
        """UIセットアップ"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # ヘッダーラベル
        self.header_label = QLabel(tr("template_preview_title"))
        self.header_label.setStyleSheet("font-weight: bold; font-size: 12pt; padding: 5px;")
        layout.addWidget(self.header_label)
        
        # 区切り線
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # プレビューテキストエリア
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont("Consolas", 11))
        self.preview_text.setPlaceholderText(tr("template_placeholder_content"))
        layout.addWidget(self.preview_text)
    
    def update_preview(self, pre_template: str = "",
                      main_content: str = "", post_template: str = ""):
        """プレビューを更新（リアルタイム対応）"""
        # 値が変更された場合のみ更新
        if (self.current_pre_template != pre_template or
            self.current_main_content != main_content or
            self.current_post_template != post_template):

            self.current_pre_template = pre_template
            self.current_main_content = main_content
            self.current_post_template = post_template

            # タイマーを再開（連続更新を防ぐ）
            self.update_timer.start()
    
    def _update_preview(self):
        """実際のプレビュー更新処理"""
        # プレースホルダーテキストが空の場合のデフォルト設定を改善
        main_content = self.current_main_content
        if not main_content.strip():
            # プレースホルダーテキストの代わりに空文字を使用（実際のプロンプトでは不要）
            main_content = ""

        # 最終プロンプトを構築
        final_prompt = self.template_manager.build_final_prompt(
            self.current_pre_template,
            main_content,
            self.current_post_template
        )
        
        # プレビューテキストを設定
        self.preview_text.setPlainText(final_prompt)
        
        # カーソルを先頭に移動
        cursor = self.preview_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        self.preview_text.setTextCursor(cursor)
        
        # プレビュー内容変更シグナルを送信（トークンカウント更新用）
        self.prompt_content_changed.emit(final_prompt)
    
    def update_language(self):
        """言語変更時のUI更新"""
        self.header_label.setText(tr("template_preview_title"))
        self.preview_text.setPlaceholderText(tr("template_placeholder_content"))
        
        # プレビューを再更新
        self._update_preview()
    
    def clear_preview(self):
        """プレビューをクリア"""
        self.current_pre_template = ""
        self.current_main_content = ""
        self.current_post_template = ""
        self._update_preview()
    
    def get_current_prompt(self) -> str:
        """現在のプロンプトテキストを取得"""
        return self.preview_text.toPlainText()
    
    def copy_to_clipboard(self):
        """プレビュー内容をクリップボードにコピー"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.get_current_prompt())


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # テストウィンドウ
    widget = PromptPreviewWidget()
    widget.resize(400, 300)
    widget.show()
    
    # テストデータ
    widget.update_preview(
        pre_template="Code Review",
        main_content="def hello():\n    print('Hello World')",
        post_template="Explanation Request"
    )
    
    sys.exit(app.exec())