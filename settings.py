# settings.py

"""
Global constants used across the entire game.

Centralizing values here means:
- No magic numbers scattered across files
- Easy to tweak speed, size, colors in one place
"""

# ── Screen ────────────────────────────────────────────────
WIDTH  = 600
HEIGHT = 700

# ── Frame rate ────────────────────────────────────────────
FPS = 60

# ── Grid ──────────────────────────────────────────────────
TILE_SIZE = 21          # pixels per tile

# Centers the 28-col x 31-row grid inside the window
MAP_OFFSET_X = (WIDTH  - 28 * TILE_SIZE) // 2   # 6 px
MAP_OFFSET_Y = (HEIGHT - 31 * TILE_SIZE) // 2   # 24 px

# ── Movement ──────────────────────────────────────────────
# How many frames between each tile step.
# Lower = faster.  At 60 FPS, 10 → moves 6 tiles/sec.
PACMAN_SPEED = 10   # frames per tile
GHOST_SPEED  = 15   # frames per tile (ghosts are slower)

# How many frames ghosts stay frightened after a power pellet
FRIGHTENED_DURATION = 300   # 5 seconds at 60 FPS

# ── Ghost count ───────────────────────────────────────────
NUM_GHOSTS = 4

# ── Colors (RGB) ──────────────────────────────────────────
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
BLUE   = (  0,   0, 200)
YELLOW = (255, 255,   0)
PINK   = (255, 184, 255)
RED    = (255,   0,   0)
CYAN   = (  0, 255, 255)
ORANGE = (255, 165,   0)
DARK_BLUE = (0, 0, 139)     # frightened ghost color