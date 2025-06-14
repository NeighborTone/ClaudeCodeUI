# -*- coding: utf-8 -*-
"""
Test module for path_converter.py
"""
import unittest
import os
from test_config import BaseTestCase

class TestPathConverter(BaseTestCase):
    """Test PathConverter class"""
    
    def setUp(self):
        super().setUp()
        from core.path_converter import PathConverter
        self.path_converter = PathConverter
    
    def test_is_wsl_environment(self):
        """Test WSL environment detection"""
        result = self.path_converter.is_wsl_environment()
        self.assertIsInstance(result, bool)
        # Should detect current environment correctly
        if 'WSL_DISTRO_NAME' in os.environ or 'WSL_INTEROP' in os.environ:
            self.assertTrue(result)
    
    def test_windows_to_wsl_conversion(self):
        """Test Windows to WSL path conversion"""
        # Test basic Windows path
        windows_path = "C:\\Users\\owner\\file.txt"
        wsl_path = self.path_converter.windows_to_wsl(windows_path)
        self.assertEqual(wsl_path, "/mnt/c/Users/owner/file.txt")
        
        # Test different drive
        windows_path = "D:\\Projects\\code\\main.py"
        wsl_path = self.path_converter.windows_to_wsl(windows_path)
        self.assertEqual(wsl_path, "/mnt/d/Projects/code/main.py")
        
        # Test forward slashes in Windows path
        windows_path = "C:/Users/owner/file.txt"
        wsl_path = self.path_converter.windows_to_wsl(windows_path)
        self.assertEqual(wsl_path, "/mnt/c/Users/owner/file.txt")
    
    def test_wsl_to_windows_conversion(self):
        """Test WSL to Windows path conversion"""
        # Test basic WSL path
        wsl_path = "/mnt/c/Users/owner/file.txt"
        windows_path = self.path_converter.wsl_to_windows(wsl_path)
        self.assertEqual(windows_path, "C:\\Users\\owner\\file.txt")
        
        # Test different drive
        wsl_path = "/mnt/d/Projects/code/main.py"
        windows_path = self.path_converter.wsl_to_windows(wsl_path)
        self.assertEqual(windows_path, "D:\\Projects\\code\\main.py")
    
    def test_relative_paths(self):
        """Test relative path handling"""
        relative_path = "src/main.py"
        
        # WSL conversion should preserve relative paths
        wsl_result = self.path_converter.windows_to_wsl(relative_path)
        self.assertEqual(wsl_result, "src/main.py")
        
        # Windows conversion should preserve relative paths
        windows_result = self.path_converter.wsl_to_windows(relative_path)
        self.assertEqual(windows_result, "src/main.py")
    
    def test_already_converted_paths(self):
        """Test paths that are already in target format"""
        # WSL path passed to windows_to_wsl
        wsl_path = "/mnt/c/Users/owner/file.txt"
        result = self.path_converter.windows_to_wsl(wsl_path)
        self.assertEqual(result, wsl_path)
        
        # Non-WSL Unix path to wsl_to_windows
        unix_path = "/home/user/file.txt"
        result = self.path_converter.wsl_to_windows(unix_path)
        self.assertEqual(result, unix_path)
    
    def test_convert_path_wsl_mode(self):
        """Test convert_path with WSL mode"""
        windows_path = "C:\\Users\\owner\\file.txt"
        result = self.path_converter.convert_path(windows_path, 'wsl')
        self.assertEqual(result, "/mnt/c/Users/owner/file.txt")
    
    def test_convert_path_windows_mode(self):
        """Test convert_path with Windows mode"""
        windows_path = "C:\\Users\\owner\\file.txt"
        result = self.path_converter.convert_path(windows_path, 'windows')
        self.assertEqual(result, "C:/Users/owner/file.txt")
        
        # Should always use forward slashes in Windows mode
        self.assertNotIn('\\\\', result)
    
    def test_convert_path_default_mode(self):
        """Test convert_path with unknown mode"""
        windows_path = "C:\\Users\\owner\\file.txt"
        result = self.path_converter.convert_path(windows_path, 'unknown')
        # Should default to forward slash conversion
        self.assertEqual(result, "C:/Users/owner/file.txt")
    
    def test_get_default_mode(self):
        """Test default mode detection"""
        default_mode = self.path_converter.get_default_mode()
        self.assertIn(default_mode, ['wsl', 'windows'])
        
        # Should match WSL environment detection
        is_wsl = self.path_converter.is_wsl_environment()
        if is_wsl:
            self.assertEqual(default_mode, 'wsl')
        else:
            self.assertEqual(default_mode, 'windows')
    
    def test_backslash_handling(self):
        """Test consistent backslash to forward slash conversion"""
        test_paths = [
            "C:\\Users\\owner\\file.txt",
            "path\\to\\file.py",
            "D:\\Projects\\code\\main.py"
        ]
        
        for path in test_paths:
            # Both modes should eliminate backslashes
            wsl_result = self.path_converter.convert_path(path, 'wsl')
            windows_result = self.path_converter.convert_path(path, 'windows')
            
            self.assertNotIn('\\\\', wsl_result)
            self.assertNotIn('\\\\', windows_result)
    
    def test_case_sensitivity(self):
        """Test drive letter case handling"""
        # Test lowercase drive
        path_lower = "c:\\users\\owner\\file.txt"
        wsl_result = self.path_converter.windows_to_wsl(path_lower)
        self.assertEqual(wsl_result, "/mnt/c/users/owner/file.txt")
        
        # Test uppercase drive
        path_upper = "C:\\Users\\owner\\file.txt"
        wsl_result = self.path_converter.windows_to_wsl(path_upper)
        self.assertEqual(wsl_result, "/mnt/c/Users/owner/file.txt")
    
    def test_edge_cases(self):
        """Test edge cases and special characters"""
        # Empty string
        self.assertEqual(self.path_converter.convert_path("", 'wsl'), "")
        
        # Path with spaces
        path_with_spaces = "C:\\Program Files\\My App\\file.txt"
        wsl_result = self.path_converter.windows_to_wsl(path_with_spaces)
        self.assertEqual(wsl_result, "/mnt/c/Program Files/My App/file.txt")
        
        # Path with special characters
        path_special = "C:\\Users\\owner\\file-name_123.txt"
        wsl_result = self.path_converter.windows_to_wsl(path_special)
        self.assertEqual(wsl_result, "/mnt/c/Users/owner/file-name_123.txt")

if __name__ == '__main__':
    unittest.main()