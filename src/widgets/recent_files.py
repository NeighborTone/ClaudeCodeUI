# -*- coding: utf-8 -*-
"""
Recent Files Widget - 最近使用したファイルの表示ウィジェット
"""
import os
from typing import List, Dict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem, 
                              QLabel, QHBoxLayout, QPushButton)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from src.core.ui_strings import tr


class RecentFilesWidget(QWidget):
    """最近使用したファイルの表示ウィジェット"""
    
    file_selected = Signal(dict)  # ファイル選択シグナル
    
    def __init__(self, max_items=10, parent=None):
        super().__init__(parent)
        self.max_items = max_items
        self.recent_files = []  # ファイル情報のリスト
        self.setup_ui()
    
    def setup_ui(self):
        """UIセットアップ"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # ヘッダー
        header_layout = QHBoxLayout()
        
        self.label = QLabel(tr("recent_files_header"))
        self.label.setFont(QFont("", 9, QFont.Bold))
        header_layout.addWidget(self.label)
        
        # クリアボタン
        self.clear_btn = QPushButton(tr("button_clear"))
        self.clear_btn.setMaximumWidth(50)
        self.clear_btn.clicked.connect(self.clear_recent_files)
        header_layout.addWidget(self.clear_btn)
        
        layout.addLayout(header_layout)
        
        # ファイルリスト
        self.list_widget = QListWidget()
        self.list_widget.setMaximumHeight(200)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.list_widget)
        
        # 初期状態では非表示
        self.setVisible(False)
    
    def add_file(self, file_info: Dict):
        """ファイルを最近使用したリストに追加
        
        Args:
            file_info: ファイル情報辞書 (name, relative_path, workspace等)
        """
        if not file_info or 'relative_path' not in file_info:
            return
        
        file_path = file_info['relative_path']
        
        # 既存のエントリを削除
        self.recent_files = [f for f in self.recent_files if f.get('relative_path') != file_path]
        
        # 先頭に追加
        self.recent_files.insert(0, file_info)
        
        # 最大数を超える場合は末尾を削除
        self.recent_files = self.recent_files[:self.max_items]
        
        # 表示を更新
        self.update_display()
    
    def update_display(self):
        """表示を更新"""
        self.list_widget.clear()
        
        if not self.recent_files:
            self.setVisible(False)
            return
        
        self.setVisible(True)
        
        for file_info in self.recent_files:
            item = QListWidgetItem()
            
            # ファイル名とパス情報を表示
            name = file_info.get('name', '')
            relative_path = file_info.get('relative_path', '')
            workspace = file_info.get('workspace', '')
            
            # ファイルタイプに基づいてアイコンを選択
            file_ext = os.path.splitext(name)[1].lower()
            
            # アイコン選択（prompt_input.pyと同じロジック）
            image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.ico'}
            source_extensions = {'.py', '.cpp', '.c', '.h', '.hpp', '.js', '.ts', '.jsx', '.tsx', '.html', '.css'}
            config_extensions = {'.json', '.yaml', '.yml', '.xml', '.toml', '.ini', '.conf', '.cfg', '.config', '.csv'}
            media_extensions = {'.wav', '.mp3', '.mp4', '.avi', '.mov'}
            
            if file_ext in image_extensions:
                icon = "🖼️"
            elif file_ext in source_extensions:
                icon = "📝"
            elif file_ext in config_extensions:
                icon = "⚙️"
            elif file_ext in media_extensions:
                icon = "🎵"
            else:
                icon = "📄"
            
            # 表示テキスト作成
            parent_dir = os.path.dirname(relative_path) if relative_path else ''
            if parent_dir:
                display_text = f"{icon} {name} ({parent_dir})"
            else:
                display_text = f"{icon} {name}"
            
            item.setText(display_text)
            item.setData(Qt.UserRole, file_info)
            item.setToolTip(f"{relative_path} - {workspace}")
            
            self.list_widget.addItem(item)
    
    def clear_recent_files(self):
        """最近使用したファイルをクリア"""
        self.recent_files.clear()
        self.update_display()
    
    def get_recent_files(self) -> List[Dict]:
        """最近使用したファイルのリストを取得"""
        return self.recent_files.copy()
    
    def set_recent_files(self, files: List[Dict]):
        """最近使用したファイルのリストを設定"""
        self.recent_files = files[:self.max_items]
        self.update_display()
    
    def _on_item_clicked(self, item: QListWidgetItem):
        """アイテムクリック時の処理"""
        file_info = item.data(Qt.UserRole)
        if file_info:
            self.file_selected.emit(file_info)
    
    def _on_item_double_clicked(self, item: QListWidgetItem):
        """アイテムダブルクリック時の処理（プロンプトに追加）"""
        file_info = item.data(Qt.UserRole)
        if file_info:
            # ダブルクリックの場合は異なるシグナルを発行する可能性があるが
            # 現在は同じ処理とする
            self.file_selected.emit(file_info)
    
    def update_language(self):
        """言語変更時にUIを更新"""
        self.label.setText(tr("recent_files_header"))
        self.clear_btn.setText(tr("button_clear"))