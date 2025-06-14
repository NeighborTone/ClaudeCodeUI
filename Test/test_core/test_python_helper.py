# -*- coding: utf-8 -*-
"""
Test module for python_helper.py
"""
import unittest
import os
import tempfile
from unittest.mock import patch, Mock
from test_config import BaseTestCase

class TestPythonHelper(BaseTestCase):
    """Test PythonHelper class"""
    
    def setUp(self):
        super().setUp()
        from core.python_helper import PythonHelper
        self.python_helper = PythonHelper
    
    def test_is_wsl_environment(self):
        """Test WSL environment detection"""
        result = self.python_helper.is_wsl_environment()
        self.assertIsInstance(result, bool)
        
        # Test with mock environment variables
        with patch.dict(os.environ, {'WSL_DISTRO_NAME': 'Ubuntu'}, clear=False):
            self.assertTrue(self.python_helper.is_wsl_environment())
        
        with patch.dict(os.environ, {'WSL_INTEROP': '/run/WSL/123'}, clear=False):
            self.assertTrue(self.python_helper.is_wsl_environment())
    
    def test_get_python_version(self):
        """Test Python version detection"""
        # Test with current Python executable
        import sys
        version = self.python_helper.get_python_version(sys.executable)
        self.assertIsNotNone(version)
        self.assertIn('Python', version)
        
        # Test with non-existent executable
        version = self.python_helper.get_python_version('/nonexistent/python')
        self.assertIsNone(version)
    
    @patch('shutil.which')
    def test_find_python_executables_mock(self, mock_which):
        """Test finding Python executables with mocking"""
        # Mock shutil.which to return test executables
        def mock_which_side_effect(name):
            if name == 'python3':
                return '/usr/bin/python3'
            elif name == 'python':
                return '/usr/bin/python'
            return None
        
        mock_which.side_effect = mock_which_side_effect
        
        with patch.object(self.python_helper, 'get_python_version') as mock_get_version:
            mock_get_version.return_value = 'Python 3.12.3'
            
            executables = self.python_helper.find_python_executables()
            self.assertIsInstance(executables, list)
            
            if executables:
                exe = executables[0]
                self.assertIn('path', exe)
                self.assertIn('version', exe)
                self.assertIn('type', exe)
                self.assertEqual(exe['type'], 'system')
    
    def test_find_python_executables_real(self):
        """Test finding Python executables in real environment"""
        executables = self.python_helper.find_python_executables()
        self.assertIsInstance(executables, list)
        
        # Should find at least current Python
        self.assertGreater(len(executables), 0)
        
        for exe in executables:
            self.assertIn('path', exe)
            self.assertIn('version', exe)
            self.assertIn('type', exe)
            self.assertIn(exe['type'], ['system', 'windows'])
    
    def test_get_recommended_python(self):
        """Test recommended Python selection"""
        recommended = self.python_helper.get_recommended_python()
        if recommended:  # May be None if no Python found
            self.assertIsInstance(recommended, str)
            self.assertTrue(os.path.exists(recommended) or recommended.endswith('.exe'))
    
    def test_create_run_script(self):
        """Test run script creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = os.path.join(temp_dir, 'test_script.py')
            
            # Create a test Python script
            with open(script_path, 'w') as f:
                f.write('print("Hello World")')
            
            # Create run script
            run_script_path = self.python_helper.create_run_script(script_path)
            
            # Verify run script was created
            self.assertTrue(os.path.exists(run_script_path))
            self.assertTrue(run_script_path.endswith('run.sh'))
            
            # Verify script content
            with open(run_script_path, 'r') as f:
                content = f.read()
                self.assertIn('#!/bin/bash', content)
                self.assertIn('test_script.py', content)
                self.assertIn(temp_dir, content)
            
            # Verify script is executable
            file_stat = os.stat(run_script_path)
            self.assertTrue(file_stat.st_mode & 0o111)  # Check execute permission
    
    def test_get_execution_instructions(self):
        """Test execution instructions generation"""
        instructions = self.python_helper.get_execution_instructions()
        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)
        
        # Should contain relevant sections
        if self.python_helper.is_wsl_environment():
            self.assertIn('WSL環境', instructions)
            self.assertIn('推奨実行方法', instructions)
        else:
            self.assertIn('Windows環境', instructions)
        
        self.assertIn('利用可能なPython実行環境', instructions)
    
    @patch.dict(os.environ, {'WSL_DISTRO_NAME': 'Ubuntu'}, clear=True)
    def test_wsl_specific_behavior(self):
        """Test WSL-specific behavior"""
        # Force WSL environment
        self.assertTrue(self.python_helper.is_wsl_environment())
        
        # Test default mode
        from core.path_converter import PathConverter
        default_mode = PathConverter.get_default_mode()
        self.assertEqual(default_mode, 'wsl')
        
        # Test instructions contain WSL info
        instructions = self.python_helper.get_execution_instructions()
        self.assertIn('WSL環境', instructions)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_windows_specific_behavior(self):
        """Test Windows-specific behavior"""
        # Remove WSL environment variables
        if 'WSL_DISTRO_NAME' in os.environ:
            del os.environ['WSL_DISTRO_NAME']
        if 'WSL_INTEROP' in os.environ:
            del os.environ['WSL_INTEROP']
        
        # Should not detect WSL
        self.assertFalse(self.python_helper.is_wsl_environment())
    
    def test_error_handling(self):
        """Test error handling in various scenarios"""
        # Test with invalid script path
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_path = os.path.join(temp_dir, 'nonexistent', 'script.py')
            
            # Should handle missing directory gracefully
            try:
                run_script = self.python_helper.create_run_script(invalid_path)
                # If it succeeds, the run script should still be created
                self.assertTrue(run_script.endswith('run.sh'))
            except Exception as e:
                # Or it should raise a reasonable exception
                self.assertIsInstance(e, (OSError, IOError))
    
    def test_consistency(self):
        """Test consistency of results"""
        # Multiple calls should return consistent results
        is_wsl_1 = self.python_helper.is_wsl_environment()
        is_wsl_2 = self.python_helper.is_wsl_environment()
        self.assertEqual(is_wsl_1, is_wsl_2)
        
        executables_1 = self.python_helper.find_python_executables()
        executables_2 = self.python_helper.find_python_executables()
        # Should find same executables (order might differ)
        self.assertEqual(len(executables_1), len(executables_2))

if __name__ == '__main__':
    unittest.main()