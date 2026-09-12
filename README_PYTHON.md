# Point - Python Port

A complete, faithful Python port of the 2D C++ SDL2 action game **Point**, built with **Pygame**.

## Overview

**Point** is a physics-based arcade action game where you control a floating Ghost character (`Me`). By left-clicking on nearby pumpkins (friends) or spiders (enemies), you attach a rope and swing like a pendulum across level space while avoiding spiders and rising lava. Collecting pumpkins awards score (+100 per pumpkin) and tracks total score and kills.

This repository contains the full Python port converted from the original C++ SDL2 implementation while preserving exact gameplay mechanics, pendulum physics, collision rules, UI menus, audio, and persistent scoreboards.

---

## Relationship to the Original C++ Project

- **Original Engine**: C++11, SDL2, SDL2_image, SDL2_ttf, SDL2_mixer.
- **Python Framework**: Python 3.8+ with Pygame 2.6.1.
- **Equivalence**: All original asset files (`texture/`, `sound/`, `font/`), physics constants (`GRAVITY = 0.4`), UI layouts, pendulum formulas, and scoreboard I/O (`ScoreBoard.txt`) have been preserved 1:1.

---

## Supported Platforms

- **Windows** 10 / 11
- **macOS** 10.15+
- **Linux** (Ubuntu, Debian, Fedora, Arch, etc.)

---

## Prerequisites

- **Python**: Version 3.8 or higher.
- **Pip**: Latest Python package manager.

---

## Installation & Setup

### 1. Create a Virtual Environment (Optional but Recommended)

#### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run the Game

Launch the application using one of the following commands from the root directory:

```bash
python -m py_point.main
```

Or directly via main script:

```bash
python py_point/main.py
```

---

## Game Controls & Rules

| Input Action | Game Behavior |
| :--- | :--- |
| **Left Mouse Click & Hold** | Attach rope to the nearest pumpkin or spider from cursor position and swing |
| **Left Mouse Release** | Release rope and launch into momentum-based flight |
| **Main Menu -> PLAY** | Start a new game session |
| **Main Menu / End Menu -> EXIT** | Close application |
| **End Menu -> RETRY** | Restart game after game over |

### Game Rules
1. **Score Points**: Collect pumpkins (`Gold_1.png`) to gain +100 points and increment kill counter.
2. **Avoid Hazards**: Touching spiders (`Spider2.png`) or rising lava causes immediate Game Over (`lmao ded`).
3. **High Scores**: Top scores are appended and sorted in `ScoreBoard.txt` and displayed on the End Menu LeaderBoard.

---

## Testing Commands

Run the automated test suite with `pytest`:

```bash
python -m pytest -v
```

### Linting & Formatting Check

```bash
pip install flake8 black
flake8 py_point tests
black --check py_point tests
```

---

## Packaging & Distribution

To create a standalone desktop executable using **PyInstaller**:

### Windows
```powershell
pyinstaller --noconfirm --onedir --windowed `
  --add-data "texture;texture" `
  --add-data "sound;sound" `
  --add-data "font;font" `
  --add-data "ScoreBoard.txt;." `
  py_point/main.py
```

### macOS / Linux
```bash
pyinstaller --noconfirm --onedir --windowed \
  --add-data "texture:texture" \
  --add-data "sound:sound" \
  --add-data "font:font" \
  --add-data "ScoreBoard.txt:." \
  py_point/main.py
```

The resulting executable will be placed in the `dist/` directory.

---

## Project Structure

```
Point/
├── py_point/
│   ├── __init__.py           # Package marker
│   ├── main.py               # Main game loop and audio setup
│   ├── vector.py             # Vector and VectorAlgebra math
│   ├── object.py             # Object entity struct (Vec2, Vel2, Acc2, Object)
│   ├── me.py                 # Hero player class (Me), collision & score hits
│   ├── lava.py               # Rising lava hazard entity
│   ├── rope.py               # Pendulum rope physics & target selection
│   ├── object_manager.py     # Level generation and chunk spawning
│   ├── event_manager.py      # UI button hit testing and mouse input
│   ├── ltexture.py           # Pygame font texture helper
│   └── render_window.py      # Display window, asset loader, & menu renderers
├── tests/
│   ├── test_vector.py        # Vector math unit tests
│   ├── test_physics.py       # Physics step unit tests
│   ├── test_collision.py     # Collision detection unit tests
│   ├── test_scoreboard.py    # Score persistence unit tests
│   └── test_event_mgr.py     # UI hit testing unit tests
├── font/                     # Original OTF font assets
├── sound/                    # Original WAV/MP3 audio assets
├── texture/                  # Original PNG/JPG image assets
├── ScoreBoard.txt            # Persistent score data file
├── pyproject.toml            # Package manifest
├── requirements.txt          # Dependencies specification
└── README_PYTHON.md          # Python documentation
```

---

## Troubleshooting

- **Audio Warning / No Sound**: If no audio device is connected, the game will automatically disable sound output and continue running silently without crashing.
- **Font Rendering**: If `font/halloween.otf` is missing, Pygame automatically falls back to system fonts.

---

## License & Attribution

- **Original Author**: Pham Duc Hoang (ID: 22021200), UET (QH-2022)
- **Python Port**: Maintained as part of the Point game project.
