# -*- coding: utf-8 -*-
"""
Prompt Input Widget - プロンプト入力ウィジェット
"""
import os
import re
from typing import Dict, List, Optional
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QPushButton, 
                              QHBoxLayout, QListWidget, QListWidgetItem, 
                              QLabel, QApplication)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QKeyEvent, QTextCursor, QFont

from src.core.indexing_adapter import AdaptiveFileSearcher
from src.core.workspace_manager import WorkspaceManager
from src.core.token_counter import TokenCounter
from src.core.path_converter import PathConverter
from src.core.ui_strings import tr
from src.ui.style_themes import get_completion_widget_style, get_main_font


class SimpleTextEdit(QTextEdit):
    """シンプルなテキストエディット（カスタムキーハンドリング付き）"""
    
    special_key_pressed = Signal(QKeyEvent)
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def keyPressEvent(self, event: QKeyEvent):
        # 特殊キーは親に委譲
        if (event.key() in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Return, Qt.Key_Escape] or
            (event.key() == Qt.Key_Return and event.modifiers() & Qt.ShiftModifier)):
            self.special_key_pressed.emit(event)
            return
        
        # 通常のキー処理
        super().keyPressEvent(event)


class SimpleCompletionWidget(QWidget):
    """シンプルな補完ウィジェット"""
    
    item_selected = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip)
        self.setMinimumHeight(600)
        self.setMaximumHeight(900)
        self.setMinimumWidth(600)
        self.setMaximumWidth(800)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.label = QLabel(tr("completion_header"))
        layout.addWidget(self.label)
        
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.list_widget)
        
        self.items = []
        self.setStyleSheet(get_completion_widget_style())
    
    def show_items(self, items: List[Dict], pos, symbol: str = '@'):
        """補完候補を表示"""
        self.items = items
        self.list_widget.clear()
        
        # シンボルに応じてラベルを更新
        try:
            if symbol == '!':
                self.label.setText(tr("completion_header_files"))
            elif symbol == '#':
                self.label.setText(tr("completion_header_folders"))
            else:  # '@'
                self.label.setText(tr("completion_header"))
        except:
            # フォールバック用テキスト
            if symbol == '!':
                self.label.setText("ファイルを選択: (Escで閉じる)")
            elif symbol == '#':
                self.label.setText("フォルダを選択: (Escで閉じる)")
            else:  # '@'
                self.label.setText("ファイル・フォルダを選択: (Escで閉じる)")
        
        if not items:
            self.hide()
            return
        
        for item in items:
            list_item = QListWidgetItem()
            item_type = item.get('type', 'file')
            
            if item_type == 'folder':
                icon = "📁"
                type_text = f" {tr('completion_folder')}"
            else:
                # ファイルタイプに基づいてアイコンを選択
                file_ext = os.path.splitext(item['name'])[1].lower()
                
                # 画像ファイル
                image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.ico'}
                # ソースファイル
                source_extensions = {'.py', '.cpp', '.c', '.h', '.hpp', '.js', '.ts', '.jsx', '.tsx', '.html', '.css'}
                # 設定ファイル
                config_extensions = {'.json', '.yaml', '.yml', '.xml', '.toml', '.ini', '.conf', '.cfg', '.config', '.csv'}
                # メディアファイル
                media_extensions = {'.wav', '.mp3', '.mp4', '.avi', '.mov'}
                
                if file_ext in image_extensions:
                    icon = "🖼️"  # 画像アイコン
                elif file_ext in source_extensions:
                    icon = "📝"  # ソースコードアイコン
                elif file_ext in config_extensions:
                    icon = "⚙️"  # 設定ファイルアイコン
                elif file_ext in media_extensions:
                    icon = "🎵"  # メディアファイルアイコン
                else:
                    icon = "📄"  # デフォルトファイルアイコン
                
                type_text = f" {tr('completion_file')}"
            
            # パス情報を追加して表示
            relative_path = item.get('relative_path', '')
            parent_dir = os.path.dirname(relative_path) if relative_path else ''
            
            if parent_dir:
                # 親ディレクトリがある場合
                display_text = f"{icon} {item['name']} ({parent_dir}) - {item['workspace']}"
            else:
                # ルートレベルの場合
                display_text = f"{icon} {item['name']} - {item['workspace']}"
            
            list_item.setText(display_text)
            list_item.setData(Qt.UserRole, item)
            self.list_widget.addItem(list_item)
        
        self.list_widget.setCurrentRow(0)
        self.move(pos)
        self.show()
    
    def _on_item_clicked(self, item):
        """アイテムクリック時"""
        data = item.data(Qt.UserRole)
        if data:
            self.item_selected.emit(data)
    
    def select_current(self):
        """現在の選択を確定"""
        current_item = self.list_widget.currentItem()
        if current_item:
            self._on_item_clicked(current_item)
    
    def move_up(self):
        """上に移動"""
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            self.list_widget.setCurrentRow(current_row - 1)
    
    def move_down(self):
        """下に移動"""
        current_row = self.list_widget.currentRow()
        if current_row < self.list_widget.count() - 1:
            self.list_widget.setCurrentRow(current_row + 1)


class PromptInputWidget(QWidget):
    """プロンプト入力ウィジェット"""
    
    generate_and_copy = Signal(str, str)
    text_changed = Signal(str)  # テキスト変更シグナル（リアルタイム更新用）
    
    def __init__(self, workspace_manager: WorkspaceManager, fast_searcher = None, parent=None):
        super().__init__(parent)
        
        self.workspace_manager = workspace_manager
        self.file_searcher = fast_searcher
        self.thinking_level = "think"
        
        # 状態管理
        self.current_match = None  # {'symbol': '@'/'$'/'#', 'match': regex_match, 'query': str}
        self.completion_active = False
        self.current_completion_symbol = '@'  # 現在の補完モード
        
        # プレビューへの参照（後で設定される）
        self.prompt_preview = None
        
        self.setup_ui()
        self.setup_completion()
    
    def setup_ui(self):
        """UIセットアップ"""
        layout = QVBoxLayout(self)
        
        # ヘッダー
        header_layout = QHBoxLayout()
        self.prompt_label = QLabel(tr("prompt_header"))
        header_layout.addWidget(self.prompt_label)
        
        self.token_count_label = QLabel(f"0 {tr('prompt_tokens')}")
        self.token_count_label.setAlignment(Qt.AlignRight)
        header_layout.addWidget(self.token_count_label)
        
        layout.addLayout(header_layout)
        
        # テキストエディット
        self.text_edit = SimpleTextEdit()
        self.text_edit.setAcceptRichText(False)
        self.text_edit.setPlaceholderText(tr("prompt_placeholder"))
        layout.addWidget(self.text_edit)
        
        # ボタン
        button_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton(tr("button_generate"))
        self.generate_btn.clicked.connect(self.generate_prompt)
        button_layout.addWidget(self.generate_btn)
        
        self.clear_btn = QPushButton(tr("button_clear"))
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_btn)
        
        layout.addLayout(button_layout)
        
        # イベント接続
        self.text_edit.special_key_pressed.connect(self.handle_special_key)
        self.text_edit.textChanged.connect(self.on_text_changed)
        # プレビュー更新をデバウンスに変更
        self.text_edit.textChanged.connect(self._start_preview_timer)
    
    def setup_completion(self):
        """補完システムセットアップ"""
        self.completion_widget = SimpleCompletionWidget(self)
        self.completion_widget.item_selected.connect(self.on_completion_selected)
        self.completion_widget.hide()
        
        self.completion_timer = QTimer()
        self.completion_timer.setSingleShot(True)
        self.completion_timer.timeout.connect(self.show_completion)
        
        # プレビュー更新用デバウンスタイマー
        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self._emit_text_changed)
    
    def handle_special_key(self, event: QKeyEvent):
        """特殊キーハンドリング"""
        if event.key() == Qt.Key_Return and event.modifiers() & Qt.ShiftModifier:
            self.generate_prompt()
            return
        
        if self.completion_active:
            if event.key() == Qt.Key_Escape:
                self.hide_completion()
            elif event.key() == Qt.Key_Return:
                self.completion_widget.select_current()
            elif event.key() == Qt.Key_Up:
                self.completion_widget.move_up()
            elif event.key() == Qt.Key_Down:
                self.completion_widget.move_down()
        else:
            # 補完が非アクティブな場合は通常のキー処理
            QTextEdit.keyPressEvent(self.text_edit, event)
    
    def on_text_changed(self):
        """テキスト変更時の処理"""
        self.update_token_count()
        
        # @/$/#検索
        cursor = self.text_edit.textCursor()
        text = self.text_edit.toPlainText()
        cursor_pos = cursor.position()
        
        # @/!/# パターンを検索（単一正規表現で効率化）
        current_match = None
        pattern = r'([@!#])([^\s@!#]*)'
        
        for match in re.finditer(pattern, text):
            start, end = match.span()
            if start <= cursor_pos <= end:
                symbol = match.group(1)
                query = match.group(2)
                current_match = {
                    'symbol': symbol,
                    'match': match,
                    'query': query
                }
                break
        
        if current_match:
            self.current_match = current_match
            self.completion_timer.start(200)
        else:
            self.hide_completion()
    
    def show_completion(self):
        """補完表示"""
        if not self.current_match or not self.file_searcher:
            return
        
        symbol = self.current_match['symbol']
        query = self.current_match['query']
        
        # シンボルに応じて適切な検索メソッドを呼び出し
        if symbol == '!':
            matches = self.file_searcher.search_files_only_by_name(query)
        elif symbol == '#':
            matches = self.file_searcher.search_folders_only_by_name(query)
        else:  # '@'
            matches = self.file_searcher.search_files_by_name(query)
        
        if matches:
            cursor = self.text_edit.textCursor()
            cursor_rect = self.text_edit.cursorRect(cursor)
            bottom_left = cursor_rect.bottomLeft()
            # 補完ウィジェットの位置調整
            bottom_left.setY(bottom_left.y() + 8)
            global_pos = self.text_edit.mapToGlobal(bottom_left)
            
            self.current_completion_symbol = symbol
            self.completion_widget.show_items(matches, global_pos, symbol)
            self.completion_active = True
    
    def hide_completion(self):
        """補完を隠す"""
        self.completion_widget.hide()
        self.completion_active = False
        self.text_edit.setFocus()
    
    def on_completion_selected(self, item_data: dict):
        """補完選択時"""
        if not self.current_match:
            return
        
        # ワークスペース相対パスを取得
        file_path = item_data['path']
        workspace_relative_path = None
        
        for workspace in self.workspace_manager.get_workspaces():
            workspace_path = workspace['path']
            if file_path.startswith(workspace_path):
                workspace_relative_path = os.path.relpath(file_path, workspace_path)
                break
        
        if workspace_relative_path is None:
            workspace_relative_path = os.path.basename(file_path)
        
        workspace_relative_path = PathConverter.normalize_path(workspace_relative_path)
        
        # テキスト置換（常に@から始まる形式で挿入）
        text = self.text_edit.toPlainText()
        start, end = self.current_match['match'].span()
        new_text = text[:start] + f"@{workspace_relative_path}" + text[end:]
        
        # カーソル位置を保存
        new_cursor_pos = start + len(f"@{workspace_relative_path}")
        
        # テキストを設定
        self.text_edit.setPlainText(new_text)
        
        # カーソル位置を復元
        cursor = self.text_edit.textCursor()
        cursor.setPosition(new_cursor_pos)
        self.text_edit.setTextCursor(cursor)
        
        self.hide_completion()
    
    def generate_prompt(self):
        """プロンプト生成"""
        # プレビュー内容を基準にした生成可能性を判定
        if not self.is_generation_possible():
            return
        
        # テンプレート統合は親ウィンドウで処理するため、生のテキストを渡す
        text = self.text_edit.toPlainText().strip()
        self.generate_and_copy.emit(text, self.thinking_level)
    
    def clear_all(self):
        """クリア"""
        self.text_edit.clear()
        self.hide_completion()
        self.update_token_count()
    
    def set_thinking_level(self, level: str):
        """思考レベル設定"""
        self.thinking_level = level
        self.update_token_count()
    
    
    def update_token_count(self, full_prompt_text: str = None):
        """
        トークン数更新
        
        Args:
            full_prompt_text: フルプロンプトテキスト（プレビューから）
                            Noneの場合は従来通りメインテキストのみでカウント
        """
        if full_prompt_text is not None:
            # プレビューからのフルプロンプトでトークンカウント
            text = full_prompt_text
        else:
            # 従来通りのメインテキスト + 思考レベルでカウント
            text = self.text_edit.toPlainText()
            if self.thinking_level and self.thinking_level != "think":
                text = f"{self.thinking_level}\n{text}"
        
        token_count = TokenCounter.count_tokens(text)
        formatted_count = TokenCounter.format_token_count(token_count)
        # Update token count with localized text
        if tr('prompt_tokens') in formatted_count:
            self.token_count_label.setText(formatted_count)
        else:
            # Format with localized token text
            self.token_count_label.setText(f"{token_count} {tr('prompt_tokens')}")
    
    def get_prompt_text(self) -> str:
        """プロンプトテキスト取得"""
        return self.text_edit.toPlainText()
    
    def set_prompt_text(self, text: str):
        """プロンプトテキスト設定"""
        self.text_edit.setPlainText(text)
    
    def set_prompt_preview_reference(self, prompt_preview):
        """プロンプトプレビューへの参照を設定"""
        self.prompt_preview = prompt_preview
    
    def is_generation_possible(self) -> bool:
        """プロンプト生成が可能かどうかを判定"""
        if self.prompt_preview is None:
            # プレビューが利用できない場合は従来の判定（入力テキストベース）
            text = self.text_edit.toPlainText().strip()
            return bool(text)
        
        # プレビューの内容を確認
        preview_content = self.prompt_preview.get_current_prompt().strip()
        return bool(preview_content)
    
    def set_text_without_completion(self, text: str):
        """オートコンプリートを無効にしてテキスト設定"""
        # 補完タイマーを停止
        self.completion_timer.stop()
        
        # 補完ウィジェットを隠す
        self.hide_completion()
        
        # テキストを設定
        self.text_edit.setPlainText(text)
        
        # カーソルを末尾に移動
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.text_edit.setTextCursor(cursor)
        
        # フォーカスを設定
        self.text_edit.setFocus()
    
    def update_language(self):
        """言語変更時にUIを更新"""
        # 完了ウィジェットのラベル更新（現在のモードに応じて）
        try:
            if self.current_completion_symbol == '!':
                self.completion_widget.label.setText(tr("completion_header_files"))
            elif self.current_completion_symbol == '#':
                self.completion_widget.label.setText(tr("completion_header_folders"))
            else:  # '@'
                self.completion_widget.label.setText(tr("completion_header"))
        except:
            # フォールバック用テキスト
            self.completion_widget.label.setText("ファイル・フォルダを選択: (Escで閉じる)")
        
        # プロンプトヘッダー更新
        self.prompt_label.setText(tr("prompt_header"))
        
        # プレースホルダーテキスト更新
        self.text_edit.setPlaceholderText(tr("prompt_placeholder"))
        
        # ボタンテキスト更新
        self.generate_btn.setText(tr("button_generate"))
        self.clear_btn.setText(tr("button_clear"))
        
        # トークン数表示を更新
        self.update_token_count()
    
    def update_file_searcher(self, fast_searcher):
        """ファイル検索エンジンを更新"""
        self.file_searcher = fast_searcher
    
    def _start_preview_timer(self):
        """プレビュー更新タイマーを開始（デバウンス）"""
        self.preview_timer.start(500)  # 500msのデバウンス
    
    def _emit_text_changed(self):
        """テキスト変更シグナルを送信"""
        self.text_changed.emit(self.text_edit.toPlainText())