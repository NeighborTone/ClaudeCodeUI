# -*- coding: utf-8 -*-
"""
Thinking Level Selector Widget - Thinking level selection functionality
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PySide6.QtCore import Signal


class ThinkingSelectorWidget(QWidget):
    """思考レベル選択ウィジェット"""
    
    thinking_level_changed = Signal(str)  # 思考レベルが変更されたときのシグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.thinking_levels = [
            ("think", "think - 通常"),
            ("think harder", "think harder - 少し深く"),
            ("think deeply", "think deeply - 深く"),
            ("think intensely", "think intensely - 集中的に"),
            ("think longer", "think longer - 長時間"),
            ("think really hard", "think really hard - 非常に深く"),
            ("think super hard", "think super hard - 超深く"),
            ("think very hard", "think very hard - とても深く"),
            ("ultrathink", "ultrathink - 極限"),
            ("think about it", "think about it - 考え込む"),
            ("think a lot", "think a lot - たくさん考える"),
            ("think hard", "think hard - 一生懸命"),
            ("think more", "think more - もっと考える"),
            ("megathink", "megathink - メガ思考")
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # ラベル
        label = QLabel("思考レベル:")
        layout.addWidget(label)
        
        # コンボボックス
        self.combo = QComboBox()
        for level_key, level_name in self.thinking_levels:
            self.combo.addItem(level_name, level_key)
        
        # デフォルトは「通常」を選択
        self.combo.setCurrentIndex(0)
        
        self.combo.currentTextChanged.connect(self.on_selection_changed)
        layout.addWidget(self.combo)
    
    def on_selection_changed(self):
        """選択が変更されたとき"""
        current_data = self.combo.currentData()
        if current_data:
            self.thinking_level_changed.emit(current_data)
    
    def get_current_thinking_level(self) -> str:
        """現在選択されている思考レベルを取得"""
        return self.combo.currentData() or "think"
    
    def set_thinking_level(self, level: str):
        """思考レベルを設定"""
        for i in range(self.combo.count()):
            if self.combo.itemData(i) == level:
                self.combo.setCurrentIndex(i)
                break