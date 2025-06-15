# -*- coding: utf-8 -*-
"""
Token Counter - Simple token count estimation for prompts
"""
import re


class TokenCounter:
    """Simple token counter for prompt text estimation"""
    
    # Approximate token ratios based on common patterns
    # These are rough estimates - actual tokenization varies by model
    CHAR_TO_TOKEN_RATIO = 4.0  # Average: 1 token ≈ 4 characters
    JAPANESE_CHAR_TO_TOKEN_RATIO = 2.5  # Japanese tends to use more tokens per char
    
    @staticmethod
    def count_tokens(text: str) -> int:
        """
        Estimate token count for given text.
        
        Args:
            text: The text to count tokens for
            
        Returns:
            Estimated token count
        """
        if not text:
            return 0
        
        # Count Japanese characters (Hiragana, Katakana, Kanji)
        japanese_pattern = re.compile(r'[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf\u3400-\u4dbf]')
        japanese_chars = len(japanese_pattern.findall(text))
        
        # Count non-Japanese characters
        non_japanese_text = japanese_pattern.sub('', text)
        non_japanese_chars = len(non_japanese_text)
        
        # Calculate tokens with different ratios
        japanese_tokens = japanese_chars / TokenCounter.JAPANESE_CHAR_TO_TOKEN_RATIO
        non_japanese_tokens = non_japanese_chars / TokenCounter.CHAR_TO_TOKEN_RATIO
        
        # Special handling for common patterns
        # URLs and file paths tend to use more tokens
        url_pattern = re.compile(r'https?://[^\s]+|@[^\s]+')
        urls_and_paths = url_pattern.findall(text)
        extra_tokens = sum(len(url) / 2 for url in urls_and_paths)  # URLs use more tokens
        
        # Code blocks also tend to use more tokens due to syntax
        code_block_pattern = re.compile(r'```[\s\S]*?```')
        code_blocks = code_block_pattern.findall(text)
        code_extra_tokens = sum(len(block) / 3 for block in code_blocks)
        
        total_tokens = int(japanese_tokens + non_japanese_tokens + extra_tokens + code_extra_tokens)
        
        # Minimum 1 token for any non-empty text
        return max(1, total_tokens)
    
    @staticmethod
    def format_token_count(count: int) -> str:
        """
        Format token count for display.
        
        Args:
            count: Token count
            
        Returns:
            Formatted string
        """
        if count >= 1000:
            return f"{count:,}トークン"
        else:
            return f"{count}トークン"