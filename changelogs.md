# Changelog - Advanced Username Generator

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
