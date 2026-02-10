# Changelog - Advanced Username Generator

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.1] - 2026-02-10
### Added
- **Phonetic Rhymes**: Integrated `pronouncing` library (CMU Dict) for accurate rhymes (e.g., "tough" vs "rough"). Falls back to suffix matching if unavailable.
- **Robust Configuration**: Migrated `config.py` to **Pydantic**.
  - **Schema Validation**: Ensures `patterns` match `{noun}/{adjective}` placeholders and structure is correct.
  - **Environment Overrides**: Supports `UG_PATTERNS`, `UG_VIBES_TECH` etc. env variables via `os.environ`.
- **Infinite Loop Protection**: `generate_from_pattern` now has a 100-attempt limit for rhyming/alliteration to prevent hangs. returns a warning if constraints can't be met.
- **Dependency Injection**: Introduced `GenerationContext` model in `core.py` to decouple generation logic from CLI arguments.

## [2.2.0] - 2026-02-09
### Added
- **Creative Filters**: New CLI arguments `--alliteration` (force same starting letter) and `--rhyme` (suffix matching).
- **Structure Control**: Flags `--only-nouns` and `--only-adjectives` to constrain username patterns.
- **Custom Separator**: Flag `--separator "..."` to replace standard underscores (e.g., `--separator "."`).
- **Interactive Mode**: Flag `--interactive` to regenerate usernames on the fly without restarting the script.
- **Randomized Leet Speak**: `config.json` now supports lists of leet substitutions for greater variety (e.g., `a` can be `4` or `@`).
- **Improved Leet Map**: Expanded substitution table to cover all alphabet letters.

## [2.1.0] - 2026-02-09
### Added
- **New Strategy: `--realname`**: Generate usernames from a real full name (e.g., "Ivan Andrei" → "IvanA50", "ivan.andrei").
- **New Strategy: `--anagram`**: Create usernames by rearranging letters of a word with CamelCase formatting.
- **New Modifier: `--alt-caps`**: Alternating uppercase/lowercase (CaSe StYlE) effect.
- **Strategy Combining**: `--vibe` and `--profession` can now be used together to merge word pools.
- **`--version` flag**: Displays the current tool version.
- **JSON Schema Validation**: `config.json` is now validated on load for required keys and types.
- **Duplicate Elimination**: Generated usernames are guaranteed unique within a single run.
- **Length Validation**: `--length` rejects values < 3 and warns for values > 32.
- **Extended Vocabulary**: Added 2 new professions (music, gamer), 2 new mythologies (japanese, celtic), 4 new patterns, expanded all word lists.
- **Extended Help**: CLI help now includes 15+ usage examples organized by category.

### Changed
- `--vibe` and `--profession` moved out of the mutually exclusive group to allow combining.
- Complete type hints on all function signatures across all modules.
- Version bumped to 2.1.0 in `__init__.py` and `pyproject.toml`.

---

## [2.0.0] - 2026-02-04
### Added
- **Cross-Platform Sync Orchestrator**: New logic to generate names until a globally available handle is found.
- **Parallel Multi-threading**: Rewrote `checker.py` with `ThreadPoolExecutor` for high-speed concurrent checks.
- **CLI Flag `--sync`**: Allows specifying a list of platforms for mandatory availability (e.g., `--sync github,reddit`).
- **Smart Progress Tracking**: Real-time attempt counter in the terminal during the sync process.

### Changed
- Improved `checker.py` efficiency with a shared `requests.Session`.
- Refactored `cli.py` main loop into a while-based orchestrator.

---

## [1.1.0] - 2026-02-04
### Added
- **Availability Checker**: New feature to check username availability on Top 10 Social Platforms + GitHub.
- **CLI Flag `--check`**: Integrated automation for social media availability lookup.
- **Dependency `requests`**: Added to manage HTTP calls.
- **Tier 1 Targets**: Support for Facebook, YouTube, WhatsApp (via template), Instagram, TikTok, X, Snapchat, Reddit, Telegram, Threads, and Twitch.

### Changed
- Refactored `cli.py` to support post-generation network tasks.
- Updated `config.json` with a dedicated `check_targets` registry.

---

## [1.0.0] - 2026-02-04
### Added
- Initial modularized release.
- Factory pattern for username generation (`core.py`).
- Advanced formatting (Leet Speak, Special Chars, Length Enforce).
- Multi-language README (EN/RO).
- GitHub Actions CI Pipeline.
