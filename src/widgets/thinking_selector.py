# -*- coding: utf-8 -*-
"""
Thinking Level Selector Widget - Thinking level selection functionality
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PySide6.QtCore import Signal
from src.core.ui_strings import tr, UIStrings


class ThinkingSelectorWidget(QWidget):
    """思考レベル選択ウィジェット"""
    
    thinking_level_changed = Signal(str)  # 思考レベルが変更されたときのシグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 思考レベルのキーのみを定義（表示名は動的に生成）
        self.thinking_level_keys = [
            "think",
            "think more", 
            "think harder",
            "think hard",
            "think deeply",
            "think intensely", 
            "think longer",
            "think a lot",
            "think about it",
            "think very hard", 
            "think really hard",
            "think super hard",
            "megathink",
            "ultrathink"
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # ラベル
        self.label = QLabel(tr("label_thinking_level"))
        layout.addWidget(self.label)
        
        # コンボボックス
        self.combo = QComboBox()
        self.populate_combo()
        
        # デフォルトは「通常」を選択
        self.combo.setCurrentIndex(0)
        
        self.combo.currentTextChanged.connect(self.on_selection_changed)
        layout.addWidget(self.combo)
    
    def on_selection_changed(self):
        """選択が変更されたとき"""
        current_data = self.combo.currentData()
        if current_data:
            self.thinking_level_changed.emit(current_data)
    
    def populate_combo(self):
        """コンボボックスを現在の言語で埋める"""
        self.combo.clear()
        for level_key in self.thinking_level_keys:
            level_display = UIStrings.get_thinking_level_display(level_key)
            self.combo.addItem(level_display, level_key)
    
    def update_language(self):
        """言語変更時にUIを更新"""
        # ラベルを更新
        self.label.setText(tr("label_thinking_level"))
        
        # 現在の選択を保存
        current_level = self.get_current_thinking_level()
        
        # コンボボックスを再構築
        self.populate_combo()
        
        # 選択を復元
        self.set_thinking_level(current_level)
    
    def get_current_thinking_level(self) -> str:
        """現在選択されている思考レベルを取得"""
        return self.combo.currentData() or "think"
    
    def set_thinking_level(self, level: str):
        """思考レベルを設定"""
        for i in range(self.combo.count()):
            if self.combo.itemData(i) == level:
                self.combo.setCurrentIndex(i)
                break
        # デフォルトは最初の項目を選択
        if self.combo.currentIndex() == -1 and self.combo.count() > 0:
            self.combo.setCurrentIndex(0)