import random
from typing import Optional
from .config import get_config_value

def apply_leet_speak(text: str) -> str:
    """Transforms text into Leet Speak using the configuration map.
    
    Args:
        text: The string to transform.
        
    Returns:
        str: The transformed 'l33t' text.
    """
    leet_map = get_config_value('leet_map', {})
    return ''.join(leet_map.get(char, char) for char in text)

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
