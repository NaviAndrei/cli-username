#!/usr/bin/env python3
"""
Entry point wrapper for the Username Generator.
This script redirects execution to the modularized package.
"""
import sys
from pathlib import Path

# Add current directory to sys.path to ensure the 'username_generator' package is importable
sys.path.append(str(Path(__file__).parent))

try:
    from username_generator.cli import main
except ImportError as e:
    print(f"Critical Error: Cannot import 'username_generator' package.\nDetails: {e}")
    sys.exit(1)

if __name__ == "__main__":
    main()
