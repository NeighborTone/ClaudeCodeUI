# -*- coding: utf-8 -*-
"""
Test module for thinking_selector.py
"""
import unittest
from unittest.mock import Mock, patch
from test_config import BaseTestCase

class TestThinkingSelectorWidget(BaseTestCase):
    """Test ThinkingSelectorWidget class"""
    
    def setUp(self):
        super().setUp()
        # Import with mocked Qt
        from widgets.thinking_selector import ThinkingSelectorWidget
        self.thinking_selector_class = ThinkingSelectorWidget
    
    def test_initialization(self):
        """Test widget initialization"""
        widget = self.thinking_selector_class()
        
        # Should have thinking levels defined
        self.assertIsInstance(widget.thinking_levels, list)
        self.assertGreater(len(widget.thinking_levels), 0)
        
        # Each thinking level should be a tuple with key and display name
        for level in widget.thinking_levels:
            self.assertIsInstance(level, tuple)
            self.assertEqual(len(level), 2)
            self.assertIsInstance(level[0], str)  # key
            self.assertIsInstance(level[1], str)  # display name
    
    def test_thinking_levels_content(self):
        """Test thinking levels content"""
        widget = self.thinking_selector_class()
        
        # Check specific thinking levels
        level_keys = [level[0] for level in widget.thinking_levels]
        
        # Should contain essential thinking levels
        essential_levels = ['think', 'think more', 'think harder', 'ultrathink', 'megathink']
        for essential in essential_levels:
            self.assertIn(essential, level_keys)
        
        # Check that display names are in Japanese
        display_names = [level[1] for level in widget.thinking_levels]
        for display_name in display_names:
            # Should contain Japanese characters or be descriptive
            self.assertGreater(len(display_name), 0)
    
    def test_thinking_levels_order(self):
        """Test thinking levels are in logical order"""
        widget = self.thinking_selector_class()
        
        level_keys = [level[0] for level in widget.thinking_levels]
        
        # Basic thinking should come first
        self.assertEqual(level_keys[0], 'think')
        
        # Ultrathink should be near the end
        self.assertIn('ultrathink', level_keys[-3:])
    
    def test_get_current_thinking_level(self):
        """Test getting current thinking level"""
        widget = self.thinking_selector_class()
        
        # Should return default level
        current = widget.get_current_thinking_level()
        self.assertIsInstance(current, str)
        self.assertEqual(current, 'think')  # Default should be 'think'
    
    def test_set_thinking_level(self):
        """Test setting thinking level"""
        widget = self.thinking_selector_class()
        
        # Test setting valid level
        widget.set_thinking_level('ultrathink')
        # Note: In mock environment, we can't verify combo selection, 
        # but we can verify the method doesn't crash
        
        # Test setting invalid level (should handle gracefully)
        widget.set_thinking_level('invalid_level')
        # Should not crash
    
    def test_thinking_level_keys_uniqueness(self):
        """Test that thinking level keys are unique"""
        widget = self.thinking_selector_class()
        
        level_keys = [level[0] for level in widget.thinking_levels]
        unique_keys = set(level_keys)
        
        # All keys should be unique
        self.assertEqual(len(level_keys), len(unique_keys))
    
    def test_thinking_level_display_names_uniqueness(self):
        """Test that display names are unique"""
        widget = self.thinking_selector_class()
        
        display_names = [level[1] for level in widget.thinking_levels]
        unique_names = set(display_names)
        
        # All display names should be unique
        self.assertEqual(len(display_names), len(unique_names))
    
    def test_signal_definition(self):
        """Test signal definition"""
        widget = self.thinking_selector_class()
        
        # Should have signal attribute
        self.assertTrue(hasattr(widget, 'thinking_level_changed'))
    
    def test_combo_setup(self):
        """Test combo box setup"""
        widget = self.thinking_selector_class()
        
        # Should have combo attribute
        self.assertTrue(hasattr(widget, 'combo'))
        
        # Combo should be set up (in mock environment, this just verifies no crash)
        self.assertIsNotNone(widget.combo)
    
    def test_on_selection_changed(self):
        """Test selection change handler"""
        widget = self.thinking_selector_class()
        
        # Should have method
        self.assertTrue(hasattr(widget, 'on_selection_changed'))
        self.assertTrue(callable(widget.on_selection_changed))
        
        # Should not crash when called
        widget.on_selection_changed()
    
    def test_default_thinking_level(self):
        """Test default thinking level selection"""
        widget = self.thinking_selector_class()
        
        # Default should be first item ('think')
        expected_default = widget.thinking_levels[0][0]
        self.assertEqual(expected_default, 'think')
    
    def test_thinking_levels_completeness(self):
        """Test that all expected thinking levels are present"""
        widget = self.thinking_selector_class()
        
        level_keys = [level[0] for level in widget.thinking_levels]
        
        # Expected levels based on the implementation
        expected_levels = [
            'think',
            'think more', 
            'think harder',
            'think hard',
            'think deeply',
            'think intensely',
            'think longer',
            'think a lot',
            'think about it',
            'think very hard',
            'think really hard',
            'think super hard',
            'megathink',
            'ultrathink'
        ]
        
        for expected in expected_levels:
            self.assertIn(expected, level_keys, f"Missing thinking level: {expected}")
    
    def test_thinking_levels_japanese_descriptions(self):
        """Test that thinking levels have Japanese descriptions"""
        widget = self.thinking_selector_class()
        
        for level_key, display_name in widget.thinking_levels:
            # Display name should contain the English key
            self.assertIn(level_key, display_name)
            
            # Should contain Japanese characters (hiragana, katakana, or kanji)
            has_japanese = any(
                '\u3040' <= char <= '\u309f' or  # Hiragana
                '\u30a0' <= char <= '\u30ff' or  # Katakana
                '\u4e00' <= char <= '\u9faf'     # Kanji
                for char in display_name
            )
            self.assertTrue(has_japanese, f"Display name should contain Japanese: {display_name}")
    
    def test_thinking_level_progression(self):
        """Test logical progression of thinking levels"""
        widget = self.thinking_selector_class()
        
        level_keys = [level[0] for level in widget.thinking_levels]
        
        # Basic progression checks
        think_index = level_keys.index('think')
        think_more_index = level_keys.index('think more')
        ultrathink_index = level_keys.index('ultrathink')
        
        # More intense thinking should come after basic thinking
        self.assertLess(think_index, think_more_index)
        self.assertLess(think_more_index, ultrathink_index)
    
    def test_widget_parent_handling(self):
        """Test widget parent parameter handling"""
        # Test with None parent
        widget1 = self.thinking_selector_class(None)
        self.assertIsNotNone(widget1)
        
        # Test with mock parent
        mock_parent = Mock()
        widget2 = self.thinking_selector_class(mock_parent)
        self.assertIsNotNone(widget2)
    
    def test_setup_ui_method(self):
        """Test setup_ui method"""
        widget = self.thinking_selector_class()
        
        # Should have setup_ui method
        self.assertTrue(hasattr(widget, 'setup_ui'))
        self.assertTrue(callable(widget.setup_ui))
        
        # Method should be callable without error
        # (In real environment this sets up the UI, in mock it's harmless)
        widget.setup_ui()

if __name__ == '__main__':
    unittest.main()