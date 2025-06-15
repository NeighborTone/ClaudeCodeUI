# -*- coding: utf-8 -*-
"""
Material Theme - マテリアルテーマ定義
モダンなマテリアルデザインインスパイアテーマ
"""
from PySide6.QtGui import QFont
from .base_theme import BaseTheme
from src.core.ui_strings import tr


class MaterialTheme(BaseTheme):
    """マテリアルテーマクラス - モダンなマテリアルデザイン"""
    
    def get_display_name(self):
        return tr("theme_material_name")
    
    def _build_theme(self):
        return {
            "main": """
            QWidget {
                background-color: #fafafa;
                color: #212121;
                font-family: "Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif;
            }
            QPushButton {
                background-color: #2196f3;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                color: #ffffff;
                font-size: 11pt;
                font-weight: 500;
                min-height: 32px;
                min-width: 80px;
                text-transform: uppercase;
                letter-spacing: 0.3px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #9e9e9e;
            }
            QLineEdit, QTextEdit, QComboBox {
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-size: 16px;
                padding: 12px 0px 8px 0px;
                background-color: transparent;
                color: #212121;
                border-radius: 0px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-bottom: 2px solid #2196f3;
                background-color: rgba(33, 150, 243, 0.05);
            }
            QLabel {
                color: #616161;
                font-size: 14px;
                font-weight: 400;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #212121;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #757575;
                margin-right: 8px;
            }
            QSlider::groove:horizontal {
                border: none;
                height: 4px;
                background: #e0e0e0;
                margin: 10px 0;
                border-radius: 2px;
            }
            QSlider::sub-page:horizontal {
                background: #2196f3;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #2196f3;
                border: none;
                width: 20px;
                height: 20px;
                margin: -8px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #1976d2;
            }
            QTextEdit {
                border: 1px solid #e0e0e0;
                background-color: #ffffff;
                color: #212121;
                font-family: "Roboto Mono", "Consolas", "Courier New", monospace;
                font-size: 14px;
                padding: 16px;
                border-radius: 8px;
                line-height: 1.5;
            }
            QTextEdit:focus {
                border: 2px solid #2196f3;
                background-color: #ffffff;
            }
            QTreeWidget {
                background-color: #ffffff;
                color: #212121;
                border: 1px solid #e0e0e0;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
                alternate-background-color: #f5f5f5;
                border-radius: 8px;
                outline: none;
            }
            QTreeWidget::item {
                padding: 12px 8px;
                border: none;
                border-bottom: 1px solid #eeeeee;
            }
            QTreeWidget::item:hover {
                background-color: #f5f5f5;
            }
            QTreeWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                border: none;
            }
""" + self.get_tree_branch_styles("#757575", "#757575") + """
            QHeaderView::section {
                background-color: #f5f5f5;
                color: #424242;
                padding: 12px 8px;
                border: none;
                border-bottom: 1px solid #e0e0e0;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-size: 12px;
            }
            QScrollBar:vertical {
                background-color: transparent;
                width: 12px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: #bdbdbd;
                min-height: 30px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #9e9e9e;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background-color: transparent;
                height: 12px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background-color: #bdbdbd;
                min-width: 30px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #9e9e9e;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QListWidget {
                background-color: #ffffff;
                color: #212121;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                outline: none;
            }
            QListWidget::item {
                padding: 12px 16px;
                border: none;
                border-bottom: 1px solid #eeeeee;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QMenu {
                background-color: #ffffff;
                color: #212121;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px 0px;
            }
            QMenu::item {
                padding: 12px 24px;
                border: none;
            }
            QMenu::item:selected {
                background-color: #f5f5f5;
                color: #1976d2;
            }
            QMenuBar {
                background-color: #ffffff;
                color: #212121 !important;
                border-bottom: 1px solid #e0e0e0;
                font-size: 14px !important;
                font-weight: 500 !important;
                spacing: 4px !important;
            }
            QMenuBar::item {
                padding: 8px 16px !important;
                color: #212121 !important;
                background: transparent !important;
                margin: 0px !important;
                border: none !important;
                font-size: 14px !important;
                font-weight: 500 !important;
                border-radius: 4px !important;
            }
            QMenuBar::item:selected,
            QMenuBar::item:hover {
                background-color: #f5f5f5 !important;
                color: #1976d2 !important;
            }
            QMenuBar::item:pressed {
                background-color: #e3f2fd !important;
                color: #1976d2 !important;
            }
            QStatusBar {
                background-color: #f5f5f5;
                color: #616161;
                border-top: 1px solid #e0e0e0;
                font-size: 12px;
            }
            QSplitter::handle {
                background-color: #e0e0e0;
                border: none;
            }
            QSplitter::handle:hover {
                background-color: #bdbdbd;
            }
            QToolTip {
                background-color: #616161;
                color: #ffffff;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 13px;
            }
            QMessageBox {
                background-color: #ffffff;
                color: #212121;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                min-height: 32px;
                margin: 4px;
            }
            QGroupBox {
                color: #424242;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 16px;
                padding-top: 16px;
                font-weight: 500;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #1976d2;
                background-color: #fafafa;
            }
            """,
            "completion_widget": """
            QWidget {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
            QLabel {
                color: #1976d2;
                font-weight: 500;
                padding: 12px;
                font-size: 14px;
                background-color: #f5f5f5;
                border-bottom: 1px solid #e0e0e0;
            }
            QListWidget {
                background-color: #ffffff;
                color: #212121;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 12px 16px;
                border: none;
                border-bottom: 1px solid #eeeeee;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            """,
            "main_font": QFont("Roboto", 10, QFont.Weight.Normal)
        }