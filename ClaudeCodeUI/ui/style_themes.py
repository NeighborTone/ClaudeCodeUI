"""
UIテーマ定義モジュール
- 複数のテーマ（ライト、ダーク、サイバーパンク）を提供
- 動的なテーマ切り替えをサポート
"""
from PySide6.QtGui import QFont


class ThemeManager:
    """テーマ管理クラス"""
    
    def __init__(self):
        self.themes = {
            "light": self._get_light_theme(),
            "dark": self._get_dark_theme(),
            "cyberpunk": self._get_cyberpunk_theme()
        }
        self.current_theme = "cyberpunk"  # デフォルトテーマ
    
    def get_theme_names(self):
        """利用可能なテーマ名のリストを取得"""
        return list(self.themes.keys())
    
    def get_theme_display_names(self):
        """表示用のテーマ名マッピングを取得"""
        return {
            "light": "ライトモード",
            "dark": "ダークモード",
            "cyberpunk": "サイバーパンク"
        }
    
    def set_theme(self, theme_name):
        """テーマを設定"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
    
    def get_current_theme_style(self):
        """現在のテーマのスタイルシートを取得"""
        return self.themes[self.current_theme]["main"]
    
    def get_completion_widget_style(self):
        """現在のテーマのファイル補完ウィジェットスタイルを取得"""
        return self.themes[self.current_theme]["completion_widget"]
    
    def get_main_font(self):
        """現在のテーマのメインフォントを取得"""
        return self.themes[self.current_theme]["main_font"]
    
    def _get_light_theme(self):
        """ライトテーマ定義"""
        theme = {
            "main": """
            QWidget {
                background-color: #ffffff;
                color: #2b2b2b;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 10px;
                color: #2b2b2b;
                font-size: 14pt;
                min-height: 40px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #999999;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QLineEdit, QLabel, QSlider, QTextEdit, QComboBox {
                border: 1px solid #cccccc;
                font-size: 12pt;
                padding: 5px;
                background-color: #ffffff;
                color: #2b2b2b;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: #f9f9f9;
                border: 2px solid #0078d4;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #2b2b2b;
                selection-background-color: #0078d4;
                selection-color: #ffffff;
            }
            QTextEdit {
                border: 1px solid #cccccc;
                background-color: #ffffff;
                color: #2b2b2b;
                font-family: "Consolas", "Courier New", monospace;
                font-size: 11pt;
                padding: 10px;
                border-radius: 8px;
            }
            QTextEdit:focus {
                border: 2px solid #0078d4;
                background-color: #f9f9f9;
            }
            QTreeWidget {
                background-color: #ffffff;
                color: #2b2b2b;
                border: 1px solid #cccccc;
                selection-background-color: #0078d4;
                selection-color: #ffffff;
                alternate-background-color: #f5f5f5;
            }
            QTreeWidget::item {
                padding: 5px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTreeWidget::item:hover {
                background-color: #e8f0ff;
            }
            QTreeWidget::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: #2b2b2b;
                padding: 5px;
                border: 1px solid #cccccc;
                font-weight: bold;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 16px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                min-height: 20px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #999999;
            }
            QScrollBar:horizontal {
                background-color: #f0f0f0;
                height: 16px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background-color: #c0c0c0;
                min-width: 20px;
                border-radius: 8px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #999999;
            }
            QListWidget {
                background-color: #ffffff;
                color: #2b2b2b;
                border: 1px solid #cccccc;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #e0e0e0;
            }
            QListWidget::item:hover {
                background-color: #e8f0ff;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QMenu {
                background-color: #ffffff;
                color: #2b2b2b;
                border: 1px solid #cccccc;
            }
            QMenu::item {
                padding: 8px 25px;
            }
            QMenu::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #f0f0f0;
                color: #2b2b2b;
                border-bottom: 1px solid #cccccc;
            }
            QMenuBar::item {
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QStatusBar {
                background-color: #f0f0f0;
                color: #2b2b2b;
                border-top: 1px solid #cccccc;
            }
            QSplitter::handle {
                background-color: #cccccc;
            }
            QSplitter::handle:hover {
                background-color: #999999;
            }
            QToolTip {
                background-color: #f0f0f0;
                color: #2b2b2b;
                border: 1px solid #cccccc;
                padding: 5px;
                border-radius: 4px;
                font-size: 10pt;
            }
            QMessageBox {
                background-color: #ffffff;
                color: #2b2b2b;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                min-height: 30px;
            }
            """,
            "completion_widget": """
            QWidget {
                background-color: #f9f9f9;
                border: 2px solid #0078d4;
                border-radius: 8px;
            }
            QLabel {
                color: #0078d4;
                font-weight: bold;
                padding: 5px;
            }
            QListWidget {
                background-color: #ffffff;
                color: #2b2b2b;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QListWidget::item:hover {
                background-color: #e8f0ff;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            """,
            "main_font": QFont("Segoe UI", 10)
        }
        return theme
    
    def _get_dark_theme(self):
        """ダークテーマ定義"""
        theme = {
            "main": """
            QWidget {
                background-color: #2b2b2b;
                color: #e0e0e0;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }
            QPushButton {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 10px;
                color: #e0e0e0;
                font-size: 14pt;
                min-height: 40px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #505050;
                border: 1px solid #777777;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
            QLineEdit, QLabel, QSlider, QTextEdit, QComboBox {
                border: 1px solid #555555;
                font-size: 12pt;
                padding: 5px;
                background-color: #3c3c3c;
                color: #e0e0e0;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: #404040;
                border: 2px solid #007acc;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #e0e0e0;
                selection-background-color: #007acc;
                selection-color: #ffffff;
            }
            QTextEdit {
                border: 1px solid #555555;
                background-color: #2d2d2d;
                color: #e0e0e0;
                font-family: "Consolas", "Courier New", monospace;
                font-size: 11pt;
                padding: 10px;
                border-radius: 8px;
            }
            QTextEdit:focus {
                border: 2px solid #007acc;
                background-color: #333333;
            }
            QTreeWidget {
                background-color: #2b2b2b;
                color: #e0e0e0;
                border: 1px solid #555555;
                selection-background-color: #007acc;
                selection-color: #ffffff;
                alternate-background-color: #323232;
            }
            QTreeWidget::item {
                padding: 5px;
                border-bottom: 1px solid #404040;
            }
            QTreeWidget::item:hover {
                background-color: #404040;
            }
            QTreeWidget::item:selected {
                background-color: #007acc;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                color: #e0e0e0;
                padding: 5px;
                border: 1px solid #555555;
                font-weight: bold;
            }
            QScrollBar:vertical {
                background-color: #2b2b2b;
                width: 16px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: #555555;
                min-height: 20px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #777777;
            }
            QScrollBar:horizontal {
                background-color: #2b2b2b;
                height: 16px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background-color: #555555;
                min-width: 20px;
                border-radius: 8px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #777777;
            }
            QListWidget {
                background-color: #2b2b2b;
                color: #e0e0e0;
                border: 1px solid #555555;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #404040;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
            QListWidget::item:selected {
                background-color: #007acc;
                color: #ffffff;
            }
            QMenu {
                background-color: #2b2b2b;
                color: #e0e0e0;
                border: 1px solid #555555;
            }
            QMenu::item {
                padding: 8px 25px;
            }
            QMenu::item:selected {
                background-color: #007acc;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border-bottom: 1px solid #555555;
            }
            QMenuBar::item {
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #505050;
            }
            QStatusBar {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border-top: 1px solid #555555;
            }
            QSplitter::handle {
                background-color: #555555;
            }
            QSplitter::handle:hover {
                background-color: #777777;
            }
            QToolTip {
                background-color: #404040;
                color: #e0e0e0;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 4px;
                font-size: 10pt;
            }
            QMessageBox {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                min-height: 30px;
            }
            """,
            "completion_widget": """
            QWidget {
                background-color: #404040;
                border: 2px solid #007acc;
                border-radius: 8px;
            }
            QLabel {
                color: #50c7ff;
                font-weight: bold;
                padding: 5px;
            }
            QListWidget {
                background-color: #2b2b2b;
                color: #e0e0e0;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #404040;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
            QListWidget::item:selected {
                background-color: #007acc;
                color: #ffffff;
            }
            """,
            "main_font": QFont("Segoe UI", 10)
        }
        return theme
    
    def _get_cyberpunk_theme(self):
        """サイバーパンクテーマ定義（既存のスタイル）"""
        theme = {
            "main": """
            QWidget {
                background-color: #1a1a2e;
                color: #ffffff;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }
            QPushButton {
                background-color: #1a1a2e;
                border: 1px solid #8a3ffc;
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
                font-size: 14pt;
                min-height: 40px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #007C8A;
                border: 1px solid #00FFAA;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
            QLineEdit, QLabel, QSlider, QTextEdit, QComboBox {
                border: 1px solid #8a3ffc;
                font-size: 12pt;
                padding: 5px;
                background-color: #1a1a2e;
                color: #ffffff;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: #33334d;
                border: 1px solid #00FFAA;
            }
            QComboBox QAbstractItemView {
                background-color: #1a1a2e;
                color: #ffffff;
                selection-background-color: #007C8A;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 10px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #9687A3, stop:1 #c4c4c4);
                margin: 2px 0;
            }
            QSlider::add-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #9687A3, stop:1 #c4c4c4);
            }
            QSlider::sub-page:horizontal {
                background: #2AE6C7;
            }
            QSlider::handle:horizontal {
                background: #8a3ffc;
                border: 1px solid #8a3ffc;
                width: 22px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #00D1FF;
                border: 1px solid #00D1FF;
                width: 22px;
                height: 22px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:pressed {
                background: #FF4500;
                border: 1px solid #FF4500;
                width: 22px;
                height: 22px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QTabWidget::pane {
                border-top: 2px solid #8a3ffc;
            }
            QTabBar::tab {
                background: #1a1a2e;
                color: #ffffff;
                padding: 10px;
                font-size: 12pt;
            }
            QTabBar::tab:hover {
                background: #007C8A;
                color: #ffffff;
                padding: 10px;
                font-size: 12pt;
            }
            QTabBar::tab:selected {
                background-color: #2980b9;
                border: 1px solid #00FFAA;
            }
            QListWidget::item:selected {
                background-color: #007C8A;
                color: #ffffff;
            }
            QTextEdit {
                border: 1px solid #8a3ffc;
                background-color: #1a1a2e;
                color: #ffffff;
                font-family: "Consolas", "Courier New", monospace;
                font-size: 11pt;
                padding: 10px;
                border-radius: 8px;
            }
            QTextEdit:focus {
                border: 2px solid #00FFAA;
                background-color: #252540;
            }
            QTreeWidget {
                background-color: #1a1a2e;
                color: #ffffff;
                border: 1px solid #8a3ffc;
                selection-background-color: #007C8A;
                alternate-background-color: #252540;
            }
            QTreeWidget::item {
                padding: 5px;
                border-bottom: 1px solid #2a2a3e;
            }
            QTreeWidget::item:hover {
                background-color: #007C8A;
            }
            QTreeWidget::item:selected {
                background-color: #2980b9;
                color: #ffffff;
            }
            QTreeWidget::branch:has-siblings:!adjoins-item {
                border-image: url(none) 0;
            }
            QTreeWidget::branch:has-siblings:adjoins-item {
                border-image: url(none) 0;
            }
            QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {
                border-image: url(none) 0;
            }
            QHeaderView::section {
                background-color: #2a2a3e;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #8a3ffc;
                font-weight: bold;
            }
            QScrollBar:vertical {
                background-color: #1a1a2e;
                width: 16px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: #8a3ffc;
                min-height: 20px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #00FFAA;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background-color: #1a1a2e;
                height: 16px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background-color: #8a3ffc;
                min-width: 20px;
                border-radius: 8px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #00FFAA;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QListWidget {
                background-color: #1a1a2e;
                color: #ffffff;
                border: 1px solid #8a3ffc;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #2a2a3e;
            }
            QListWidget::item:hover {
                background-color: #007C8A;
            }
            QListWidget::item:selected {
                background-color: #2980b9;
                color: #ffffff;
            }
            QMenu {
                background-color: #1a1a2e;
                color: #ffffff;
                border: 1px solid #8a3ffc;
            }
            QMenu::item {
                padding: 8px 25px;
            }
            QMenu::item:selected {
                background-color: #007C8A;
            }
            QMenuBar {
                background-color: #1a1a2e;
                color: #ffffff;
                border-bottom: 1px solid #8a3ffc;
            }
            QMenuBar::item {
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #007C8A;
            }
            QStatusBar {
                background-color: #1a1a2e;
                color: #ffffff;
                border-top: 1px solid #8a3ffc;
            }
            QSplitter::handle {
                background-color: #8a3ffc;
            }
            QSplitter::handle:hover {
                background-color: #00FFAA;
            }
            QToolTip {
                background-color: #2a2a3e;
                color: #00FFAA;
                border: 1px solid #8a3ffc;
                padding: 5px;
                border-radius: 4px;
                font-size: 10pt;
            }
            QMessageBox {
                background-color: #1a1a2e;
                color: #ffffff;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                min-height: 30px;
            }
            QFileDialog {
                background-color: #1a1a2e;
                color: #ffffff;
            }
            QGroupBox {
                color: #00FFAA;
                border: 1px solid #8a3ffc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            """,
            "completion_widget": """
            QWidget {
                background-color: #2a2a3e;
                border: 2px solid #8a3ffc;
                border-radius: 8px;
            }
            QLabel {
                color: #00FFAA;
                font-weight: bold;
                padding: 5px;
            }
            QListWidget {
                background-color: #1a1a2e;
                color: #ffffff;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #2a2a3e;
            }
            QListWidget::item:hover {
                background-color: #007C8A;
            }
            QListWidget::item:selected {
                background-color: #2980b9;
                color: #ffffff;
            }
            """,
            "main_font": QFont("Verdana", 10)
        }
        return theme


# グローバルインスタンス
theme_manager = ThemeManager()


def apply_theme(widget, theme_name=None):
    """ウィジェットにテーマを適用"""
    if theme_name:
        theme_manager.set_theme(theme_name)
    widget.setStyleSheet(theme_manager.get_current_theme_style())


def get_completion_widget_style():
    """ファイル補完ウィジェットのスタイルを取得"""
    return theme_manager.get_completion_widget_style()


def get_main_font():
    """メインフォントを取得"""
    return theme_manager.get_main_font()