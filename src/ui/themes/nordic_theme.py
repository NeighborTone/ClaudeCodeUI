# -*- coding: utf-8 -*-
"""
Nordic Theme - ノルディックテーマ定義
北欧風の落ち着いたカラーパレット
"""
from PySide6.QtGui import QFont
from .base_theme import BaseTheme
from src.core.ui_strings import tr


class NordicTheme(BaseTheme):
    """ノルディックテーマクラス"""
    
    def get_display_name(self):
        return tr("theme_nordic_name")
    
    def _build_theme(self):
        return {
            "main": """
            QWidget {
                background-color: #2e3440;
                color: #d8dee9;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }
            QPushButton {
                background-color: #3b4252;
                border: 1px solid #4c566a;
                border-radius: 8px;
                padding: 10px;
                color: #d8dee9;
                font-size: 14pt;
                min-height: 40px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #434c5e;
                border: 1px solid #5e81ac;
            }
            QPushButton:pressed {
                background-color: #4c566a;
            }
            QLineEdit, QLabel, QSlider, QTextEdit, QComboBox {
                border: 1px solid #4c566a;
                font-size: 12pt;
                padding: 5px;
                background-color: #3b4252;
                color: #d8dee9;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: #434c5e;
                border: 2px solid #88c0d0;
            }
            QComboBox QAbstractItemView {
                background-color: #3b4252;
                color: #d8dee9;
                selection-background-color: #5e81ac;
                selection-color: #eceff4;
            }
            QTextEdit {
                border: 1px solid #4c566a;
                background-color: #2e3440;
                color: #d8dee9;
                font-family: "Consolas", "Courier New", monospace;
                font-size: 11pt;
                padding: 10px;
                border-radius: 8px;
            }
            QTextEdit:focus {
                border: 2px solid #88c0d0;
                background-color: #3b4252;
            }
            QTreeWidget {
                background-color: #2e3440;
                color: #d8dee9;
                border: 1px solid #4c566a;
                selection-background-color: #5e81ac;
                selection-color: #eceff4;
                alternate-background-color: #3b4252;
            }
            QTreeWidget::item {
                padding: 5px;
                border-bottom: 1px solid #434c5e;
            }
            QTreeWidget::item:hover {
                background-color: #434c5e;
            }
            QTreeWidget::item:selected {
                background-color: #5e81ac;
                color: #eceff4;
            }
            QHeaderView::section {
                background-color: #3b4252;
                color: #d8dee9;
                padding: 5px;
                border: 1px solid #4c566a;
                font-weight: bold;
            }
            QScrollBar:vertical {
                background-color: #2e3440;
                width: 16px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: #4c566a;
                min-height: 20px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #5e81ac;
            }
            QScrollBar:horizontal {
                background-color: #2e3440;
                height: 16px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background-color: #4c566a;
                min-width: 20px;
                border-radius: 8px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #5e81ac;
            }
            QListWidget {
                background-color: #2e3440;
                color: #d8dee9;
                border: 1px solid #4c566a;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #434c5e;
            }
            QListWidget::item:hover {
                background-color: #434c5e;
            }
            QListWidget::item:selected {
                background-color: #5e81ac;
                color: #eceff4;
            }
            QMenu {
                background-color: #2e3440;
                color: #d8dee9;
                border: 1px solid #4c566a;
            }
            QMenu::item {
                padding: 8px 25px;
            }
            QMenu::item:selected {
                background-color: #5e81ac;
                color: #eceff4;
            }
            QMenuBar {
                background-color: #3b4252;
                color: #d8dee9 !important;
                border-bottom: 1px solid #4c566a;
                font-size: 9pt !important;
                font-weight: normal !important;
            }
            QMenuBar::item {
                padding: 4px 8px !important;
                color: #d8dee9 !important;
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
                background-color: #434c5e !important;
                color: #d8dee9 !important;
            }
            QMenuBar::item:pressed {
                background-color: #5e81ac !important;
                color: #eceff4 !important;
            }
            QStatusBar {
                background-color: #3b4252;
                color: #d8dee9;
                border-top: 1px solid #4c566a;
            }
            QSplitter::handle {
                background-color: #4c566a;
            }
            QSplitter::handle:hover {
                background-color: #5e81ac;
            }
            QToolTip {
                background-color: #434c5e;
                color: #eceff4;
                border: 1px solid #4c566a;
                padding: 5px;
                border-radius: 4px;
                font-size: 10pt;
            }
            QMessageBox {
                background-color: #2e3440;
                color: #d8dee9;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                min-height: 30px;
            }
            """,
            "completion_widget": """
            QWidget {
                background-color: #434c5e;
                border: 2px solid #88c0d0;
                border-radius: 8px;
            }
            QLabel {
                color: #88c0d0;
                font-weight: bold;
                padding: 5px;
            }
            QListWidget {
                background-color: #2e3440;
                color: #d8dee9;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #434c5e;
            }
            QListWidget::item:hover {
                background-color: #434c5e;
            }
            QListWidget::item:selected {
                background-color: #5e81ac;
                color: #eceff4;
            }
            """,
            "main_font": QFont("Segoe UI", 10)
        }