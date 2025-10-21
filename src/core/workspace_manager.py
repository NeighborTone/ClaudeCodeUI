# -*- coding: utf-8 -*-
"""
Workspace Manager - VSCode-like workspace functionality
"""
import os
import json
from typing import List, Dict, Optional, TYPE_CHECKING
from pathlib import Path
from src.core.logger import get_logger

if TYPE_CHECKING:
    from src.core.sqlite_indexer import SQLiteIndexer


class WorkspaceManager:
    """Workspace (project folder) management class"""

    def __init__(self, config_file: str = "saved/workspace.json", sqlite_indexer: Optional['SQLiteIndexer'] = None):
        self.config_file = config_file
        self.workspaces: List[Dict[str, str]] = []
        self.logger = get_logger(__name__)
        self.sqlite_indexer = sqlite_indexer  # SQLiteIndexerへの参照
        self.load_workspaces()
    
    def load_workspaces(self) -> None:
        """Load saved workspace information"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.workspaces = data.get('workspaces', [])
        except Exception as e:
            self.logger.error(f"Workspace loading error ({self.config_file}): {e}")
            self.workspaces = []
    
    def save_workspaces(self) -> None:
        """Save workspace information"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'workspaces': self.workspaces}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Workspace saving error ({self.config_file}): {e}")
    
    def add_workspace(self, path: str, name: Optional[str] = None) -> bool:
        """Add workspace"""
        if not os.path.exists(path) or not os.path.isdir(path):
            return False
        
        path = os.path.abspath(path)
        
        # Check if already exists
        for workspace in self.workspaces:
            if workspace['path'] == path:
                return False
        
        if name is None:
            name = os.path.basename(path)
        
        self.workspaces.append({
            'name': name,
            'path': path
        })
        
        self.save_workspaces()
        return True
    
    def remove_workspace(self, path: str) -> bool:
        """Remove workspace"""
        path = os.path.abspath(path)
        for i, workspace in enumerate(self.workspaces):
            if workspace['path'] == path:
                del self.workspaces[i]
                self.save_workspaces()
                return True
        return False
    
    def get_workspaces(self) -> List[Dict[str, str]]:
        """Get all workspaces"""
        return self.workspaces.copy()
    
    def get_all_files(self, extensions: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        全ワークスペースから全ファイルを取得

        SQLiteインデックスが利用可能な場合はそれを使用し、
        そうでない場合はフォールバックとしてos.walk()を使用
        """
        self.logger.debug(f"Getting all files from {len(self.workspaces)} workspaces")

        # SQLiteインデックスが利用可能な場合
        if self.sqlite_indexer:
            self.logger.debug("Using SQLite indexer for get_all_files()")
            try:
                # 拡張子リストを正規化（セットからリストに変換）
                ext_list = list(extensions) if extensions and isinstance(extensions, set) else extensions

                # SQLiteから全ファイルを取得
                files = self.sqlite_indexer.get_all_entries(entry_type='file', extensions=ext_list)

                self.logger.debug(f"Total files found (SQLite): {len(files)}")
                return files

            except Exception as e:
                self.logger.warning(f"SQLite indexer error, falling back to os.walk(): {e}")

        # フォールバック: 従来のos.walk()方式
        self.logger.debug("Using fallback os.walk() for get_all_files()")
        return self._get_all_files_fallback(extensions)

    def _get_all_files_fallback(self, extensions: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        os.walk()を使用したフォールバック実装（従来の実装）
        """
        files = []

        # Default extensions for programming files
        if extensions is None:
            extensions = {
                # Programming languages (highest priority)
                '.py', '.cpp', '.c', '.h', '.hpp', '.cxx', '.hxx',
                '.cs', '.java', '.js', '.ts', '.jsx', '.tsx',
                '.go', '.rs', '.php', '.rb', '.swift', '.kt',

                # Unreal Engine files
                '.uproject', '.uplugin', '.uasset', '.umap', '.ucpp',
                '.build', '.target', '.ini', '.cfg', '.config',

                # Config and data files
                '.json', '.yaml', '.yml', '.xml', '.toml',
                '.ini', '.conf', '.csv', '.txt', '.md', '.rst',

                # Build files
                '.cmake', '.make', '.gradle', '.sln', '.vcxproj',
                '.pro', '.pri', '.qmake',

                # Shaders
                '.hlsl', '.glsl', '.shader', '.cginc', '.compute',

                # Image files (lower priority for autocomplete)
                '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif',
                '.webp', '.svg', '.ico', '.psd', '.ai', '.eps',

                # Audio files (lower priority for autocomplete)
                '.wav', '.mp3', '.flac', '.aac', '.ogg', '.wma',
                '.m4a', '.opus', '.aiff', '.au',

                # Video files (lower priority for autocomplete)
                '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv',
                '.webm', '.m4v', '.3gp', '.ogv'
            }

        for workspace in self.workspaces:
            workspace_path = workspace['path']
            self.logger.debug(f"Processing workspace: {workspace['name']} at {workspace_path}")

            if not os.path.exists(workspace_path):
                self.logger.warning(f"Workspace path does not exist: {workspace_path}")
                continue

            workspace_file_count = 0
            for root, dirs, file_list in os.walk(workspace_path):
                # Exclude hidden directories and build/cache directories (but allow .claude)
                dirs[:] = [d for d in dirs if (not d.startswith('.') or d == '.claude') and d not in [
                    'node_modules', '__pycache__', 'Binaries', 'Intermediate',
                    'Saved', 'DerivedDataCache', '.vs', 'obj', 'bin'
                ]]

                for file in file_list:
                    if file.startswith('.'):
                        continue

                    file_path = os.path.join(root, file)

                    try:
                        relative_path = os.path.relpath(file_path, workspace_path)
                    except (ValueError, OSError) as e:
                        # 特殊パスエラーをスキップ
                        self.logger.debug(f"Skipping file with invalid path: {file_path} ({e})")
                        continue

                    # Extension filter
                    file_ext = os.path.splitext(file)[1].lower()

                    # Always include certain important files regardless of extension
                    important_files = {
                        'readme', 'license', 'changelog', 'makefile', 'dockerfile',
                        'cmakelist', 'cmakelists', 'requirements', 'package',
                        'gulpfile', 'gruntfile', 'webpack', 'tsconfig', 'jsconfig'
                    }

                    file_name_lower = file.lower()
                    is_important = any(important in file_name_lower for important in important_files)

                    if file_ext in extensions or is_important:
                        files.append({
                            'name': file,
                            'path': file_path,
                            'relative_path': relative_path,
                            'workspace': workspace['name']
                        })
                        workspace_file_count += 1

            self.logger.debug(f"Found {workspace_file_count} files in workspace {workspace['name']}")

        self.logger.debug(f"Total files found (fallback): {len(files)}")
        return files
    
    def search_files(self, query: str, extensions: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        ファイル名で検索

        SQLiteインデックスが利用可能な場合はそれを使用し、
        そうでない場合はフォールバックとして全ファイル取得→フィルタリングを使用
        """
        self.logger.debug(f"Searching files with query: {query}")

        # SQLiteインデックスが利用可能な場合
        if self.sqlite_indexer:
            self.logger.debug("Using SQLite indexer for search_files()")
            try:
                # SQLiteの検索機能を使用
                from src.core.sqlite_indexer import FileEntry

                # search_by_prefix()はFileEntryのリストを返すため、辞書に変換
                search_results = self.sqlite_indexer.search_by_prefix(query, max_results=100)

                # FileEntryから辞書形式に変換し、ファイルのみフィルタ
                results = []
                for entry in search_results:
                    if entry.type == 'file':
                        results.append({
                            'name': entry.name,
                            'path': entry.path,
                            'relative_path': entry.relative_path,
                            'workspace': entry.workspace
                        })

                self.logger.debug(f"Found {len(results)} matching files (SQLite)")
                return results

            except Exception as e:
                self.logger.warning(f"SQLite indexer search error, falling back: {e}")

        # フォールバック: 従来の全ファイル取得→フィルタリング方式
        self.logger.debug("Using fallback search for search_files()")
        return self._search_files_fallback(query, extensions)

    def _search_files_fallback(self, query: str, extensions: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        従来の検索実装（全ファイル取得→フィルタリング）
        """
        all_files = self._get_all_files_fallback(extensions)
        self.logger.debug(f"Searching in {len(all_files)} files (fallback)")

        query_lower = query.lower()

        results = []
        for file_info in all_files:
            file_name_lower = file_info['name'].lower()
            relative_path_lower = file_info['relative_path'].lower()

            if query_lower in file_name_lower or query_lower in relative_path_lower:
                results.append(file_info)
                self.logger.debug(f"File match: {file_info['name']} (workspace: {file_info['workspace']})")

        self.logger.debug(f"Found {len(results)} matching files (fallback)")
        return results
    
    def get_all_folders(self) -> List[Dict[str, str]]:
        """
        全ワークスペースから全フォルダを取得

        SQLiteインデックスが利用可能な場合はそれを使用し、
        そうでない場合はフォールバックとしてos.walk()を使用
        """
        self.logger.debug(f"Getting all folders from {len(self.workspaces)} workspaces")

        # SQLiteインデックスが利用可能な場合
        if self.sqlite_indexer:
            self.logger.debug("Using SQLite indexer for get_all_folders()")
            try:
                # SQLiteから全フォルダを取得
                folders = self.sqlite_indexer.get_all_entries(entry_type='folder')

                self.logger.debug(f"Total folders found (SQLite): {len(folders)}")
                return folders

            except Exception as e:
                self.logger.warning(f"SQLite indexer error, falling back to os.walk(): {e}")

        # フォールバック: 従来のos.walk()方式
        self.logger.debug("Using fallback os.walk() for get_all_folders()")
        return self._get_all_folders_fallback()

    def _get_all_folders_fallback(self) -> List[Dict[str, str]]:
        """
        os.walk()を使用したフォルダ取得のフォールバック実装
        """
        folders = []

        for workspace in self.workspaces:
            workspace_path = workspace['path']
            self.logger.debug(f"Processing workspace folders: {workspace['name']} at {workspace_path}")

            if not os.path.exists(workspace_path):
                self.logger.warning(f"Workspace path does not exist: {workspace_path}")
                continue

            workspace_folder_count = 0
            for root, dirs, file_list in os.walk(workspace_path):
                # Exclude hidden directories and build/cache directories (but allow .claude)
                dirs[:] = [d for d in dirs if (not d.startswith('.') or d == '.claude') and d not in [
                    'node_modules', '__pycache__', 'Binaries', 'Intermediate',
                    'Saved', 'DerivedDataCache', '.vs', 'obj', 'bin'
                ]]

                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)

                    try:
                        relative_path = os.path.relpath(dir_path, workspace_path)
                    except (ValueError, OSError) as e:
                        # 特殊パスエラーをスキップ
                        self.logger.debug(f"Skipping folder with invalid path: {dir_path} ({e})")
                        continue

                    folders.append({
                        'name': dir_name,
                        'path': dir_path,
                        'relative_path': relative_path,
                        'workspace': workspace['name'],
                        'type': 'folder'
                    })
                    workspace_folder_count += 1

            self.logger.debug(f"Found {workspace_folder_count} folders in workspace {workspace['name']}")

        self.logger.debug(f"Total folders found (fallback): {len(folders)}")
        return folders
    
    def search_folders(self, query: str) -> List[Dict[str, str]]:
        """
        フォルダ名で検索

        SQLiteインデックスが利用可能な場合はそれを使用し、
        そうでない場合はフォールバックとして全フォルダ取得→フィルタリングを使用
        """
        self.logger.debug(f"Searching folders with query: {query}")

        # SQLiteインデックスが利用可能な場合
        if self.sqlite_indexer:
            self.logger.debug("Using SQLite indexer for search_folders()")
            try:
                # SQLiteの検索機能を使用
                from src.core.sqlite_indexer import FileEntry

                # search_by_prefix()はFileEntryのリストを返すため、辞書に変換
                search_results = self.sqlite_indexer.search_by_prefix(query, max_results=100)

                # FileEntryから辞書形式に変換し、フォルダのみフィルタ
                results = []
                for entry in search_results:
                    if entry.type == 'folder':
                        results.append({
                            'name': entry.name,
                            'path': entry.path,
                            'relative_path': entry.relative_path,
                            'workspace': entry.workspace,
                            'type': 'folder'
                        })

                self.logger.debug(f"Found {len(results)} matching folders (SQLite)")
                return results

            except Exception as e:
                self.logger.warning(f"SQLite indexer search error, falling back: {e}")

        # フォールバック: 従来の全フォルダ取得→フィルタリング方式
        self.logger.debug("Using fallback search for search_folders()")
        return self._search_folders_fallback(query)

    def _search_folders_fallback(self, query: str) -> List[Dict[str, str]]:
        """
        従来のフォルダ検索実装（全フォルダ取得→フィルタリング）
        """
        all_folders = self._get_all_folders_fallback()
        self.logger.debug(f"Searching in {len(all_folders)} folders (fallback)")

        query_lower = query.lower()

        results = []
        for folder_info in all_folders:
            folder_name_lower = folder_info['name'].lower()
            relative_path_lower = folder_info['relative_path'].lower()

            if query_lower in folder_name_lower or query_lower in relative_path_lower:
                results.append(folder_info)
                self.logger.debug(f"Folder match: {folder_info['name']} (workspace: {folder_info['workspace']})")

        self.logger.debug(f"Found {len(results)} matching folders (fallback)")
        return results
    
    def search_files_and_folders(self, query: str, extensions: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        ファイルとフォルダを両方検索

        SQLiteインデックスが利用可能な場合は1回のクエリで両方取得し、
        そうでない場合はフォールバックとして個別検索
        """
        self.logger.debug(f"Searching files and folders with query: '{query}'")

        # SQLiteインデックスが利用可能な場合
        if self.sqlite_indexer:
            self.logger.debug("Using SQLite indexer for search_files_and_folders()")
            try:
                # SQLiteの検索機能を使用（1回のクエリで両方取得）
                from src.core.sqlite_indexer import FileEntry

                search_results = self.sqlite_indexer.search_by_prefix(query, max_results=100)

                # FileEntryから辞書形式に変換
                all_results = []
                for entry in search_results:
                    all_results.append({
                        'name': entry.name,
                        'path': entry.path,
                        'relative_path': entry.relative_path,
                        'workspace': entry.workspace,
                        'type': entry.type
                    })

                files_count = sum(1 for r in all_results if r['type'] == 'file')
                folders_count = sum(1 for r in all_results if r['type'] == 'folder')

                self.logger.debug(f"Combined search found {files_count} files and {folders_count} folders (SQLite)")
                return all_results

            except Exception as e:
                self.logger.warning(f"SQLite indexer search error, falling back: {e}")

        # フォールバック: 従来の個別検索方式
        self.logger.debug("Using fallback search for search_files_and_folders()")
        files = self._search_files_fallback(query, extensions)
        folders = self._search_folders_fallback(query)

        # Add type information to files
        for file_info in files:
            file_info['type'] = 'file'

        # Combine results
        all_results = files + folders

        self.logger.debug(f"Combined search found {len(files)} files and {len(folders)} folders (fallback)")
        return all_results