# Advanced Username Generator

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful, modularized Python CLI tool designed to generate unique and memorable online identities. Built with SOLID principles and a focus on clean code, this generator offers multiple strategies and dynamic modifiers to suit any digital platform.

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
The **Advanced Username Generator** transforms the mundane task of choosing a handle into a creative experience. Whether you need a persona for gaming, professional coding, or social media, this tool provides diverse algorithms and real-time text transformations to ensure your name stands out.

##  Key Features
- **Multiple Generation Strategies**:
    - `Timestamp`: Unique names based on current date and time.
    - `Retro`: Classic internet style (Adjective + Noun + Number).
    - `Vibe`: Themed identities like *Cyber*, *Fantasy*, *Scifi*, or *Nature*.
    - `Profession`: Tailored usernames for *Developers*, *Designers*, and *Writers*.
    - `Mythology`: Names inspired by *Greek*, *Norse*, and *Egyptian* pantheons.
    - `Keywords`: Flexible combinations of your own seed words.
- **Dynamic Text Modifiers**:
    - **Leet Speak**: Automatic character substitution (e.g., `a` -> `4`).
    - **Prefix/Suffix injection**: Add status words like `The`, `Master`, or `Real`.
    - **Special Character Insertion**: Add `_`, `.`, or `-` for a professional look.
    - **Length Enforcement**: Perfect fit for any platform's constraints (truncation or padding).

##  System Architecture
The project follows a modular structure to ensure maintainability and testability:

```text
username_generator/
├── username.py             # Entry point wrapper script
├── config.json             # External vocabulary and leet mappings
└── username_generator/     # Core application package
    ├── cli.py              # CLI Interface and argument parsing
    ├── core.py             # Central generation logic (Factory pattern)
    ├── config.py           # Config loader with LRU caching
    ├── modifiers.py        # Text transformation algorithms
    ├── exceptions.py       # Package-specific custom exceptions
    └── __init__.py         # Package identification and versioning
```

##  Installation & Setup

### Prerequisites
- Python 3.9 or higher

### Step-by-Step Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/username_generator.git
   cd username_generator
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Verify Configuration**:
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
- **`core.py`**: Implements specialized generators that pull data from the global config and apply dynamic templates.
- **`modifiers.py`**: Pure functions for atomic text operations (e.g., `strip_numbers`, `apply_special_chars`).
- **`config.py`**: Built-in efficient config distribution using `functools.lru_cache` to minimize disk access.

---

##  Configuration (config.json)
The `config.json` file serves as the application's "brain". It allows you to customize the entire vocabulary (adjectives, nouns, gods, profession patterns) without touching a single line of Python code.

##  Contributing
Contributions are welcome! If you'd like to improve the Advanced Username Generator, please follow these steps:

1. **Fork the Project** (click the Fork button at the top right of this page).
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`).
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`).
4. **Push to the Branch** (`git push origin feature/AmazingFeature`).
5. **Open a Pull Request**.

Please ensure your code follows PEP 8 standards and includes appropriate docstrings.

---
*Developed with modern Python standards (PEP 8, Type Hinting, Google Docstrings).*
