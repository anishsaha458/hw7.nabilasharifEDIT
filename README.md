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


-code is displaying screen with no visual features
-none of the features have been implemented
-needs to be implemented

A map rendering file is not present in the files. The map loading/rendering will be in a separate map.py file. There isn't a preference for the size of each tile. 

-all future implementations stated in the txt file will be implemented which is drawing the grid map, moving the pac man with no ghosts, adding pellets, adding collisions, and adding random ghosts

-new files were created in order to complete the foundational pac man game set up
-game, pacman, ghost, map, settings, main, level1

-a full pacman class was creaed as well as a ghost class

The full pacman has buffered arrow-key input, tile-by-tile grid movement with tunnel wrap, wall collision, pellet/power pellet which mutates the map, and score tracking

The full ghost class has random direction AI with no reversals, frightened mode, respawn on being eaten, and 4 distinct colors.

Updates on previous files:
game.py()- 
update() is complete which moves Pac-man, detects what was eaten, frightens ghosts on power pellets, moves all ghosts, checks ghosts collisions, checks win condition, 
handle_events()- forwards keys to Pac-man and handles R to restart
draw()- handles all entities plus a score and win/death overlays

map.py- grid changed from list-of-strings to lists-of-lists so tiles can be mutated
and added set_tile(), is_wall(), tile_center(), tile_to_pixel(), pixel_to_tile()

settings.py- added PACMAN_SPEED, GHOST_SPEED, FRIGHTENED_DURATION, NUM_GHOSTS, RED, CYAN, ORANGE, DARK_BLUE

The level1.txt is changed to a 28*31 tile grid

Current Progress
PLANNED PHASES

Phase 1

Window + game loop-- mostly done COMPLETE

Phase 2

Draw grid map COMPLETE

Phase 3

Move Pacman (no ghosts) COMPLETE

Phase 4

Add pellets COMPLETE

Phase 5

Add collision COMPLETE

Phase 6

Add ghosts (random) COMPLETE

Phase 7

Add AI COMPLETE

current point:
pacman/
├── main.py          # Entry point
├── game.py          # Game engine: loop, coordination, HUD, overlays
├── settings.py      # All constants (size, speed, color, timing)
├── map.py           # Map class: load, render, tile mutation
├── pacman.py        # Pacman class: input, movement, eating, animation
├── ghost.py         # Ghost class: random AI, frightened mode
│
└── level/
    └── level1.txt   # 28×31 tile grid

how to run:
pip install pygame
python main.py

ensure all the files are in the same directory before running
