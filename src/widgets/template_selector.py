# -*- coding: utf-8 -*-
"""
Template Selector Widget - テンプレート選択ウィジェット
プリプロンプトとポストプロンプトの選択機能
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QComboBox, QMessageBox)
from PySide6.QtCore import Signal, QTimer
from src.core.template_manager import get_template_manager
from src.core.ui_strings import tr


class TemplateSelector(QWidget):
    """テンプレート選択ウィジェット"""
    
    # シグナル
    template_changed = Signal()  # テンプレート選択変更時
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.template_manager = get_template_manager()
        self.setup_ui()
        self.load_templates()
        
        # 言語変更対応用のタイマー
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_language)
        self.update_timer.setSingleShot(True)
    
    def setup_ui(self):
        """UIセットアップ"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)
        
        # プリプロンプト選択
        pre_layout = QHBoxLayout()
        self.pre_label = QLabel(tr("label_pre_template"))
        self.pre_combo = QComboBox()
        self.pre_combo.setMinimumWidth(200)
        self.pre_combo.currentTextChanged.connect(self.on_template_changed)
        
        pre_layout.addWidget(self.pre_label)
        pre_layout.addWidget(self.pre_combo, 1)
        layout.addLayout(pre_layout)
        
        # ポストプロンプト選択
        post_layout = QHBoxLayout()
        self.post_label = QLabel(tr("label_post_template"))
        self.post_combo = QComboBox()
        self.post_combo.setMinimumWidth(200)
        self.post_combo.currentTextChanged.connect(self.on_template_changed)
        
        post_layout.addWidget(self.post_label)
        post_layout.addWidget(self.post_combo, 1)
        layout.addLayout(post_layout)
        
        # プレビューボタンは削除（リアルタイム更新に変更）
    
    def load_templates(self):
        """テンプレートを読み込み"""
        # テンプレートマネージャーから最新データを取得
        self.template_manager.reload_templates()
        
        # プリプロンプトコンボボックス
        self.pre_combo.clear()
        self.pre_combo.addItem(tr("template_none"))
        pre_templates = self.template_manager.get_pre_template_names()
        self.pre_combo.addItems(pre_templates)
        
        # ポストプロンプトコンボボックス
        self.post_combo.clear()
        self.post_combo.addItem(tr("template_none"))
        post_templates = self.template_manager.get_post_template_names()
        self.post_combo.addItems(post_templates)
    
    def on_template_changed(self):
        """テンプレート選択変更時"""
        self.template_changed.emit()
    
    def get_selected_pre_template(self) -> str:
        """選択されたプリプロンプトテンプレート名を取得"""
        current_text = self.pre_combo.currentText()
        if current_text == tr("template_none"):
            return ""
        return current_text
    
    def get_selected_post_template(self) -> str:
        """選択されたポストプロンプトテンプレート名を取得"""
        current_text = self.post_combo.currentText()
        if current_text == tr("template_none"):
            return ""
        return current_text
    
    def set_selected_pre_template(self, template_name: str):
        """プリプロンプトテンプレートを設定"""
        if not template_name:
            template_name = tr("template_none")
        
        index = self.pre_combo.findText(template_name)
        if index >= 0:
            self.pre_combo.setCurrentIndex(index)
    
    def set_selected_post_template(self, template_name: str):
        """ポストプロンプトテンプレートを設定"""
        if not template_name:
            template_name = tr("template_none")
        
        index = self.post_combo.findText(template_name)
        if index >= 0:
            self.post_combo.setCurrentIndex(index)
    
    
    def update_language(self):
        """言語変更時のUI更新"""
        # ラベルを更新
        self.pre_label.setText(tr("label_pre_template"))
        self.post_label.setText(tr("label_post_template"))
        
        # 現在の選択を保存
        pre_selection = self.get_selected_pre_template()
        post_selection = self.get_selected_post_template()
        
        # コンボボックスの "なし" 項目を更新
        none_text = tr("template_none")
        
        # プリプロンプトコンボボックス更新
        if self.pre_combo.count() > 0:
            self.pre_combo.setItemText(0, none_text)
        
        # ポストプロンプトコンボボックス更新
        if self.post_combo.count() > 0:
            self.post_combo.setItemText(0, none_text)
        
        # 選択を復元
        self.set_selected_pre_template(pre_selection)
        self.set_selected_post_template(post_selection)
    
    def refresh_templates(self):
        """テンプレートを再読み込み"""
        # 現在の選択を保存
        pre_selection = self.get_selected_pre_template()
        post_selection = self.get_selected_post_template()
        
        # テンプレートを再読み込み
        self.load_templates()
        
        # 選択を復元（可能であれば）
        self.set_selected_pre_template(pre_selection)
        self.set_selected_post_template(post_selection)




if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # テストウィンドウ
    widget = TemplateSelector()
    widget.show()
    
    sys.exit(app.exec())