"""
Utility functions for text processing
"""
import re
import unicodedata
from typing import List, Tuple


def normalize_arabic_text(text: str) -> str:
    """Normalize Arabic text by removing diacritics and standardizing characters"""
    # Remove diacritics (tashkeel)
    text = re.sub(r'[\u064B-\u065F\u0670\u0640]', '', text)
    
    # Normalize Unicode (NFD normalization)
    text = unicodedata.normalize('NFD', text)
    
    # Remove combining characters
    text = ''.join(c for c in text if not unicodedata.combining(c))
    
    return text


def create_flexible_pattern(word: str) -> str:
    """Create a regex pattern that matches variations of a word"""
    # Normalize the word first
    normalized_word = normalize_arabic_text(word)
    
    # Create pattern that allows:
    # 1. Extra repeated characters
    # 2. Tatweel (ـ) characters between letters
    # 3. Case variations
    pattern_chars = []
    
    for char in normalized_word:
        if char.isalpha():
            # Allow the character followed by optional repetitions and optional tatweel
            pattern_chars.append(f"{re.escape(char)}+[\u0640]*")
        else:
            pattern_chars.append(re.escape(char))
    
    # Join with optional tatweel between characters
    pattern = '[\u0640]*'.join(pattern_chars)
    
    # Add word boundaries (but be flexible with Arabic)
    return f"(?<![\\w\u0600-\u06FF]){pattern}(?![\\w\u0600-\u06FF])"


def remove_diacritics(text: str) -> str:
    """Remove Arabic diacritical marks from text"""
    # Arabic diacritics range includes Fatha, Kasra, Damma, etc.
    diacritics_pattern = re.compile(r'[\u064B-\u065F\u0670]')
    return diacritics_pattern.sub('', text)


def sanitize_message(message: str, insults: List[str]) -> Tuple[str, List[str]]:
    """Sanitize a message by replacing detected insults with asterisks"""
    normalized_message = normalize_arabic_text(message.lower())
    found_insults = []
    sanitized_message = message
    
    for insult in insults:
        flexible_pattern = create_flexible_pattern(insult)
        pattern = re.compile(flexible_pattern, flags=re.IGNORECASE | re.UNICODE)
        
        matches = pattern.finditer(normalized_message)
        
        for match in matches:
            found_insults.append(match.group())
            start, end = match.span()
            replacement = '*' * (end - start)
            sanitized_message = sanitized_message[:start] + replacement + sanitized_message[end:]
    
    return sanitized_message, found_insults


def word_by_word_sanitize(message: str, insults: List[str]) -> Tuple[str, List[str]]:
    """Alternative approach: Check each word individually for better accuracy"""
    words = message.split()
    detected_words = []
    final_sanitized_words = []
    
    for word in words:
        word_detected = False
        normalized_word = normalize_arabic_text(word.lower())
        
        for insult in insults:
            flexible_pattern = create_flexible_pattern(insult)
            pattern = re.compile(flexible_pattern, flags=re.IGNORECASE | re.UNICODE)
            
            if pattern.search(normalized_word):
                detected_words.append(word)
                final_sanitized_words.append('*' * len(word))
                word_detected = True
                break
        
        if not word_detected:
            final_sanitized_words.append(word)
    
    return ' '.join(final_sanitized_words), detected_words


def filter_inappropriate_words(message: str) -> bool:
    """
    Filter messages containing variations of banned words like "قص"
    """
    if not message:
        return False
    
    # Convert to lowercase for case-insensitive matching
    text_lower = message.lower()
    
    # Pattern to match variations of "قص"
    forbidden_pattern = r'^(?!.*ق\s*ص)(?:[قص]{2,}|صق)$'
    
    # Check if the message matches the pattern
    return bool(re.search(forbidden_pattern, text_lower))
