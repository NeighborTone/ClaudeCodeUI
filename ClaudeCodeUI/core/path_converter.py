# -*- coding: utf-8 -*-
"""
Path Converter - Windows/WSL path conversion utility
"""
import os
import re
from typing import Optional


class PathConverter:
    """Path conversion utility for Windows/WSL compatibility"""
    
    @staticmethod
    def is_wsl_environment() -> bool:
        """Check if running in WSL environment"""
        # Check for WSL-specific environment variables
        return 'WSL_DISTRO_NAME' in os.environ or 'WSL_INTEROP' in os.environ
    
    @staticmethod
    def windows_to_wsl(path: str) -> str:
        """
        Convert Windows path to WSL path format.
        
        Examples:
            C:\\Users\\owner\\file.txt -> /mnt/c/Users/owner/file.txt
            D:\\Projects\\code -> /mnt/d/Projects/code
        """
        # Already in WSL format
        if path.startswith('/mnt/'):
            return path
        
        # Match Windows absolute path pattern
        match = re.match(r'^([A-Za-z]):[\\\/](.*)$', path)
        if match:
            drive_letter = match.group(1).lower()
            path_part = match.group(2)
            # Convert backslashes to forward slashes
            path_part = path_part.replace('\\', '/')
            return f'/mnt/{drive_letter}/{path_part}'
        
        # For relative paths or already Unix-style paths, just convert backslashes
        return path.replace('\\', '/')
    
    @staticmethod
    def wsl_to_windows(path: str) -> str:
        """
        Convert WSL path to Windows path format.
        
        Examples:
            /mnt/c/Users/owner/file.txt -> C:\\Users\\owner\\file.txt
            /mnt/d/Projects/code -> D:\\Projects\\code
        """
        # Match WSL mount point pattern
        match = re.match(r'^/mnt/([a-z])/(.*)$', path)
        if match:
            drive_letter = match.group(1).upper()
            path_part = match.group(2)
            # Convert forward slashes to backslashes
            path_part = path_part.replace('/', '\\')
            return f'{drive_letter}:\\{path_part}'
        
        # For non-WSL paths, return as-is with forward slashes
        return path
    
    @staticmethod
    def convert_path(path: str, mode: str) -> str:
        """
        Convert path based on the specified mode.
        
        Args:
            path: The path to convert
            mode: 'wsl' or 'windows'
            
        Returns:
            Converted path string (always with forward slashes)
        """
        if mode == 'wsl':
            return PathConverter.windows_to_wsl(path)
        elif mode == 'windows':
            # Windows mode: always use forward slashes for Claude Code compatibility
            return path.replace('\\', '/')
        else:
            # Default to just converting backslashes to forward slashes
            return path.replace('\\', '/')
    
    @staticmethod
    def get_default_mode() -> str:
        """Get the default path mode based on the environment"""
        return 'wsl' if PathConverter.is_wsl_environment() else 'windows'