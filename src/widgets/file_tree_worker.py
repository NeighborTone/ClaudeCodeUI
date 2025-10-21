# -*- coding: utf-8 -*-
"""
File Tree Worker - Asynchronous file tree loading worker
"""
import os
import json
from typing import List, Dict, Tuple, Optional, Set
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
    # 遅延読み込み用フィールド
    is_loaded: bool = False      # 子要素が読み込み済みか
    has_children: bool = None    # 子要素の有無（None=未確認）
    is_placeholder: bool = False # プレースホルダーノードか

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
        
        # ファイルタイプ設定を外部ファイルから読み込む
        self._load_file_filters()
    
    def _load_file_filters(self):
        """外部ファイルからファイルフィルター設定を読み込む"""
        try:
            # 設定ファイルのパスを取得
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            config_path = os.path.join(project_root, 'data', 'file_filters.json')
            
            # JSONファイルを読み込む
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 設定を適用（listからsetに変換）
            self.allowed_extensions = set(config.get('allowed_extensions', []))
            self.important_files = set(config.get('important_files', []))
            self.excluded_dirs = set(config.get('excluded_dirs', []))
            
            logger.info(f"File filters loaded from {config_path}")
            
        except FileNotFoundError:
            logger.warning(f"File filters config not found, using default settings")
            self._set_default_filters()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file filters config: {e}")
            self._set_default_filters()
        except Exception as e:
            logger.error(f"Error loading file filters config: {e}")
            self._set_default_filters()
    
    def _set_default_filters(self):
        """デフォルトのファイルフィルター設定を適用"""
        # 外部設定ファイルが読み込めない場合はすべてを許可
        logger.warning("File filters configuration not available. All files and folders will be displayed.")
        
        # すべての拡張子を許可（空のセットは条件判定で使用しない）
        self.allowed_extensions = None  # Noneはフィルタリング無効を意味する
        
        # 重要なファイル名（フィルタリング無効時は使用しない）
        self.important_files = set()
        
        # 除外するディレクトリ（空のセットで全フォルダを表示）
        self.excluded_dirs = set()
    
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
                
                # 進捗を報告（最初から0%以上になるように調整）
                progress = ((idx + 0.5) / total_workspaces) * 100
                self.progress.emit(progress, f"Loading workspace: {workspace_name}")
                
                logger.info(f"Loading workspace: {workspace_path}")
                
                # ワークスペースノードを作成
                workspace_node = TreeNode(
                    name=workspace_name,
                    path=workspace_path,
                    type='workspace'
                )
                
                # ワークスペースの内容を読み込む（遅延読み込み版を使用）
                self._populate_node_shallow(workspace_node, workspace_path)
                
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

    def _populate_node_shallow(self, parent_node: TreeNode, path: str):
        """ノードに子要素を追加（1階層のみ、遅延読み込み用）

        フォルダにはプレースホルダーノードを追加して展開可能にする。
        ファイルは通常通り追加する。
        """
        if self.should_stop:
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

            # フォルダを追加（プレースホルダー付き）
            for folder_name, folder_path in folders:
                if self.should_stop:
                    return

                folder_node = TreeNode(
                    name=folder_name,
                    path=folder_path,
                    type='folder',
                    is_loaded=False,  # まだ読み込まれていない
                    has_children=True  # フォルダなので子要素がある可能性がある
                )

                # プレースホルダーノードを追加（展開可能にするため）
                placeholder = TreeNode(
                    name="読み込み中...",
                    path="",
                    type='placeholder',
                    is_placeholder=True
                )
                folder_node.children.append(placeholder)

                parent_node.children.append(folder_node)

            # ファイルを追加
            for file_name, file_path in files:
                if self.should_stop:
                    return

                file_ext = os.path.splitext(file_name)[1].lower()
                file_name_lower = file_name.lower()

                # 重要なファイルかチェック
                is_important = any(important in file_name_lower for important in self.important_files)

                # 許可された拡張子または重要なファイルのみ追加
                if self.allowed_extensions is None or file_ext in self.allowed_extensions or is_important:
                    file_node = TreeNode(
                        name=file_name,
                        path=file_path,
                        type='file',
                        is_loaded=True  # ファイルは子がないので読み込み済み
                    )
                    parent_node.children.append(file_node)

            # 親ノードを読み込み済みとマーク
            parent_node.is_loaded = True

        except PermissionError as e:
            logger.warning(f"Permission denied: {path} - {e}")
        except Exception as e:
            logger.error(f"Error loading folder: {path} - {e}")

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
            
            # 深いディレクトリでも進捗を報告（簡易的な実装）
            if current_depth <= 2:  # 浅い階層でのみ進捗を報告
                dir_name = os.path.basename(path)
                self.progress.emit(-1, f"Scanning: {dir_name}")  # -1は特殊な値として使用
            
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
                # allowed_extensions が None の場合はすべてのファイルを許可
                if self.allowed_extensions is None or file_ext in self.allowed_extensions or is_important:
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