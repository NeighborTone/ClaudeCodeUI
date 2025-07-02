# -*- coding: utf-8 -*-
"""
Prompt History Widget - プロンプト履歴表示・選択ウィジェット
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                              QListWidgetItem, QPushButton, QLineEdit, QSplitter,
                              QTextEdit, QLabel, QMessageBox, QGroupBox)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from src.core.prompt_history_manager import get_prompt_history_manager
from src.core.ui_strings import tr


class PromptHistoryWidget(QWidget):
    """プロンプト履歴を表示・選択するウィジェット"""
    
    prompt_selected = Signal(dict)  # プロンプトが選択されたときのシグナル
    
    def __init__(self, parent=None):
        """初期化"""
        super().__init__(parent)
        self.history_manager = get_prompt_history_manager()
        self.current_history = []
        self.setup_ui()
        self.load_history()
        
        # 履歴更新のシグナルを接続
        self.history_manager.history_updated.connect(self.load_history)
    
    def setup_ui(self):
        """UIのセットアップ"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 検索エリア
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(tr("prompt_history_search_placeholder"))
        self.search_input.textChanged.connect(self.on_search_text_changed)
        
        self.clear_all_button = QPushButton(tr("button_clear_all"))
        self.clear_all_button.clicked.connect(self.on_clear_all_clicked)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.clear_all_button)
        layout.addLayout(search_layout)
        
        # スプリッター（左右分割：リストと詳細表示）
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # 左側：履歴リスト
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # 履歴リストのラベル
        list_label = QLabel(tr("label_history_list"))
        list_label.setStyleSheet("font-weight: bold; padding: 5px;")
        left_layout.addWidget(list_label)
        
        self.history_list = QListWidget()
        self.history_list.currentItemChanged.connect(self.on_item_selected)
        self.history_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        left_layout.addWidget(self.history_list)
        
        splitter.addWidget(left_widget)
        
        # 右側：詳細表示エリア
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # プレビューラベル
        preview_label = QLabel(tr("label_prompt_preview"))
        preview_label.setStyleSheet("font-weight: bold; padding: 5px;")
        right_layout.addWidget(preview_label)
        
        # 詳細表示エリア
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setContentsMargins(5, 5, 5, 5)
        
        # メタ情報表示
        meta_group = QGroupBox(tr("label_meta_info"))
        meta_layout = QVBoxLayout(meta_group)
        self.meta_info_label = QLabel()
        self.meta_info_label.setWordWrap(True)
        self.meta_info_label.setStyleSheet("padding: 5px;")
        meta_layout.addWidget(self.meta_info_label)
        details_layout.addWidget(meta_group)
        
        # プロンプト内容表示
        self.prompt_display = QTextEdit()
        self.prompt_display.setReadOnly(True)
        self.prompt_display.setFont(QFont("Consolas", 9))
        details_layout.addWidget(self.prompt_display, 1)  # stretch factor 1
        
        # ボタンエリア
        button_layout = QHBoxLayout()
        self.use_button = QPushButton(tr("button_use_prompt"))
        self.use_button.clicked.connect(self.on_use_clicked)
        self.use_button.setEnabled(False)
        
        self.delete_button = QPushButton(tr("button_delete"))
        self.delete_button.clicked.connect(self.on_delete_clicked)
        self.delete_button.setEnabled(False)
        
        button_layout.addWidget(self.use_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        details_layout.addLayout(button_layout)
        
        right_layout.addWidget(details_widget)
        splitter.addWidget(right_widget)
        
        # 左右の幅を設定（左:右 = 2:3の比率）
        splitter.setSizes([400, 600])
        
        # 検索デバウンスタイマー
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
    
    def load_history(self):
        """履歴を読み込む"""
        self.history_list.clear()
        self.current_history = self.history_manager.get_history()
        
        for entry in self.current_history:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, entry)
            
            # 表示テキストの作成
            timestamp = entry.get('timestamp', '')
            title = entry.get('title', '').replace('\n', ' ')
            display_text = f"[{timestamp}] {title}"
            item.setText(display_text)
            
            self.history_list.addItem(item)
        
        # リストが空の場合の処理
        if self.history_list.count() == 0:
            self.meta_info_label.setText(tr("no_history"))
            self.prompt_display.clear()
            self.use_button.setEnabled(False)
            self.delete_button.setEnabled(False)
    
    def on_search_text_changed(self, text: str):
        """検索テキストが変更されたとき"""
        self.search_timer.stop()
        self.search_timer.start(300)  # 300ms後に検索実行
    
    def perform_search(self):
        """検索を実行"""
        query = self.search_input.text().strip()
        
        if not query:
            self.load_history()
            return
        
        # 検索実行
        results = self.history_manager.search_history(query)
        
        # リストをクリアして結果を表示
        self.history_list.clear()
        for entry in results:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, entry)
            
            timestamp = entry.get('timestamp', '')
            title = entry.get('title', '').replace('\n', ' ')
            display_text = f"[{timestamp}] {title}"
            item.setText(display_text)
            
            self.history_list.addItem(item)
    
    def on_item_selected(self, current: QListWidgetItem, previous: QListWidgetItem):
        """リストアイテムが選択されたとき"""
        if not current:
            self.meta_info_label.clear()
            self.prompt_display.clear()
            self.use_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            return
        
        entry = current.data(Qt.UserRole)
        
        # メタ情報を表示
        timestamp = entry.get('timestamp', '')
        thinking_level = entry.get('thinking_level', '')
        pre_template = entry.get('pre_template', 'None')
        post_template = entry.get('post_template', 'None')
        
        meta_text = f"Time: {timestamp}\n"
        meta_text += f"Thinking Level: {thinking_level}\n"
        meta_text += f"Pre-template: {pre_template}\n"
        meta_text += f"Post-template: {post_template}"
        self.meta_info_label.setText(meta_text)
        
        # プロンプト内容を表示
        prompt = entry.get('prompt', '')
        self.prompt_display.setPlainText(prompt)
        
        # ボタンを有効化
        self.use_button.setEnabled(True)
        self.delete_button.setEnabled(True)
    
    def on_item_double_clicked(self, item: QListWidgetItem):
        """アイテムがダブルクリックされたとき"""
        if item:
            self.on_use_clicked()
    
    def on_use_clicked(self):
        """使用ボタンがクリックされたとき"""
        current = self.history_list.currentItem()
        if current:
            entry = current.data(Qt.UserRole)
            self.prompt_selected.emit(entry)
    
    def on_delete_clicked(self):
        """削除ボタンがクリックされたとき"""
        current = self.history_list.currentItem()
        if not current:
            return
        
        # 確認ダイアログ
        reply = QMessageBox.question(
            self,
            tr("confirm_delete_title"),
            tr("confirm_delete_message"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            entry = current.data(Qt.UserRole)
            prompt_id = entry.get('id')
            if prompt_id:
                self.history_manager.delete_prompt(prompt_id)
    
    def on_clear_all_clicked(self):
        """全削除ボタンがクリックされたとき"""
        # 確認ダイアログ
        reply = QMessageBox.question(
            self,
            tr("confirm_clear_all_title"),
            tr("confirm_clear_all_message"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.history_manager.clear_history()