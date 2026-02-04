import random
import datetime
from typing import List, Optional
from .config import get_config_value
from .exceptions import ValidationError

def generate_timestamp_username(base_word: str = "Owl") -> str:
    """Generates a username formatted with the current timestamp.
    
    Args:
        base_word: The starting string for the username.
        
    Returns:
        str: A username like 'Word_MMDD_HHMM'.
    """
    now = datetime.datetime.now()
    return f"{base_word}_{now.strftime('%m%d_%H%M')}"

def generate_from_pattern(adjectives: List[str], nouns: List[str]) -> str:
    """Internal helper that constructs a username based on config patterns.
    
    Args:
        adjectives: A list of adjectives to choose from.
        nouns: A list of nouns to choose from.
        
    Returns:
        str: A randomly generated username.
    """
    patterns = get_config_value('patterns', ["{adjective}{noun}{number}"])
    pattern = random.choice(patterns)
    
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    num = str(random.randint(1, 999))
    
    # Simple template replacement for flexible combinations
    result = pattern.replace("{adjective}", adj)\
                    .replace("{noun}", noun)\
                    .replace("{number}", num)
    return result

def generate_retro_username() -> str:
    """Generates a retro-style username using predefined words.
    
    Returns:
        str: A username inspired by early internet conventions.
    """
    retro_conf = get_config_value('retro_words', {})
    adjectives = retro_conf.get('adjectives', ['Retro'])
    nouns = retro_conf.get('nouns', ['User'])
    return generate_from_pattern(adjectives, nouns)

def generate_vibe_username(vibe: str) -> str:
    """Generates a username based on a specific 'vibe' or theme.
    
    Args:
        vibe: The theme name (e.g., 'cyber', 'fantasy').
        
    Raises:
        ValidationError: If the requested vibe does not exist in the config.
        
    Returns:
        str: A themed username.
    """
    vibes_conf = get_config_value('vibes', {})
    
    if vibe not in vibes_conf:
        available = list(vibes_conf.keys())
        raise ValidationError(f"Invalid vibe '{vibe}'. Available: {available}")
        
    data = vibes_conf[vibe]
    return generate_from_pattern(data['adjectives'], data['nouns'])

def generate_profession_username(profession: str) -> str:
    """Generates a username based on professional titles.
    
    Args:
        profession: The job title/category.
        
    Raises:
        ValidationError: If the profession does not exist in the config.
        
    Returns:
        str: A career-inspired username.
    """
    prof_conf = get_config_value('professions', {})
    
    if profession not in prof_conf:
        available = list(prof_conf.keys())
        raise ValidationError(f"Invalid profession '{profession}'. Available: {available}")

    data = prof_conf[profession]
    return generate_from_pattern(data['adjectives'], data['nouns'])

def generate_mythology_username(pantheon: str = "greek") -> str:
    """Generates a username inspired by mythology.
    
    Args:
        pantheon: The mythology origin (e.g., 'greek', 'norse').
        
    Returns:
        str: A mythological name combined with random patterns.
    """
    myth_conf = get_config_value('mythology', {})
    
    # Random selection logic if pantheon is missing or requested as 'random'
    if pantheon == 'random' or pantheon not in myth_conf:
        pantheon = random.choice(list(myth_conf.keys())) if myth_conf else None
        
    if not pantheon:
        return f"Legend{random.randint(1,99)}"

    names = myth_conf.get(pantheon, [])
    if not names:
        return f"Zeus{random.randint(1,99)}"
        
    god_name = random.choice(names)
    patterns = ["{god}", "The{god}", "{god}_{number}", "{god}TheGreat"]
    pattern = random.choice(patterns)
    
    return pattern.replace("{god}", god_name).replace("{number}", str(random.randint(1, 99)))

def generate_keyword_username(keywords: List[str]) -> str:
    """Combines user-provided keywords into a single username.
    
    Args:
        keywords: A list of words to mix.
        
    Raises:
        ValidationError: If keywords list is empty.
        
    Returns:
        str: A combined keyword username.
    """
    if not keywords:
        raise ValidationError("Keywords list cannot be empty.")
        
    if len(keywords) == 1:
        base = keywords[0]
    else:
        w1, w2 = random.sample(keywords, 2)
        base = w1 + w2.capitalize()
        
    return f"{base}{random.randint(10, 99)}"

def generate_standard_username(base_word: str = "user") -> str:
    """Default generation logic when no specific strategy is selected.
    
    Args:
        base_word: The starting seed word.
        
    Returns:
        str: A basic 'word + number' username.
    """
    return f"{base_word}{random.randint(100, 999)}"

def generate_base_username(args) -> str:
    """Factory method that dispatches the generation request to the correct function.
    
    Args:
        args: Parsed CLI argument namespace.
        
    Returns:
        str: The raw base username (before modifiers).
    """
    if args.timestamp:
        return generate_timestamp_username(args.base_word)
    elif args.retro:
        return generate_retro_username()
    elif args.vibe:
        return generate_vibe_username(args.vibe)
    elif args.keywords:
        return generate_keyword_username(args.keywords)
    elif args.profession:
        return generate_profession_username(args.profession)
    elif getattr(args, 'mythology', False):
        m_val = args.mythology if isinstance(args.mythology, str) else 'random'
        return generate_mythology_username(m_val)
    else:
        return generate_standard_username(args.base_word)
