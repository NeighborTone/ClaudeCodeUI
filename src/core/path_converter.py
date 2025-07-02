# -*- coding: utf-8 -*-
"""
Path Converter - Unified forward slash path formatting
"""


class PathConverter:
    """Path conversion utility for unified forward slash formatting"""
    
    @staticmethod
    def normalize_path(path: str) -> str:
        """
        Normalize path to use forward slashes only.
        
        Args:
            path: The path to normalize
            
        Returns:
            Path with forward slashes only
        """
        return path.replace('\\', '/')