# -*- coding: utf-8 -*-
"""
Electric Theme - エレクトリックテーマ定義
大胆で鮮やかな色使いのテーマ
"""
from PySide6.QtGui import QFont
from .base_theme import BaseTheme
from src.core.ui_strings import tr


class ElectricTheme(BaseTheme):
    """エレクトリックテーマクラス - 大胆で鮮やかな色使い"""
    
    def get_display_name(self):
        return tr("theme_electric_name")
    
    def _build_theme(self):
        return {
            "main": """
            QWidget {
                background-color: #0a0a0a;
                color: #ffffff;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }
            QPushButton {
                background-color: #1a1a1a;
                border: 2px solid #ff0080;
                border-radius: 12px;
                padding: 12px;
                color: #ffffff;
                font-size: 14pt;
                font-weight: bold;
                min-height: 40px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #ff0080;
                border: 2px solid #00ffff;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #00ffff;
                border: 2px solid #ffff00;
                color: #000000;
            }
            QLineEdit, QLabel, QSlider, QTextEdit, QComboBox {
                border: 2px solid #00ffff;
                font-size: 12pt;
                padding: 8px;
                background-color: #1a1a1a;
                color: #ffffff;
                border-radius: 8px;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: #2a2a2a;
                border: 2px solid #ff0080;
            }
            QComboBox QAbstractItemView {
                background-color: #1a1a1a;
                color: #ffffff;
                selection-background-color: #ff0080;
                selection-color: #ffffff;
                border: 2px solid #00ffff;
            }
            QSlider::groove:horizontal {
                border: 2px solid #00ffff;
                height: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff0080, stop:1 #00ffff);
                margin: 2px 0;
                border-radius: 6px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff0080, stop:1 #ffff00);
                border-radius: 6px;
            }
            QSlider::handle:horizontal {
                background: #ffff00;
                border: 2px solid #ff0080;
                width: 24px;
                margin: -8px 0;
                border-radius: 12px;
            }
            QSlider::handle:horizontal:hover {
                background: #00ffff;
                border: 2px solid #ffff00;
            }
            QTextEdit {
                border: 2px solid #00ffff;
                background-color: #0a0a0a;
                color: #ffffff;
                font-family: "Consolas", "Courier New", monospace;
                font-size: 11pt;
                padding: 12px;
                border-radius: 12px;
            }
            QTextEdit:focus {
                border: 3px solid #ff0080;
                background-color: #1a1a1a;
            }
            QTreeWidget {
                background-color: #0a0a0a;
                color: #ffffff;
                border: 2px solid #00ffff;
                selection-background-color: #ff0080;
                selection-color: #ffffff;
                alternate-background-color: #1a1a1a;
                border-radius: 8px;
            }
            QTreeWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333333;
            }
            QTreeWidget::item:hover {
                background-color: #2a2a2a;
                color: #00ffff;
            }
            QTreeWidget::item:selected {
                background-color: #ff0080;
                color: #ffffff;
                border: 1px solid #00ffff;
            }
""" + self.get_tree_branch_styles("#00ffff", "#ff0080") + """
            QHeaderView::section {
                background-color: #1a1a1a;
                color: #ffffff;
                padding: 8px;
                border: 2px solid #00ffff;
                font-weight: bold;
                font-size: 12pt;
            }
            QScrollBar:vertical {
                background-color: #0a0a0a;
                width: 18px;
                border: 2px solid #ff0080;
                border-radius: 9px;
            }
            QScrollBar::handle:vertical {
                background-color: #00ffff;
                min-height: 25px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #ffff00;
            }
            QScrollBar:horizontal {
                background-color: #0a0a0a;
                height: 18px;
                border: 2px solid #ff0080;
                border-radius: 9px;
            }
            QScrollBar::handle:horizontal {
                background-color: #00ffff;
                min-width: 25px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #ffff00;
            }
            QListWidget {
                background-color: #0a0a0a;
                color: #ffffff;
                border: 2px solid #00ffff;
                padding: 8px;
                border-radius: 8px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333333;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
                color: #00ffff;
            }
            QListWidget::item:selected {
                background-color: #ff0080;
                color: #ffffff;
            }
            QMenu {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 2px solid #00ffff;
                border-radius: 8px;
            }
            QMenu::item {
                padding: 10px 30px;
            }
            QMenu::item:selected {
                background-color: #ff0080;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #0a0a0a;
                color: #ffffff !important;
                border-bottom: 2px solid #00ffff;
                font-size: 10pt !important;
                font-weight: bold !important;
            }
            QMenuBar::item {
                padding: 6px 12px !important;
                color: #ffffff !important;
                background: transparent !important;
                margin: 0px !important;
                border: none !important;
                font-size: 10pt !important;
                font-weight: bold !important;
                min-width: 30px !important;
                min-height: 20px !important;
            }
            QMenuBar::item:selected,
            QMenuBar::item:hover {
                background-color: #ff0080 !important;
                color: #ffffff !important;
                border-radius: 4px !important;
            }
            QMenuBar::item:pressed {
                background-color: #00ffff !important;
                color: #000000 !important;
            }
            QStatusBar {
                background-color: #1a1a1a;
                color: #ffffff;
                border-top: 2px solid #00ffff;
            }
            QSplitter::handle {
                background-color: #ff0080;
                border: 1px solid #00ffff;
            }
            QSplitter::handle:hover {
                background-color: #00ffff;
            }
            QToolTip {
                background-color: #2a2a2a;
                color: #00ffff;
                border: 2px solid #ff0080;
                padding: 8px;
                border-radius: 8px;
                font-size: 11pt;
                font-weight: bold;
            }
            QMessageBox {
                background-color: #0a0a0a;
                color: #ffffff;
                border: 2px solid #00ffff;
            }
            QMessageBox QPushButton {
                min-width: 100px;
                min-height: 35px;
            }
            QGroupBox {
                color: #00ffff;
                border: 2px solid #ff0080;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 12px;
                font-weight: bold;
                font-size: 12pt;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #ffff00;
            }
            """,
            "completion_widget": """
            QWidget {
                background-color: #2a2a2a;
                border: 3px solid #ff0080;
                border-radius: 12px;
            }
            QLabel {
                color: #00ffff;
                font-weight: bold;
                padding: 8px;
                font-size: 12pt;
            }
            QListWidget {
                background-color: #0a0a0a;
                color: #ffffff;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #333333;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
                color: #00ffff;
            }
            QListWidget::item:selected {
                background-color: #ff0080;
                color: #ffffff;
            }
            """,
            "main_font": QFont("Segoe UI", 10, QFont.Weight.Bold)
        }