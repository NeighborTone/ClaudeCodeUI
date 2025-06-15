# -*- coding: utf-8 -*-
"""
Sci-Fi Theme - サイファイテーマ定義
未来的な青系のSF感あふれるテーマ
"""
from PySide6.QtGui import QFont
from .base_theme import BaseTheme
from src.core.ui_strings import tr


class SciFiTheme(BaseTheme):
    """サイファイテーマクラス - 未来的な青系のSF感"""
    
    def get_display_name(self):
        return tr("theme_scifi_name")
    
    def _build_theme(self):
        return {
            "main": """
            QWidget {
                background-color: #0a0f1a;
                color: #b3e5fc;
                font-family: "Consolas", "Liberation Mono", "DejaVu Sans Mono", monospace;
            }
            QPushButton {
                background-color: #1a237e;
                border: 2px solid #0288d1;
                border-radius: 4px;
                padding: 10px 20px;
                color: #e1f5fe;
                font-size: 11pt;
                font-weight: bold;
                min-height: 32px;
                min-width: 90px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #0288d1;
                border: 2px solid #00bcd4;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #00838f;
                border: 2px solid #004d40;
                color: #e0f2f1;
            }
            QLineEdit, QLabel, QSlider, QTextEdit, QComboBox {
                border: 1px solid #0288d1;
                font-size: 11pt;
                padding: 6px;
                background-color: #0d1421;
                color: #b3e5fc;
                border-radius: 4px;
                selection-background-color: #1976d2;
                selection-color: #ffffff;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: #1a237e;
                border: 2px solid #00bcd4;
                color: #e1f5fe;
            }
            QLabel {
                border: none;
                background-color: transparent;
                color: #81d4fa;
            }
            QComboBox QAbstractItemView {
                background-color: #0d1421;
                color: #b3e5fc;
                selection-background-color: #1976d2;
                selection-color: #ffffff;
                border: 1px solid #0288d1;
                border-radius: 4px;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
                background-color: #1a237e;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 7px solid #0288d1;
                margin-right: 6px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #0288d1;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0d1421, stop:1 #1a237e);
                margin: 4px 0;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00bcd4, stop:1 #0288d1);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #00e5ff;
                border: 2px solid #0288d1;
                width: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #18ffff;
                border: 2px solid #00bcd4;
            }
            QTextEdit {
                border: 2px solid #0288d1;
                background-color: #0a0f1a;
                color: #b3e5fc;
                font-family: "Consolas", "Liberation Mono", "DejaVu Sans Mono", monospace;
                font-size: 11pt;
                padding: 12px;
                border-radius: 6px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border: 2px solid #00bcd4;
                background-color: #0d1421;
                color: #e1f5fe;
            }
            QTreeWidget {
                background-color: #0a0f1a;
                color: #b3e5fc;
                border: 2px solid #0288d1;
                selection-background-color: #1976d2;
                selection-color: #ffffff;
                alternate-background-color: #0d1421;
                border-radius: 6px;
                gridline-color: #1a237e;
            }
            QTreeWidget::item {
                padding: 6px;
                border-bottom: 1px solid #1a237e;
                border-right: 1px solid #1a237e;
            }
            QTreeWidget::item:hover {
                background-color: #1a237e;
                color: #e1f5fe;
            }
            QTreeWidget::item:selected {
                background-color: #1976d2;
                color: #ffffff;
                border: 1px solid #00bcd4;
            }
""" + self.get_tree_branch_styles("#00bcd4", "#0288d1") + """
            QHeaderView::section {
                background-color: #1a237e;
                color: #e1f5fe;
                padding: 8px;
                border: 1px solid #0288d1;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QScrollBar:vertical {
                background-color: #0d1421;
                width: 16px;
                border: 1px solid #0288d1;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical {
                background-color: #1976d2;
                min-height: 25px;
                border-radius: 6px;
                margin: 2px;
                border: 1px solid #0288d1;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #00bcd4;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background-color: #1a237e;
                height: 16px;
                border: 1px solid #0288d1;
                border-radius: 8px;
            }
            QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {
                background-color: #0288d1;
            }
            QScrollBar:horizontal {
                background-color: #0d1421;
                height: 16px;
                border: 1px solid #0288d1;
                border-radius: 8px;
            }
            QScrollBar::handle:horizontal {
                background-color: #1976d2;
                min-width: 25px;
                border-radius: 6px;
                margin: 2px;
                border: 1px solid #0288d1;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #00bcd4;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background-color: #1a237e;
                width: 16px;
                border: 1px solid #0288d1;
                border-radius: 8px;
            }
            QScrollBar::add-line:horizontal:hover, QScrollBar::sub-line:horizontal:hover {
                background-color: #0288d1;
            }
            QListWidget {
                background-color: #0a0f1a;
                color: #b3e5fc;
                border: 2px solid #0288d1;
                padding: 6px;
                border-radius: 6px;
                gridline-color: #1a237e;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #1a237e;
                border-radius: 2px;
            }
            QListWidget::item:hover {
                background-color: #1a237e;
                color: #e1f5fe;
            }
            QListWidget::item:selected {
                background-color: #1976d2;
                color: #ffffff;
            }
            QMenu {
                background-color: #0d1421;
                color: #b3e5fc;
                border: 2px solid #0288d1;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
                margin: 1px;
            }
            QMenu::item:selected {
                background-color: #1976d2;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #0a0f1a;
                color: #b3e5fc !important;
                border-bottom: 2px solid #0288d1;
                font-size: 10pt !important;
                font-weight: bold !important;
                spacing: 6px !important;
            }
            QMenuBar::item {
                padding: 6px 12px !important;
                color: #b3e5fc !important;
                background: transparent !important;
                margin: 0px !important;
                border: none !important;
                font-size: 10pt !important;
                font-weight: bold !important;
                border-radius: 4px !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
            }
            QMenuBar::item:selected,
            QMenuBar::item:hover {
                background-color: #1a237e !important;
                color: #e1f5fe !important;
            }
            QMenuBar::item:pressed {
                background-color: #1976d2 !important;
                color: #ffffff !important;
            }
            QStatusBar {
                background-color: #0d1421;
                color: #81d4fa;
                border-top: 2px solid #0288d1;
                font-weight: bold;
                padding: 4px;
            }
            QSplitter::handle {
                background-color: #0288d1;
                border: 1px solid #00bcd4;
            }
            QSplitter::handle:hover {
                background-color: #00bcd4;
            }
            QToolTip {
                background-color: #1a237e;
                color: #e1f5fe;
                border: 2px solid #00bcd4;
                padding: 8px;
                border-radius: 6px;
                font-size: 10pt;
                font-weight: bold;
            }
            QMessageBox {
                background-color: #0a0f1a;
                color: #b3e5fc;
                border: 2px solid #0288d1;
                border-radius: 8px;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                min-height: 30px;
            }
            QGroupBox {
                color: #81d4fa;
                border: 2px solid #0288d1;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px 0 6px;
                color: #00e5ff;
                background-color: #0a0f1a;
            }
            """,
            "completion_widget": """
            QWidget {
                background-color: #0d1421;
                border: 2px solid #00bcd4;
                border-radius: 8px;
            }
            QLabel {
                color: #00e5ff;
                font-weight: bold;
                padding: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                background-color: #1a237e;
                border-bottom: 1px solid #0288d1;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QListWidget {
                background-color: #0a0f1a;
                color: #b3e5fc;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-bottom: 1px solid #1a237e;
                border-radius: 2px;
            }
            QListWidget::item:hover {
                background-color: #1a237e;
                color: #e1f5fe;
            }
            QListWidget::item:selected {
                background-color: #1976d2;
                color: #ffffff;
            }
            """,
            "main_font": QFont("Consolas", 10, QFont.Weight.Normal)
        }