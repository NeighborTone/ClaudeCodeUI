# -*- coding: utf-8 -*-
"""
File Tree Worker - Asynchronous file tree loading worker
"""
import os
from typing import List, Dict, Tuple, Optional
from PySide6.QtCore import QObject, Signal, QThread
from dataclasses import dataclass

from src.core.logger import logger


@dataclass
class TreeNode:
    """ツリーノードのデータクラス"""
    name: str
    path: str
    type: str  # 'workspace', 'folder', 'file'
    children: List['TreeNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class FileTreeWorker(QObject):
    """ファイルツリーの非同期読み込みワーカー"""
    
    # シグナル定義
    started = Signal()
    progress = Signal(float, str)  # progress percentage, message
    workspace_loaded = Signal(str, object)  # workspace_path, TreeNode
    completed = Signal()
    failed = Signal(str)  # error message
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.workspaces = []
        self.should_stop = False
        self.max_depth = 15
        
        # ファイルタイプ設定（FileTreeWidgetから移植）
        self.allowed_extensions = {
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
        
        # 重要なファイル名
        self.important_files = {
            'readme', 'license', 'changelog', 'makefile', 'dockerfile',
            'cmakelist', 'cmakelists', 'requirements', 'package',
            'gulpfile', 'gruntfile', 'webpack', 'tsconfig', 'jsconfig'
        }
        
        # 除外するディレクトリ
        self.excluded_dirs = {
            'node_modules', '__pycache__', 'Binaries', 'Intermediate', 
            'Saved', 'DerivedDataCache', '.git', '.svn', '.hg'
        }
    
    def set_workspaces(self, workspaces: List[Dict[str, str]]):
        """ワークスペースを設定"""
        self.workspaces = workspaces
    
    def stop(self):
        """処理を停止"""
        self.should_stop = True
    
    def run(self):
        """ワーカーのメイン処理"""
        try:
            self.should_stop = False
            self.started.emit()
            
            total_workspaces = len(self.workspaces)
            
            for idx, workspace in enumerate(self.workspaces):
                if self.should_stop:
                    break
                
                workspace_path = workspace['path']
                workspace_name = workspace['name']
                
                # 進捗を報告
                progress = (idx / total_workspaces) * 100
                self.progress.emit(progress, f"Loading workspace: {workspace_name}")
                
                logger.info(f"Loading workspace: {workspace_path}")
                
                # ワークスペースノードを作成
                workspace_node = TreeNode(
                    name=workspace_name,
                    path=workspace_path,
                    type='workspace'
                )
                
                # ワークスペースの内容を読み込む
                self._populate_node(workspace_node, workspace_path, 0)
                
                # ワークスペースの読み込み完了を通知
                self.workspace_loaded.emit(workspace_path, workspace_node)
                
                # 次のワークスペースの進捗
                progress = ((idx + 1) / total_workspaces) * 100
                self.progress.emit(progress, f"Completed: {workspace_name}")
            
            if not self.should_stop:
                self.completed.emit()
            
        except Exception as e:
            logger.error(f"Error in FileTreeWorker: {e}")
            self.failed.emit(str(e))
    
    def _populate_node(self, parent_node: TreeNode, path: str, current_depth: int):
        """ノードに子要素を追加（再帰的）"""
        if self.should_stop:
            return
        
        if current_depth >= self.max_depth:
            return
        
        try:
            if not os.path.exists(path):
                logger.warning(f"Path does not exist: {path}")
                return
            
            items = os.listdir(path)
            items.sort()
            
            # フォルダとファイルを分離
            folders = []
            files = []
            
            for item in items:
                if self.should_stop:
                    return
                
                item_path = os.path.join(path, item)
                
                # 隠しファイルと除外ディレクトリをスキップ（.claudeは許可）
                if item.startswith('.') and item != '.claude':
                    continue
                if item in self.excluded_dirs:
                    continue
                
                if os.path.isdir(item_path):
                    folders.append((item, item_path))
                else:
                    files.append((item, item_path))
            
            # フォルダを先に追加
            for folder_name, folder_path in folders:
                if self.should_stop:
                    return
                
                folder_node = TreeNode(
                    name=folder_name,
                    path=folder_path,
                    type='folder'
                )
                parent_node.children.append(folder_node)
                
                # 再帰的にサブフォルダを処理
                self._populate_node(folder_node, folder_path, current_depth + 1)
            
            # ファイルを追加
            for file_name, file_path in files:
                if self.should_stop:
                    return
                
                file_ext = os.path.splitext(file_name)[1].lower()
                file_name_lower = file_name.lower()
                
                # 重要なファイルかチェック
                is_important = any(important in file_name_lower for important in self.important_files)
                
                # 許可された拡張子または重要なファイルのみ追加
                if file_ext in self.allowed_extensions or is_important:
                    file_node = TreeNode(
                        name=file_name,
                        path=file_path,
                        type='file'
                    )
                    parent_node.children.append(file_node)
        
        except PermissionError as e:
            logger.warning(f"Permission denied: {path} - {e}")
        except Exception as e:
            logger.error(f"Error loading folder: {path} - {e}")


class FileTreeLoadingThread(QThread):
    """ファイルツリー読み込み用のスレッド"""
    
    def __init__(self, worker: FileTreeWorker, parent=None):
        super().__init__(parent)
        self.worker = worker
        # ワーカーをスレッドに移動
        self.worker.moveToThread(self)
    
    def run(self):
        """スレッドのメイン処理"""
        self.worker.run()