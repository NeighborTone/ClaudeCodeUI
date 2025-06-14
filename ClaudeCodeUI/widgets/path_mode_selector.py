# -*- coding: utf-8 -*-
"""
Path Mode Selector Widget - Path format selection functionality
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PySide6.QtCore import Signal

from core.path_converter import PathConverter
from core.ui_strings import tr, UIStrings


class PathModeSelectorWidget(QWidget):
    """パスモード選択ウィジェット"""
    
    path_mode_changed = Signal(str)  # パスモードが変更されたときのシグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # パスモードのキーのみを定義（表示名は動的に生成）
        self.path_mode_keys = ["windows", "wsl"]
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # ラベル
        self.label = QLabel(tr("label_path_mode"))
        layout.addWidget(self.label)
        
        # コンボボックス
        self.combo = QComboBox()
        self.populate_combo()
        
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
    
    def populate_combo(self):
        """コンボボックスを現在の言語で埋める"""
        self.combo.clear()
        for mode_key in self.path_mode_keys:
            mode_display = UIStrings.get_path_mode_display(mode_key)
            self.combo.addItem(mode_display, mode_key)
    
    def update_language(self):
        """言語変更時にUIを更新"""
        # ラベルを更新
        self.label.setText(tr("label_path_mode"))
        
        # 現在の選択を保存
        current_mode = self.get_current_path_mode()
        
        # コンボボックスを再構築
        self.populate_combo()
        
        # 選択を復元
        self.set_path_mode(current_mode)
    
    def get_current_path_mode(self) -> str:
        """現在選択されているパスモードを取得"""
        return self.combo.currentData() or "windows"
    
    def set_path_mode(self, mode: str):
        """パスモードを設定"""
        for i in range(self.combo.count()):
            if self.combo.itemData(i) == mode:
                self.combo.setCurrentIndex(i)
                break
        # デフォルトが見つからない場合は最初の項目を選択
        if self.combo.currentIndex() == -1 and self.combo.count() > 0:
            self.combo.setCurrentIndex(0)