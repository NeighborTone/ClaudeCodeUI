# -*- coding: utf-8 -*-
"""
File Tree Widget - File explorer-like tree view
"""
import os
from typing import Optional, List
from PySide6.QtWidgets import (QTreeWidget, QTreeWidgetItem, QVBoxLayout, 
                              QWidget, QPushButton, QHBoxLayout, QFileDialog,
                              QMenu, QMessageBox)
from PySide6.QtCore import Signal, Qt, QUrl
from PySide6.QtGui import QAction, QIcon, QDragEnterEvent, QDropEvent

from core.workspace_manager import WorkspaceManager
from core.ui_strings import tr


class FileTreeWidget(QWidget):
    """File tree widget"""
    
    file_selected = Signal(str)  # File selected signal
    file_double_clicked = Signal(str)  # File double-clicked signal
    
    def __init__(self, workspace_manager: WorkspaceManager = None, parent=None):
        super().__init__(parent)
        
        # Use provided workspace_manager or create new one
        self.workspace_manager = workspace_manager if workspace_manager else WorkspaceManager()
        self.setup_ui()
        self.load_workspaces()
        
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
        self.refresh_btn.clicked.connect(self.refresh_tree)
        toolbar_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(toolbar_layout)
        
        # ツリーウィジェット
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel(tr("tree_header"))
        self.tree.itemClicked.connect(self.on_item_clicked)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.tree)
    
    def update_language(self):
        """言語変更時にUIを更新"""
        self.add_workspace_btn.setText(tr("button_add_folder"))
        self.refresh_btn.setText(tr("button_refresh"))
        self.tree.setHeaderLabel(tr("tree_header"))
    
    def add_workspace(self):
        """ワークスペースを追加"""
        folder_path = QFileDialog.getExistingDirectory(
            self, tr("dialog_select_folder"), os.path.expanduser("~")
        )
        
        if folder_path:
            if self.workspace_manager.add_workspace(folder_path):
                self.load_workspaces()
                # Process UI updates immediately to ensure sync
                from PySide6.QtCore import QCoreApplication
                QCoreApplication.processEvents()
            else:
                QMessageBox.warning(self, tr("dialog_warning"), tr("msg_folder_already_exists"))
    
    def load_workspaces(self):
        """ワークスペースを読み込んでツリーに表示"""
        self.tree.clear()
        
        workspaces = self.workspace_manager.get_workspaces()
        for workspace in workspaces:
            workspace_item = QTreeWidgetItem(self.tree)
            workspace_item.setText(0, workspace['name'])
            workspace_item.setData(0, Qt.UserRole, {
                'type': 'workspace',
                'path': workspace['path']
            })
            
            # ワークスペースを展開した状態にする
            workspace_item.setExpanded(True)
            
            # ファイルとフォルダを追加
            self.populate_workspace(workspace_item, workspace['path'])
    
    def populate_workspace(self, parent_item: QTreeWidgetItem, path: str, max_depth: int = 6, current_depth: int = 0):
        """Populate workspace with folders and files"""
        if current_depth >= max_depth:
            return
            
        try:
            if not os.path.exists(path):
                print(f"Path does not exist: {path}")
                return
                
            items = os.listdir(path)
            items.sort()
            
            print(f"Loading directory: {path} (depth: {current_depth}, items: {len(items)})")
            
            # Separate folders and files
            folders = []
            files = []
            
            for item in items:
                item_path = os.path.join(path, item)
                
                # Skip hidden files and specific directories
                if item.startswith('.'):
                    continue
                if item in ['node_modules', '__pycache__', 'Binaries', 'Intermediate', 'Saved', 'DerivedDataCache']:
                    continue
                    
                if os.path.isdir(item_path):
                    folders.append((item, item_path))
                else:
                    files.append((item, item_path))
            
            # Add folders first
            for folder_name, folder_path in folders:
                folder_item = QTreeWidgetItem(parent_item)
                folder_item.setText(0, folder_name)
                folder_item.setData(0, Qt.UserRole, {
                    'type': 'folder',
                    'path': folder_path
                })
                
                # Recursively add subfolders and files
                self.populate_workspace(folder_item, folder_path, max_depth, current_depth + 1)
            
            # Add files (expanded extension support)
            allowed_extensions = {
                # Programming languages
                '.py', '.cpp', '.c', '.h', '.hpp', '.cxx', '.hxx',
                '.cs', '.java', '.js', '.ts', '.jsx', '.tsx',
                '.go', '.rs', '.php', '.rb', '.swift', '.kt',
                
                # Unreal Engine files
                '.uproject', '.uplugin', '.uasset', '.umap', '.ucpp',
                '.build', '.target', '.ini', '.cfg', '.config',
                
                # Unity files
                '.unity', '.prefab', '.asset', '.mat', '.anim', '.controller',
                '.overrideController', '.mask', '.physicMaterial', '.physicsMaterial2D',
                '.guiskin', '.fontsettings', '.cubemap', '.flare', '.preset',
                '.playable', '.signal', '.mixer', '.cs.meta', '.unity.meta',
                '.prefab.meta', '.asset.meta', '.mat.meta', '.anim.meta',
                
                # Config and data files
                '.json', '.yaml', '.yml', '.xml', '.toml',
                '.csv', '.txt', '.md', '.rst',
                
                # Build files
                '.cmake', '.make', '.gradle', '.sln', '.vcxproj',
                '.pro', '.pri', '.qmake',
                
                # Shaders
                '.hlsl', '.glsl', '.shader', '.cginc', '.compute',
                
                # Image files
                '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif',
                '.webp', '.svg', '.ico', '.psd', '.ai', '.eps',
                
                # Audio files
                '.wav', '.mp3', '.flac', '.aac', '.ogg', '.wma',
                '.m4a', '.opus', '.aiff', '.au',
                
                # Video files
                '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv',
                '.webm', '.m4v', '.3gp', '.ogv'
            }
            
            for file_name, file_path in files:
                file_ext = os.path.splitext(file_name)[1].lower()
                
                # Always include certain important files regardless of extension
                important_files = {
                    'readme', 'license', 'changelog', 'makefile', 'dockerfile',
                    'cmakelist', 'cmakelists', 'requirements', 'package',
                    'gulpfile', 'gruntfile', 'webpack', 'tsconfig', 'jsconfig'
                }
                
                file_name_lower = file_name.lower()
                is_important = any(important in file_name_lower for important in important_files)
                
                if file_ext in allowed_extensions or is_important:
                    file_item = QTreeWidgetItem(parent_item)
                    file_item.setText(0, file_name)
                    file_item.setData(0, Qt.UserRole, {
                        'type': 'file',
                        'path': file_path
                    })
                    print(f"Added file: {file_name}")
                    
        except PermissionError as e:
            print(f"Permission denied: {path} - {e}")
        except Exception as e:
            print(f"Error loading folder: {path} - {e}")
    
    def refresh_tree(self):
        """ツリーを更新"""
        self.load_workspaces()
    
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
                self.load_workspaces()
    
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
            self.load_workspaces()
            # Notify that workspaces have been updated
            from PySide6.QtCore import QCoreApplication
            QCoreApplication.processEvents()  # Process UI updates immediately
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