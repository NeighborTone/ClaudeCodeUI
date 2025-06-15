"""
UIスタイル定義モジュール
- サイバーパンク風のスタイルを提供
- 全体的なカラースキームとフォント設定
"""
from PySide6.QtGui import QFont

def apply_cyberpunk_style(widget):
    """サイバーパンク風のスタイルをウィジェットに適用する"""
    style_sheet = """
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
    """
    widget.setStyleSheet(style_sheet)
    
def get_main_font():
    """メインフォントを取得"""
    return QFont("Verdana", 10)
    
def get_dialog_style():
    """ダイアログ用のスタイルを取得"""
    return {
        "dialog": """
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
        """,
        "ok_button": """
            QPushButton {
                background-color: #5cb85c;
                color: #ffffff;
                border-radius: 10px;
                padding: 5px;
                margin: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #4f9f4f;
            }
            QPushButton:pressed {
                background-color: #458b45;
            }
        """,
        "cancel_button": """
            QPushButton {
                background-color: #d9534f;
                color: #ffffff;
                border-radius: 10px;
                padding: 5px;
                margin: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c94c4c;
            }
            QPushButton:pressed {
                background-color: #b43c3c;
            }
        """
    }
    
def get_drag_drop_style(active=False):
    """ドラッグ＆ドロップ領域のスタイルを取得"""
    if active:
        return """
            QLabel {
                border: 3px solid #00FFAA;
                padding: 20px;
                color: #00FFAA;
                font-size: 14pt;
                background-color: rgba(0, 255, 170, 0.2);
                font-weight: bold;
                border-radius: 8px;
            }
        """
    else:
        return """
            QLabel {
                border: 2px dashed #8a3ffc;
                padding: 20px;
                color: #8a3ffc;
                font-size: 14pt;
                background-color: rgba(138, 63, 252, 0.05);
                border-radius: 8px;
            }
        """

def get_completion_widget_style():
    """ファイル補完ウィジェットのスタイルを取得"""
    return """
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
    """ 