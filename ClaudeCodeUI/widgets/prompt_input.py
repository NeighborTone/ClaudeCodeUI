# -*- coding: utf-8 -*-
"""
Prompt Input Widget - Prompt input area and keybind functionality
"""
import os
import re
from typing import Dict, List, Optional, Callable
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QPushButton, 
                              QHBoxLayout, QListWidget, QListWidgetItem, 
                              QLabel, QFrame, QSplitter, QApplication)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QKeyEvent, QTextCursor, QFont

from core.file_searcher import FileSearcher
from core.workspace_manager import WorkspaceManager
from core.token_counter import TokenCounter
from core.path_converter import PathConverter
from ui.style_themes import get_completion_widget_style, get_main_font


class FileCompletionWidget(QWidget):
    """ファイル補完候補を表示するウィジェット"""
    
    file_selected = Signal(str, str)  # (filename, file_path)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip)
        self.setMaximumHeight(200)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.label = QLabel("ファイルを選択:")
        layout.addWidget(self.label)
        
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list_widget)
        
        self.current_filename = ""
        self.file_matches = []
        
        # スタイルを適用
        self.setStyleSheet(get_completion_widget_style())
    
    def show_completions(self, filename: str, matches: List[Dict[str, str]], pos):
        """補完候補を表示"""
        self.current_filename = filename
        self.file_matches = matches
        
        self.list_widget.clear()
        
        if not matches:
            self.hide()
            return
        
        for match in matches:
            item = QListWidgetItem()
            item.setText(f"{match['name']} ({match['workspace']})")
            item.setData(Qt.UserRole, match)
            self.list_widget.addItem(item)
        
        self.move(pos)
        self.show()
        
        # 最初のアイテムを選択
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)
    
    def on_item_clicked(self, item):
        """アイテムがクリックされたとき"""
        file_data = item.data(Qt.UserRole)
        if file_data:
            self.file_selected.emit(self.current_filename, file_data['path'])
            self.hide()
    
    def on_item_double_clicked(self, item):
        """アイテムがダブルクリックされたとき"""
        self.on_item_clicked(item)
    
    def select_current_item(self):
        """現在選択されているアイテムを選択"""
        current_item = self.list_widget.currentItem()
        if current_item:
            self.on_item_clicked(current_item)
    
    def navigate_up(self):
        """上のアイテムに移動"""
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            self.list_widget.setCurrentRow(current_row - 1)
    
    def navigate_down(self):
        """下のアイテムに移動"""
        current_row = self.list_widget.currentRow()
        if current_row < self.list_widget.count() - 1:
            self.list_widget.setCurrentRow(current_row + 1)


class PromptInputWidget(QWidget):
    """プロンプト入力ウィジェット"""
    
    generate_and_copy = Signal(str, str)  # (prompt, thinking_level)
    
    def __init__(self, workspace_manager: WorkspaceManager, parent=None):
        super().__init__(parent)
        
        self.workspace_manager = workspace_manager
        self.file_searcher = FileSearcher(workspace_manager)
        self.thinking_level = "think"
        self.path_mode = PathConverter.get_default_mode()
        
        self.file_completion_widget = None
        self.completion_timer = QTimer()
        self.completion_timer.setSingleShot(True)
        self.completion_timer.timeout.connect(self.show_file_completions)
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # プロンプト入力エリアとトークン数表示
        header_layout = QHBoxLayout()
        prompt_label = QLabel("プロンプト (Enterで改行, Shift+Enterで生成&コピー):")
        header_layout.addWidget(prompt_label)
        
        # トークン数表示ラベル
        self.token_count_label = QLabel("0トークン")
        self.token_count_label.setAlignment(Qt.AlignRight)
        header_layout.addWidget(self.token_count_label)
        
        layout.addLayout(header_layout)
        
        self.text_edit = QTextEdit()
        self.text_edit.setAcceptRichText(False)
        
        # プレースホルダーテキスト
        self.text_edit.setPlaceholderText(
            "プロンプトを入力してください...\n"
            "- Enterで改行\n"
            "- Shift+Enterで生成&コピー\n"
            "- @filename でファイルを指定"
        )
        
        layout.addWidget(self.text_edit)
        
        # ボタン
        button_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("生成&コピー (Shift+Enter)")
        self.generate_btn.clicked.connect(self.generate_prompt)
        button_layout.addWidget(self.generate_btn)
        
        self.clear_btn = QPushButton("クリア")
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_btn)
        
        layout.addLayout(button_layout)
        
        # イベント処理
        self.text_edit.keyPressEvent = self.text_edit_key_press_event
        self.text_edit.textChanged.connect(self.on_text_changed)
        
        # ファイル補完ウィジェット
        self.file_completion_widget = FileCompletionWidget(self)
        self.file_completion_widget.file_selected.connect(self.on_file_selected)
        self.file_completion_widget.hide()
    
    def text_edit_key_press_event(self, event: QKeyEvent):
        """テキストエリアのキーイベント処理"""
        # Shift+Enter で生成&コピー
        if event.key() == Qt.Key_Return and event.modifiers() & Qt.ShiftModifier:
            self.generate_prompt()
            return
        
        # ファイル補完が表示されている場合
        if self.file_completion_widget.isVisible():
            if event.key() == Qt.Key_Escape:
                self.file_completion_widget.hide()
                return
            elif event.key() == Qt.Key_Return:
                self.file_completion_widget.select_current_item()
                return
            elif event.key() == Qt.Key_Up:
                self.file_completion_widget.navigate_up()
                return
            elif event.key() == Qt.Key_Down:
                self.file_completion_widget.navigate_down()
                return
        
        # 通常のキー処理
        QTextEdit.keyPressEvent(self.text_edit, event)
    
    def on_text_changed(self):
        """Text changed event handler"""
        self.completion_timer.stop()
        
        # Update token count
        self.update_token_count()
        
        # Detect @ at cursor position
        cursor = self.text_edit.textCursor()
        text = self.text_edit.toPlainText()
        cursor_pos = cursor.position()
        
        # Look for @ before cursor position
        at_match = None
        for match in re.finditer(r'@([^\s@]*)', text):
            start, end = match.span()
            if start <= cursor_pos <= end:
                at_match = match
                break
        
        if at_match:
            # Get the filename part
            filename = at_match.group(1)
            
            # Start timer to show completions
            self.current_at_match = at_match
            self.completion_timer.start(300)  # Show completions after 300ms
        else:
            self.file_completion_widget.hide()
    
    def show_file_completions(self):
        """Show file completion candidates"""
        if not hasattr(self, 'current_at_match'):
            return
        
        filename = self.current_at_match.group(1)
        matches = self.file_searcher.search_files_by_name(filename)
        
        if matches:
            # Calculate cursor position
            cursor = self.text_edit.textCursor()
            cursor_rect = self.text_edit.cursorRect(cursor)
            global_pos = self.text_edit.mapToGlobal(cursor_rect.bottomLeft())
            
            self.file_completion_widget.show_completions(filename, matches, global_pos)
    
    def on_file_selected(self, filename: str, file_path: str):
        """File selected event handler"""
        # Find the workspace root for this file to create relative path
        workspace_relative_path = None
        for workspace in self.workspace_manager.get_workspaces():
            workspace_path = workspace['path']
            if file_path.startswith(workspace_path):
                # Create relative path from workspace root
                workspace_relative_path = os.path.relpath(file_path, workspace_path)
                break
        
        if workspace_relative_path is None:
            # Fallback to absolute path if no workspace found
            workspace_relative_path = file_path
        
        # Convert path based on selected mode
        workspace_relative_path = PathConverter.convert_path(workspace_relative_path, self.path_mode)
        
        # Replace @filename with @relative/path in the text
        cursor = self.text_edit.textCursor()
        text = self.text_edit.toPlainText()
        
        if hasattr(self, 'current_at_match'):
            start, end = self.current_at_match.span()
            
            # Create the replacement text with file path (Claude Code format)
            replacement_text = f"@{workspace_relative_path}"
            
            # Replace the @filename with the file path
            new_text = text[:start] + replacement_text + text[end:]
            self.text_edit.setPlainText(new_text)
            
            # Position cursor after the inserted path
            new_cursor_pos = start + len(replacement_text)
            cursor.setPosition(new_cursor_pos)
            self.text_edit.setTextCursor(cursor)
        
        self.file_completion_widget.hide()
    
    def set_thinking_level(self, level: str):
        """思考レベルを設定"""
        self.thinking_level = level
        # Update token count when thinking level changes
        self.update_token_count()
    
    def generate_prompt(self):
        """Generate prompt and copy to clipboard"""
        text = self.text_edit.toPlainText().strip()
        if not text:
            return
        
        # File paths are already inserted when files are selected (@relative/path/to/file.ext)
        # Claude Code will automatically read the file content
        final_prompt = text
        
        # Add thinking level
        if self.thinking_level and self.thinking_level != "think":
            final_prompt = f"{self.thinking_level}\n{final_prompt}"
        
        # Copy to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(final_prompt)
        
        # Emit signal
        self.generate_and_copy.emit(final_prompt, self.thinking_level)
    
    def clear_all(self):
        """すべてクリア"""
        self.text_edit.clear()
        self.file_completion_widget.hide()
        self.update_token_count()
    
    def get_prompt_text(self) -> str:
        """プロンプトテキストを取得"""
        return self.text_edit.toPlainText()
    
    def set_prompt_text(self, text: str):
        """プロンプトテキストを設定"""
        self.text_edit.setPlainText(text)
    
    def update_token_count(self):
        """Update token count display"""
        text = self.text_edit.toPlainText()
        
        # Include thinking level in token count if it's not default
        if self.thinking_level and self.thinking_level != "think":
            text = f"{self.thinking_level}\n{text}"
        
        token_count = TokenCounter.count_tokens(text)
        formatted_count = TokenCounter.format_token_count(token_count)
        self.token_count_label.setText(formatted_count)
    
    def set_path_mode(self, mode: str):
        """パスモードを設定"""
        self.path_mode = mode