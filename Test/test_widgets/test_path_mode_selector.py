# -*- coding: utf-8 -*-
"""
Test module for path_mode_selector.py
"""
import unittest
from unittest.mock import Mock, patch
from test_config import BaseTestCase

class TestPathModeSelectorWidget(BaseTestCase):
    """Test PathModeSelectorWidget class"""
    
    def setUp(self):
        super().setUp()
        # Import with mocked Qt
        from widgets.path_mode_selector import PathModeSelectorWidget
        self.path_mode_selector_class = PathModeSelectorWidget
    
    def test_initialization(self):
        """Test widget initialization"""
        widget = self.path_mode_selector_class()
        
        # Should have path modes defined
        self.assertIsInstance(widget.path_modes, list)
        self.assertGreater(len(widget.path_modes), 0)
        
        # Each path mode should be a tuple with key and display name
        for mode in widget.path_modes:
            self.assertIsInstance(mode, tuple)
            self.assertEqual(len(mode), 2)
            self.assertIsInstance(mode[0], str)  # key
            self.assertIsInstance(mode[1], str)  # display name
    
    def test_path_modes_content(self):
        """Test path modes content"""
        widget = self.path_mode_selector_class()
        
        # Check specific path modes
        mode_keys = [mode[0] for mode in widget.path_modes]
        
        # Should contain essential path modes
        essential_modes = ['windows', 'wsl']
        for essential in essential_modes:
            self.assertIn(essential, mode_keys)
        
        # Check that display names are descriptive
        display_names = [mode[1] for mode in widget.path_modes]
        for display_name in display_names:
            self.assertGreater(len(display_name), 0)
            # Should contain mode description
            if 'windows' in display_name.lower():
                self.assertIn('Windows', display_name)
            elif 'wsl' in display_name.lower():
                self.assertIn('WSL', display_name)
    
    def test_path_modes_order(self):
        """Test path modes are in logical order"""
        widget = self.path_mode_selector_class()
        
        mode_keys = [mode[0] for mode in widget.path_modes]
        
        # Windows should come first (more common)
        self.assertEqual(mode_keys[0], 'windows')
        
        # WSL should be second
        self.assertEqual(mode_keys[1], 'wsl')
    
    def test_get_current_path_mode(self):
        """Test getting current path mode"""
        widget = self.path_mode_selector_class()
        
        # Should return default mode
        current = widget.get_current_path_mode()
        self.assertIsInstance(current, str)
        self.assertIn(current, ['windows', 'wsl'])
    
    def test_set_path_mode(self):
        """Test setting path mode"""
        widget = self.path_mode_selector_class()
        
        # Test setting valid mode
        widget.set_path_mode('wsl')
        # Note: In mock environment, we can't verify combo selection, 
        # but we can verify the method doesn't crash
        
        # Test setting invalid mode (should handle gracefully)
        widget.set_path_mode('invalid_mode')
        # Should not crash
    
    def test_path_mode_keys_uniqueness(self):
        """Test that path mode keys are unique"""
        widget = self.path_mode_selector_class()
        
        mode_keys = [mode[0] for mode in widget.path_modes]
        unique_keys = set(mode_keys)
        
        # All keys should be unique
        self.assertEqual(len(mode_keys), len(unique_keys))
    
    def test_path_mode_display_names_uniqueness(self):
        """Test that display names are unique"""
        widget = self.path_mode_selector_class()
        
        display_names = [mode[1] for mode in widget.path_modes]
        unique_names = set(display_names)
        
        # All display names should be unique
        self.assertEqual(len(display_names), len(unique_names))
    
    def test_signal_definition(self):
        """Test signal definition"""
        widget = self.path_mode_selector_class()
        
        # Should have signal attribute
        self.assertTrue(hasattr(widget, 'path_mode_changed'))
    
    def test_combo_setup(self):
        """Test combo box setup"""
        widget = self.path_mode_selector_class()
        
        # Should have combo attribute
        self.assertTrue(hasattr(widget, 'combo'))
        
        # Combo should be set up (in mock environment, this just verifies no crash)
        self.assertIsNotNone(widget.combo)
    
    def test_on_selection_changed(self):
        """Test selection change handler"""
        widget = self.path_mode_selector_class()
        
        # Should have method
        self.assertTrue(hasattr(widget, 'on_selection_changed'))
        self.assertTrue(callable(widget.on_selection_changed))
        
        # Should not crash when called
        widget.on_selection_changed()
    
    @patch('core.path_converter.PathConverter.get_default_mode')
    def test_default_mode_selection(self, mock_get_default_mode):
        """Test default mode selection based on environment"""
        # Test WSL environment default
        mock_get_default_mode.return_value = 'wsl'
        widget = self.path_mode_selector_class()
        # In real environment, this would set WSL as default
        
        # Test Windows environment default
        mock_get_default_mode.return_value = 'windows'
        widget = self.path_mode_selector_class()
        # In real environment, this would set Windows as default
    
    def test_path_modes_completeness(self):
        """Test that all expected path modes are present"""
        widget = self.path_mode_selector_class()
        
        mode_keys = [mode[0] for mode in widget.path_modes]
        
        # Expected modes
        expected_modes = ['windows', 'wsl']
        
        for expected in expected_modes:
            self.assertIn(expected, mode_keys, f"Missing path mode: {expected}")
        
        # Should have exactly these modes (no extras)
        self.assertEqual(len(mode_keys), len(expected_modes))
    
    def test_path_mode_descriptions(self):
        """Test path mode descriptions"""
        widget = self.path_mode_selector_class()
        
        for mode_key, display_name in widget.path_modes:
            # Display name should contain the mode key or description
            if mode_key == 'windows':
                self.assertIn('Windows', display_name)
                self.assertIn('標準', display_name)  # Should mention standard format
            elif mode_key == 'wsl':
                self.assertIn('WSL', display_name)
                self.assertIn('/mnt/c', display_name)  # Should mention WSL format
    
    def test_japanese_localization(self):
        """Test Japanese localization"""
        widget = self.path_mode_selector_class()
        
        for mode_key, display_name in widget.path_modes:
            # Should contain Japanese characters
            has_japanese = any(
                '\u3040' <= char <= '\u309f' or  # Hiragana
                '\u30a0' <= char <= '\u30ff' or  # Katakana
                '\u4e00' <= char <= '\u9faf'     # Kanji
                for char in display_name
            )
            self.assertTrue(has_japanese, f"Display name should contain Japanese: {display_name}")
    
    def test_widget_parent_handling(self):
        """Test widget parent parameter handling"""
        # Test with None parent
        widget1 = self.path_mode_selector_class(None)
        self.assertIsNotNone(widget1)
        
        # Test with mock parent
        mock_parent = Mock()
        widget2 = self.path_mode_selector_class(mock_parent)
        self.assertIsNotNone(widget2)
    
    def test_setup_ui_method(self):
        """Test setup_ui method"""
        widget = self.path_mode_selector_class()
        
        # Should have setup_ui method
        self.assertTrue(hasattr(widget, 'setup_ui'))
        self.assertTrue(callable(widget.setup_ui))
        
        # Method should be callable without error
        widget.setup_ui()
    
    def test_mode_value_consistency(self):
        """Test mode value consistency with PathConverter"""
        widget = self.path_mode_selector_class()
        
        mode_keys = [mode[0] for mode in widget.path_modes]
        
        # Mode keys should match those used in PathConverter
        from core.path_converter import PathConverter
        
        # Test that modes are valid for PathConverter
        for mode_key in mode_keys:
            # Should not crash when used with PathConverter
            try:
                result = PathConverter.convert_path('C:\\test\\path', mode_key)
                self.assertIsInstance(result, str)
            except Exception as e:
                self.fail(f"PathConverter failed with mode '{mode_key}': {e}")
    
    def test_environment_detection_integration(self):
        """Test integration with environment detection"""
        from core.path_converter import PathConverter
        
        # Get environment default mode
        default_mode = PathConverter.get_default_mode()
        self.assertIn(default_mode, ['windows', 'wsl'])
        
        # Widget should support this mode
        widget = self.path_mode_selector_class()
        mode_keys = [mode[0] for mode in widget.path_modes]
        self.assertIn(default_mode, mode_keys)
    
    def test_label_text(self):
        """Test label text"""
        widget = self.path_mode_selector_class()
        
        # Should have setup UI with label (can't verify text in mock environment)
        # But we can verify the setup process doesn't crash
        widget.setup_ui()

if __name__ == '__main__':
    unittest.main()