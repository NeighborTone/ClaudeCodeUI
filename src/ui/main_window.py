# -*- coding: utf-8 -*-
"""
Main Window - Main application window
"""
import os
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
from src.widgets.file_tree import FileTreeWidget
from src.widgets.prompt_input import PromptInputWidget
from src.widgets.thinking_selector import ThinkingSelectorWidget
from src.widgets.path_mode_selector import PathModeSelectorWidget
from src.widgets.prompt_preview import PromptPreviewWidget
from src.widgets.template_selector import TemplateSelector
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
        
        # 言語マネージャーを初期化
        self.language_manager = get_language_manager(self.settings_manager)
        set_language_manager(self.language_manager)
        
        # 言語変更時のコールバックを登録
        self.language_manager.register_language_change_callback("main_window", self._on_language_changed)
        
        # 設定から思考レベル、パスモード、テーマ、プレビュー表示、スプリッターサイズ、テンプレート選択を復元
        thinking_level = self.settings_manager.get_thinking_level()
        path_mode = self.settings_manager.get_path_mode()
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
        
        # パスモードを設定
        if path_mode:
            self.path_mode_selector.set_path_mode(path_mode)
            self.prompt_input.set_path_mode(path_mode)
        
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
        
        # 思考レベル選択とパスモード選択を横並びに配置
        selector_layout = QHBoxLayout()
        
        # 思考レベル選択
        self.thinking_selector = ThinkingSelectorWidget()
        selector_layout.addWidget(self.thinking_selector)
        
        # パスモード選択
        self.path_mode_selector = PathModeSelectorWidget()
        selector_layout.addWidget(self.path_mode_selector)
        
        right_layout.addLayout(selector_layout)
        
        # テンプレート選択
        self.template_selector = TemplateSelector()
        right_layout.addWidget(self.template_selector)
        
        # プロンプト入力
        self.prompt_input = PromptInputWidget(self.workspace_manager)
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
        
        # パスモード変更
        self.path_mode_selector.path_mode_changed.connect(self.on_path_mode_changed)
        
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
        refresh_action.triggered.connect(self.file_tree.refresh_tree)
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
            theme_action.triggered.connect(lambda checked, t=theme_name: self.change_theme(t))
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
        
        # 思考レベル表示
        self.thinking_level_label = QLabel(f"{tr('label_thinking_level')} think")
        self.statusBar().addPermanentWidget(self.thinking_level_label)
    
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
    
    def on_path_mode_changed(self, mode: str):
        """パスモードが変更されたとき"""
        self.prompt_input.set_path_mode(mode)
        self.settings_manager.set_path_mode(mode)
        self.statusBar().showMessage(tr("status_path_mode_changed", mode=mode), 2000)
    
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
        
        # パスを適切に変換
        workspace_relative_path = PathConverter.convert_path(workspace_relative_path, self.prompt_input.path_mode)
        
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
        self.path_mode_selector.update_language()
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
    
    def on_splitter_moved(self, pos: int, index: int):
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