Replica of Pac-Man

# 🟡 Pac-Man Clone (Pygame, OOP)

## 📌 Overview

This project is a **from-scratch Pac-Man clone** built using **Pygame** and an **Object-Oriented Programming (OOP)** approach.

The goal of this project is not just to recreate the game, but to:

* Understand **game architecture**
* Learn **grid-based movement systems**
* Practice **clean, modular Python design**

---

## 🚧 Current Progress (Phase 2 Complete)

So far, the project includes:

### ✅ Phase 1: Game Engine

* Window creation using Pygame
* Main game loop:

  * Input handling
  * Game state updates
  * Rendering
* Frame rate control (FPS)

### ✅ Phase 2: Grid + Map System

* Tile-based level system using a `.txt` file
* Map loading into a 2D grid
* Rendering:

  * Walls (`#`) as blue rectangles
  * Pellets (`.`) as white dots

---

## 🧱 Project Structure

```
pacman/
├── main.py          # Entry point (starts the game)
├── game.py          # Core game loop + logic
├── settings.py      # Global constants
│
├── level/
│   └── level1.txt   # Map layout (grid-based)
```

---

## 🧠 Key Concepts Implemented

### 1. Game Loop

The core structure used in most games:

```
while running:
    handle_input()
    update()
    draw()
```

---

### 2. Grid-Based System

The game world is built from a **2D grid**, loaded from a text file:

```
############################
#............##............#
#.####.#####.##.#####.####.#
#..........................#
############################
```

Each symbol represents a tile:

| Symbol | Meaning |
| ------ | ------- |
| `#`    | Wall    |
| `.`    | Pellet  |
| space  | Empty   |

---

### 3. Grid → Pixel Conversion

Each tile is converted into screen coordinates:

```
x = column * TILE_SIZE
y = row * TILE_SIZE
```

This allows the game to:

* Render correctly
* Enable future movement and collision logic

---

## ▶️ How to Run the Project

### 1. Activate your environment (recommended)

```
source venv/bin/activate
```

### 2. Run the game

```
python main.py
```

---

## ⚠️ Requirements

* Python **3.11 or 3.12** (Pygame may not work on newer versions like 3.14)
* Pygame:

```
pip install pygame
```

---

## 🎮 Current Output

* A window opens
* A Pac-Man-style maze is rendered
* Walls and pellets are visible
* No movement yet (coming next)

---

## 🔜 Next Steps

Upcoming features:

* 🟡 Pac-Man entity (player)
* ⌨️ Keyboard input
* 🧭 Grid-based movement
* 🍒 Pellet collection
* 👻 Ghosts + AI behavior
* 💥 Collision system

---

## 🎯 Learning Goals

This project is designed to teach:

* Clean OOP design in Python
* Game loop architecture
* Tile-based game systems
* Step-by-step feature building

---

## 📝 Notes

This project is being built incrementally to ensure:

* Full understanding of each component
* No “magic” or copied code
* Strong foundational knowledge of game development

---



---
PLANNED PHASES

Phase 1

Window + game loop-- mostly done

Phase 2

Draw grid map

Phase 3

Move Pacman (no ghosts)

Phase 4

Add pellets

Phase 5

Add collision

Phase 6

Add ghosts (random)

Phase 7

Add AI

