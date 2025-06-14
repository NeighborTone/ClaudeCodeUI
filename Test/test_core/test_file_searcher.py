# -*- coding: utf-8 -*-
"""
Test module for file_searcher.py
"""
import unittest
import os
import tempfile
from unittest.mock import Mock
from test_config import BaseTestCase

class TestFileSearcher(BaseTestCase):
    """Test FileSearcher class"""
    
    def setUp(self):
        super().setUp()
        # Create temporary workspace with test files
        self.temp_workspace_dir = tempfile.mkdtemp()
        self.create_test_files()
        
        # Create mock workspace manager
        self.mock_workspace_manager = Mock()
        self.setup_mock_workspace_manager()
        
        from core.file_searcher import FileSearcher
        self.file_searcher = FileSearcher(self.mock_workspace_manager)
    
    def tearDown(self):
        super().tearDown()
        import shutil
        if os.path.exists(self.temp_workspace_dir):
            shutil.rmtree(self.temp_workspace_dir)
    
    def create_test_files(self):
        """Create test files for searching"""
        files = [
            'main.py',
            'app.py',
            'utils.py',
            'config.json',
            'README.md',
            'test_app.py',
            'component.tsx',
            'style.css',
            'index.html',
            'package.json',
            'src/core.py',
            'src/helper.py',
            'tests/test_main.py',
            'docs/guide.md',
            'scripts/build.sh'
        ]
        
        for file_path in files:
            full_path = os.path.join(self.temp_workspace_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(f'# Content of {file_path}')
    
    def setup_mock_workspace_manager(self):
        """Setup mock workspace manager with test data"""
        # Mock workspace data
        workspace_data = {
            'path': self.temp_workspace_dir,
            'name': 'test_workspace'
        }
        
        # Mock file data
        files_data = []
        for root, dirs, files in os.walk(self.temp_workspace_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.temp_workspace_dir)
                files_data.append({
                    'path': full_path,
                    'relative_path': rel_path,
                    'workspace': self.temp_workspace_dir,
                    'name': file
                })
        
        self.mock_workspace_manager.get_all_workspace_files.return_value = files_data
        self.mock_workspace_manager.get_workspaces.return_value = [workspace_data]
    
    def test_initialization(self):
        """Test FileSearcher initialization"""
        self.assertIsNotNone(self.file_searcher.workspace_manager)
        self.assertEqual(self.file_searcher.workspace_manager, self.mock_workspace_manager)
    
    def test_search_files_by_name_exact_match(self):
        """Test exact filename matching"""
        results = self.file_searcher.search_files_by_name('main.py')
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # Should find exact match
        found_main = any(r['name'] == 'main.py' for r in results)
        self.assertTrue(found_main)
        
        # Check result structure
        for result in results:
            self.assertIn('name', result)
            self.assertIn('path', result)
            self.assertIn('workspace', result)
            self.assertIn('relative_path', result)
    
    def test_search_files_by_name_partial_match(self):
        """Test partial filename matching"""
        results = self.file_searcher.search_files_by_name('app')
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # Should find files containing 'app'
        app_files = [r for r in results if 'app' in r['name'].lower()]
        self.assertGreater(len(app_files), 0)
    
    def test_search_files_by_name_case_insensitive(self):
        """Test case insensitive search"""
        results_lower = self.file_searcher.search_files_by_name('main')
        results_upper = self.file_searcher.search_files_by_name('MAIN')
        results_mixed = self.file_searcher.search_files_by_name('Main')
        
        # Should return same results regardless of case
        self.assertEqual(len(results_lower), len(results_upper))
        self.assertEqual(len(results_lower), len(results_mixed))
    
    def test_search_files_by_name_no_results(self):
        """Test search with no results"""
        results = self.file_searcher.search_files_by_name('nonexistent_file_xyz')
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)
    
    def test_search_files_by_name_empty_query(self):
        """Test search with empty query"""
        results = self.file_searcher.search_files_by_name('')
        self.assertIsInstance(results, list)
        # Empty query should return no results or all results depending on implementation
        # The current implementation should return no results for empty query
    
    def test_search_files_by_name_extension_matching(self):
        """Test search by file extension"""
        # Search for Python files
        py_results = self.file_searcher.search_files_by_name('.py')
        py_files = [r for r in py_results if r['name'].endswith('.py')]
        self.assertGreater(len(py_files), 0)
        
        # Search for JSON files
        json_results = self.file_searcher.search_files_by_name('.json')
        json_files = [r for r in json_results if r['name'].endswith('.json')]
        self.assertGreater(len(json_files), 0)
    
    def test_search_files_by_name_path_matching(self):
        """Test search including path components"""
        # Search for files in src directory
        src_results = self.file_searcher.search_files_by_name('src')
        
        # Should find files that have 'src' in their path
        src_files = [r for r in src_results if 'src' in r['relative_path']]
        self.assertGreater(len(src_files), 0)
    
    def test_search_result_relevance_scoring(self):
        """Test search result relevance scoring"""
        # Search for 'test' which should match multiple files
        results = self.file_searcher.search_files_by_name('test')
        
        if len(results) > 1:
            # Results should be sorted by relevance
            # Exact filename matches should come first
            exact_matches = [r for r in results if r['name'].lower() == 'test']
            if exact_matches:
                # Exact match should be first
                self.assertEqual(results[0]['name'].lower(), 'test')
    
    def test_search_result_workspace_info(self):
        """Test workspace information in search results"""
        results = self.file_searcher.search_files_by_name('main')
        
        for result in results:
            self.assertIn('workspace', result)
            self.assertEqual(result['workspace'], self.temp_workspace_dir)
            
            # Path should be absolute
            self.assertTrue(os.path.isabs(result['path']))
            
            # Relative path should not be absolute
            self.assertFalse(os.path.isabs(result['relative_path']))
    
    def test_search_files_by_content_basic(self):
        """Test basic content search functionality"""
        # Add some content to test files
        test_file = os.path.join(self.temp_workspace_dir, 'test_content.py')
        with open(test_file, 'w') as f:
            f.write('def test_function():\n    return "hello world"')
        
        # Update mock to include the new file
        self.setup_mock_workspace_manager()
        
        results = self.file_searcher.search_files_by_content('test_function')
        
        # Should find files containing the search term
        self.assertIsInstance(results, list)
    
    def test_search_performance(self):
        """Test search performance with reasonable response time"""
        import time
        
        start_time = time.time()
        results = self.file_searcher.search_files_by_name('main')
        end_time = time.time()
        
        # Search should complete within reasonable time (1 second for small dataset)
        search_time = end_time - start_time
        self.assertLess(search_time, 1.0)
    
    def test_search_with_special_characters(self):
        """Test search with special characters in filename"""
        # Create file with special characters
        special_file = os.path.join(self.temp_workspace_dir, 'test-file_123.py')
        with open(special_file, 'w') as f:
            f.write('# Special file')
        
        self.setup_mock_workspace_manager()
        
        # Search for parts of the filename
        results = self.file_searcher.search_files_by_name('test-file')
        found = any(r['name'] == 'test-file_123.py' for r in results)
        self.assertTrue(found)
    
    def test_search_result_limit(self):
        """Test search result limiting"""
        # Search for common term that might return many results
        results = self.file_searcher.search_files_by_name('.')  # Should match many files
        
        # Should have reasonable limit on results
        self.assertLessEqual(len(results), 50)  # Assuming reasonable limit
    
    def test_search_with_no_workspaces(self):
        """Test search when no workspaces are available"""
        # Create searcher with empty workspace manager
        empty_mock = Mock()
        empty_mock.get_all_workspace_files.return_value = []
        empty_mock.get_workspaces.return_value = []
        
        from core.file_searcher import FileSearcher
        empty_searcher = FileSearcher(empty_mock)
        
        results = empty_searcher.search_files_by_name('main')
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)
    
    def test_search_unicode_handling(self):
        """Test search with unicode characters"""
        # Create file with unicode characters
        unicode_file = os.path.join(self.temp_workspace_dir, 'テスト.py')
        try:
            with open(unicode_file, 'w', encoding='utf-8') as f:
                f.write('# Unicode test file')
            
            self.setup_mock_workspace_manager()
            
            # Search for unicode filename
            results = self.file_searcher.search_files_by_name('テスト')
            
            self.assertIsInstance(results, list)
            # Should handle unicode without errors
            
        except UnicodeError:
            # If unicode not supported in filesystem, that's ok
            pass

if __name__ == '__main__':
    unittest.main()