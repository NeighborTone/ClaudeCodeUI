# -*- coding: utf-8 -*-
"""
Dark Theme - ダークテーマ定義
"""
from PySide6.QtGui import QFont
from .base_theme import BaseTheme
from core.ui_strings import tr


class DarkTheme(BaseTheme):
    """ダークテーマクラス"""
    
    def get_display_name(self):
        return tr("theme_dark_name")
    
    def _build_theme(self):
        return {
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
                color: #e0e0e0 !important;
                border-bottom: 1px solid #555555;
                font-size: 9pt !important;
                font-weight: normal !important;
            }
            QMenuBar::item {
                padding: 4px 8px !important;
                color: #e0e0e0 !important;
                background: transparent !important;
                margin: 0px !important;
                border: none !important;
                font-size: 9pt !important;
                font-weight: normal !important;
                min-width: 30px !important;
                min-height: 20px !important;
            }
            QMenuBar::item:selected,
            QMenuBar::item:hover {
                background-color: #505050 !important;
                color: #e0e0e0 !important;
            }
            QMenuBar::item:pressed {
                background-color: #666666 !important;
                color: #ffffff !important;
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