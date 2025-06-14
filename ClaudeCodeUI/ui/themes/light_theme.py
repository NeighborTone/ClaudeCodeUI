# -*- coding: utf-8 -*-
"""
Light Theme - ライトテーマ定義
"""
from PySide6.QtGui import QFont
from .base_theme import BaseTheme
from core.ui_strings import tr


class LightTheme(BaseTheme):
    """ライトテーマクラス"""
    
    def get_display_name(self):
        return tr("theme_light_name")
    
    def _build_theme(self):
        return {
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
                color: #2b2b2b !important;
                border-bottom: 1px solid #cccccc;
                font-size: 9pt !important;
                font-weight: normal !important;
            }
            QMenuBar::item {
                padding: 4px 8px !important;
                color: #2b2b2b !important;
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
                background-color: #e0e0e0 !important;
                color: #2b2b2b !important;
            }
            QMenuBar::item:pressed {
                background-color: #d0d0d0 !important;
                color: #2b2b2b !important;
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