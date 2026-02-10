import argparse
import random
import datetime
import logging
from typing import List, Optional, Any
from pydantic import BaseModel

from .config import get_config_value
from .exceptions import ValidationError
from .modifiers import is_alliterative, is_rhyming

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class GenerationContext(BaseModel):
    """Context object holding generation constraints and options."""
    only_nouns: bool = False
    only_adjectives: bool = False
    alliteration: bool = False
    rhyme: bool = False
    separator: Optional[str] = None

def generate_timestamp_username(base_word: str = "Owl") -> str:
    """Generates a username formatted with the current timestamp.
    
    Args:
        base_word: The prefix for the timestamped username.
        
    Returns:
        str: Username like "Word_MMDD_HHMM".
    """
    now = datetime.datetime.now()
    return f"{base_word}_{now.strftime('%m%d_%H%M')}"

def generate_from_pattern(adjectives: List[str], nouns: List[str], context: GenerationContext = None) -> str:
    """Constructs a username based on patterns and context constraints.
    
    Features infinite loop protection: retries up to 100 times to satisfy
    rhyme/alliteration constraints, then falls back with a warning.
    Args:
        adjectives: List of available adjectives.
        nouns: List of available nouns.
        context: Optional generation context (constraints, separator).
        
    Returns:
        str: Constructed username.
    """
    context = context or GenerationContext()
    all_patterns = get_config_value('patterns', ["{adjective}{noun}{number}"])
    
    # --- 1. Filter Patterns ---
    if context.only_nouns:
        patterns = [p for p in all_patterns if "{noun}" in p and "{adjective}" not in p]
        if not patterns:
            patterns = ["{noun}{number}", "The{noun}", "Iam{noun}"] 
    elif context.only_adjectives:
        patterns = [p for p in all_patterns if "{adjective}" in p and "{noun}" not in p]
        if not patterns:
             patterns = ["{adjective}{number}", "Very{adjective}"]
    else:
        patterns = all_patterns

    pattern = random.choice(patterns)
    
    # --- 2. Word Selection (with Protected Retry) ---
    max_retries = 100
    adj, noun = "", ""
    
    # Constraints check
    need_check = context.alliteration or context.rhyme
    attempts = 0
    
    while attempts < max_retries:
        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        attempts += 1
        
        if not need_check:
            break
            
        valid = True
        if context.alliteration and not is_alliterative(adj, noun):
            valid = False
        if context.rhyme and not is_rhyming(adj, noun):
            valid = False
            
        if valid:
            break
    
    # Warning if constraints failed
    if need_check and attempts >= max_retries:
        logger.warning(f"Could not satisfy constraints (Rhyme={context.rhyme}, Allit={context.alliteration}) after {max_retries} attempts. Returning non-matching pair.")

    num = str(random.randint(1, 999))
    
    # --- 3. Apply Custom Separator ---
    if context.separator is not None:
        pattern = pattern.replace("_", context.separator)

    # --- 4. Final Construction ---
    result = pattern.replace("{adjective}", adj)\
                    .replace("{noun}", noun)\
                    .replace("{number}", num)
    return result

def generate_retro_username(context: GenerationContext = None) -> str:
    """Generates a retro-style username using predefined words.
    
    Args:
        context: Generation context.
        
    Returns:
        str: Retro username (e.g., "RetroUser99").
    """
    retro_conf = get_config_value('retro_words', {})
    adjectives = retro_conf.get('adjectives', ['Retro'])
    nouns = retro_conf.get('nouns', ['User'])
    return generate_from_pattern(adjectives, nouns, context)

def generate_vibe_username(vibe: str, context: GenerationContext = None) -> str:
    """Generates a username based on a specific 'vibe' or theme.
    
    Args:
        vibe: The theme key (e.g., 'tech', 'fantasy').
        context: Generation context.
        
    Returns:
        str: Vibe-themed username.
        
    Raises:
        ValidationError: If the vibe key is invalid.
    """
    vibes_conf = get_config_value('vibes', {})
    
    if vibe not in vibes_conf:
        available = list(vibes_conf.keys())
        raise ValidationError(f"Invalid vibe '{vibe}'. Available: {available}")
        
    data = vibes_conf[vibe]
    return generate_from_pattern(data['adjectives'], data['nouns'], context)

def generate_profession_username(profession: str, context: GenerationContext = None) -> str:
    """Generates a username based on professional titles.
    
    Args:
        profession: The profession key (e.g., 'developer').
        context: Generation context.
        
    Returns:
        str: Profession-themed username.
        
    Raises:
        ValidationError: If the profession key is invalid.
    """
    prof_conf = get_config_value('professions', {})
    
    if profession not in prof_conf:
        available = list(prof_conf.keys())
        raise ValidationError(f"Invalid profession '{profession}'. Available: {available}")

    data = prof_conf[profession]
    return generate_from_pattern(data['adjectives'], data['nouns'], context)

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

def generate_realname_username(full_name: str) -> str:
    """Generates creative usernames from a real full name.
    
    Args:
        full_name: The user's real name (e.g., "Ivan Alexandrescu").
        
    Raises:
        ValidationError: If the name is empty.
        
    Returns:
        str: A creative username derived from the real name.
    """
    if not full_name or not full_name.strip():
        raise ValidationError("Real name cannot be empty.")
    
    # Split name into components
    parts = full_name.strip().split()
    
    if len(parts) == 1:
        # Single word: generate simple variants
        name = parts[0]
        patterns = [
            f"{name}{random.randint(10, 99)}",
            f"The{name}",
            f"{name}_Official",
            f"Real{name}",
            f"x{name}x",
        ]
        return random.choice(patterns)
    
    # Extract first and last name
    first = parts[0]
    last = parts[-1]
    
    # Initials for short variants
    first_initial = first[0].upper()
    last_initial = last[0].upper()
    
    # Varied combination patterns
    patterns = [
        # Classic combinations
        f"{first}{last}",
        f"{first}{last[:3]}",
        f"{first[:3]}{last}",
        f"{first}_{last}",
        # With initials
        f"{first_initial}.{last}{random.randint(1, 99)}",
        f"{first}{last_initial}{random.randint(10, 99)}",
        f"{first_initial}{last_initial}_{random.randint(100, 999)}",
        # Modern style
        f"The{first}_{last_initial}",
        f"{first.lower()}.{last.lower()}",
        f"{last}{first[:2]}{random.randint(1, 99)}",
        # Shortened style
        f"{first[:2]}{last[:4]}",
        f"{last[:3]}{first[:3]}_{random.randint(10, 99)}",
    ]
    
    return random.choice(patterns)

def generate_anagram_username(word: str) -> str:
    """Generates a username by rearranging the letters of a word.
    
    Creates a random anagram from the input, then applies CamelCase
    formatting for readability.
    
    Args:
        word: The source word to create an anagram from.
        
    Raises:
        ValidationError: If the word is too short (less than 3 characters).
        
    Returns:
        str: An anagram-based username.
    """
    # Filter only letters from input
    letters_only = [c for c in word if c.isalpha()]
    
    if len(letters_only) < 3:
        raise ValidationError("Word must have at least 3 letters for anagram generation.")
    
    # Shuffle letters to create a random permutation
    shuffled = letters_only.copy()
    
    # Try max 20 times to avoid original word
    max_shuffles = 20
    for _ in range(max_shuffles):
        random.shuffle(shuffled)
        if ''.join(shuffled).lower() != ''.join(letters_only).lower():
            break
    
    # Build username from anagram with CamelCase
    anagram = ''.join(shuffled)
    
    # Apply CamelCase: capitalize every 3-5 letters
    result = []
    chunk_size = random.randint(3, min(5, len(anagram)))
    for i, char in enumerate(anagram):
        if i % chunk_size == 0:
            result.append(char.upper())
        else:
            result.append(char.lower())
    
    final = ''.join(result)
    
    # Optionally add numeric suffix for uniqueness
    if random.choice([True, False]):
        final += str(random.randint(1, 99))
    
    return final

def generate_standard_username(base_word: str = "user") -> str:
    """Default generation logic when no specific strategy is selected.
    
    Args:
        base_word: The starting seed word.
        
    Returns:
        str: A basic 'word + number' username.
    """
    return f"{base_word}{random.randint(100, 999)}"

def generate_combined_username(vibe: str, profession: str, context: GenerationContext = None) -> str:
    """Generates a username by merging word pools from a vibe and a profession.
    
    Args:
        vibe: The theme key.
        profession: The profession key.
        context: Generation context.
        
    Returns:
        str: Mixed-strategy username.
        
    Raises:
        ValidationError: If keys are invalid.
    """
    vibes_conf = get_config_value('vibes', {})
    prof_conf = get_config_value('professions', {})
    
    if vibe not in vibes_conf:
        raise ValidationError(f"Invalid vibe '{vibe}'. Available: {list(vibes_conf.keys())}")
    if profession not in prof_conf:
        raise ValidationError(f"Invalid profession '{profession}'. Available: {list(prof_conf.keys())}")
    
    vibe_data = vibes_conf[vibe]
    prof_data = prof_conf[profession]
    
    if random.choice([True, False]):
        adjectives = vibe_data['adjectives']
        nouns = prof_data['nouns']
    else:
        adjectives = prof_data['adjectives']
        nouns = vibe_data['nouns']
    
    return generate_from_pattern(adjectives, nouns, context)

def generate_base_username(args: argparse.Namespace) -> str:
    """Factory method that dispatches the generation request to the correct function.
    
    Args:
        args: Parsed CLI argument namespace.
        
    Returns:
        str: The raw base username (before modifiers).
    """
    # Construct context from arguments
    context = GenerationContext(
        only_nouns=getattr(args, 'only_nouns', False),
        only_adjectives=getattr(args, 'only_adjectives', False),
        alliteration=getattr(args, 'alliteration', False),
        rhyme=getattr(args, 'rhyme', False),
        separator=getattr(args, 'separator', None)
    )

    # Combined mode: --vibe + --profession together
    if args.vibe and args.profession:
        return generate_combined_username(args.vibe, args.profession, context)
    elif args.timestamp:
        return generate_timestamp_username(args.base_word)
    elif args.retro:
        return generate_retro_username(context)
    elif args.vibe:
        return generate_vibe_username(args.vibe, context)
    elif args.profession:
        return generate_profession_username(args.profession, context)
    elif args.keywords:
        return generate_keyword_username(args.keywords)
    elif getattr(args, 'mythology', False):
        m_val = args.mythology if isinstance(args.mythology, str) else 'random'
        return generate_mythology_username(m_val)
    elif args.realname:
        return generate_realname_username(args.realname)
    elif args.anagram:
        return generate_anagram_username(args.anagram)
    else:
        return generate_standard_username(args.base_word)


