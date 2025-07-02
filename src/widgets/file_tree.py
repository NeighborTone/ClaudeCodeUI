# -*- coding: utf-8 -*-
"""
File Tree Widget - File explorer-like tree view
"""
import os
from typing import Optional, List
from PySide6.QtWidgets import (QTreeWidget, QTreeWidgetItem, QVBoxLayout, 
                              QWidget, QPushButton, QHBoxLayout, QFileDialog,
                              QMenu, QMessageBox, QLineEdit, QComboBox, QLabel,
                              QAbstractItemView, QHeaderView)
from PySide6.QtCore import Signal, Qt, QUrl, QTimer
from PySide6.QtGui import QAction, QIcon, QDragEnterEvent, QDropEvent, QBrush, QColor

from src.core.workspace_manager import WorkspaceManager
from src.core.ui_strings import tr
from src.core.logger import logger
from src.widgets.file_tree_worker import FileTreeWorker, FileTreeLoadingThread, TreeNode


class FileTreeWidget(QWidget):
    """File tree widget"""
    
    file_selected = Signal(str)  # File selected signal
    file_double_clicked = Signal(str)  # File double-clicked signal
    workspace_changed = Signal()  # Workspace changed signal
    
    def __init__(self, workspace_manager: WorkspaceManager = None, parent=None):
        super().__init__(parent)
        
        # Use provided workspace_manager or create new one
        self.workspace_manager = workspace_manager if workspace_manager else WorkspaceManager()
        
        # Search functionality
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
        self.search_delay = 300  # 300ms delay for debouncing
        
        # File type filter categories
        self.file_categories = {
            'all': set(),  # Empty set means all files
            'source': {
                '.py', '.cpp', '.c', '.h', '.hpp', '.cxx', '.hxx',
                '.cs', '.java', '.js', '.ts', '.jsx', '.tsx',
                '.go', '.rs', '.php', '.rb', '.swift', '.kt',
                '.hlsl', '.glsl', '.shader', '.cginc', '.compute'
            },
            'images': {
                '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif',
                '.webp', '.svg', '.ico', '.psd', '.ai', '.eps'
            },
            'media': {
                '.wav', '.mp3', '.flac', '.aac', '.ogg', '.wma',
                '.m4a', '.opus', '.aiff', '.au',
                '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv',
                '.webm', '.m4v', '.3gp', '.ogv'
            },
            'config': {
                '.json', '.yaml', '.yml', '.xml', '.toml', '.ini', '.cfg', '.config',
                '.cmake', '.make', '.gradle', '.sln', '.vcxproj',
                '.pro', '.pri', '.qmake', '.build', '.target'
            },
            'docs': {
                '.csv', '.txt', '.md', '.rst'
            },
            'game': {
                '.uproject', '.uplugin', '.uasset', '.umap', '.ucpp',
                '.unity', '.prefab', '.asset', '.mat', '.anim', '.controller',
                '.overrideController', '.mask', '.physicMaterial', '.physicsMaterial2D',
                '.guiskin', '.fontsettings', '.cubemap', '.flare', '.preset',
                '.playable', '.signal', '.mixer', '.cs.meta', '.unity.meta',
                '.prefab.meta', '.asset.meta', '.mat.meta', '.anim.meta'
            }
        }
        
        # ワーカーとスレッドの初期化
        self.loading_thread = None
        self.loading_worker = None
        self.is_loading = False
        self.pending_workspace_update = False
        self.loading_item = None  # 読み込み中表示用アイテム
        
        # アニメーション用
        self.loading_animation_timer = QTimer()
        self.loading_animation_timer.timeout.connect(self.update_loading_animation)
        self.loading_animation_timer.setInterval(500)  # 500msごとに更新
        self.loading_dots_count = 0
        self.loading_base_text = ""
        
        self.setup_ui()
        # Defer workspace loading to improve startup speed
        QTimer.singleShot(100, self.load_workspaces_async)
        
        # Enable drag & drop
        self.setAcceptDrops(True)
    
    def setup_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # ツールバー
        toolbar_layout = QHBoxLayout()
        
        self.add_workspace_btn = QPushButton(tr("button_add_folder"))
        self.add_workspace_btn.clicked.connect(self.add_workspace)
        toolbar_layout.addWidget(self.add_workspace_btn)
        
        self.refresh_btn = QPushButton(tr("button_refresh"))
        self.refresh_btn.clicked.connect(self.rebuild_index)
        toolbar_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(toolbar_layout)
        
        # 検索バー
        search_layout = QHBoxLayout()
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(tr("search_placeholder"))
        self.search_box.setToolTip(tr("search_tooltip"))
        self.search_box.textChanged.connect(self.on_search_text_changed)
        search_layout.addWidget(self.search_box)
        
        layout.addLayout(search_layout)
        
        # フィルターバー
        filter_layout = QHBoxLayout()
        
        filter_label = QLabel(tr("filter_label"))
        filter_layout.addWidget(filter_label)
        
        self.filter_combo = QComboBox()
        self.filter_combo.setToolTip(tr("filter_tooltip"))
        self.populate_filter_combo()
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.filter_combo)
        
        layout.addLayout(filter_layout)
        
        # ツリーウィジェット
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel(tr("tree_header"))
        self.tree.itemClicked.connect(self.on_item_clicked)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        
        # 水平スクロールバーの設定
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tree.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        # ヘッダーのリサイズ設定
        header = self.tree.header()
        header.setStretchLastSection(True)  # 最後のセクションを伸縮可能に
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # ヘッダーを自動伸縮
        
        layout.addWidget(self.tree)
    
    def update_language(self):
        """言語変更時にUIを更新"""
        self.add_workspace_btn.setText(tr("button_add_folder"))
        self.refresh_btn.setText(tr("button_refresh"))
        self.tree.setHeaderLabel(tr("tree_header"))
        self.search_box.setPlaceholderText(tr("search_placeholder"))
        self.search_box.setToolTip(tr("search_tooltip"))
        self.filter_combo.setToolTip(tr("filter_tooltip"))
        self.populate_filter_combo()  # Refresh filter combo with new language
    
    def add_workspace(self):
        """ワークスペースを追加"""
        folder_path = QFileDialog.getExistingDirectory(
            self, tr("dialog_select_folder"), os.path.expanduser("~")
        )
        
        if folder_path:
            if self.workspace_manager.add_workspace(folder_path):
                self.load_workspaces_async()
                # ワークスペース変更を通知
                self.workspace_changed.emit()
            else:
                QMessageBox.warning(self, tr("dialog_warning"), tr("msg_folder_already_exists"))
    
    def load_workspaces_async(self):
        """ワークスペースを非同期で読み込む"""
        if self.is_loading:
            self.pending_workspace_update = True
            return
        
        self.tree.clear()
        self.loading_item = None  # クリア時にリセット
        workspaces = self.workspace_manager.get_workspaces()
        
        if not workspaces:
            return
        
        # 非同期読み込みを開始
        self.start_async_loading(workspaces)
    
    def start_async_loading(self, workspaces: List[dict]):
        """非同期読み込みを開始"""
        self.is_loading = True
        
        # 既存のスレッドを停止
        if self.loading_thread and self.loading_thread.isRunning():
            self.loading_worker.stop()
            self.loading_thread.quit()
            self.loading_thread.wait()
        
        # 新しいワーカーとスレッドを作成
        self.loading_worker = FileTreeWorker()
        self.loading_thread = FileTreeLoadingThread(self.loading_worker)
        
        # ワーカーの設定
        self.loading_worker.set_workspaces(workspaces)
        
        # シグナルを接続
        self.loading_worker.started.connect(self.on_loading_started)
        self.loading_worker.progress.connect(self.on_loading_progress)
        self.loading_worker.workspace_loaded.connect(self.on_workspace_loaded)
        self.loading_worker.completed.connect(self.on_loading_completed)
        self.loading_worker.failed.connect(self.on_loading_failed)
        
        # スレッドを開始
        self.loading_thread.start()
        
    def on_loading_started(self):
        """読み込み開始時の処理"""
        logger.info("File tree loading started")
        
        # 読み込み中表示を追加
        if not self.loading_item:
            self.loading_item = QTreeWidgetItem(self.tree)
            self.loading_base_text = tr("tree_loading_message").rstrip('.')  # 末尾の.を除去
            self.loading_item.setText(0, self.loading_base_text)
            self.loading_item.setToolTip(0, tr("tree_loading_tooltip"))
            # アイコンやスタイルを設定して目立たせる
            font = self.loading_item.font(0)
            font.setItalic(True)
            self.loading_item.setFont(0, font)
            
            # アニメーションを開始
            self.loading_dots_count = 0
            self.loading_animation_timer.start()
        
    def on_loading_progress(self, progress: float, message: str):
        """読み込み進捗の処理"""
        if progress >= 0:
            logger.debug(f"File tree loading: {progress:.1f}% - {message}")
        
        # ツールチップにのみ詳細情報を表示
        if self.loading_item:
            self.loading_item.setToolTip(0, message)
        
    def on_workspace_loaded(self, workspace_path: str, tree_node: TreeNode):
        """ワークスペースが読み込まれたときの処理"""
        # 初回のワークスペース読み込み時に読み込み中表示を削除
        if self.loading_item:
            self.tree.takeTopLevelItem(self.tree.indexOfTopLevelItem(self.loading_item))
            self.loading_item = None
            # アニメーションも停止
            self.loading_animation_timer.stop()
        
        # ツリーにワークスペースを追加
        workspace_item = QTreeWidgetItem(self.tree)
        workspace_item.setText(0, tree_node.name)
        workspace_item.setData(0, Qt.UserRole, {
            'type': 'workspace',
            'path': workspace_path
        })
        workspace_item.setExpanded(True)
        
        # 子ノードを再帰的に追加
        self._add_tree_nodes(workspace_item, tree_node.children)
        
    def _add_tree_nodes(self, parent_item: QTreeWidgetItem, nodes: List[TreeNode]):
        """ツリーノードを再帰的に追加"""
        for node in nodes:
            item = QTreeWidgetItem(parent_item)
            item.setText(0, node.name)
            item.setData(0, Qt.UserRole, {
                'type': node.type,
                'path': node.path
            })
            
            if node.children:
                self._add_tree_nodes(item, node.children)
                
    def on_loading_completed(self):
        """読み込み完了時の処理"""
        logger.info("File tree loading completed")
        self.is_loading = False
        
        # アニメーションを停止
        self.loading_animation_timer.stop()
        
        # MainWindowに通知
        parent = self.parent()
        while parent:
            if hasattr(parent, 'on_file_tree_loading_completed'):
                parent.on_file_tree_loading_completed()
                break
            parent = parent.parent()
        
        # ペンディングの更新があれば実行
        if self.pending_workspace_update:
            self.pending_workspace_update = False
            QTimer.singleShot(100, self.load_workspaces_async)
        
    def on_loading_failed(self, error_message: str):
        """読み込み失敗時の処理"""
        logger.error(f"File tree loading failed: {error_message}")
        self.is_loading = False
        
        # アニメーションを停止
        self.loading_animation_timer.stop()
        
        # 読み込み中表示をエラー表示に変更
        if self.loading_item:
            self.loading_item.setText(0, tr("tree_loading_failed"))
            self.loading_item.setToolTip(0, error_message)
            # エラーを示す色に変更（例：赤）
            self.loading_item.setForeground(0, QBrush(QColor(Qt.red)))
        
        # エラーメッセージを表示
        QMessageBox.warning(self, tr("dialog_warning"), 
                          f"Failed to load file tree: {error_message}")
        
    def load_workspaces(self):
        """ワークスペースを読み込む（後方互換性のため）"""
        self.load_workspaces_async()
    
    def rebuild_index(self):
        """インデックスを再構築"""
        # インデックス再構築の信号を発信
        self.workspace_changed.emit()
        # ツリーも再読み込み
        self.refresh_tree()
    
    def refresh_tree(self):
        """ツリーを更新（検索とフィルターもリセット）"""
        # 検索ボックスをクリア
        self.search_box.clear()
        
        # フィルターを「すべて」にリセット
        self.filter_combo.setCurrentIndex(0)  # First item is "All Files"
        
        # ツリーを再読み込み
        self.load_workspaces_async()
    
    def on_item_clicked(self, item: QTreeWidgetItem, column: int = 0):
        """アイテムがクリックされたとき"""
        data = item.data(0, Qt.UserRole)
        if data and data['type'] == 'file':
            self.file_selected.emit(data['path'])
    
    def on_item_double_clicked(self, item: QTreeWidgetItem, column: int = 0):
        """アイテムがダブルクリックされたとき"""
        data = item.data(0, Qt.UserRole)
        if data and data['type'] == 'file':
            self.file_double_clicked.emit(data['path'])
    
    def show_context_menu(self, position):
        """コンテキストメニューを表示"""
        item = self.tree.itemAt(position)
        if not item:
            return
        
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        menu = QMenu()
        
        if data['type'] == 'workspace':
            remove_action = QAction(tr("context_remove_workspace"), self)
            remove_action.triggered.connect(lambda: self.remove_workspace(data['path']))
            menu.addAction(remove_action)
        
        elif data['type'] == 'file':
            copy_path_action = QAction(tr("context_copy_path"), self)
            copy_path_action.triggered.connect(lambda: self.copy_path_to_clipboard(data['path']))
            menu.addAction(copy_path_action)
        
        menu.exec(self.tree.mapToGlobal(position))
    
    def remove_workspace(self, path: str):
        """ワークスペースを削除"""
        reply = QMessageBox.question(
            self, tr("dialog_confirm"), 
            tr("msg_confirm_remove_workspace", path=path),
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.workspace_manager.remove_workspace(path):
                self.load_workspaces_async()
                # ワークスペース変更を通知
                self.workspace_changed.emit()
    
    def copy_path_to_clipboard(self, path: str):
        """パスをクリップボードにコピー"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(path)
    
    def get_selected_file(self) -> Optional[str]:
        """Get selected file path"""
        current_item = self.tree.currentItem()
        if current_item:
            data = current_item.data(0, Qt.UserRole)
            if data and data['type'] == 'file':
                return data['path']
        return None
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            # Check if any of the URLs are directories
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if os.path.isdir(path):
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        urls = event.mimeData().urls()
        added_count = 0
        
        for url in urls:
            path = url.toLocalFile()
            if os.path.isdir(path):
                if self.workspace_manager.add_workspace(path):
                    added_count += 1
        
        if added_count > 0:
            self.load_workspaces_async()
            # ワークスペース変更を通知してインデックス構築をトリガー
            self.workspace_changed.emit()
            QMessageBox.information(
                self, tr("dialog_success"), 
                tr("msg_folders_added", count=added_count)
            )
        else:
            QMessageBox.warning(
                self, tr("dialog_warning"), 
                tr("msg_no_valid_folders")
            )
        
        event.acceptProposedAction()
    
    def on_search_text_changed(self, text: str):
        """検索テキストが変更されたときの処理（デバウンス付き）"""
        self.search_timer.stop()
        self.search_timer.start(self.search_delay)
    
    def perform_search(self):
        """実際の検索処理を実行"""
        self.apply_filters()
    
    def apply_filters(self):
        """検索とフィルターを組み合わせて適用"""
        search_text = self.search_box.text().strip().lower()
        current_filter = self.get_current_filter_key()
        
        if not search_text and current_filter == 'all':
            # 検索テキストもフィルターもない場合、すべて表示
            self.show_all_items()
        else:
            # 検索とフィルターを実行
            self.filter_tree_items(search_text, current_filter)
    
    def populate_filter_combo(self):
        """フィルターコンボボックスを設定"""
        current_selection = self.filter_combo.currentText() if hasattr(self, 'filter_combo') else tr("filter_all")
        
        self.filter_combo.clear()
        self.filter_combo.addItem(tr("filter_all"))
        self.filter_combo.addItem(tr("filter_source"))
        self.filter_combo.addItem(tr("filter_images"))
        self.filter_combo.addItem(tr("filter_media"))
        self.filter_combo.addItem(tr("filter_config"))
        self.filter_combo.addItem(tr("filter_docs"))
        self.filter_combo.addItem(tr("filter_game"))
        
        # Restore previous selection if possible
        index = self.filter_combo.findText(current_selection)
        if index >= 0:
            self.filter_combo.setCurrentIndex(index)
    
    def get_current_filter_key(self) -> str:
        """現在選択されているフィルターのキーを取得"""
        current_text = self.filter_combo.currentText()
        filter_map = {
            tr("filter_all"): 'all',
            tr("filter_source"): 'source',
            tr("filter_images"): 'images',
            tr("filter_media"): 'media',
            tr("filter_config"): 'config',
            tr("filter_docs"): 'docs',
            tr("filter_game"): 'game'
        }
        return filter_map.get(current_text, 'all')
    
    def on_filter_changed(self):
        """フィルターが変更されたときの処理"""
        self.apply_filters()
    
    def show_all_items(self):
        """すべてのアイテムを表示"""
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            self.set_item_visible_recursive(item, True)
    
    def filter_tree_items(self, search_text: str, filter_key: str):
        """ツリーアイテムを検索テキストとファイルタイプでフィルタリング"""
        for i in range(self.tree.topLevelItemCount()):
            workspace_item = self.tree.topLevelItem(i)
            # ワークスペースは常に表示
            workspace_item.setHidden(False)
            # 子アイテムをフィルタリング
            has_visible_children = self.filter_item_recursive(workspace_item, search_text, filter_key)
            # 子に表示可能なアイテムがない場合はワークスペースを非表示
            workspace_item.setHidden(not has_visible_children)
    
    def filter_item_recursive(self, item: QTreeWidgetItem, search_text: str, filter_key: str) -> bool:
        """再帰的にアイテムをフィルタリング（子に一致するものがあるかチェック）"""
        has_visible_children = False
        item_matches = False
        
        # 現在のアイテムの名前をチェック
        item_name = item.text(0).lower()
        data = item.data(0, Qt.UserRole)
        
        # ワークスペース以外のアイテムのみ名前とタイプでマッチング
        if data and data.get('type') != 'workspace':
            # 検索テキストのマッチング
            search_matches = not search_text or search_text in item_name
            
            # ファイルタイプフィルターのマッチング
            type_matches = True
            if data.get('type') == 'file' and filter_key != 'all':
                file_ext = os.path.splitext(item_name)[1].lower()
                type_matches = file_ext in self.file_categories.get(filter_key, set())
            
            item_matches = search_matches and type_matches
        
        # 子アイテムを再帰的にチェック
        for i in range(item.childCount()):
            child = item.child(i)
            child_has_match = self.filter_item_recursive(child, search_text, filter_key)
            if child_has_match:
                has_visible_children = True
        
        # アイテム自体がマッチするか、子にマッチするものがある場合は表示
        should_show = item_matches or has_visible_children
        
        # ワークスペースアイテムは特別扱い（常に表示するが、子の状態によって決まる）
        if data and data.get('type') == 'workspace':
            item.setHidden(False)
            return has_visible_children
        else:
            item.setHidden(not should_show)
            return should_show
    
    def set_item_visible_recursive(self, item: QTreeWidgetItem, visible: bool):
        """再帰的にアイテムの表示状態を設定"""
        item.setHidden(not visible)
        for i in range(item.childCount()):
            child = item.child(i)
            self.set_item_visible_recursive(child, visible)
    
    def update_loading_animation(self):
        """読み込み中アニメーションを更新"""
        if not self.loading_item:
            return
        
        # ドットの数を循環させる（0, 1, 2, 3, 0, 1, 2, 3...)
        self.loading_dots_count = (self.loading_dots_count + 1) % 4
        dots = '.' * self.loading_dots_count
        
        # シンプルなドットアニメーションのみ
        text = f"{self.loading_base_text}{dots}"
        self.loading_item.setText(0, text)