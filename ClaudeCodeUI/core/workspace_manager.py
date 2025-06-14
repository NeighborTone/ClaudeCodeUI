# -*- coding: utf-8 -*-
"""
Workspace Manager - VSCode-like workspace functionality
"""
import os
import json
from typing import List, Dict, Optional
from pathlib import Path


class WorkspaceManager:
    """ワークスペース（プロジェクトフォルダ）の管理を行うクラス"""
    
    def __init__(self, config_file: str = "config/workspace.json"):
        self.config_file = config_file
        self.workspaces: List[Dict[str, str]] = []
        self.load_workspaces()
    
    def load_workspaces(self) -> None:
        """保存されたワークスペース情報を読み込み"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.workspaces = data.get('workspaces', [])
        except Exception as e:
            print(f"ワークスペース読み込みエラー: {e}")
            self.workspaces = []
    
    def save_workspaces(self) -> None:
        """ワークスペース情報を保存"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'workspaces': self.workspaces}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"ワークスペース保存エラー: {e}")
    
    def add_workspace(self, path: str, name: Optional[str] = None) -> bool:
        """ワークスペースを追加"""
        if not os.path.exists(path) or not os.path.isdir(path):
            return False
        
        path = os.path.abspath(path)
        
        # 既に存在するかチェック
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
        """ワークスペースを削除"""
        path = os.path.abspath(path)
        for i, workspace in enumerate(self.workspaces):
            if workspace['path'] == path:
                del self.workspaces[i]
                self.save_workspaces()
                return True
        return False
    
    def get_workspaces(self) -> List[Dict[str, str]]:
        """全ワークスペースを取得"""
        return self.workspaces.copy()
    
    def get_all_files(self, extensions: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """Get all files from all workspaces"""
        files = []
        
        print(f"WorkspaceManager.get_all_files called with {len(self.workspaces)} workspaces")
        
        # Default extensions for programming files
        if extensions is None:
            extensions = {
                # Programming languages
                '.py', '.cpp', '.c', '.h', '.hpp', '.cxx', '.hxx',
                '.cs', '.java', '.js', '.ts', '.jsx', '.tsx',
                '.go', '.rs', '.php', '.rb', '.swift', '.kt',
                
                # Unreal Engine files
                '.uproject', '.uplugin', '.uasset', '.umap', '.ucpp',
                '.build', '.target', '.ini', '.cfg', '.config',
                
                # Config and data files
                '.json', '.yaml', '.yml', '.xml', '.toml',
                '.csv', '.txt', '.md', '.rst',
                
                # Build files
                '.cmake', '.make', '.gradle', '.sln', '.vcxproj',
                '.pro', '.pri', '.qmake',
                
                # Shaders
                '.hlsl', '.glsl', '.shader', '.cginc', '.compute'
            }
        
        for workspace in self.workspaces:
            workspace_path = workspace['path']
            print(f"Processing workspace: {workspace['name']} at {workspace_path}")
            
            if not os.path.exists(workspace_path):
                print(f"Workspace path does not exist: {workspace_path}")
                continue
                
            workspace_file_count = 0
            for root, dirs, file_list in os.walk(workspace_path):
                # Exclude hidden directories and build/cache directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in [
                    'node_modules', '__pycache__', 'Binaries', 'Intermediate', 
                    'Saved', 'DerivedDataCache', '.vs', 'obj', 'bin'
                ]]
                
                for file in file_list:
                    if file.startswith('.'):
                        continue
                        
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, workspace_path)
                    
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
            
            print(f"Found {workspace_file_count} files in workspace {workspace['name']}")
        
        print(f"Total files found: {len(files)}")
        return files
    
    def search_files(self, query: str, extensions: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """Search files by name"""
        print(f"WorkspaceManager.search_files called with query: '{query}'")
        
        all_files = self.get_all_files(extensions)
        print(f"Got {len(all_files)} files to search in")
        
        query_lower = query.lower()
        
        results = []
        for file_info in all_files:
            file_name_lower = file_info['name'].lower()
            relative_path_lower = file_info['relative_path'].lower()
            
            if query_lower in file_name_lower or query_lower in relative_path_lower:
                results.append(file_info)
                print(f"  Match found: {file_info['name']} (workspace: {file_info['workspace']})")
        
        print(f"Found {len(results)} matching files")
        return results
    
    def get_all_folders(self) -> List[Dict[str, str]]:
        """Get all folders from all workspaces"""
        folders = []
        
        print(f"WorkspaceManager.get_all_folders called with {len(self.workspaces)} workspaces")
        
        for workspace in self.workspaces:
            workspace_path = workspace['path']
            print(f"Processing workspace folders: {workspace['name']} at {workspace_path}")
            
            if not os.path.exists(workspace_path):
                print(f"Workspace path does not exist: {workspace_path}")
                continue
                
            workspace_folder_count = 0
            for root, dirs, file_list in os.walk(workspace_path):
                # Exclude hidden directories and build/cache directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in [
                    'node_modules', '__pycache__', 'Binaries', 'Intermediate', 
                    'Saved', 'DerivedDataCache', '.vs', 'obj', 'bin'
                ]]
                
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    relative_path = os.path.relpath(dir_path, workspace_path)
                    
                    folders.append({
                        'name': dir_name,
                        'path': dir_path,
                        'relative_path': relative_path,
                        'workspace': workspace['name'],
                        'type': 'folder'
                    })
                    workspace_folder_count += 1
            
            print(f"Found {workspace_folder_count} folders in workspace {workspace['name']}")
        
        print(f"Total folders found: {len(folders)}")
        return folders
    
    def search_folders(self, query: str) -> List[Dict[str, str]]:
        """Search folders by name"""
        print(f"WorkspaceManager.search_folders called with query: '{query}'")
        
        all_folders = self.get_all_folders()
        print(f"Got {len(all_folders)} folders to search in")
        
        query_lower = query.lower()
        
        results = []
        for folder_info in all_folders:
            folder_name_lower = folder_info['name'].lower()
            relative_path_lower = folder_info['relative_path'].lower()
            
            if query_lower in folder_name_lower or query_lower in relative_path_lower:
                results.append(folder_info)
                print(f"  Folder match found: {folder_info['name']} (workspace: {folder_info['workspace']})")
        
        print(f"Found {len(results)} matching folders")
        return results
    
    def search_files_and_folders(self, query: str, extensions: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """Search both files and folders by name"""
        print(f"WorkspaceManager.search_files_and_folders called with query: '{query}'")
        
        # Get both files and folders
        files = self.search_files(query, extensions)
        folders = self.search_folders(query)
        
        # Add type information to files
        for file_info in files:
            file_info['type'] = 'file'
        
        # Combine results
        all_results = files + folders
        
        print(f"Combined search found {len(files)} files and {len(folders)} folders")
        return all_results