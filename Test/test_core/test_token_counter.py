# -*- coding: utf-8 -*-
"""
Test module for token_counter.py
"""
import unittest
from test_config import BaseTestCase

class TestTokenCounter(BaseTestCase):
    """Test TokenCounter class"""
    
    def setUp(self):
        super().setUp()
        from core.token_counter import TokenCounter
        self.token_counter = TokenCounter
    
    def test_empty_text(self):
        """Test empty text returns 0"""
        self.assertEqual(self.token_counter.count_tokens(""), 0)
        self.assertEqual(self.token_counter.count_tokens(None), 0)
    
    def test_simple_english_text(self):
        """Test simple English text counting"""
        result = self.token_counter.count_tokens("Hello World")
        self.assertGreater(result, 0)
        self.assertIsInstance(result, int)
    
    def test_japanese_text(self):
        """Test Japanese text counting"""
        result = self.token_counter.count_tokens("こんにちは世界")
        self.assertGreater(result, 0)
        # Japanese should generally use different token ratio
        english_result = self.token_counter.count_tokens("Hello World")
        # Both should be reasonable but may differ
        self.assertIsInstance(result, int)
    
    def test_mixed_text(self):
        """Test mixed Japanese and English text"""
        mixed_text = "Hello こんにちは World 世界"
        result = self.token_counter.count_tokens(mixed_text)
        self.assertGreater(result, 0)
    
    def test_file_paths(self):
        """Test file path handling"""
        file_path_text = "@src/main.py @config/settings.json"
        result = self.token_counter.count_tokens(file_path_text)
        self.assertGreater(result, 0)
    
    def test_urls(self):
        """Test URL handling"""
        url_text = "Visit https://example.com/api/v1/users for more info"
        result = self.token_counter.count_tokens(url_text)
        self.assertGreater(result, 0)
    
    def test_code_blocks(self):
        """Test code block handling"""
        code_text = """```python
def hello():
    print("Hello World")
```"""
        result = self.token_counter.count_tokens(code_text)
        self.assertGreater(result, 0)
    
    def test_thinking_levels(self):
        """Test thinking level text"""
        thinking_text = "ultrathink\nThis is a complex problem to solve."
        result = self.token_counter.count_tokens(thinking_text)
        self.assertGreater(result, 0)
    
    def test_format_token_count(self):
        """Test token count formatting"""
        # Test small numbers
        formatted = self.token_counter.format_token_count(5)
        self.assertEqual(formatted, "5トークン")
        
        # Test large numbers
        formatted = self.token_counter.format_token_count(1500)
        self.assertEqual(formatted, "1,500トークン")
        
        formatted = self.token_counter.format_token_count(0)
        self.assertEqual(formatted, "0トークン")
    
    def test_minimum_token_count(self):
        """Test minimum token count for non-empty text"""
        result = self.token_counter.count_tokens("a")
        self.assertGreaterEqual(result, 1)
    
    def test_consistency(self):
        """Test that same input produces same output"""
        text = "This is a test message with 日本語 mixed in."
        result1 = self.token_counter.count_tokens(text)
        result2 = self.token_counter.count_tokens(text)
        self.assertEqual(result1, result2)
    
    def test_various_lengths(self):
        """Test different text lengths"""
        short_text = "Hi"
        medium_text = "This is a medium length text with some content."
        long_text = "This is a much longer text that contains multiple sentences. " * 10
        
        short_result = self.token_counter.count_tokens(short_text)
        medium_result = self.token_counter.count_tokens(medium_text)
        long_result = self.token_counter.count_tokens(long_text)
        
        # Longer text should generally have more tokens
        self.assertLess(short_result, medium_result)
        self.assertLess(medium_result, long_result)

if __name__ == '__main__':
    unittest.main()