# -*- coding: utf-8 -*-
"""
Indexing Adapter - SQLite-based indexing system
"""
import os
from typing import List, Dict, Any, Optional
from PySide6.QtCore import QObject, Signal

from src.core.settings import SettingsManager
from src.core.sqlite_indexer import SQLiteIndexer
from src.core.sqlite_indexing_worker import SQLiteIndexingManager
from src.core.fast_sqlite_searcher import FastSQLiteSearcher


class IndexingAdapter(QObject):
    """
    SQLite-based indexing system adapter
    """
    
    # Signal definitions
    indexing_started = Signal()
    indexing_progress = Signal(float, str)
    indexing_completed = Signal(dict)
    indexing_failed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.settings_manager = SettingsManager()
        
        # Initialize SQLite system only
        from src.core.logger import logger
        logger.info("Initializing SQLite indexing system")
        self.indexing_manager = SQLiteIndexingManager(self)
        self.searcher = FastSQLiteSearcher(self.indexing_manager.get_indexer())
        
        # Connect signals
        self.indexing_manager.indexing_started.connect(self.indexing_started)
        self.indexing_manager.indexing_progress.connect(self.indexing_progress)
        self.indexing_manager.indexing_completed.connect(self.indexing_completed)
        self.indexing_manager.indexing_failed.connect(self.indexing_failed)
    
    def get_indexer(self):
        """Get the active indexer"""
        return self.indexing_manager.get_indexer()
    
    def get_searcher(self):
        """Get the active search system"""
        return self.searcher
    
    def is_indexing(self) -> bool:
        """Check if indexing is in progress"""
        return self.indexing_manager.is_indexing()
    
    def start_indexing(self, workspaces: List[Dict[str, str]], rebuild_all: bool = False) -> bool:
        """Start indexing"""
        return self.indexing_manager.start_indexing(workspaces, rebuild_all)
    
    def start_smart_indexing(self, workspaces: List[Dict[str, str]]) -> bool:
        """Start indexing only if needed"""
        return self.indexing_manager.start_smart_indexing(workspaces)
    
    def check_indexing_needed(self, workspaces: List[Dict[str, str]]) -> bool:
        """Check if indexing is needed"""
        return self.indexing_manager.check_indexing_needed(workspaces)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics"""
        stats = self.indexing_manager.get_stats()
        stats['system_type'] = 'SQLite'
        return stats
    
    def clear_index(self):
        """Clear the index"""
        if hasattr(self.indexing_manager, 'clear_index'):
            self.indexing_manager.clear_index()
    
    def force_rebuild(self, workspaces: List[Dict[str, str]]) -> bool:
        """Force rebuild the index"""
        if hasattr(self.indexing_manager, 'force_rebuild'):
            return self.indexing_manager.force_rebuild(workspaces)
        else:
            return self.start_indexing(workspaces, rebuild_all=True)
    
    def close(self):
        """Clean up resources"""
        if hasattr(self.indexing_manager, 'close'):
            self.indexing_manager.close()


class AdaptiveFileSearcher:
    """
    SQLite-based file search system adapter
    Maintains the existing FastFileSearcher interface for compatibility
    """
    
    def __init__(self, indexing_adapter: IndexingAdapter):
        self.indexing_adapter = indexing_adapter
        self.searcher = indexing_adapter.get_searcher()
    
    def extract_file_mentions(self, text: str) -> List:
        """Extract @filename mentions from text"""
        return self.searcher.extract_file_mentions(text)
    
    def search_files_by_name(self, query: str) -> List[Dict[str, str]]:
        """Search for files/folders by name"""
        return self.searcher.search_files_by_name(query)
    
    def search_files_only_by_name(self, query: str) -> List[Dict[str, str]]:
        """Search for files only by name (for ! pattern)"""
        return self.searcher.search_files_only_by_name(query)
    
    def search_folders_only_by_name(self, query: str) -> List[Dict[str, str]]:
        """Search for folders only by name (for # pattern)"""
        return self.searcher.search_folders_only_by_name(query)
    
    def get_file_content_preview(self, file_path: str, max_lines: int = 10) -> str:
        """Get file content preview"""
        return self.searcher.get_file_content_preview(file_path, max_lines)
    
    def resolve_file_mentions(self, text: str) -> Dict[str, List[Dict[str, str]]]:
        """Resolve all @filename mentions in text"""
        return self.searcher.resolve_file_mentions(text)
    
    def replace_file_mentions_with_content(self, text: str, selected_files: Dict[str, str]) -> str:
        """Replace @filename mentions with file content"""
        return self.searcher.replace_file_mentions_with_content(text, selected_files)
    
    def get_completion_suggestions(self, partial_filename: str) -> List[str]:
        """Get completion suggestions from partial filename"""
        return self.searcher.get_completion_suggestions(partial_filename)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get search statistics"""
        return self.searcher.get_stats()
    
    def get_quick_suggestions(self, partial_filename: str) -> List[Dict[str, str]]:
        """Get quick completion suggestions"""
        if hasattr(self.searcher, 'get_quick_suggestions'):
            return self.searcher.get_quick_suggestions(partial_filename)
        else:
            suggestions = self.get_completion_suggestions(partial_filename)
            return [{'name': name, 'display_name': name, 'type': 'file'} for name in suggestions]
    
    def set_max_results(self, max_results: int):
        """Set maximum results count"""
        if hasattr(self.searcher, 'set_max_results'):
            self.searcher.set_max_results(max_results)
    
    def clear_cache(self):
        """Clear search cache"""
        if hasattr(self.searcher, 'clear_cache'):
            self.searcher.clear_cache()


def create_indexing_system(parent=None) -> tuple:
    """
    Create appropriate indexing system
    Returns: (IndexingAdapter, AdaptiveFileSearcher)
    """
    indexing_adapter = IndexingAdapter(parent)
    file_searcher = AdaptiveFileSearcher(indexing_adapter)
    
    return indexing_adapter, file_searcher