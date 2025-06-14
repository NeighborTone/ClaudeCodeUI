# -*- coding: utf-8 -*-
"""
Test module for workspace_manager.py
"""
import unittest
import os
import tempfile
import json
from test_config import BaseTestCase

class TestWorkspaceManager(BaseTestCase):
    """Test WorkspaceManager class"""
    
    def setUp(self):
        super().setUp()
        # Create temporary workspace and config
        self.temp_workspace_dir = tempfile.mkdtemp()
        self.temp_config_dir = tempfile.mkdtemp()
        self.temp_config_file = os.path.join(self.temp_config_dir, 'workspace.json')
        
        # Create test files and directories
        self.create_test_workspace()
        
        from core.workspace_manager import WorkspaceManager
        self.workspace_manager_class = WorkspaceManager
    
    def tearDown(self):
        super().tearDown()
        # Clean up temp files and directories
        import shutil
        if os.path.exists(self.temp_workspace_dir):
            shutil.rmtree(self.temp_workspace_dir)
        if os.path.exists(self.temp_config_dir):
            shutil.rmtree(self.temp_config_dir)
    
    def create_test_workspace(self):
        """Create a test workspace with various files"""
        # Create directory structure
        dirs = [
            'src',
            'src/components',
            'tests',
            'config',
            'docs',
            'node_modules',  # Should be ignored
            '__pycache__'    # Should be ignored
        ]
        
        for dir_path in dirs:
            os.makedirs(os.path.join(self.temp_workspace_dir, dir_path), exist_ok=True)
        
        # Create test files
        files = [
            'main.py',
            'requirements.txt',
            'README.md',
            'src/app.py',
            'src/utils.py',
            'src/components/button.py',
            'tests/test_app.py',
            'config/settings.json',
            'docs/guide.md',
            'node_modules/package.js',  # Should be ignored
            '__pycache__/cache.pyc'     # Should be ignored
        ]
        
        for file_path in files:
            full_path = os.path.join(self.temp_workspace_dir, file_path)
            with open(full_path, 'w') as f:
                f.write(f'# Content of {file_path}')
    
    def test_initialization(self):
        """Test WorkspaceManager initialization"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        self.assertIsInstance(manager.workspaces, list)
        self.assertEqual(len(manager.workspaces), 0)  # Initially empty
    
    def test_add_workspace(self):
        """Test adding workspace"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        
        # Add workspace
        success = manager.add_workspace(self.temp_workspace_dir)
        self.assertTrue(success)
        
        # Check workspace was added
        workspaces = manager.get_workspaces()
        self.assertEqual(len(workspaces), 1)
        self.assertEqual(workspaces[0]['path'], self.temp_workspace_dir)
        self.assertIn('name', workspaces[0])
    
    def test_add_duplicate_workspace(self):
        """Test adding duplicate workspace"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        
        # Add workspace twice
        success1 = manager.add_workspace(self.temp_workspace_dir)
        success2 = manager.add_workspace(self.temp_workspace_dir)
        
        self.assertTrue(success1)
        self.assertFalse(success2)  # Should reject duplicate
        
        # Should still have only one workspace
        workspaces = manager.get_workspaces()
        self.assertEqual(len(workspaces), 1)
    
    def test_add_nonexistent_workspace(self):
        """Test adding non-existent workspace"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        
        nonexistent_path = '/nonexistent/path'
        success = manager.add_workspace(nonexistent_path)
        self.assertFalse(success)
        
        workspaces = manager.get_workspaces()
        self.assertEqual(len(workspaces), 0)
    
    def test_remove_workspace(self):
        """Test removing workspace"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        
        # Add then remove workspace
        manager.add_workspace(self.temp_workspace_dir)
        success = manager.remove_workspace(self.temp_workspace_dir)
        self.assertTrue(success)
        
        workspaces = manager.get_workspaces()
        self.assertEqual(len(workspaces), 0)
    
    def test_remove_nonexistent_workspace(self):
        """Test removing non-existent workspace"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        
        success = manager.remove_workspace('/nonexistent/path')
        self.assertFalse(success)
    
    def test_get_workspace_files(self):
        """Test getting workspace files"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        manager.add_workspace(self.temp_workspace_dir)
        
        files = manager.get_workspace_files(self.temp_workspace_dir)
        self.assertIsInstance(files, list)
        self.assertGreater(len(files), 0)
        
        # Check that some expected files are present
        file_names = [os.path.basename(f) for f in files]
        self.assertIn('main.py', file_names)
        self.assertIn('requirements.txt', file_names)
        self.assertIn('README.md', file_names)
        
        # Check that ignored files are not present
        self.assertNotIn('cache.pyc', file_names)
        self.assertNotIn('package.js', file_names)
    
    def test_get_all_workspace_files(self):
        """Test getting all workspace files"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        manager.add_workspace(self.temp_workspace_dir)
        
        all_files = manager.get_all_workspace_files()
        self.assertIsInstance(all_files, list)
        self.assertGreater(len(all_files), 0)
        
        # Should include files from the workspace
        file_paths = [f['path'] for f in all_files]
        main_py_path = os.path.join(self.temp_workspace_dir, 'main.py')
        self.assertIn(main_py_path, file_paths)
    
    def test_is_file_in_workspace(self):
        """Test file in workspace check"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        manager.add_workspace(self.temp_workspace_dir)
        
        # Test file in workspace
        test_file = os.path.join(self.temp_workspace_dir, 'main.py')
        self.assertTrue(manager.is_file_in_workspace(test_file))
        
        # Test file not in workspace
        external_file = '/some/other/file.py'
        self.assertFalse(manager.is_file_in_workspace(external_file))
    
    def test_get_workspace_for_file(self):
        """Test getting workspace for file"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        manager.add_workspace(self.temp_workspace_dir)
        
        # Test file in workspace
        test_file = os.path.join(self.temp_workspace_dir, 'src', 'app.py')
        workspace = manager.get_workspace_for_file(test_file)
        self.assertIsNotNone(workspace)
        self.assertEqual(workspace['path'], self.temp_workspace_dir)
        
        # Test file not in workspace
        external_file = '/some/other/file.py'
        workspace = manager.get_workspace_for_file(external_file)
        self.assertIsNone(workspace)
    
    def test_save_load_workspaces(self):
        """Test workspace persistence"""
        # Create manager and add workspace
        manager1 = self.workspace_manager_class(config_file=self.temp_config_file)
        manager1.add_workspace(self.temp_workspace_dir)
        manager1.save_workspaces()
        
        # Create new manager (should load saved workspaces)
        manager2 = self.workspace_manager_class(config_file=self.temp_config_file)
        workspaces = manager2.get_workspaces()
        
        self.assertEqual(len(workspaces), 1)
        self.assertEqual(workspaces[0]['path'], self.temp_workspace_dir)
    
    def test_file_filtering(self):
        """Test file filtering functionality"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        manager.add_workspace(self.temp_workspace_dir)
        
        files = manager.get_workspace_files(self.temp_workspace_dir)
        
        # Check supported extensions are included
        supported_files = [f for f in files if f.endswith(('.py', '.md', '.txt', '.json'))]
        self.assertGreater(len(supported_files), 0)
        
        # Check that all returned files have supported extensions
        for file_path in files:
            ext = os.path.splitext(file_path)[1].lower()
            self.assertIn(ext, manager.SUPPORTED_EXTENSIONS)
    
    def test_directory_exclusion(self):
        """Test directory exclusion"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        manager.add_workspace(self.temp_workspace_dir)
        
        files = manager.get_workspace_files(self.temp_workspace_dir)
        
        # Check that excluded directories are not included
        for file_path in files:
            self.assertNotIn('node_modules', file_path)
            self.assertNotIn('__pycache__', file_path)
    
    def test_relative_path_calculation(self):
        """Test relative path calculation"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        manager.add_workspace(self.temp_workspace_dir)
        
        all_files = manager.get_all_workspace_files()
        
        for file_info in all_files:
            self.assertIn('path', file_info)
            self.assertIn('relative_path', file_info)
            self.assertIn('workspace', file_info)
            
            # Relative path should not start with /
            self.assertFalse(file_info['relative_path'].startswith('/'))
            
            # Relative path should be shorter than absolute path
            self.assertLess(len(file_info['relative_path']), len(file_info['path']))
    
    def test_workspace_name_generation(self):
        """Test workspace name generation"""
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        manager.add_workspace(self.temp_workspace_dir)
        
        workspaces = manager.get_workspaces()
        workspace = workspaces[0]
        
        # Name should be the directory name
        expected_name = os.path.basename(self.temp_workspace_dir)
        self.assertEqual(workspace['name'], expected_name)
    
    def test_invalid_config_file_handling(self):
        """Test handling of invalid config files"""
        # Create invalid JSON config
        with open(self.temp_config_file, 'w') as f:
            f.write('invalid json {')
        
        # Should gracefully handle invalid config
        manager = self.workspace_manager_class(config_file=self.temp_config_file)
        self.assertEqual(len(manager.get_workspaces()), 0)
    
    def test_multiple_workspaces(self):
        """Test handling multiple workspaces"""
        # Create second workspace
        second_workspace = tempfile.mkdtemp()
        os.makedirs(os.path.join(second_workspace, 'src'))
        with open(os.path.join(second_workspace, 'app.py'), 'w') as f:
            f.write('# Second workspace')
        
        try:
            manager = self.workspace_manager_class(config_file=self.temp_config_file)
            manager.add_workspace(self.temp_workspace_dir)
            manager.add_workspace(second_workspace)
            
            workspaces = manager.get_workspaces()
            self.assertEqual(len(workspaces), 2)
            
            all_files = manager.get_all_workspace_files()
            # Should have files from both workspaces
            workspace_paths = set(f['workspace'] for f in all_files)
            self.assertEqual(len(workspace_paths), 2)
            
        finally:
            import shutil
            if os.path.exists(second_workspace):
                shutil.rmtree(second_workspace)

if __name__ == '__main__':
    unittest.main()