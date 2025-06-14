# -*- coding: utf-8 -*-
"""
Test module for settings.py
"""
import unittest
import os
import tempfile
import json
from test_config import BaseTestCase

class TestSettingsManager(BaseTestCase):
    """Test SettingsManager class"""
    
    def setUp(self):
        super().setUp()
        # Create temporary config file for testing
        self.temp_config_dir = tempfile.mkdtemp()
        self.temp_config_file = os.path.join(self.temp_config_dir, 'test_settings.json')
        
        from core.settings import SettingsManager
        self.settings_manager_class = SettingsManager
    
    def tearDown(self):
        super().tearDown()
        # Clean up temp files
        if os.path.exists(self.temp_config_file):
            os.remove(self.temp_config_file)
        os.rmdir(self.temp_config_dir)
    
    def test_default_settings_load(self):
        """Test loading default settings"""
        settings = self.settings_manager_class(self.temp_config_file)
        
        # Check default values exist
        self.assertIsNotNone(settings.get('window.width'))
        self.assertIsNotNone(settings.get('window.height'))
        self.assertIsNotNone(settings.get('ui.thinking_level'))
        self.assertIsNotNone(settings.get('ui.theme'))
        
        # Check specific default values
        self.assertEqual(settings.get('window.width'), 1200)
        self.assertEqual(settings.get('window.height'), 800)
        self.assertEqual(settings.get('ui.thinking_level'), 'think')
    
    def test_get_set_operations(self):
        """Test get and set operations"""
        settings = self.settings_manager_class(self.temp_config_file)
        
        # Test simple get/set
        settings.set('test.value', 'hello')
        self.assertEqual(settings.get('test.value'), 'hello')
        
        # Test nested get/set
        settings.set('test.nested.deep.value', 42)
        self.assertEqual(settings.get('test.nested.deep.value'), 42)
        
        # Test get with default
        self.assertEqual(settings.get('nonexistent.key', 'default'), 'default')
        self.assertIsNone(settings.get('nonexistent.key'))
    
    def test_window_geometry_methods(self):
        """Test window geometry specific methods"""
        settings = self.settings_manager_class(self.temp_config_file)
        
        # Test setting window geometry
        settings.set_window_geometry(100, 200, 800, 600)
        
        # Test getting window geometry
        geometry = settings.get_window_geometry()
        self.assertEqual(geometry['x'], 100)
        self.assertEqual(geometry['y'], 200)
        self.assertEqual(geometry['width'], 800)
        self.assertEqual(geometry['height'], 600)
    
    def test_thinking_level_methods(self):
        """Test thinking level specific methods"""
        settings = self.settings_manager_class(self.temp_config_file)
        
        # Test setting thinking level
        settings.set_thinking_level('ultrathink')
        self.assertEqual(settings.get_thinking_level(), 'ultrathink')
        
        # Test default thinking level
        settings.set('ui.thinking_level', None)
        self.assertEqual(settings.get_thinking_level(), 'think')
    
    def test_path_mode_methods(self):
        """Test path mode specific methods"""
        settings = self.settings_manager_class(self.temp_config_file)
        
        # Test setting path mode
        settings.set_path_mode('wsl')
        self.assertEqual(settings.get_path_mode(), 'wsl')
        
        # Test None path mode (auto-detect)
        settings.set_path_mode(None)
        self.assertIsNone(settings.get_path_mode())
    
    def test_theme_methods(self):
        """Test theme specific methods"""
        settings = self.settings_manager_class(self.temp_config_file)
        
        # Test setting theme
        settings.set_theme('dark')
        self.assertEqual(settings.get_theme(), 'dark')
        
        # Test default theme
        settings = self.settings_manager_class(self.temp_config_file + '_new')
        self.assertEqual(settings.get_theme(), 'cyberpunk')
    
    def test_font_settings_methods(self):
        """Test font settings methods"""
        settings = self.settings_manager_class(self.temp_config_file)
        
        # Test setting font
        settings.set_font_settings('Arial', 12)
        font_settings = settings.get_font_settings()
        self.assertEqual(font_settings['family'], 'Arial')
        self.assertEqual(font_settings['size'], 12)
    
    def test_save_load_persistence(self):
        """Test save and load persistence"""
        # Create first settings instance
        settings1 = self.settings_manager_class(self.temp_config_file)
        settings1.set('test.persistence', 'persistent_value')
        settings1.set_thinking_level('megathink')
        settings1.save_settings()
        
        # Create second settings instance (should load saved data)
        settings2 = self.settings_manager_class(self.temp_config_file)
        self.assertEqual(settings2.get('test.persistence'), 'persistent_value')
        self.assertEqual(settings2.get_thinking_level(), 'megathink')
    
    def test_merge_settings(self):
        """Test settings merging functionality"""
        # Create config file with partial settings
        partial_config = {
            'window': {'width': 1000},  # Missing height
            'ui': {'theme': 'light'},   # Missing other ui settings
            'new_section': {'value': 'test'}  # New section
        }
        
        with open(self.temp_config_file, 'w') as f:
            json.dump(partial_config, f)
        
        settings = self.settings_manager_class(self.temp_config_file)
        
        # Should have merged with defaults
        self.assertEqual(settings.get('window.width'), 1000)  # From file
        self.assertEqual(settings.get('window.height'), 800)  # From defaults
        self.assertEqual(settings.get('ui.theme'), 'light')   # From file
        self.assertEqual(settings.get('ui.thinking_level'), 'think')  # From defaults
        self.assertEqual(settings.get('new_section.value'), 'test')  # From file
    
    def test_invalid_config_file_handling(self):
        """Test handling of invalid config files"""
        # Create invalid JSON file
        with open(self.temp_config_file, 'w') as f:
            f.write('invalid json content {')
        
        # Should gracefully fallback to defaults
        settings = self.settings_manager_class(self.temp_config_file)
        self.assertEqual(settings.get('window.width'), 1200)  # Default value
    
    def test_nonexistent_config_file(self):
        """Test handling when config file doesn't exist"""
        nonexistent_file = os.path.join(self.temp_config_dir, 'nonexistent.json')
        settings = self.settings_manager_class(nonexistent_file)
        
        # Should use defaults
        self.assertEqual(settings.get('window.width'), 1200)
        self.assertEqual(settings.get('ui.thinking_level'), 'think')
    
    def test_config_directory_creation(self):
        """Test automatic config directory creation"""
        nested_config_file = os.path.join(self.temp_config_dir, 'subdir', 'config.json')
        settings = self.settings_manager_class(nested_config_file)
        
        settings.set('test.value', 'test')
        settings.save_settings()
        
        # Directory should be created and file should exist
        self.assertTrue(os.path.exists(nested_config_file))
    
    def test_data_types(self):
        """Test various data types in settings"""
        settings = self.settings_manager_class(self.temp_config_file)
        
        # Test different data types
        test_data = {
            'string': 'hello world',
            'integer': 42,
            'float': 3.14,
            'boolean': True,
            'list': [1, 2, 3],
            'dict': {'nested': 'value'}
        }
        
        for key, value in test_data.items():
            settings.set(f'test.{key}', value)
            retrieved = settings.get(f'test.{key}')
            self.assertEqual(retrieved, value)
            self.assertEqual(type(retrieved), type(value))
    
    def test_dot_notation_edge_cases(self):
        """Test edge cases in dot notation"""
        settings = self.settings_manager_class(self.temp_config_file)
        
        # Test single key (no dots)
        settings.set('single', 'value')
        self.assertEqual(settings.get('single'), 'value')
        
        # Test empty key parts
        settings.set('a..b', 'value')  # Double dot
        self.assertEqual(settings.get('a..b'), 'value')
        
        # Test overwriting nested structure
        settings.set('test.nested', {'original': 'value'})
        settings.set('test.nested.new', 'new_value')
        self.assertEqual(settings.get('test.nested.new'), 'new_value')
        self.assertEqual(settings.get('test.nested.original'), 'value')

if __name__ == '__main__':
    unittest.main()