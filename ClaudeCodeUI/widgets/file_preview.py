# -*- coding: utf-8 -*-
"""
File Preview Widget - File content preview with syntax highlighting
"""
import os
import re
import mimetypes
from typing import Optional, List, Dict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QLabel, 
                              QScrollArea, QFrame, QHBoxLayout, QSplitter,
                              QTreeWidget, QTreeWidgetItem, QLineEdit, QPushButton)
from PySide6.QtCore import Signal, Qt, QThread, QTimer
from PySide6.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter, QTextDocument, QPixmap


class SyntaxHighlighter(QSyntaxHighlighter):
    """シンタックスハイライター"""
    
    def __init__(self, parent: QTextDocument = None, file_extension: str = ""):
        super().__init__(parent)
        self.file_extension = file_extension.lower()
        self.setup_highlighting_rules()
        self.search_term = ""
    
    def setup_highlighting_rules(self):
        """ハイライト規則を設定"""
        self.highlighting_rules = []
        
        # 基本フォーマット
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(86, 156, 214))  # Blue
        keyword_format.setFontWeight(QFont.Bold)
        
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(206, 145, 120))  # Orange
        
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(106, 153, 85))  # Green
        comment_format.setFontItalic(True)
        
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(220, 220, 170))  # Yellow
        
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(181, 206, 168))  # Light green
        
        # Python
        if self.file_extension in ['.py']:
            python_keywords = [
                'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
                'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
                'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
                'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
                'while', 'with', 'yield', 'None', 'True', 'False'
            ]
            for keyword in python_keywords:
                pattern = f'\\b{keyword}\\b'
                self.highlighting_rules.append((re.compile(pattern), keyword_format))
            
            # Python strings
            self.highlighting_rules.append((re.compile(r'".*?"'), string_format))
            self.highlighting_rules.append((re.compile(r"'.*?'"), string_format))
            
            # Python comments
            self.highlighting_rules.append((re.compile(r'#.*'), comment_format))
            
            # Python functions
            self.highlighting_rules.append((re.compile(r'\bdef\s+(\w+)'), function_format))
        
        # JavaScript/TypeScript
        elif self.file_extension in ['.js', '.ts', '.jsx', '.tsx']:
            js_keywords = [
                'abstract', 'arguments', 'await', 'boolean', 'break', 'byte',
                'case', 'catch', 'char', 'class', 'const', 'continue',
                'debugger', 'default', 'delete', 'do', 'double', 'else',
                'enum', 'eval', 'export', 'extends', 'false', 'final',
                'finally', 'float', 'for', 'function', 'goto', 'if',
                'implements', 'import', 'in', 'instanceof', 'int', 'interface',
                'let', 'long', 'native', 'new', 'null', 'package', 'private',
                'protected', 'public', 'return', 'short', 'static', 'super',
                'switch', 'synchronized', 'this', 'throw', 'throws',
                'transient', 'true', 'try', 'typeof', 'var', 'void',
                'volatile', 'while', 'with', 'yield'
            ]
            for keyword in js_keywords:
                pattern = f'\\b{keyword}\\b'
                self.highlighting_rules.append((re.compile(pattern), keyword_format))
            
            # JavaScript strings
            self.highlighting_rules.append((re.compile(r'".*?"'), string_format))
            self.highlighting_rules.append((re.compile(r"'.*?'"), string_format))
            self.highlighting_rules.append((re.compile(r'`.*?`'), string_format))
            
            # JavaScript comments
            self.highlighting_rules.append((re.compile(r'//.*'), comment_format))
            self.highlighting_rules.append((re.compile(r'/\*.*?\*/'), comment_format))
        
        # C/C++
        elif self.file_extension in ['.c', '.cpp', '.h', '.hpp', '.cxx', '.hxx']:
            cpp_keywords = [
                'alignas', 'alignof', 'and', 'and_eq', 'asm', 'atomic_cancel',
                'atomic_commit', 'atomic_noexcept', 'auto', 'bitand', 'bitor',
                'bool', 'break', 'case', 'catch', 'char', 'char8_t', 'char16_t',
                'char32_t', 'class', 'compl', 'concept', 'const', 'consteval',
                'constexpr', 'constinit', 'const_cast', 'continue', 'co_await',
                'co_return', 'co_yield', 'decltype', 'default', 'delete', 'do',
                'double', 'dynamic_cast', 'else', 'enum', 'explicit', 'export',
                'extern', 'false', 'float', 'for', 'friend', 'goto', 'if',
                'inline', 'int', 'long', 'mutable', 'namespace', 'new',
                'noexcept', 'not', 'not_eq', 'nullptr', 'operator', 'or',
                'or_eq', 'private', 'protected', 'public', 'reflexpr',
                'register', 'reinterpret_cast', 'requires', 'return', 'short',
                'signed', 'sizeof', 'static', 'static_assert', 'static_cast',
                'struct', 'switch', 'synchronized', 'template', 'this',
                'thread_local', 'throw', 'true', 'try', 'typedef', 'typeid',
                'typename', 'union', 'unsigned', 'using', 'virtual', 'void',
                'volatile', 'wchar_t', 'while', 'xor', 'xor_eq'
            ]
            for keyword in cpp_keywords:
                pattern = f'\\b{keyword}\\b'
                self.highlighting_rules.append((re.compile(pattern), keyword_format))
            
            # C++ strings
            self.highlighting_rules.append((re.compile(r'".*?"'), string_format))
            self.highlighting_rules.append((re.compile(r"'.*?'"), string_format))
            
            # C++ comments
            self.highlighting_rules.append((re.compile(r'//.*'), comment_format))
            self.highlighting_rules.append((re.compile(r'/\*.*?\*/'), comment_format))
        
        # Numbers (for all languages)
        self.highlighting_rules.append((re.compile(r'\b\d+\.?\d*\b'), number_format))
    
    def highlightBlock(self, text: str):
        """テキストブロックをハイライト"""
        # Apply syntax highlighting rules
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, format)
        
        # Highlight search terms
        if self.search_term:
            search_format = QTextCharFormat()
            search_format.setBackground(QColor(255, 255, 0, 100))  # Yellow highlight
            
            try:
                search_pattern = re.compile(re.escape(self.search_term), re.IGNORECASE)
                for match in search_pattern.finditer(text):
                    start, end = match.span()
                    self.setFormat(start, end - start, search_format)
            except re.error:
                # Handle regex errors gracefully
                pass
    
    def set_search_term(self, term: str):
        """検索語を設定"""
        self.search_term = term
        self.rehighlight()


class FileLoadThread(QThread):
    """ファイル読み込み用スレッド"""
    
    content_loaded = Signal(str, str)  # content, error_message
    
    def __init__(self, file_path: str, max_lines: int = 5000):
        super().__init__()
        self.file_path = file_path
        self.max_lines = max_lines
    
    def run(self):
        """ファイルを読み込む"""
        try:
            # ファイルサイズをチェック
            file_size = os.path.getsize(self.file_path)
            
            # 巨大ファイル（10MB以上）はプレビューを中断
            if file_size > 10 * 1024 * 1024:  # 10MB
                content = "プレビューを中断しました。\n\n"
                content += f"ファイルサイズが大きすぎます: {self.format_file_size(file_size)}\n"
                content += "このファイルは直接開いてご確認ください。"
                self.content_loaded.emit(content, "")
                return
            
            # テキストファイルとして読み込み試行
            lines_read = 0
            content_lines = []
            
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    content_lines.append(line.rstrip('\n\r'))
                    lines_read += 1
                    
                    # 5000行を超えた場合は読み込み停止
                    if lines_read >= self.max_lines:
                        content_lines.append("")
                        content_lines.append(f"[ファイルが大きいため先頭{self.max_lines}行のみ表示]")
                        content_lines.append("残りの内容は直接ファイルを開いてご確認ください。")
                        break
            
            content = '\n'.join(content_lines)
            self.content_loaded.emit(content, "")
            
        except UnicodeDecodeError:
            # バイナリファイルの場合
            content = "プレビューを中断しました。\n\n"
            content += "[バイナリファイル]\n"
            content += f"ファイルサイズ: {self.format_file_size(os.path.getsize(self.file_path))}\n"
            content += "バイナリファイルはプレビューできません。\n"
            content += "適切なアプリケーションで開いてご確認ください。"
            self.content_loaded.emit(content, "")
        
        except Exception as e:
            self.content_loaded.emit("", f"ファイル読み込みエラー: {str(e)}")
    
    def format_file_size(self, size: int) -> str:
        """ファイルサイズを読みやすい形式でフォーマット"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


class FilePreviewWidget(QWidget):
    """ファイルプレビューウィジェット"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file_path = ""
        self.load_thread = None
        self.syntax_highlighter = None
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # ヘッダー
        self.header_label = QLabel("プレビュー")
        self.header_label.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(self.header_label)
        
        # ファイル情報
        self.info_label = QLabel("ファイルを選択してください")
        self.info_label.setStyleSheet("color: gray; padding: 5px;")
        layout.addWidget(self.info_label)
        
        # プレビューエリア
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.preview_text)
        
        # 検索バー
        search_layout = QHBoxLayout()
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("ファイル内検索...")
        self.search_bar.textChanged.connect(self.on_search_text_changed)
        search_layout.addWidget(self.search_bar)
        
        self.search_clear_btn = QPushButton("クリア")
        self.search_clear_btn.clicked.connect(self.clear_search)
        self.search_clear_btn.setMaximumWidth(60)
        search_layout.addWidget(self.search_clear_btn)
        
        layout.addLayout(search_layout)
    
    def preview_file(self, file_path: str):
        """ファイルをプレビュー"""
        if not file_path or not os.path.exists(file_path):
            self.clear_preview()
            return
        
        self.current_file_path = file_path
        
        # ファイル情報を表示
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_ext = os.path.splitext(file_path)[1]
        
        size_str = self.format_file_size(file_size)
        self.header_label.setText(f"プレビュー: {file_name}")
        self.info_label.setText(f"サイズ: {size_str} | 拡張子: {file_ext}")
        
        # 画像ファイルかどうかチェック
        if self.is_image_file(file_path):
            self.preview_image(file_path)
            return
        
        # バイナリファイルかどうかチェック
        if self.is_binary_file(file_path):
            self.preview_binary(file_path)
            return
        
        # テキストファイルとして読み込み
        self.preview_text_file(file_path, file_ext)
    
    def preview_text_file(self, file_path: str, file_ext: str):
        """テキストファイルをプレビュー"""
        self.preview_text.setPlainText("読み込み中...")
        
        # 前のスレッドがあれば停止
        if self.load_thread:
            self.load_thread.quit()
            self.load_thread.wait()
        
        # ファイル読み込みスレッドを開始
        self.load_thread = FileLoadThread(file_path)
        self.load_thread.content_loaded.connect(self.on_file_loaded)
        self.load_thread.start()
        
        # シンタックスハイライターを設定
        self.syntax_highlighter = SyntaxHighlighter(self.preview_text.document(), file_ext)
    
    def preview_image(self, file_path: str):
        """画像ファイルをプレビュー"""
        try:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                content = "プレビューを中断しました。\n\n"
                content += "[画像ファイル]\n"
                content += f"サイズ: {pixmap.width()} x {pixmap.height()}\n"
                content += f"ファイル: {os.path.basename(file_path)}\n"
                content += "画像ファイルはプレビューできません。\n"
                content += "画像ビューアーで開いてご確認ください。"
                self.preview_text.setPlainText(content)
            else:
                content = "プレビューを中断しました。\n\n"
                content += "[画像ファイル - 読み込みできませんでした]\n"
                content += "ファイルが破損しているか、サポートされていない形式です。"
                self.preview_text.setPlainText(content)
        except Exception as e:
            content = "プレビューを中断しました。\n\n"
            content += f"[画像ファイル - エラー: {str(e)}]\n"
            content += "ファイルの読み込みに失敗しました。"
            self.preview_text.setPlainText(content)
    
    def preview_binary(self, file_path: str):
        """バイナリファイルをプレビュー（廃止予定 - FileLoadThreadに統合）"""
        content = "プレビューを中断しました。\n\n"
        content += "[バイナリファイル]\n"
        content += f"ファイルサイズ: {self.format_file_size(os.path.getsize(file_path))}\n"
        content += "バイナリファイルはプレビューできません。\n"
        content += "適切なアプリケーションで開いてご確認ください。"
        self.preview_text.setPlainText(content)
    
    def on_file_loaded(self, content: str, error_message: str):
        """ファイル読み込み完了"""
        if error_message:
            self.preview_text.setPlainText(f"エラー: {error_message}")
        else:
            self.preview_text.setPlainText(content)
    
    def clear_preview(self):
        """プレビューをクリア"""
        self.current_file_path = ""
        self.header_label.setText("プレビュー")
        self.info_label.setText("ファイルを選択してください")
        self.preview_text.clear()
        self.syntax_highlighter = None
        self.search_bar.clear()
    
    def is_image_file(self, file_path: str) -> bool:
        """画像ファイルかどうかチェック"""
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.ico', '.tiff', '.webp'}
        return os.path.splitext(file_path)[1].lower() in image_extensions
    
    def is_binary_file(self, file_path: str) -> bool:
        """バイナリファイルかどうかチェック"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if b'\0' in chunk:  # NULL文字があればバイナリ
                    return True
                
                # テキスト文字の比率をチェック
                text_chars = sum(1 for b in chunk if 32 <= b <= 126 or b in [9, 10, 13])
                return text_chars / len(chunk) < 0.75 if chunk else False
        except:
            return True
    
    def format_file_size(self, size: int) -> str:
        """ファイルサイズを読みやすい形式でフォーマット"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    def on_search_text_changed(self, text: str):
        """検索テキスト変更時の処理"""
        self.search_timer.stop()
        if text.strip():
            self.search_timer.start(300)  # 300ms後に検索実行
        else:
            self.clear_search_highlight()
    
    def perform_search(self):
        """検索を実行"""
        search_term = self.search_bar.text().strip()
        if search_term and self.syntax_highlighter:
            self.syntax_highlighter.set_search_term(search_term)
    
    def clear_search(self):
        """検索をクリア"""
        self.search_bar.clear()
        self.clear_search_highlight()
    
    def clear_search_highlight(self):
        """検索ハイライトをクリア"""
        if self.syntax_highlighter:
            self.syntax_highlighter.set_search_term("")