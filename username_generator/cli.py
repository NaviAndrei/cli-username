import argparse
import sys
import csv
import json
from typing import List, Optional

# Relative imports for package/module execution
from .config import get_config_value, load_config
from .core import generate_base_username
from .modifiers import (
    apply_leet_speak, 
    apply_prefix_suffix, 
    apply_special_chars, 
    strip_numbers, 
    enforce_length
)
from .checker import check_username_availability
from .exceptions import UsernameGeneratorError

def setup_parser() -> argparse.ArgumentParser:
    """Configures an organized CLI parser with logical groups.
    
    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Advanced Username Generator - Create unique online identities.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Example: python username.py --count 5 --vibe tech --use-leet"
    )

    # Load configuration for dynamic choices
    try:
        load_config()
    except Exception:
        pass

    # GROUP 1: Basic Configuration
    base_group = parser.add_argument_group("Basic Settings")
    base_group.add_argument("--count", type=int, default=1, metavar="NR", help="Number of usernames to generate.")
    base_group.add_argument("--base-word", default="user", metavar="WORD", help="Base word for generation (if no special mode is used).")

    # GROUP 2: Generation Strategies (Mutually Exclusive)
    gen_group = parser.add_argument_group("Generation Strategies (choose one)")
    exclusive = gen_group.add_mutually_exclusive_group()
    
    exclusive.add_argument("--timestamp", action="store_true", help="Generate a unique name based on current timestamp.")
    exclusive.add_argument("--retro", action="store_true", help="Classic internet style (Name + Random numbers).")
    
    vibes_keys = list(get_config_value('vibes', {}).keys())
    exclusive.add_argument("--vibe", choices=vibes_keys, metavar="STYLE", help="Themed username styles.")
    
    prof_keys = list(get_config_value('professions', {}).keys())
    exclusive.add_argument("--profession", choices=prof_keys, metavar="PROFESSION", help="Professional area based usernames.")
    
    myth_keys = list(get_config_value('mythology', {}).keys())
    exclusive.add_argument("--mythology", nargs='?', const='random', choices=myth_keys + ['random'], metavar="MYTH", help="Mythological pantheon names (e.g., greek, norse).")
    
    exclusive.add_argument("--keywords", nargs='+', metavar="KEYWORDS", help="Combine your own list of keywords.")

    # GROUP 3: Post-Generation Modifiers
    mod_group = parser.add_argument_group("Effects and Adjustments")
    mod_group.add_argument("--use-leet", action="store_true", help="Transform text into Leet Speak (3l33t).")
    mod_group.add_argument("--use-prefix-suffix", action="store_true", help="Add catchy prefixes/suffixes (e.g., 'The', 'Real', 'xX').")
    mod_group.add_argument("--no-numbers", action="store_true", help="Remove all digits from the final result.")
    mod_group.add_argument("--use-special-chars", action="store_true", help="Insert special characters (._-) for a 'pro' look.")
    mod_group.add_argument("--length", type=int, default=0, metavar="LEN", help="Enforce a fixed length (truncate or pad if necessary).")

    # GROUP 4: Export and Saving
    export_group = parser.add_argument_group("Data Export")
    export_group.add_argument("--output", metavar="FILE", help="Path to the output file.")
    export_group.add_argument("--format", choices=['txt', 'json', 'csv'], default='txt', help="Output file format.")

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
        
    if args.length > 0:
        username = enforce_length(username, args.length)
        
    return username

def save_output(usernames: List[str], args: argparse.Namespace):
    """Handles saving usernames to a file or printing them to stdout.
    
    Args:
        usernames: List of generated usernames.
        args: Parsed CLI arguments containing output settings.
    """
    if not args.output:
        for u in usernames:
            print(f"Generated: {u}")
        return

    try:
        with open(args.output, 'w', newline='', encoding='utf-8') as f:
            if args.format == 'json':
                json.dump(usernames, f, indent=2)
            elif args.format == 'csv':
                writer = csv.writer(f)
                for u in usernames:
                    writer.writerow([u])
            else:
                for u in usernames:
                    f.write(u + '\n')
        print(f"Successfully saved {len(usernames)} usernames to {args.output}")
    except IOError as e:
        print(f"Write error: {e}", file=sys.stderr)

def main():
    """Main entry point for the CLI application."""
    parser = setup_parser()
    args = parser.parse_args()
    
    results = []
    
    try:
        sync_platforms = args.sync.split(",") if args.sync else []
        
        found_count = 0
        attempts = 0
        max_attempts = args.count * 50 # Prevent infinite loops
        
        while found_count < args.count and attempts < max_attempts:
            attempts += 1
            base = generate_base_username(args)
            final = process_username(base, args)
            
            # Logic for Sync Mode
            if sync_platforms:
                print(f"🔄 [Attempt {attempts}] Sync-checking: {final}", end="\r")
                checker_results = check_username_availability(final, sync_platforms)
                
                # Check if available on ALL requested platforms
                is_fully_synced = all(status == "AVAILABLE" for status in checker_results.values())
                
                if is_fully_synced:
                    print(f"\n✨ Found Synced Handle: {final}")
                    for p, s in checker_results.items():
                        print(f"  - {p:12}: ✅ AVAILABLE")
                    results.append(final)
                    found_count += 1
                continue # Skip standard logic in sync mode
                
            # Logic for Standard or --check Mode
            results.append(final)
            found_count += 1
            
            if args.check:
                print(f"\nChecking availability for: {final}")
                checker_results = check_username_availability(final)
                for platform, status in checker_results.items():
                    if status == "AVAILABLE":
                        display = "✅ AVAILABLE"
                    elif status == "TAKEN":
                        display = "❌ TAKEN"
                    elif status == "BLOCKED/WAF":
                        display = "🛡️  BLOCKED (BOT PROTECTION)"
                    else:
                        display = f"⚠️  {status}"
                    print(f"  - {platform:12}: {display}")
            
        print(f"\nGeneration complete. ({attempts} attempts made)")
        save_output(results, args)
        
    except UsernameGeneratorError as e:
        print(f"Generation Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
