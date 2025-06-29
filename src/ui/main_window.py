# -*- coding: utf-8 -*-
"""
Main Window - Main application window
"""
import os
from typing import List, Dict
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QSplitter, QStatusBar, QMenuBar, QMenu, QMessageBox,
                              QApplication, QLabel, QDialog, QScrollArea, QTextEdit,
                              QPushButton, QDialogButtonBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QScreen

from src.core.workspace_manager import WorkspaceManager
from src.core.settings import SettingsManager
from src.core.python_helper import PythonHelper
from src.core.path_converter import PathConverter
from src.core.language_manager import get_language_manager, set_language_manager
from src.core.ui_strings import tr
from src.core.prompt_history_manager import get_prompt_history_manager
from src.core.indexing_adapter import create_indexing_system
from src.widgets.file_tree import FileTreeWidget
from src.widgets.prompt_input import PromptInputWidget
from src.widgets.thinking_selector import ThinkingSelectorWidget
from src.widgets.prompt_preview import PromptPreviewWidget
from src.widgets.template_selector import TemplateSelector
from src.widgets.prompt_history import PromptHistoryWidget
from src.core.template_manager import get_template_manager
from src.ui.style_themes import apply_theme, theme_manager, get_main_font


class UsageDialog(QDialog):
    """使い方を表示するスクロール可能なダイアログ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("usage_title"))
        self.setModal(True)
        self.resize(700, 500)
        
        # メインレイアウト
        layout = QVBoxLayout(self)
        
        # スクロールエリア
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # スクロール内容のウィジェット
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        
        # コンテンツレイアウト
        content_layout = QVBoxLayout(content_widget)
        
        # テキストエディット（読み取り専用）
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(get_main_font())
        content_layout.addWidget(self.text_edit)
        
        # ボタンボックス
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
    
    def set_usage_text(self, text: str):
        """使い方テキストを設定"""
        self.text_edit.setPlainText(text.strip())


class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    
    def __init__(self):
        super().__init__()
        
        # 設定とマネージャー
        self.settings_manager = SettingsManager()
        self.workspace_manager = WorkspaceManager()
        
        # インデックス管理システム（新しい統合システム）
        self.indexing_manager, self.fast_searcher = create_indexing_system(self)
        
        
        # 言語マネージャーを初期化
        self.language_manager = get_language_manager(self.settings_manager)
        set_language_manager(self.language_manager)
        
        # 言語変更時のコールバックを登録
        self.language_manager.register_language_change_callback("main_window", self._on_language_changed)
        
        # 設定から思考レベル、テーマ、プレビュー表示、スプリッターサイズ、テンプレート選択を復元
        thinking_level = self.settings_manager.get_thinking_level()
        theme_name = self.settings_manager.get_theme()
        preview_visible = self.settings_manager.get_preview_visible()
        splitter_sizes = self.settings_manager.get_splitter_sizes()
        selected_pre_template = self.settings_manager.get_selected_pre_template()
        selected_post_template = self.settings_manager.get_selected_post_template()
        
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        
        # ウィンドウジオメトリの復元（中心配置との調整）
        self.setup_window_position()
        
        # 保存されたテーマを適用
        apply_theme(self, theme_name)
        
        # 思考レベルを設定
        self.thinking_selector.set_thinking_level(thinking_level)
        self.prompt_input.set_thinking_level(thinking_level)
        
        # プレビュー表示状態を復元
        self.prompt_preview.setVisible(preview_visible)
        self.preview_action.setChecked(preview_visible)
        
        # スプリッターサイズを復元
        self.main_splitter.setSizes(splitter_sizes)
        
        # テンプレート選択を復元
        if selected_pre_template:
            self.template_selector.set_selected_pre_template(selected_pre_template)
        if selected_post_template:
            self.template_selector.set_selected_post_template(selected_post_template)
        
        # スプリッターサイズ変更時のシグナル接続
        self.main_splitter.splitterMoved.connect(self.on_splitter_moved)
        
        # 初期プロンプトプレビューを更新（少し遅延させる）
        QTimer.singleShot(100, self.update_prompt_preview)
        
        # 自動保存タイマー
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_settings)
        self.auto_save_timer.start(30000)  # 30秒ごとに自動保存
        
        # Initialize indexing system
        QTimer.singleShot(500, self.check_indexing_needed)
    
    def setup_ui(self):
        """UIの初期化"""
        self.setWindowTitle("Claude Code PromptUI")
        
        # アプリケーションアイコンを設定
        icon_path = "assets/icons/main/claude-ai-icon.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setMinimumSize(800, 600)
        
        # 初期ウィンドウサイズを設定（位置は後で決定）
        self.resize(1200, 800)
        
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # メインレイアウト
        main_layout = QHBoxLayout(central_widget)
        
        # スプリッター
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)
        
        # 左側：ファイルツリー（WorkspaceManagerを共有）
        self.file_tree = FileTreeWidget(self.workspace_manager)
        self.file_tree.setMinimumWidth(250)
        self.file_tree.setMaximumWidth(400)
        self.main_splitter.addWidget(self.file_tree)
        
        # 中央：プロンプトプレビューエリア
        self.prompt_preview = PromptPreviewWidget()
        self.prompt_preview.setMinimumWidth(300)
        self.main_splitter.addWidget(self.prompt_preview)
        
        # 右側：プロンプト入力エリア
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 思考レベル選択
        self.thinking_selector = ThinkingSelectorWidget()
        right_layout.addWidget(self.thinking_selector)
        
        # テンプレート選択
        self.template_selector = TemplateSelector()
        right_layout.addWidget(self.template_selector)
        
        # プロンプト入力
        self.prompt_input = PromptInputWidget(self.workspace_manager, self.fast_searcher)
        right_layout.addWidget(self.prompt_input)
        
        self.main_splitter.addWidget(right_widget)
        
        # スプリッターの初期比率を設定
        self.main_splitter.setStretchFactor(0, 0)  # ファイルツリーは固定
        self.main_splitter.setStretchFactor(1, 1)  # プレビューエリアは伸縮
        self.main_splitter.setStretchFactor(2, 1)  # プロンプト入力エリアは伸縮
        
        # イベント接続
        self.setup_connections()
    
    def setup_connections(self):
        """イベント接続"""
        # 思考レベル変更
        self.thinking_selector.thinking_level_changed.connect(self.on_thinking_level_changed)
        
        # テンプレート変更
        self.template_selector.template_changed.connect(self.on_template_changed)
        
        # プロンプト生成
        self.prompt_input.generate_and_copy.connect(self.on_prompt_generated)
        
        # プロンプトテキスト変更（リアルタイム更新用）
        self.prompt_input.text_changed.connect(self.update_prompt_preview)
        
        # プレビュー内容変更（トークンカウント更新用）
        self.prompt_preview.prompt_content_changed.connect(self.on_preview_content_changed)
        
        # ファイル選択
        self.file_tree.file_selected.connect(self.on_file_selected)
        self.file_tree.file_double_clicked.connect(self.on_file_double_clicked)
        
        # ワークスペース変更
        self.file_tree.workspace_changed.connect(self.on_workspace_changed)
        
        # インデックス管理イベント
        self.indexing_manager.indexing_started.connect(self.on_indexing_started)
        self.indexing_manager.indexing_progress.connect(self.on_indexing_progress)
        self.indexing_manager.indexing_completed.connect(self.on_indexing_completed)
        self.indexing_manager.indexing_failed.connect(self.on_indexing_failed)
    
    def setup_menu(self):
        """メニューバーの設定"""
        menubar = self.menuBar()
        
        # ファイルメニュー
        file_menu = menubar.addMenu(tr("menu_file"))
        
        # ワークスペース追加
        add_workspace_action = QAction(tr("menu_add_workspace"), self)
        add_workspace_action.setShortcut("Ctrl+O")
        add_workspace_action.triggered.connect(self.file_tree.add_workspace)
        file_menu.addAction(add_workspace_action)
        
        # 更新
        refresh_action = QAction(tr("button_refresh"), self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.file_tree.rebuild_index)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        # 終了
        exit_action = QAction(tr("menu_exit"), self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 編集メニュー
        edit_menu = menubar.addMenu(tr("menu_edit"))
        
        # クリア
        clear_action = QAction(tr("button_clear"), self)
        clear_action.setShortcut("Ctrl+Shift+C")
        clear_action.triggered.connect(self.prompt_input.clear_all)
        edit_menu.addAction(clear_action)
        
        # 生成&コピー
        generate_action = QAction(tr("button_generate"), self)
        generate_action.setShortcut("Shift+Return")
        generate_action.triggered.connect(self.prompt_input.generate_prompt)
        edit_menu.addAction(generate_action)
        
        edit_menu.addSeparator()
        
        # プロンプト履歴
        prompt_history_action = QAction(tr("menu_prompt_history"), self)
        prompt_history_action.setShortcut("Ctrl+H")
        prompt_history_action.triggered.connect(self.show_prompt_history)
        edit_menu.addAction(prompt_history_action)
        
        
        # 表示メニュー
        view_menu = menubar.addMenu(tr("menu_view"))
        
        # プレビュー表示切り替え
        self.preview_action = QAction(tr("menu_toggle_preview"), self)
        self.preview_action.setCheckable(True)
        self.preview_action.setChecked(True)
        self.preview_action.triggered.connect(self.toggle_preview)
        view_menu.addAction(self.preview_action)
        
        view_menu.addSeparator()
        
        # テーマメニュー
        theme_menu = view_menu.addMenu(tr("menu_theme"))
        theme_names = theme_manager.get_theme_names()
        theme_display_names = theme_manager.get_theme_display_names()
        
        for theme_name in theme_names:
            display_name = theme_display_names.get(theme_name, theme_name)
            theme_action = QAction(display_name, self)
            theme_action.triggered.connect(lambda _checked=False, t=theme_name: self.change_theme(t))
            theme_menu.addAction(theme_action)
        
        # 設定メニュー
        settings_menu = menubar.addMenu(tr("menu_settings"))
        
        # 言語メニュー
        language_menu = settings_menu.addMenu(tr("menu_language"))
        
        # 日本語
        japanese_action = QAction(tr("menu_language_japanese"), self)
        japanese_action.triggered.connect(lambda: self.language_manager.set_language("ja"))
        language_menu.addAction(japanese_action)
        
        # 英語
        english_action = QAction(tr("menu_language_english"), self)
        english_action.triggered.connect(lambda: self.language_manager.set_language("en"))
        language_menu.addAction(english_action)
        
        # インデックスメニュー
        index_menu = menubar.addMenu("インデックス")
        
        rebuild_index_action = QAction("インデックスを再構築", self)
        rebuild_index_action.triggered.connect(self.rebuild_index)
        index_menu.addAction(rebuild_index_action)
        
        reload_index_action = QAction("インデックスを再読み込み", self)
        reload_index_action.triggered.connect(self.reload_index)
        index_menu.addAction(reload_index_action)
        
        index_menu.addSeparator()
        
        # 起動最適化メニュー
        startup_stats_action = QAction("🚀 起動統計", self)
        startup_stats_action.triggered.connect(self.show_startup_stats)
        index_menu.addAction(startup_stats_action)
        
        force_optimize_action = QAction("⚡ 起動最適化を実行", self)
        force_optimize_action.triggered.connect(self.force_startup_optimization)
        index_menu.addAction(force_optimize_action)
        
        index_menu.addSeparator()
        
        index_stats_action = QAction("インデックス統計", self)
        index_stats_action.triggered.connect(self.show_index_stats)
        index_menu.addAction(index_stats_action)
        
        # ヘルプメニュー
        help_menu = menubar.addMenu(tr("menu_help"))
        
        # 使い方
        usage_action = QAction(tr("menu_usage"), self)
        usage_action.triggered.connect(self.show_usage)
        help_menu.addAction(usage_action)
        
        # Python実行環境
        python_env_action = QAction(tr("menu_python_env"), self)
        python_env_action.triggered.connect(self.show_python_environment)
        help_menu.addAction(python_env_action)
        
        help_menu.addSeparator()
        
        # バージョン情報
        about_action = QAction(tr("menu_about"), self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """ステータスバーの設定"""
        self.statusBar().showMessage(tr("status_ready"))
        
        # 既存のpermanentウィジェットをクリア
        self.statusBar().clearMessage()
        for widget in self.statusBar().findChildren(QLabel):
            self.statusBar().removeWidget(widget)
            widget.deleteLater()
        
        # プログレス表示（通常は非表示）
        self.progress_label = QLabel()
        self.statusBar().addWidget(self.progress_label)
        self.progress_label.hide()
        
        # インデックス状態表示
        self.index_status_label = QLabel("インデックス: 未構築")
        self.statusBar().addPermanentWidget(self.index_status_label)
        
        # 思考レベル表示
        self.thinking_level_label = QLabel(f"{tr('label_thinking_level')} think")
        self.statusBar().addPermanentWidget(self.thinking_level_label)
        
        # インデックス統計を更新
        self.update_index_status()
    
    def setup_window_position(self):
        """ウィンドウ位置とサイズを設定（初回起動時は中心配置、以降は保存された位置を復元）"""
        settings_file_exists = os.path.exists(self.settings_manager.config_file)
        
        if settings_file_exists:
            # 設定ファイルが存在する場合
            geometry = self.settings_manager.get_window_geometry()
            
            # 保存された位置がデフォルト位置(100, 100)かどうかを判定
            # デフォルト位置の場合は初回起動とみなして中心配置
            is_default_position = (geometry['x'] == 100 and geometry['y'] == 100)
            
            if not is_default_position:
                # カスタム位置が保存されている場合は復元
                self.setGeometry(geometry['x'], geometry['y'], geometry['width'], geometry['height'])
            else:
                # デフォルト位置の場合は中心配置を適用
                self.resize(geometry['width'], geometry['height'])
                self.center_on_primary_screen()
        else:
            # 設定ファイルが存在しない場合（真の初回起動）
            self.center_on_primary_screen()
    
    def load_window_geometry(self):
        """レガシーメソッド - setup_window_position()に移行済み"""
        pass
    
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
        self.thinking_level_label.setText(f"{tr('label_thinking_level')} {level}")
        self.statusBar().showMessage(tr("status_thinking_level_changed", level=level), 2000)
        
        # プロンプトプレビューを更新
        self.update_prompt_preview()
    
    
    def on_prompt_generated(self, main_content: str, thinking_level: str):
        """プロンプトが生成されたとき"""
        # テンプレートセレクターから選択された内容を取得
        pre_template = self.template_selector.get_selected_pre_template()
        post_template = self.template_selector.get_selected_post_template()
        
        # テンプレートマネージャーで最終プロンプトを構築
        template_manager = get_template_manager()
        final_prompt = template_manager.build_final_prompt(
            thinking_level, pre_template, main_content, post_template
        )
        
        # クリップボードにコピー
        clipboard = QApplication.clipboard()
        clipboard.setText(final_prompt)
        
        # プロンプト履歴に保存
        history_manager = get_prompt_history_manager()
        history_manager.add_prompt(
            prompt=final_prompt,
            thinking_level=thinking_level,
            pre_template=pre_template,
            post_template=post_template
        )
        
        # ステータス表示
        lines = len(final_prompt.split('\n'))
        chars = len(final_prompt)
        self.statusBar().showMessage(tr("status_prompt_copied", lines=lines, chars=chars), 3000)
    
    def on_file_selected(self, file_path: str):
        """ファイルが選択されたとき"""
        self.statusBar().showMessage(tr("status_file_selected", filename=os.path.basename(file_path)), 2000)
    
    def on_file_double_clicked(self, file_path: str):
        """ファイルがダブルクリックされたとき"""
        # ワークスペース相対パスを取得
        workspace_relative_path = None
        for workspace in self.workspace_manager.get_workspaces():
            workspace_path = workspace['path']
            if file_path.startswith(workspace_path):
                workspace_relative_path = os.path.relpath(file_path, workspace_path)
                break
        
        if workspace_relative_path is None:
            workspace_relative_path = os.path.basename(file_path)
        
        # パスを正規化（「/」区切りに統一）
        workspace_relative_path = PathConverter.normalize_path(workspace_relative_path)
        
        # ファイル内容をプロンプトに挿入
        current_text = self.prompt_input.get_prompt_text()
        if current_text:
            new_text = f"{current_text}\n\n@{workspace_relative_path}"
        else:
            new_text = f"@{workspace_relative_path}"
        
        # オートコンプリートを一時的に無効化してテキストを設定
        self.prompt_input.set_text_without_completion(new_text)
        self.statusBar().showMessage(tr("status_file_added", filename=workspace_relative_path), 2000)
    
    def on_template_changed(self):
        """テンプレート選択変更時"""
        # 選択されたテンプレートを設定に保存
        pre_template = self.template_selector.get_selected_pre_template()
        post_template = self.template_selector.get_selected_post_template()
        self.settings_manager.set_selected_pre_template(pre_template)
        self.settings_manager.set_selected_post_template(post_template)
        
        # プロンプトプレビューを更新
        self.update_prompt_preview()
    
    
    def update_prompt_preview(self, text: str = None):
        """プロンプトプレビューを更新"""
        # 現在の値を取得
        thinking_level = self.thinking_selector.get_current_thinking_level()
        pre_template = self.template_selector.get_selected_pre_template()
        post_template = self.template_selector.get_selected_post_template()
        
        # テキストが指定されていない場合は現在の内容を取得
        if text is None:
            text = self.prompt_input.get_prompt_text()
        
        # プレビューを更新
        self.prompt_preview.update_preview(
            thinking_level=thinking_level,
            pre_template=pre_template,
            main_content=text,
            post_template=post_template
        )
    
    def on_preview_content_changed(self, full_prompt_text: str):
        """プレビュー内容変更時（トークンカウント更新）"""
        # プレビューの内容を基準にトークンカウントを更新
        self.prompt_input.update_token_count(full_prompt_text)
    
    def _on_language_changed(self, language):
        """言語変更時のコールバック"""
        # メニューを再構築
        self.menuBar().clear()
        self.setup_menu()
        
        # メニュー再構築後にテーマスタイルを再適用
        apply_theme(self)
        
        # ステータスバーを更新
        self.setup_status_bar()
        
        # 子ウィジェットの言語を更新
        self.file_tree.update_language()
        self.prompt_input.update_language()
        self.thinking_selector.update_language()
        self.template_selector.update_language()
        self.prompt_preview.update_language()
        
        # 状態メッセージを更新
        self.statusBar().showMessage(tr("status_language_changed", language=language), 3000)
    
    def show_usage(self):
        """使い方を表示"""
        usage_text = tr("usage_content")
        
        dialog = UsageDialog(self)
        dialog.set_usage_text(usage_text)
        dialog.exec()
    
    def show_about(self):
        """バージョン情報を表示"""
        about_text = tr("about_content")
        
        QMessageBox.about(self, tr("about_title"), about_text)
    
    def show_python_environment(self):
        """Python実行環境の情報を表示"""
        env_info = PythonHelper.get_execution_instructions()
        
        dialog = UsageDialog(self)
        dialog.setWindowTitle(tr("python_env_title"))
        dialog.set_usage_text(env_info)
        dialog.exec()
    
    def show_prompt_history(self):
        """プロンプト履歴ダイアログを表示"""
        # ダイアログの作成
        dialog = QDialog(self)
        dialog.setWindowTitle(tr("prompt_history_title"))
        dialog.setModal(True)
        
        # メインウィンドウのサイズを取得して、やや小さめに設定
        main_width = self.width()
        main_height = self.height()
        dialog_width = int(main_width * 0.85)  # メインウィンドウの85%
        dialog_height = int(main_height * 0.95)  # メインウィンドウの95%（縦長に）
        dialog.resize(dialog_width, dialog_height)
        
        # ダイアログを画面中央に配置
        screen = self.screen()
        if screen:
            screen_rect = screen.availableGeometry()
            x = (screen_rect.width() - dialog_width) // 2
            y = (screen_rect.height() - dialog_height) // 2
            dialog.move(x, y)
        
        # レイアウト
        layout = QVBoxLayout(dialog)
        
        # プロンプト履歴ウィジェット
        history_widget = PromptHistoryWidget(dialog)
        layout.addWidget(history_widget)
        
        # プロンプトが選択されたときの処理
        def on_prompt_selected(entry):
            # 選択されたプロンプトの内容を抽出
            prompt = entry.get('prompt', '')
            thinking_level = entry.get('thinking_level', '')
            pre_template = entry.get('pre_template', '')
            post_template = entry.get('post_template', '')
            
            # メインのプロンプトテキストを抽出（thinking levelとテンプレートを除く）
            main_content = prompt
            
            # thinking levelを削除
            if thinking_level and main_content.startswith(thinking_level):
                main_content = main_content[len(thinking_level):].strip()
            
            # pre templateを削除
            if pre_template and pre_template != 'None':
                template_manager = get_template_manager()
                pre_content = template_manager.get_pre_template_content(pre_template)
                if pre_content and main_content.startswith(pre_content):
                    main_content = main_content[len(pre_content):].strip()
            
            # post templateを削除
            if post_template and post_template != 'None':
                template_manager = get_template_manager()
                post_content = template_manager.get_post_template_content(post_template)
                if post_content and main_content.endswith(post_content):
                    main_content = main_content[:-len(post_content)].strip()
            
            # UI要素に設定
            self.prompt_input.set_text_without_completion(main_content)
            self.thinking_selector.set_thinking_level(thinking_level)
            self.template_selector.set_selected_pre_template(pre_template if pre_template != 'None' else '')
            self.template_selector.set_selected_post_template(post_template if post_template != 'None' else '')
            
            # ダイアログを閉じる
            dialog.accept()
        
        history_widget.prompt_selected.connect(on_prompt_selected)
        
        # ダイアログを表示
        dialog.exec()
    
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
            self.statusBar().showMessage(tr("status_theme_changed", theme=display_name), 3000)
    
    def toggle_preview(self):
        """プレビュー表示を切り替え"""
        is_visible = self.preview_action.isChecked()
        self.prompt_preview.setVisible(is_visible)
        
        # 設定を保存
        self.settings_manager.set_preview_visible(is_visible)
        
        if is_visible:
            self.statusBar().showMessage(tr("status_preview_shown"), 2000)
        else:
            self.statusBar().showMessage(tr("status_preview_hidden"), 2000)
    
    def on_splitter_moved(self, _pos: int, _index: int):
        """スプリッターが移動されたとき"""
        sizes = self.main_splitter.sizes()
        self.settings_manager.set_splitter_sizes(sizes)
    
    def center_on_primary_screen(self):
        """ウィンドウをプライマリーモニターの中心に配置"""
        # プライマリーモニターを取得
        app = QApplication.instance()
        if app is None:
            return
        
        primary_screen = app.primaryScreen()
        if primary_screen is None:
            return
        
        # プライマリーモニターの幾何学情報を取得
        screen_geometry = primary_screen.availableGeometry()
        
        # ウィンドウサイズを取得（未設定の場合はデフォルトサイズ使用）
        window_size = self.size()
        if window_size.width() < 800 or window_size.height() < 600:
            # 初回起動時のデフォルトサイズ
            window_size.setWidth(1200)
            window_size.setHeight(800)
            self.resize(window_size)
        
        # 中心座標を計算
        x = screen_geometry.x() + (screen_geometry.width() - window_size.width()) // 2
        y = screen_geometry.y() + (screen_geometry.height() - window_size.height()) // 2
        
        # ウィンドウを移動
        self.move(x, y)
    
    def closeEvent(self, event: QCloseEvent):
        """ウィンドウが閉じられるとき"""
        # 設定を保存
        self.save_window_geometry()
        self.settings_manager.save_settings()
        
        # 自動保存タイマーを停止
        self.auto_save_timer.stop()
        
        event.accept()
    
    # インデックス管理メソッド
    def update_index_status(self):
        """インデックス状態を更新"""
        try:
            stats = self.indexing_manager.get_stats()
            total_entries = stats.get('total_entries', 0)
            files = stats.get('files', 0)
            folders = stats.get('folders', 0)
            
            if total_entries > 0:
                self.index_status_label.setText(f"インデックス: {files}ファイル, {folders}フォルダ")
            else:
                self.index_status_label.setText("インデックス: 未構築")
        except Exception as e:
            self.index_status_label.setText("インデックス: エラー")
            from src.core.logger import logger
            logger.error(f"インデックス状態更新エラー: {e}")
    
    def rebuild_index(self):
        """インデックスを再構築"""
        if self.indexing_manager.is_indexing():
            QMessageBox.information(self, "情報", "インデックス構築中です。しばらくお待ちください。")
            return
        
        workspaces = self.workspace_manager.get_workspaces()
        if not workspaces:
            QMessageBox.information(self, "情報", "ワークスペースが登録されていません。")
            return
        
        reply = QMessageBox.question(
            self, "確認", 
            "インデックスを再構築しますか？\n大きなプロジェクトでは時間がかかる場合があります。",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.indexing_manager.start_indexing(workspaces, rebuild_all=True)
    
    def reload_index(self):
        """インデックスを再読み込み"""
        if self.indexing_manager.is_indexing():
            QMessageBox.information(self, "情報", "インデックス構築中です。しばらくお待ちください。")
            return
        
        # 新しい統合システムでは再読み込みは自動的に処理される
        self.update_index_status()
        
        # ファイル検索システムのキャッシュをクリア
        if hasattr(self.fast_searcher, 'clear_cache'):
            self.fast_searcher.clear_cache()
        
        QMessageBox.information(self, "成功", "インデックスを再読み込みしました。")
    
    def show_index_stats(self):
        """インデックス統計を表示"""
        try:
            stats = self.indexing_manager.get_stats()
            
            import time
            last_updated = stats.get('last_updated', 0)
            if last_updated > 0:
                last_updated_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_updated))
            else:
                last_updated_str = "未構築"
            
            message = f"""インデックス統計情報:

総エントリ数: {stats.get('total_entries', 0)}
ファイル数: {stats.get('files', 0)}
フォルダ数: {stats.get('folders', 0)}
ワークスペース数: {stats.get('workspaces', 0)}
拡張子数: {stats.get('extensions', 0)}
最終更新: {last_updated_str}"""
            
            QMessageBox.information(self, "インデックス統計", message)
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"統計情報の取得に失敗しました: {e}")
    
    def show_startup_stats(self):
        """起動統計を表示"""
        try:
            stats = self.indexing_manager.get_stats() if hasattr(self.indexing_manager, 'get_stats') else {}
            
            message = f"""システム統計:

インデックス情報:
- 総エントリ数: {stats.get('total_entries', 0)}
- ファイル数: {stats.get('files', 0)}
- フォルダ数: {stats.get('folders', 0)}
- ワークスペース数: {stats.get('workspaces', 0)}
- 拡張子の種類: {stats.get('extensions', 0)}

状態:
- インデックス構築中: {'はい' if self.indexing_manager.is_indexing() else 'いいえ'}"""
            
            QMessageBox.information(self, "システム統計", message)
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"統計情報の取得に失敗しました: {e}")
    
    def force_startup_optimization(self):
        """インデックスを強制的に再構築"""
        from src.core.logger import logger
        
        try:
            workspaces = self.workspace_manager.get_workspaces()
            if not workspaces:
                QMessageBox.information(self, "情報", "ワークスペースが登録されていません。")
                return
            
            reply = QMessageBox.question(
                self, "確認", 
                "インデックスの再構築を実行しますか？\n\n"
                "この処理では以下が実行されます:\n"
                "• 既存インデックスのクリア\n"
                "• 全ワークスペースの再インデックス\n"
                "• ファイル検索の最適化",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                logger.info("Manual index rebuild started")
                
                # インデックス再構築を実行
                self.indexing_manager.start_indexing(workspaces, rebuild_all=True)
                
                QMessageBox.information(
                    self, "完了", 
                    "インデックスの再構築を開始しました。\n\n"
                    "構築完了まで数分かかる場合があります。"
                )
                
        except Exception as e:
            logger.error(f"Manual index rebuild failed: {e}")
            QMessageBox.critical(self, "エラー", f"インデックス再構築の実行に失敗しました: {e}")
    
    def on_workspace_changed(self):
        """ワークスペース変更時に自動的にインデックスを再構築"""
        # ワークスペースを取得
        workspaces = self.workspace_manager.get_workspaces()
        if not workspaces:
            self.update_index_status()
            return
        
        # ステータスメッセージを表示
        self.statusBar().showMessage("ワークスペースが変更されました。インデックスを再構築しています...", 3000)
        
        # インデックスを再構築
        self.indexing_manager.start_indexing(workspaces, rebuild_all=True)
    
    def start_smart_indexing(self, workspaces: List[Dict[str, str]]):
        """必要な場合のみインデックス構築を開始"""
        if not self.indexing_manager.check_indexing_needed(workspaces):
            # インデックス不要の場合、既存インデックスの状態を更新
            self.update_index_status()
            return
        
        # インデックス構築が必要な場合のみ実行
        self.indexing_manager.start_smart_indexing(workspaces)
    
    def check_indexing_needed(self):
        """インデックスの必要性をチェックし、必要に応じて構築を実行"""
        from src.core.logger import logger
        
        try:
            workspaces = self.workspace_manager.get_workspaces()
            
            if not workspaces:
                logger.info("No workspaces configured")
                return
            
            # Check if indexing is needed
            if hasattr(self.indexing_manager, 'check_indexing_needed'):
                if self.indexing_manager.check_indexing_needed(workspaces):
                    logger.info(f"Starting background indexing for {len(workspaces)} workspace(s)")
                    self.indexing_manager.start_smart_indexing(workspaces)
                else:
                    logger.info("Index is up to date")
            
            # Update index status
            self.update_index_status()
            
        except Exception as e:
            logger.error(f"Error checking indexing requirements: {e}")
            # Fallback to basic indexing
            self.initialize_index_on_startup_fallback()
    
    def initialize_index_on_startup_fallback(self):
        """起動時のインデックス初期化（フォールバック）"""
        workspaces = self.workspace_manager.get_workspaces()
        if not workspaces:
            self.update_index_status()
            return
        
        if not self.indexing_manager.check_indexing_needed(workspaces):
            self.update_index_status()
            from src.core.logger import logger
            logger.info("起動時: 既存インデックスが有効なため、再構築をスキップしました")
            return
        
        self.update_index_status()
        from src.core.logger import logger
        logger.info("起動時: インデックス構築が必要です（手動で「更新」ボタンを押してインデックスを再構築してください）")
    
    # インデックス管理イベントハンドラー
    def on_indexing_started(self):
        """インデックス構築開始時"""
        self.progress_label.setText("インデックス構築中...")
        self.progress_label.show()
        self.index_status_label.setText("インデックス: 構築中...")
    
    def on_indexing_progress(self, progress: float, message: str):
        """インデックス構築進捗更新時"""
        self.progress_label.setText(f"{message} ({progress:.1f}%)")
    
    def on_indexing_completed(self, stats: dict):
        """インデックス構築完了時"""
        self.progress_label.hide()
        self.update_index_status()
        
        # ファイル検索システムのキャッシュをクリアして更新
        if hasattr(self.fast_searcher, 'clear_cache'):
            self.fast_searcher.clear_cache()
        
        # プロンプト入力ウィジェットに通知
        self.prompt_input.update_file_searcher(self.fast_searcher)
        
        files = stats.get('total_files_indexed', stats.get('files', 0))
        folders = stats.get('total_folders_indexed', stats.get('folders', 0))
        self.statusBar().showMessage(f"インデックス構築完了: {files}ファイル, {folders}フォルダ", 3000)
    
    def on_indexing_failed(self, error_message: str):
        """インデックス構築失敗時"""
        self.progress_label.hide()
        self.index_status_label.setText("インデックス: エラー")
        QMessageBox.critical(self, "エラー", f"インデックス構築に失敗しました:\n{error_message}")