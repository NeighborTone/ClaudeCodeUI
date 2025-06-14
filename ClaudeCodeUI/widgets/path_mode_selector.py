# -*- coding: utf-8 -*-
"""
Path Mode Selector Widget - Path format selection functionality
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PySide6.QtCore import Signal

from core.path_converter import PathConverter


class PathModeSelectorWidget(QWidget):
    """パスモード選択ウィジェット"""
    
    path_mode_changed = Signal(str)  # パスモードが変更されたときのシグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.path_modes = [
            ("windows", "Windows - 標準パス形式"),
            ("wsl", "WSL - /mnt/c形式")
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # ラベル
        label = QLabel("パスモード:")
        layout.addWidget(label)
        
        # コンボボックス
        self.combo = QComboBox()
        for mode_key, mode_name in self.path_modes:
            self.combo.addItem(mode_name, mode_key)
        
        # デフォルトは環境に応じて自動選択
        default_mode = PathConverter.get_default_mode()
        for i in range(self.combo.count()):
            if self.combo.itemData(i) == default_mode:
                self.combo.setCurrentIndex(i)
                break
        
        self.combo.currentTextChanged.connect(self.on_selection_changed)
        layout.addWidget(self.combo)
    
    def on_selection_changed(self):
        """選択が変更されたとき"""
        current_data = self.combo.currentData()
        if current_data:
            self.path_mode_changed.emit(current_data)
    
    def get_current_path_mode(self) -> str:
        """現在選択されているパスモードを取得"""
        return self.combo.currentData() or "windows"
    
    def set_path_mode(self, mode: str):
        """パスモードを設定"""
        for i in range(self.combo.count()):
            if self.combo.itemData(i) == mode:
                self.combo.setCurrentIndex(i)
                break