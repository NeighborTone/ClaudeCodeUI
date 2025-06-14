# -*- coding: utf-8 -*-
"""
Main Window - Main application window
"""
import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QSplitter, QStatusBar, QMenuBar, QMenu, QMessageBox,
                              QApplication, QLabel)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QCloseEvent

from core.workspace_manager import WorkspaceManager
from core.settings import SettingsManager
from widgets.file_tree import FileTreeWidget
from widgets.prompt_input import PromptInputWidget
from widgets.thinking_selector import ThinkingSelectorWidget
from ui.style_themes import apply_theme, theme_manager


class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    
    def __init__(self):
        super().__init__()
        
        # 設定とマネージャー
        self.settings_manager = SettingsManager()
        self.workspace_manager = WorkspaceManager()
        
        # 設定から思考レベルとテーマを復元
        thinking_level = self.settings_manager.get_thinking_level()
        theme_name = self.settings_manager.get_theme()
        
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        self.load_window_geometry()
        
        # 保存されたテーマを適用
        apply_theme(self, theme_name)
        
        # 思考レベルを設定
        self.thinking_selector.set_thinking_level(thinking_level)
        self.prompt_input.set_thinking_level(thinking_level)
        
        # 自動保存タイマー
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_settings)
        self.auto_save_timer.start(30000)  # 30秒ごとに自動保存
    
    def setup_ui(self):
        """UIの初期化"""
        self.setWindowTitle("Claude Code PromptUI")
        self.setMinimumSize(800, 600)
        
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # メインレイアウト
        main_layout = QHBoxLayout(central_widget)
        
        # スプリッター
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # 左側：ファイルツリー（WorkspaceManagerを共有）
        self.file_tree = FileTreeWidget(self.workspace_manager)
        self.file_tree.setMinimumWidth(250)
        self.file_tree.setMaximumWidth(400)
        main_splitter.addWidget(self.file_tree)
        
        # 右側：プロンプト入力エリア
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 思考レベル選択
        self.thinking_selector = ThinkingSelectorWidget()
        right_layout.addWidget(self.thinking_selector)
        
        # プロンプト入力
        self.prompt_input = PromptInputWidget(self.workspace_manager)
        right_layout.addWidget(self.prompt_input)
        
        main_splitter.addWidget(right_widget)
        
        # スプリッターの初期比率を設定
        main_splitter.setStretchFactor(0, 0)  # ファイルツリーは固定
        main_splitter.setStretchFactor(1, 1)  # プロンプト入力エリアは伸縮
        
        # イベント接続
        self.setup_connections()
    
    def setup_connections(self):
        """イベント接続"""
        # 思考レベル変更
        self.thinking_selector.thinking_level_changed.connect(self.on_thinking_level_changed)
        
        # プロンプト生成
        self.prompt_input.generate_and_copy.connect(self.on_prompt_generated)
        
        # ファイル選択
        self.file_tree.file_selected.connect(self.on_file_selected)
        self.file_tree.file_double_clicked.connect(self.on_file_double_clicked)
    
    def setup_menu(self):
        """メニューバーの設定"""
        menubar = self.menuBar()
        
        # ファイルメニュー
        file_menu = menubar.addMenu("ファイル(&F)")
        
        # ワークスペース追加
        add_workspace_action = QAction("ワークスペース追加(&A)", self)
        add_workspace_action.setShortcut("Ctrl+O")
        add_workspace_action.triggered.connect(self.file_tree.add_workspace)
        file_menu.addAction(add_workspace_action)
        
        # 更新
        refresh_action = QAction("更新(&R)", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.file_tree.refresh_tree)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        # 終了
        exit_action = QAction("終了(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 編集メニュー
        edit_menu = menubar.addMenu("編集(&E)")
        
        # クリア
        clear_action = QAction("クリア(&C)", self)
        clear_action.setShortcut("Ctrl+Shift+C")
        clear_action.triggered.connect(self.prompt_input.clear_all)
        edit_menu.addAction(clear_action)
        
        # 生成&コピー
        generate_action = QAction("生成&コピー(&G)", self)
        generate_action.setShortcut("Shift+Return")
        generate_action.triggered.connect(self.prompt_input.generate_prompt)
        edit_menu.addAction(generate_action)
        
        # 表示メニュー
        view_menu = menubar.addMenu("表示(&V)")
        
        # テーマメニュー
        theme_menu = view_menu.addMenu("テーマ(&T)")
        theme_names = theme_manager.get_theme_names()
        theme_display_names = theme_manager.get_theme_display_names()
        
        for theme_name in theme_names:
            display_name = theme_display_names.get(theme_name, theme_name)
            theme_action = QAction(display_name, self)
            theme_action.triggered.connect(lambda checked, t=theme_name: self.change_theme(t))
            theme_menu.addAction(theme_action)
        
        # ヘルプメニュー
        help_menu = menubar.addMenu("ヘルプ(&H)")
        
        # 使い方
        usage_action = QAction("使い方(&U)", self)
        usage_action.triggered.connect(self.show_usage)
        help_menu.addAction(usage_action)
        
        # バージョン情報
        about_action = QAction("バージョン情報(&A)", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """ステータスバーの設定"""
        self.statusBar().showMessage("準備完了")
        
        # 思考レベル表示
        self.thinking_level_label = QLabel("思考レベル: think")
        self.statusBar().addPermanentWidget(self.thinking_level_label)
    
    def load_window_geometry(self):
        """ウィンドウジオメトリを読み込み"""
        geometry = self.settings_manager.get_window_geometry()
        self.setGeometry(geometry['x'], geometry['y'], geometry['width'], geometry['height'])
    
    def save_window_geometry(self):
        """ウィンドウジオメトリを保存"""
        geometry = self.geometry()
        self.settings_manager.set_window_geometry(
            geometry.x(), geometry.y(), geometry.width(), geometry.height()
        )
    
    def auto_save_settings(self):
        """設定の自動保存"""
        self.save_window_geometry()
        self.settings_manager.save_settings()
    
    def on_thinking_level_changed(self, level: str):
        """思考レベルが変更されたとき"""
        self.prompt_input.set_thinking_level(level)
        self.settings_manager.set_thinking_level(level)
        self.thinking_level_label.setText(f"思考レベル: {level}")
        self.statusBar().showMessage(f"思考レベルを '{level}' に変更しました", 2000)
    
    def on_prompt_generated(self, prompt: str, thinking_level: str):
        """プロンプトが生成されたとき"""
        lines = len(prompt.split('\n'))
        chars = len(prompt)
        self.statusBar().showMessage(f"プロンプトをクリップボードにコピーしました ({lines}行, {chars}文字)", 3000)
    
    def on_file_selected(self, file_path: str):
        """ファイルが選択されたとき"""
        self.statusBar().showMessage(f"選択: {os.path.basename(file_path)}", 2000)
    
    def on_file_double_clicked(self, file_path: str):
        """ファイルがダブルクリックされたとき"""
        filename = os.path.basename(file_path)
        # ファイル内容をプロンプトに挿入
        current_text = self.prompt_input.get_prompt_text()
        if current_text:
            new_text = f"{current_text}\n\n@{filename}"
        else:
            new_text = f"@{filename}"
        
        self.prompt_input.set_prompt_text(new_text)
        self.statusBar().showMessage(f"ファイルをプロンプトに追加: {filename}", 2000)
    
    def show_usage(self):
        """使い方を表示"""
        usage_text = """
Claude Code PromptUI 使い方

■ 基本操作
- Enterで改行
- Shift+Enterで生成&コピー
- @filename でファイルを指定
- 左側のファイルツリーからファイルを選択

■ ファイル指定
- @を入力すると補完候補が表示されます
- 矢印キーで選択、Enterで確定
- Escapeで補完をキャンセル

■ 思考レベル
- 右上のドロップダウンで思考レベルを選択
- 設定は自動保存されます

■ ワークスペース
- 左上の「フォルダ追加」でプロジェクトフォルダを追加
- 右クリックでワークスペースを削除
- 設定は自動保存されます

■ ショートカット
- Ctrl+O: ワークスペース追加
- F5: 更新
- Ctrl+Shift+C: クリア
- Shift+Enter: 生成&コピー
- Ctrl+Q: 終了
        """
        
        QMessageBox.information(self, "使い方", usage_text.strip())
    
    def show_about(self):
        """バージョン情報を表示"""
        about_text = """
Claude Code PromptUI
Version 1.0.0

Claude Codeのプロンプト入力を改善するためのツールです。

開発者: StudioEmbroidery
        """
        
        QMessageBox.about(self, "バージョン情報", about_text.strip())
    
    def change_theme(self, theme_name: str):
        """テーマを変更"""
        # テーママネージャーにテーマを設定
        if theme_manager.set_theme(theme_name):
            # 設定を保存
            self.settings_manager.set_theme(theme_name)
            
            # UIに新しいテーマを適用
            apply_theme(self)
            
            # ステータスバーにメッセージ表示
            theme_display_names = theme_manager.get_theme_display_names()
            display_name = theme_display_names.get(theme_name, theme_name)
            self.statusBar().showMessage(f"テーマを '{display_name}' に変更しました", 3000)
    
    def closeEvent(self, event: QCloseEvent):
        """ウィンドウが閉じられるとき"""
        # 設定を保存
        self.save_window_geometry()
        self.settings_manager.save_settings()
        
        # 自動保存タイマーを停止
        self.auto_save_timer.stop()
        
        event.accept()