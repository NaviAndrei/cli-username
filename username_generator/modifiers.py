import random
from typing import Optional
from .config import get_config_value

def apply_leet_speak(text: str) -> str:
    """Transforms text into Leet Speak using the configuration map.
    
    Supports both static substitutions (str) and randomized lists of substitutions.
    
    Args:
        text: The string to transform.
        
    Returns:
        str: The transformed 'l33t' text.
    """
    leet_map = get_config_value('leet_map', {})
    result = []
    
    for char in text:
        substitution = leet_map.get(char, char)
        
        if isinstance(substitution, list):
            result.append(random.choice(substitution))
        else:
            result.append(substitution)
            
    return ''.join(result)

def apply_prefix_suffix(username: str) -> str:
    """Randomly prepends/appends catchy prefixes or suffixes.
    
    Args:
        username: The base username.
        
    Returns:
        str: Modified username with added identifiers.
    """
    prefixes = get_config_value('prefixes', [])
    suffixes = get_config_value('suffixes', [])
    
    add_prefix = random.choice([True, False])
    add_suffix = random.choice([True, False])

    if add_prefix and prefixes:
        username = f"{random.choice(prefixes)}_{username}"
    if add_suffix and suffixes:
        username = f"{username}_{random.choice(suffixes)}"

    return username

def apply_special_chars(username: str) -> str:
    """Inserts a random special character at a random position.
    
    Args:
        username: The base username.
        
    Returns:
        str: Username with an injected special character.
    """
    special_chars = get_config_value('special_chars', "!@#$%^&*")
    if not username or not special_chars:
        return username
        
    char_to_add = random.choice(special_chars)
    insert_pos = random.randint(0, len(username))
    return username[:insert_pos] + char_to_add + username[insert_pos:]

def strip_numbers(username: str) -> str:
    """Removes all digits from the username.
    
    Args:
        username: The target string.
        
    Returns:
        str: A digit-free username.
    """
    return ''.join(char for char in username if not char.isdigit())

def enforce_length(username: str, length: int) -> str:
    """Adjusts the username to match a structural length requirement.
    
    If the string is too long, it will be truncated.
    If it is too short, it will be padded with random digits.
    
    Args:
        username: The candidate username.
        length: The target length.
        
    Returns:
        str: A username matching exactly the requested length.
    """
    if length <= 0:
        return username
        
    if len(username) > length:
        return username[:length]
    elif len(username) < length:
        padding = length - len(username)
        # Generate numeric padding efficiently
        username += ''.join(random.choices('0123456789', k=padding))
        
    return username

def apply_alt_caps(username: str) -> str:
    """Alternates uppercase/lowercase on each character (CaSe StYlE).
    
    Args:
        username: The base username to transform.
        
    Returns:
        str: Username with alternating capitalization.
    """
    # Alternation index applies only to letters, not digits/symbols
    result = []
    letter_index = 0
    for char in username:
        if char.isalpha():
            # Even indices are uppercase, odd are lowercase
            result.append(char.upper() if letter_index % 2 == 0 else char.lower())
            letter_index += 1
        else:
            result.append(char)
    return ''.join(result)

try:
    import pronouncing
except ImportError:
    pronouncing = None

# Simple in-memory cache for rhymes to avoid re-querying
_RHYME_CACHE = {}

def is_alliterative(word1: str, word2: str) -> bool:
    """Checks if two words start with the same letter (case-insensitive)."""
    if not word1 or not word2:
        return False
    return word1[0].lower() == word2[0].lower()

def is_rhyming(word1: str, word2: str) -> bool:
    """Checks if two words rhyme.
    
    Tries to use the 'pronouncing' library for phonetic rhymes.
    Falls back to suffix matching if library missing or word unknown.
    """
    if not word1 or not word2:
        return False
        
    s1 = word1.lower()
    s2 = word2.lower()
    
    # 1. Try Phonetic Rhyme (High Accuracy)
    if pronouncing:
        # Check cache first
        if s1 in _RHYME_CACHE:
            rhymes = _RHYME_CACHE[s1]
        else:
            rhymes = pronouncing.rhymes(s1)
            _RHYME_CACHE[s1] = set(rhymes) # Use set for O(1) lookup
            
        if s2 in rhymes:
            return True
        # Also check reverse in case s1 wasn't in dict but s2 might be?
        # Pronouncing usually symmetric but data might be partial.
        # Let's trust one-way check + fallback.
    
    # 2. Fallback: Suffix Matching (Heuristic)
    # Too short words: must be identical at the last letter
    if len(s1) < 3 or len(s2) < 3:
        return s1[-1] == s2[-1]
        
    # Normal words: last 2 letters
    return s1[-2:] == s2[-2:]
