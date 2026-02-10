#  Advanced Username Generator

> [🇬🇧 **Read this in English / Citește în Engleză**](README.md)

Un instrument Command Line Interface (CLI) puternic și modularizat, scris în Python, conceput pentru generarea de identități online unice și memorabile. Proiectul folosește principii de design SOLID, o arhitectură robustă (Pydantic) și o structură extensibilă pentru a oferi o varietate de strategii de generare.

---

##  Cuprins
- [Descriere Generală](#descriere-generală)
- [Funcționalități Conceptuale](#funcționalități-conceptuale)
- [Arhitectura Sistemului](#arhitectura-sistemului)
- [Instalare și Configurare](#instalare-și-configurare)
- [Ghid de Utilizare](#ghid-de-utilizare)
- [Referință Tehnică](#referință-tehnică)
- [Configurare Externă (config.json)](#configurare-externă-configjson)
- [Contribuție](#contribuție)

---

##  Descriere Generală
**Advanced Username Generator** transformă procesul banal de creare a unui nume de utilizator într-o experiență creativă. Fie că ai nevoie de un nume pentru gaming, social media sau medii profesionale, acest tool oferă algoritmi diversificați, constrângeri fonetice (rime/aliterații) și modificatori dinamici pentru a asigura unicitatea.

##  Funcționalități Conceptuale
- **Strategii Multiple de Generare**:
    - `Timestamp`: Bazat pe data și ora curentă.
    - `Retro`: Stilul clasic al internetului (adjectiv + substantiv + număr).
    - `Vibe` & `Profession`: Tematici precum *Cyber*, *Fantasy* sau *Developer*. **Pot fi combinate!**
    - `Mythology`: Nume inspirate din panteonul Grecesc, Nordi, Celtic și Japonez.
    - `Keywords`: Combină propriile tale cuvinte cheie.

- **Constrângeri Creative & Logică (Nou în v2.2)**:
    - **Rime Fonetice**: Folosește CMU Dict pentru a găsi cuvinte care *chiar* rimează (ex: `--rhyme`).
    - **Aliterație**: Forțează adjectivele și substantivele să înceapă cu aceeași literă (`--alliteration`).
    - **Control Structural**: Filtrează pattern-urile pentru a folosi doar `--only-nouns` (substantive) sau `--only-adjectives`.
    - **Separator Custom**: Înlocuiește underscore-ul standard cu propriul separator (ex: `--separator "."`).
    - **Mod Interactiv**: Regenerează rezultatele pe loc fără a reporni scriptul (`--interactive`).
    - **Protecție la Infinite Loop**: Reîncercări inteligente care previn blocarea când constrângerile sunt prea stricte.

- **Verificarea Disponibilității (OSINT)**: 
    - **Verificare Live**: Verifică instantaneu dacă numele este liber pe platforme precum *GitHub*, *Reddit*, *Instagram*.
    - **Smart Content Detection**: Scanează textul paginii pentru a identifica profilele „Not Found”.
    - **Cross-Platform Sync**: Folosește `--sync` pentru a găsi handle-uri libere pe *toate* platformele alese simultan.

- **Modificatori Dinamici**:
    - **Leet Speak**: Transformă aleatoriu caracterele în cifre (ex: `e` -> `3` sau `a` -> `@`).
    - **Prefix/Suffix**: Adaugă elemente precum `The`, `Master`.
    - **Special Chars**: Inserează caractere speciale (`_`, `.`, `-`).
    - **Enforce Length**: Ajustează lungimea finală.

##  Arhitectura Sistemului
Proiectul este organizat modular pentru a facilita mentenanța și scalabilitatea:

```text
username_generator/
├── username.py             # Entry point (wrapper)
├── config.json             # Configurație externă (cuvinte, hărți leet)
└── username_generator/     # Pachetul principal
    ├── cli.py              # Interfața CLI, Orchestrare și parsarea argumentelor
    ├── core.py             # Logica centrală (Dependency Injection via GenerationContext)
    ├── checker.py          # Verificator de disponibilitate paralel (Multi-threaded)
    ├── config.py           # Config Manager (Validare Pydantic & Caching)
    ├── modifiers.py        # Algoritmi text & funcții fonetice (pronouncing)
    ├── exceptions.py       # Excepții custom
    └── __init__.py         # Marcare pachet
```

##  Instalare și Configurare

### Cerințe
- Python 3.10+

### Pași pentru Setup
1. **Clonează repository-ul**:
   ```bash
   git clone https://github.com/NaviAndrei/cli-username.git
   cd cli-username
   ```

2. **Creează și activează un mediu virtual (venv)**:
   ```powershell
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Instalează Dependențele**:
   ```bash
   pip install pydantic pydantic-settings pronouncing requests
   # SAU
   pip install .
   ```

4. **Verifică structura**:
   Asigură-te că fișierul `config.json` este prezent în rădăcina proiectului.

##  Ghid de Utilizare

### Comanda de bază
```powershell
python username.py --count 3 --base-word Hero
```

### Exemple avansate (v2.2+)
*   **Rime și Aliterație**:
    ```powershell
    # Generează nume ca "DarkShark" sau "CyberCity"
    python username.py --vibe cyber --rhyme --count 5
    python username.py --profession gamer --alliteration
    ```
*   **Structură Custom și Separator**:
    ```powershell
    # Generează "Dev.Code.99" sau "Pro.Gamer"
    python username.py --profession developer --separator "." --only-nouns
    ```
*   **Mod Interactiv**:
    ```powershell
    # Permite regenerarea rezultatelor fără a ieși
    python username.py --vibe fantasy --interactive
    ```
*   **Combinare Vibe & Profession**:
    ```powershell
    python username.py --vibe tech --profession designer --use-leet
    ```

### Export Date
Poți salva rezultatele în formate `txt`, `json` sau `csv`:
```powershell
python username.py --count 10 --vibe fantasy --output lista.json --format json
```

##  Referință Tehnică

### Module Principale
- **`cli.py`**: Utilizează `argparse` pentru interfață. Include validare avansată a input-ului.
- **`core.py`**: Folosește **Dependency Injection** prin `GenerationContext` pentru a transmite constrângerile. Include protecție la infinite loops.
- **`modifiers.py`**: Integrează `pronouncing` pentru rime fonetice și funcții helper.
- **`config.py`**: Bazat pe **Pydantic** pentru validare strictă a schemei și suport pentru variabile de mediu (`UG_PATTERNS` etc.).

---

##  Configurare Externă (config.json)
Fișierul `config.json` permite personalizarea întregului vocabular al aplicației fără a modifica codul sursă. Poți adăuga noi `vibes`, `professions` sau zeități direct în acest fișier.

##  Contribuție
Contribuțiile sunt binevenite! Dacă dorești să îmbunătățești proiectul Advanced Username Generator, urmează acești pași:

1. **Fă un Fork** proiectului.
2. **Creează un Feature Branch**.
3. **Salvează modificările (Commit)**.
4. **Trimite către branch-ul tău (Push)**.
5. **Deschide un Pull Request**.

Te rugăm să te asiguri că noul cod respectă standardele PEP 8 și include docstrings adecvate.

---
*Proiect creat folosind cele mai bune practici Python (PEP 8, Type Hinting, Google Docstrings).*
