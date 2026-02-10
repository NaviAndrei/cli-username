import argparse
import sys
import csv
import json
from typing import List, Optional

# Relative imports for package/module execution
from . import __version__
from .config import get_config_value, load_config
from .core import generate_base_username
from .modifiers import (
    apply_leet_speak, 
    apply_prefix_suffix, 
    apply_special_chars, 
    strip_numbers, 
    enforce_length,
    apply_alt_caps
)
from .checker import check_username_availability
from .checker import check_username_availability
from .exceptions import UsernameGeneratorError

def setup_parser() -> argparse.ArgumentParser:
    """Configures an organized CLI parser with logical groups.
    
    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    # Define examples in a readable format
    examples = """
Examples:
  Basic Usage:
    python username.py --base-word Dragon --count 5
    python username.py --retro --count 3
    python username.py --timestamp

  Themed Styles (--vibe):
    python username.py --vibe tech --count 5
    python username.py --vibe mystical --use-leet
    python username.py --vibe warrior --use-prefix-suffix

  Professional Usernames:
    python username.py --profession developer --count 3
    python username.py --profession designer --use-special-chars
    python username.py --profession gamer --only-nouns


  Mythological Names:
    python username.py --mythology greek --count 5
    python username.py --mythology norse --use-leet

  Custom Keywords:
    python username.py --keywords Wolf Shadow Night --count 5
    python username.py --keywords Code Ninja Master --use-prefix-suffix

  Applying Effects:
    python username.py --vibe tech --use-leet --use-prefix-suffix
    python username.py --base-word Ace --use-special-chars --length 12

  Export to File:
    python username.py --vibe scifi --count 10 --output names.txt
    python username.py --mythology --count 20 --output data.json --format json
    python username.py --retro --count 15 --output export.csv --format csv

  Nickname from Real Name (--realname):
    python username.py --realname "Ivan Alexandrescu" --count 5
    python username.py --realname "Elena Popescu" --use-prefix-suffix

  Anagram Mode (--anagram):
    python username.py --anagram "Alexander" --count 5
    python username.py --anagram "Phoenix" --use-leet

  Alternating Caps (--alt-caps):
    python username.py --vibe tech --alt-caps --count 3
    python username.py --base-word Shadow --alt-caps

  Availability Check:
    python username.py --vibe tech --count 5 --check
    python username.py --keywords Pro Gamer --check --sync twitter,github

  Combining Strategies (--vibe + --profession):
    python username.py --vibe tech --profession developer --count 5
    python username.py --vibe warrior --profession gamer --use-leet --count 3

  Advanced Combo:
    python username.py --keywords Cyber Phoenix --use-leet --use-prefix-suffix --use-special-chars --count 10 --output pro.json --format json
"""
    
    parser = argparse.ArgumentParser(
        description="Advanced Username Generator - Create unique online identities.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=examples
    )
    
    # Flag --version: display current version
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    # Load configuration for dynamic choices
    try:
        load_config()
    except Exception:
        pass

    # GROUP 1: Basic Configuration
    base_group = parser.add_argument_group("Basic Settings")
    base_group.add_argument("--count", type=int, default=1, metavar="NR", help="Number of usernames to generate.")
    base_group.add_argument("--base-word", default="user", metavar="WORD", help="Base word for generation (if no special mode is used).")

    # GROUP 2: Generation Strategies
    # --vibe and --profession are separate to allow combining them
    gen_group = parser.add_argument_group("Generation Strategies (choose one, or combine --vibe + --profession)")
    exclusive = gen_group.add_mutually_exclusive_group()
    
    exclusive.add_argument("--timestamp", action="store_true", help="Generate a unique name based on current timestamp.")
    exclusive.add_argument("--retro", action="store_true", help="Classic internet style (Name + Random numbers).")
    
    myth_keys = list(get_config_value('mythology', {}).keys())
    exclusive.add_argument("--mythology", nargs='?', const='random', choices=myth_keys + ['random'], metavar="MYTH", help="Mythological pantheon names (e.g., greek, norse).")
    
    exclusive.add_argument("--keywords", nargs='+', metavar="KEYWORDS", help="Combine your own list of keywords.")
    exclusive.add_argument("--realname", metavar="NAME", help="Generate username from a real name (e.g., 'Ivan Alexandrescu').")
    exclusive.add_argument("--anagram", metavar="WORD", help="Generate username by rearranging letters of a word.")
    
    # --vibe and --profession are outside the exclusive group (can be combined)
    vibes_keys = list(get_config_value('vibes', {}).keys())
    gen_group.add_argument("--vibe", choices=vibes_keys, metavar="STYLE", help="Themed username styles. Can be combined with --profession.")
    
    prof_keys = list(get_config_value('professions', {}).keys())
    gen_group.add_argument("--profession", choices=prof_keys, metavar="PROFESSION", help="Professional area based usernames. Can be combined with --vibe.")

    # GROUP 3: Post-Generation Modifiers
    mod_group = parser.add_argument_group("Effects and Adjustments")
    mod_group.add_argument("--use-leet", action="store_true", help="Transform text into Leet Speak (3l33t).")
    mod_group.add_argument("--use-prefix-suffix", action="store_true", help="Add catchy prefixes/suffixes (e.g., 'The', 'Real', 'xX').")
    mod_group.add_argument("--no-numbers", action="store_true", help="Remove all digits from the final result.")
    mod_group.add_argument("--use-special-chars", action="store_true", help="Insert special characters (._-) for a 'pro' look.")
    mod_group.add_argument("--alt-caps", action="store_true", help="Alternate upper/lowercase on each letter (CaSe StYlE).")
    mod_group.add_argument("--length", type=int, default=0, metavar="LEN", help="Enforce a fixed length (truncate or pad if necessary).")

    # Structure filters (Mutually Exclusive)
    struct_group = mod_group.add_mutually_exclusive_group()
    struct_group.add_argument("--only-nouns", action="store_true", help="Use ONLY noun patterns (e.g., 'Wizard99', 'TheLord').")
    struct_group.add_argument("--only-adjectives", action="store_true", help="Use ONLY adjective patterns (e.g., 'SilentDark', 'EpicReal').")


    # GROUP 4: Export and Saving
    export_group = parser.add_argument_group("Data Export")
    export_group.add_argument("--output", metavar="FILE", help="Path to the output file.")
    export_group.add_argument("--format", choices=['txt', 'json', 'csv'], default='txt', help="Output file format.")

    # GROUP 5: Availability Check
    check_group = parser.add_argument_group("Availability Check")
    check_group.add_argument("--check", action="store_true", help="Check if the generated usernames are available on social platforms.")
    check_group.add_argument("--sync", metavar="PLATFORMS", help="Comma-separated list of platforms. Only returns usernames available on ALL specified sites.")

    # GROUP 5: Availability Check
    check_group = parser.add_argument_group("Availability Check")
    check_group.add_argument("--check", action="store_true", help="Check if the generated usernames are available on social platforms.")
    check_group.add_argument("--sync", metavar="PLATFORMS", help="Comma-separated list of platforms. Only returns usernames available on ALL specified sites.")

    return parser

def process_username(username: str, args: argparse.Namespace) -> str:
    """Applies a chain of modifiers to a username.
    
    Args:
        username: The base username to modify.
        args: Parsed CLI arguments.
        
    Returns:
        str: The transformed username.
    """
    if args.timestamp:
        return username

    if args.use_leet:
        username = apply_leet_speak(username)
    
    if args.use_prefix_suffix:
        username = apply_prefix_suffix(username)
        
    if args.no_numbers:
        username = strip_numbers(username)
        
    if args.use_special_chars:
        username = apply_special_chars(username)
    
    if args.alt_caps:
        username = apply_alt_caps(username)
        
    if args.length > 0:
        username = enforce_length(username, args.length)
        
    return username

def generate_and_print(args: argparse.Namespace) -> List[str]:
    """Runs the generation loop based on count and prints results to stdout.
    
    Args:
        args: Parsed CLI arguments containing count and generation settings.
        
    Returns:
        List[str]: The list of generated usernames.
    """
    generated_list = []
    
    print(f"\n--- Generating {args.count} usernames ---\n")
    
    for i in range(args.count):
        try:
            # 1. Generate Base
            base = generate_base_username(args)
            
            # 2. Apply Modifiers
            final = process_username(base, args)
            
            generated_list.append(final)
            print(f"[{i+1}] {final}")
            
        except ValidationError as e:
            print(f"❌ Error: {e}", file=sys.stderr)
        except Exception as e:
            print(f"❌ Unexpected Error: {e}", file=sys.stderr)
            
    return generated_list

def validate_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    """Validates conflicting argument combinations not handled by mutual exclusion groups.
    
    Args:
        args: Parsed arguments.
        parser: The argument parser instance for raising errors.
    """
    if args.sync and not args.check:
        parser.error("The --sync argument requires --check to be enabled.")

def main() -> None:
    """Main entry point for the CLI application."""
    parser = setup_parser()
    args = parser.parse_args()
    
    validate_args(args, parser)
    
    try:
        load_config()
    except Exception as e:
        print(f"❌ Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)

    while True:
        usernames = generate_and_print(args)
        
        # Check Availability if requested
        if args.check:
            print("\n🔎 Checking availability...")
            check_username_availability(usernames[0]) # Limitation: current checker supports single username or list?
            # Checker supports str -> dict. If we want list, we must iterate.
            # Adapting checker to accept list? No, iterating here.
            for u in usernames:
                 print(f"Checking {u}...")
                 res = check_username_availability(u)
                 # Simplu print
                 available = [p for p, s in res.items() if s == "AVAILABLE"]
                 if available:
                     print(f"  ✅ Available on: {', '.join(available)}")
                 else:
                     print("  ❌ Taken/Unknown on popular platforms.")
        
        # Save to file if requested
        if args.output:
            try:
                # Append mode to avoid overwriting previous sessions
                mode = 'a' if args.interactive else 'w'
                with open(args.output, mode, encoding="utf-8") as f:
                    for u in usernames:
                        f.write(u + "\n")
                print(f"\n✅ Saved to {args.output}")
            except IOError as e:
                print(f"❌ Output Error: {e}", file=sys.stderr)

        if not args.interactive:
            break
            
        # Interactive Loop
        print("\nOPTIONS: [r]egenerate | [q]uit | enter index to select (mock)")
        choice = input("Your choice > ").strip().lower()
        
        if choice == 'q':
            print("Bye! 👋")
            break
        elif choice == 'r':
            print("\n🔄 Regenerating...")
            continue
        else:
            print(f"Selection '{choice}' noted.")
            # Continue the loop, maybe they want to regenerate after selection?
            # Usually after selection we quit or stay in menu. Staying in menu.
            print("Press 'r' to generate more or 'q' to quit.")
            next_action = input("> ").strip().lower()
            if next_action == 'q':
                break

if __name__ == "__main__":
    main()
