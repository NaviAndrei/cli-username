#  Advanced Username Generator

Un instrument Command Line Interface (CLI) puternic și modularizat, scris în Python, conceput pentru generarea de identități online unice și memorabile. Proiectul folosește principii de design SOLID și o structură extensibilă pentru a oferi o varietate de strategii de generare.

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
**Advanced Username Generator** transformă procesul banal de creare a unui nume de utilizator într-o experiență creativă. Fie că ai nevoie de un nume pentru gaming, social media sau medii profesionale, acest tool oferă algoritmi diversificați și modificatori dinamici pentru a asigura unicitatea.

##  Funcționalități Conceptuale
- **Strategii Multiple de Generare**:
    - `Timestamp`: Bazat pe data și ora curentă.
    - `Retro`: Stilul clasic al internetului (adjectiv + substantiv + număr).
    - `Vibe`: Tematici precum *Cyber*, *Fantasy*, *Scifi* sau *Nature*.
    - `Profession`: Username-uri adaptate pentru *Developer*, *Designer*, *Writer*.
    - `Mythology`: Nume inspirate din panteonul Grecesc, Nordi sau Egiptean.
    - `Keywords`: Combină propriile tale cuvinte cheie.
- **Verificarea Disponibilității (OSINT)**: 
    - **Verificare Live**: Verifică instantaneu dacă numele este liber pe platforme precum *GitHub*, *Reddit*, *Instagram*, *Twitch*.
    - **Smart Content Detection**: Scanează textul paginii pentru a identifica profilele „Not Found”, chiar dacă codul HTTP este 200.
    - **Cross-Platform Sync**: Folosește `--sync` pentru a găsi handle-uri libere pe *toate* platformele alese simultan.
- **Modificatori Dinamici**:
    - **Leet Speak**: Transformă caracterele în cifre (ex: `e` -> `3`).
    - **Prefix/Suffix**: Adaugă elemente precum `The`, `Master`, `Pro`.
    - **Special Chars**: Inserează caractere speciale (`_`, `.`, `-`).
    - **Enforce Length**: Ajustează lungimea finală (trunchiere sau padding numeric).

##  Arhitectura Sistemului
Proiectul este organizat modular pentru a facilita mentenanța și scalabilitatea:

```text
username_generator/
├── username.py             # Entry point (wrapper)
├── config.json             # Configurație externă (cuvinte, hărți leet)
└── username_generator/     # Pachetul principal
    ├── cli.py              # Interfața CLI, Orchestrare și parsarea argumentelor
    ├── core.py             # Logica centrală de generare (Factory)
    ├── checker.py          # Verificator de disponibilitate paralel (Multi-threaded)
    ├── config.py           # Gestionarea încărcării și caching-ului config
    ├── modifiers.py        # Algoritmi de transformare a textului
    ├── exceptions.py       # Excepții custom (ConfigError, ValidationError)
    └── __init__.py         # Marcare pachet și versionare
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

3. **Verifică structura**:
   Asigură-te că fișierul `config.json` este prezent în rădăcina proiectului.

##  Ghid de Utilizare

### Comanda de bază
```powershell
python username.py --count 3 --base-word Hero
```

### Exemple avansate
*   **Stil Cyber cu Leet Speak**:
    ```powershell
    python username.py --count 5 --vibe cyber --use-leet
    ```
*   **Nume Mitologice (aleatoriu)**:
    ```powershell
    python username.py --mythology
    ```
*   **Combinare Keywords și caractere speciale**:
    ```powershell
    python username.py --keywords Matrix Ghost --use-special-chars
    ```
*   **Verificarea Disponibilității (Mod OSINT)**:
    ```powershell
    python username.py --count 1 --retro --check
    ```
*   **Sincronizare Multi-Platformă (Găsește un nume liber pe GitHub ȘI Reddit)**:
    ```powershell
    python username.py --count 1 --base-word Maverick --sync github,reddit
    ```

### Export Date
Poți salva rezultatele în formate `txt`, `json` sau `csv`:
```powershell
python username.py --count 10 --vibe fantasy --output lista.json --format json
```

##  Referință Tehnică

### Module Principale
- **`cli.py`**: Utilizează `argparse` pentru a valida input-ul utilizatorului. Organizează ajutorul (`--help`) în grupuri logice.
- **`core.py`**: Conține funcțiile de generare care selectează cuvinte din `config.json` bazat pe pattern-uri template.
- **`modifiers.py`**: Implementează unități de procesare atomice (ex: `apply_leet_speak`) care pot fi înlănțuite.
- **`config.py`**: Folosește `lru_cache` pentru a asigura că fișierul JSON este citit o singură dată de pe disc, îmbunătățind performanța.

---

##  Configurare Externă (config.json)
Fișierul `config.json` permite personalizarea întregului vocabular al aplicației fără a modifica codul sursă. Poți adăuga noi `vibes`, `professions` sau zeități direct în acest fișier.

##  Contribuție
Contribuțiile sunt binevenite! Dacă dorești să îmbunătățești proiectul Advanced Username Generator, urmează acești pași:

1. **Fă un Fork** proiectului (apasă butonul Fork din colțul dreapta-sus).
2. **Creează un Feature Branch** (`git checkout -b feature/AmazingFeature`).
3. **Salvează modificările (Commit)** (`git commit -m 'Adaugă AmazingFeature'`).
4. **Trimite către branch-ul tău (Push)** (`git push origin feature/AmazingFeature`).
5. **Deschide un Pull Request**.

Te rugăm să te asiguri că noul cod respectă standardele PEP 8 și include docstrings adecvate.

---
*Proiect creat folosind cele mai bune practici Python (PEP 8, Type Hinting, Google Docstrings).*
