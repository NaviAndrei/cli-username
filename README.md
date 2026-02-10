# Advanced Username Generator

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> [🇷🇴 **Read this in Romanian / Citește în Română**](README_RO.md)

A powerful, modularized Python CLI tool designed to generate unique and memorable online identities. Built with SOLID principles, robust architecture (Pydantic), and a focus on clean code, this generator offers multiple strategies and dynamic modifiers to suit any digital platform.

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Technical Reference](#technical-reference)
- [Configuration (config.json)](#configuration-configjson)
- [Contributing](#contributing)

---

##  Overview
The **Advanced Username Generator** transforms the mundane task of choosing a handle into a creative experience. Whether you need a persona for gaming, professional coding, or social media, this tool provides diverse algorithms, phonetic constraints (rhymes/alliteration), and real-time text transformations to ensure your name stands out.

##  Key Features
- **Multiple Generation Strategies**:
    - `Timestamp`: Unique names based on current date and time.
    - `Retro`: Classic internet style (Adjective + Noun + Number).
    - `Vibe` & `Profession`: Themed identities like *Cyber*, *Fantasy* or *Developer*. **Can be combined!**
    - `Mythology`: Names inspired by *Greek*, *Norse*, *Celtic*, and *Japanese* pantheons.
    - `Keywords`: Flexible combinations of your own seed words.

- **Creative Constraints & Logic (New in v2.2)**:
    - **Phonetic Rhymes**: Uses CMU Dict to find words that *actually* rhyme (e.g., `--rhyme`).
    - **Alliteration**: Forces adjectives and nouns to start with the same letter (`--alliteration`).
    - **Structure Control**: Filter patterns to use `--only-nouns` or `--only-adjectives`.
    - **Custom Separator**: Replace standard underscores with your own style (e.g., `--separator "."`).
    - **Interactive Mode**: Regenerate results on the fly without restarting the script (`--interactive`).
    - **Infinite Loop Protection**: Smart retries that prevent hanging when constraints are too strict.

- **Availability & OSINT Checker**: 
    - **Live Verification**: Instantly check if names are free on top platforms like *GitHub*, *Reddit*, *Instagram*.
    - **Smart Content Detection**: Scans page content for "Not Found" signatures.
    - **Cross-Platform Sync**: Use `--sync` to find usernames available on *all* chosen platforms.

- **Dynamic Text Modifiers**:
    - **Leet Speak**: Randomized character substitution (e.g., `a` -> `4` or `@`).
    - **Prefix/Suffix injection**: Add status words like `The`, `Master`.
    - **Special Character Insertion**: Add `_`, `.`, or `-` for a professional look.
    - **Length Enforcement**: Perfect fit for platform constraints.

##  System Architecture
The project follows a modular structure to ensure maintainability and testability:

```text
username_generator/
├── username.py             # Entry point wrapper script
├── config.json             # External vocabulary and leet mappings
└── username_generator/     # Core application package
    ├── cli.py              # CLI Interface, Orchestration, and argument parsing
    ├── core.py             # Central logic with Dependency Injection (GenerationContext)
    ├── checker.py          # Parallel Availability Checker (Multi-threaded)
    ├── config.py           # Configuration Manager (Pydantic-based validation & caching)
    ├── modifiers.py        # Text algorithms & Phonetic functions
    ├── exceptions.py       # Custom exceptions
    └── __init__.py         # Package identification
```

##  Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Python 3.10 or higher

### Step-by-Step Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/NaviAndrei/cli-username.git
   cd cli-username
   git clone https://github.com/NaviAndrei/cli-username.git
   cd cli-username
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install pydantic pydantic-settings pronouncing requests
   # OR
   pip install .
   ```

4. **Verify Configuration**:
   Ensure `config.json` is located in the project root directory.

##  Usage Guide

### Simple Run
```powershell
python username.py --count 3 --base-word Archer
```

### Advanced Examples
*   **Cyberpunk style with Leet Speak**:
    ```powershell
    python username.py --count 5 --vibe cyber --use-leet
    ```
*   **Mythological Names (Random Pantheon)**:
    ```powershell
    python username.py --mythology
    ```
*   **Combining Keywords with Special Characters**:
    ```powershell
    python username.py --keywords Matrix Shadow --use-special-chars
    ```

### Exporting Results
Save generated names to `txt`, `json`, or `csv` files:
```powershell
python username.py --count 10 --vibe fantasy --output handles.json --format json
```

##  Technical Reference

### Core Modules
- **`cli.py`**: Leverages `argparse` to provide a robust user interface. Features organized help groups and input validation.
- **`core.py`**: Uses **Dependency Injection** via `GenerationContext` to pass constraints. Implements infinite loop protection.
- **`modifiers.py`**: Contains `pronouncing` integration for rhymes and helper functions for string manipulation.
- **`config.py`**: Uses **Pydantic** for strict schema validation and environment variable overrides (`UG_PATTERNS` etc.).

---

##  Configuration (config.json)
The `config.json` file serves as the application's "brain". It allows you to customize the entire vocabulary (adjectives, nouns, gods, profession patterns) without touching a single line of Python code.

##  Contributing
Contributions are welcome! If you'd like to improve the Advanced Username Generator, please follow these steps:

1. **Fork the Project**.
2. **Create your Feature Branch**.
3. **Commit your Changes**.
4. **Push to the Branch**.
5. **Open a Pull Request**.

Please ensure your code follows PEP 8 standards and includes appropriate docstrings.

---
*Developed with modern Python standards (PEP 8, Type Hinting, Google Docstrings).*
