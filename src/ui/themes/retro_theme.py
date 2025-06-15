# -*- coding: utf-8 -*-
"""
Retro Theme - レトロテーマ定義
80年代/90年代のターミナル風レトロテーマ
"""
from PySide6.QtGui import QFont
from .base_theme import BaseTheme
from src.core.ui_strings import tr


class RetroTheme(BaseTheme):
    """レトロテーマクラス - 80年代/90年代のターミナル風デザイン"""
    
    def get_display_name(self):
        return tr("theme_retro_name")
    
    def _build_theme(self):
        return {
            "main": """
            QWidget {
                background-color: #000000;
                color: #00ff00;
                font-family: "Courier New", "Liberation Mono", "DejaVu Sans Mono", monospace;
            }
            QPushButton {
                background-color: #001100;
                border: 2px solid #00ff00;
                border-radius: 0px;
                padding: 8px 16px;
                color: #00ff00;
                font-size: 12pt;
                font-weight: bold;
                font-family: "Courier New", monospace;
                min-height: 30px;
                min-width: 80px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #000000;
                border: 2px solid #ffff00;
            }
            QPushButton:pressed {
                background-color: #ffff00;
                color: #000000;
                border: 2px solid #00ff00;
            }
            QLineEdit, QLabel, QSlider, QTextEdit, QComboBox {
                border: 1px solid #00ff00;
                font-size: 11pt;
                padding: 4px;
                background-color: #000000;
                color: #00ff00;
                font-family: "Courier New", monospace;
                border-radius: 0px;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: #001100;
                border: 2px solid #ffff00;
                color: #ffff00;
            }
            QLabel {
                border: none;
                color: #00ff00;
                background-color: transparent;
            }
            QComboBox QAbstractItemView {
                background-color: #000000;
                color: #00ff00;
                selection-background-color: #00ff00;
                selection-color: #000000;
                border: 1px solid #00ff00;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background-color: #001100;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid #00ff00;
                margin-right: 4px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #00ff00;
                height: 6px;
                background: #000000;
                margin: 4px 0;
                border-radius: 0px;
            }
            QSlider::sub-page:horizontal {
                background: #00ff00;
                border-radius: 0px;
            }
            QSlider::handle:horizontal {
                background: #ffff00;
                border: 2px solid #00ff00;
                width: 16px;
                margin: -6px 0;
                border-radius: 0px;
            }
            QSlider::handle:horizontal:hover {
                background: #00ff00;
                border: 2px solid #ffff00;
            }
            QTextEdit {
                border: 2px solid #00ff00;
                background-color: #000000;
                color: #00ff00;
                font-family: "Courier New", "Liberation Mono", monospace;
                font-size: 11pt;
                padding: 8px;
                border-radius: 0px;
                line-height: 1.2;
            }
            QTextEdit:focus {
                border: 2px solid #ffff00;
                background-color: #001100;
                color: #ffff00;
            }
            QTreeWidget {
                background-color: #000000;
                color: #00ff00;
                border: 2px solid #00ff00;
                selection-background-color: #00ff00;
                selection-color: #000000;
                alternate-background-color: #001100;
                border-radius: 0px;
                font-family: "Courier New", monospace;
            }
            QTreeWidget::item {
                padding: 4px;
                border-bottom: 1px dotted #004400;
                font-family: "Courier New", monospace;
            }
            QTreeWidget::item:hover {
                background-color: #002200;
                color: #ffff00;
            }
            QTreeWidget::item:selected {
                background-color: #00ff00;
                color: #000000;
                border: 1px solid #ffff00;
            }
""" + self.get_tree_branch_styles("#00ff00", "#00ff00") + """
            QHeaderView::section {
                background-color: #001100;
                color: #00ff00;
                padding: 6px;
                border: 2px solid #00ff00;
                font-weight: bold;
                font-family: "Courier New", monospace;
                text-transform: uppercase;
            }
            QScrollBar:vertical {
                background-color: #000000;
                width: 16px;
                border: 1px solid #00ff00;
                border-radius: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #00ff00;
                min-height: 20px;
                border-radius: 0px;
                margin: 1px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #ffff00;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background-color: #001100;
                height: 16px;
                border: 1px solid #00ff00;
            }
            QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {
                background-color: #00ff00;
            }
            QScrollBar:horizontal {
                background-color: #000000;
                height: 16px;
                border: 1px solid #00ff00;
                border-radius: 0px;
            }
            QScrollBar::handle:horizontal {
                background-color: #00ff00;
                min-width: 20px;
                border-radius: 0px;
                margin: 1px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #ffff00;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background-color: #001100;
                width: 16px;
                border: 1px solid #00ff00;
            }
            QScrollBar::add-line:horizontal:hover, QScrollBar::sub-line:horizontal:hover {
                background-color: #00ff00;
            }
            QListWidget {
                background-color: #000000;
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 4px;
                border-radius: 0px;
                font-family: "Courier New", monospace;
            }
            QListWidget::item {
                padding: 4px;
                border-bottom: 1px dotted #004400;
            }
            QListWidget::item:hover {
                background-color: #002200;
                color: #ffff00;
            }
            QListWidget::item:selected {
                background-color: #00ff00;
                color: #000000;
            }
            QMenu {
                background-color: #000000;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 0px;
                font-family: "Courier New", monospace;
            }
            QMenu::item {
                padding: 6px 20px;
                border: none;
            }
            QMenu::item:selected {
                background-color: #00ff00;
                color: #000000;
            }
            QMenuBar {
                background-color: #000000;
                color: #00ff00 !important;
                border-bottom: 2px solid #00ff00;
                font-size: 10pt !important;
                font-weight: bold !important;
                font-family: "Courier New", monospace !important;
            }
            QMenuBar::item {
                padding: 4px 8px !important;
                color: #00ff00 !important;
                background: transparent !important;
                margin: 0px !important;
                border: none !important;
                font-size: 10pt !important;
                font-weight: bold !important;
                font-family: "Courier New", monospace !important;
                text-transform: uppercase !important;
            }
            QMenuBar::item:selected,
            QMenuBar::item:hover {
                background-color: #00ff00 !important;
                color: #000000 !important;
            }
            QMenuBar::item:pressed {
                background-color: #ffff00 !important;
                color: #000000 !important;
            }
            QStatusBar {
                background-color: #001100;
                color: #00ff00;
                border-top: 2px solid #00ff00;
                font-family: "Courier New", monospace;
                font-weight: bold;
            }
            QSplitter::handle {
                background-color: #00ff00;
                border: 1px solid #ffff00;
            }
            QSplitter::handle:hover {
                background-color: #ffff00;
            }
            QToolTip {
                background-color: #001100;
                color: #ffff00;
                border: 2px solid #00ff00;
                padding: 6px;
                border-radius: 0px;
                font-size: 10pt;
                font-family: "Courier New", monospace;
                font-weight: bold;
            }
            QMessageBox {
                background-color: #000000;
                color: #00ff00;
                border: 2px solid #00ff00;
                font-family: "Courier New", monospace;
            }
            QMessageBox QPushButton {
                min-width: 60px;
                min-height: 25px;
                font-family: "Courier New", monospace;
            }
            QGroupBox {
                color: #ffff00;
                border: 2px solid #00ff00;
                border-radius: 0px;
                margin-top: 8px;
                padding-top: 8px;
                font-weight: bold;
                font-family: "Courier New", monospace;
                text-transform: uppercase;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                color: #ffff00;
                background-color: #000000;
            }
            """,
            "completion_widget": """
            QWidget {
                background-color: #001100;
                border: 2px solid #00ff00;
                border-radius: 0px;
            }
            QLabel {
                color: #ffff00;
                font-weight: bold;
                padding: 6px;
                font-family: "Courier New", monospace;
                text-transform: uppercase;
                background-color: #000000;
                border-bottom: 1px solid #00ff00;
            }
            QListWidget {
                background-color: #000000;
                color: #00ff00;
                border: none;
                outline: none;
                font-family: "Courier New", monospace;
            }
            QListWidget::item {
                padding: 6px 8px;
                border-bottom: 1px dotted #004400;
            }
            QListWidget::item:hover {
                background-color: #002200;
                color: #ffff00;
            }
            QListWidget::item:selected {
                background-color: #00ff00;
                color: #000000;
            }
            """,
            "main_font": QFont("Courier New", 10, QFont.Weight.Normal)
        }