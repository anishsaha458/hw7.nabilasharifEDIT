# ghost.py

"""
Ghost entity: AI-controlled enemy.

Behaviour:
- Moves one tile at a time on the grid (same as Pac-Man)
- Chooses a random valid direction at each intersection
- Never reverses direction unless it has no other choice
- Switches to FRIGHTENED mode when Pac-Man eats a power pellet
  - moves slower, drawn in dark blue
  - Pac-Man can eat the ghost for bonus points
- Returns to NORMAL after FRIGHTENED_DURATION frames
"""

import pygame
import random
from settings import (
    TILE_SIZE, MAP_OFFSET_X, MAP_OFFSET_Y,
    GHOST_SPEED, FRIGHTENED_DURATION,
    RED, CYAN, PINK, ORANGE, DARK_BLUE, WHITE
)

# All four cardinal directions as (row_delta, col_delta)
ALL_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Ghost states
NORMAL     = "normal"
FRIGHTENED = "frightened"


class Ghost:
    # Each ghost has its own color; cycle through this list
    COLORS = [RED, CYAN, PINK, ORANGE]

    def __init__(self, row, col, ghost_id=0):
        """
        Create a ghost at grid position (row, col).

        Args:
            ghost_id: index 0-3, used to pick color
        """
        self.row = row
        self.col = col

        self.color    = Ghost.COLORS[ghost_id % len(Ghost.COLORS)]
        self.state    = NORMAL
        self.frighten_timer = 0   # counts down from FRIGHTENED_DURATION

        # Start moving in a random direction
        self.direction = random.choice(ALL_DIRS)
        self.move_timer = 0

    # ── State control ─────────────────────────────────────

    def frighten(self):
        """
        Called by Game when Pac-Man eats a power pellet.
        Puts the ghost into FRIGHTENED mode.
        """
        self.state = FRIGHTENED
        self.frighten_timer = FRIGHTENED_DURATION

    # ── Update ────────────────────────────────────────────

    def update(self, game_map):
        """
        Called once per frame.

        1. Tick the frightened timer
        2. Move one tile every GHOST_SPEED frames
        """
        self._tick_frighten()
        self._move(game_map)

    def _tick_frighten(self):
        """Count down frightened timer; return to normal when done."""
        if self.state == FRIGHTENED:
            self.frighten_timer -= 1
            if self.frighten_timer <= 0:
                self.state = NORMAL

    def _move(self, game_map):
        """
        Advance the ghost one tile every GHOST_SPEED frames.

        Direction-choosing rules (classic Pac-Man style):
        1. Collect all directions that are NOT a wall and NOT a
           direct reversal of current movement.
        2. Pick one at random.
        3. If no options exist (dead end), allow reversal.
        """
        # Frightened ghosts move at half speed
        speed = GHOST_SPEED * 2 if self.state == FRIGHTENED else GHOST_SPEED

        self.move_timer += 1
        if self.move_timer < speed:
            return
        self.move_timer = 0

        reverse = (-self.direction[0], -self.direction[1])

        # Candidate directions: not a wall, not reversing
        options = [
            d for d in ALL_DIRS
            if d != reverse
            and not game_map.is_wall(self.row + d[0], self.col + d[1])
        ]

        # If completely stuck, allow reversal
        if not options:
            options = [
                d for d in ALL_DIRS
                if not game_map.is_wall(self.row + d[0], self.col + d[1])
            ]

        if options:
            self.direction = random.choice(options)
            dr, dc = self.direction
            new_row = self.row + dr
            new_col = (self.col + dc) % game_map.cols  # tunnel wrap
            self.row = new_row
            self.col = new_col

    # ── Rendering ─────────────────────────────────────────

    def draw(self, screen):
        """
        Draw the ghost as a rounded rectangle with eyes.

        - NORMAL:     ghost's own color + white eyes
        - FRIGHTENED: dark blue body, no eyes (just a wavy bottom)
        """
        cx, cy = self._center_pixels()
        r = TILE_SIZE // 2 - 1

        color = DARK_BLUE if self.state == FRIGHTENED else self.color

        # Body: filled circle (head) + rectangle (body)
        pygame.draw.circle(screen, color, (cx, cy - r // 3), r)
        pygame.draw.rect(screen, color, (cx - r, cy - r // 3, r * 2, r + r // 2))

        # Wavy bottom skirt (3 bumps)
        bump_r = r // 3
        for i in range(3):
            bx = cx - r + bump_r + i * bump_r * 2
            by = cy + r // 2 + r // 3
            pygame.draw.circle(screen, color, (bx, by), bump_r)

        # Eyes (only in normal mode)
        if self.state == NORMAL:
            eye_y = cy - r // 2
            for ex in [cx - r // 3, cx + r // 3]:
                pygame.draw.circle(screen, WHITE, (ex, eye_y), 3)
                pygame.draw.circle(screen, (0, 0, 200), (ex, eye_y), 1)

    def _center_pixels(self):
        """Return the pixel center of the ghost's current tile."""
        x = MAP_OFFSET_X + self.col * TILE_SIZE + TILE_SIZE // 2
        y = MAP_OFFSET_Y + self.row * TILE_SIZE + TILE_SIZE // 2
        return x, y

    # ── Helpers ───────────────────────────────────────────

    def get_position(self):
        """Return current (row, col) grid position."""
        return self.row, self.col

    def is_frightened(self):
        return self.state == FRIGHTENED