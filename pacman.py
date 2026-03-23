# pacman.py

"""
Pac-Man entity: the player-controlled character.

Key design decisions:
- Pac-Man moves ONE TILE at a time on a grid
- Input is BUFFERED: the player can press a key slightly early
  and it takes effect when Pac-Man reaches the next tile center
- Mouth animation uses a frame counter
- Pellet eating is handled here; the map tile is erased directly
"""

import pygame
from settings import (
    TILE_SIZE, MAP_OFFSET_X, MAP_OFFSET_Y,
    PACMAN_SPEED, YELLOW
)


# Direction vectors: (row_delta, col_delta)
# These match the grid: row increases downward
DIRECTIONS = {
    pygame.K_LEFT:  (0, -1),
    pygame.K_RIGHT: (0,  1),
    pygame.K_UP:    (-1, 0),
    pygame.K_DOWN:  (1,  0),
}


class Pacman:
    def __init__(self, row, col):
        """
        Create Pac-Man at grid position (row, col).

        Attributes:
            row, col        current tile position
            direction       (dr, dc) currently moving
            next_direction  buffered input (applied at next tile center)
            move_timer      counts frames; moves when it hits PACMAN_SPEED
            mouth_angle     controls mouth open/close animation (degrees)
            mouth_opening   True = opening, False = closing
            score           total pellets eaten * 10
            alive           False when a ghost catches Pac-Man
        """
        self.row = row
        self.col = col

        self.direction      = (0, 0)     # starts stationary
        self.next_direction = (0, 0)     # buffered input

        self.move_timer = 0              # frame counter for movement

        # Mouth animation
        self.mouth_angle   = 45          # degrees open (0 = closed, 45 = wide)
        self.mouth_opening = False       # currently opening or closing?

        self.score = 0
        self.alive = True
        self.last_eaten = None           # set each frame by _eat()

    # ── Input ─────────────────────────────────────────────

    def handle_input(self, event):
        """
        Buffer a direction keypress.

        The direction is stored in self.next_direction and applied
        at the next tile boundary (so input never feels unresponsive).
        """
        if event.type == pygame.KEYDOWN and event.key in DIRECTIONS:
            self.next_direction = DIRECTIONS[event.key]

    # ── Update ────────────────────────────────────────────

    def update(self, game_map):
        """
        Called once per frame.

        Steps:
        1. Try to apply buffered direction if the new path is clear
        2. Move one tile every PACMAN_SPEED frames if not blocked
        3. Eat pellet at new position
        4. Animate the mouth
        """
        self.last_eaten = None       # reset each frame before moving
        self._try_turn(game_map)
        self._move(game_map)
        self._animate_mouth()
        return self.last_eaten

    def _try_turn(self, game_map):
        """
        Apply next_direction if the tile in that direction is walkable.
        This lets Pac-Man turn the moment he reaches a valid junction.
        """
        dr, dc = self.next_direction
        if not game_map.is_wall(self.row + dr, self.col + dc):
            self.direction = self.next_direction

    def _move(self, game_map):
        """
        Advance Pac-Man by one tile every PACMAN_SPEED frames.

        - Skips movement if direction is (0, 0) or wall ahead
        - Wraps horizontally (tunnel on row 14)
        - Eats pellet at landing tile
        """
        if self.direction == (0, 0):
            return

        self.move_timer += 1
        if self.move_timer < PACMAN_SPEED:
            return
        self.move_timer = 0

        dr, dc = self.direction
        new_row = self.row + dr
        new_col = self.col + dc

        # Horizontal wrap-around (tunnel)
        new_col = new_col % game_map.cols

        # Only move if the destination is not a wall
        if not game_map.is_wall(new_row, new_col):
            self.row = new_row
            self.col = new_col
            self._eat(game_map)

    def _eat(self, game_map):
        """
        Check the current tile and eat a pellet or power pellet.

        Returns:
            'pellet'       if a regular pellet was eaten
            'power_pellet' if a power pellet was eaten
            None           otherwise
        """
        tile = game_map.get_tile(self.row, self.col)

        if tile == ".":
            game_map.set_tile(self.row, self.col, " ")
            self.score += 10
            self.last_eaten = "pellet"

        elif tile == "o":
            game_map.set_tile(self.row, self.col, " ")
            self.score += 50
            self.last_eaten = "power_pellet"

    def eat_result(self, game_map):
        """
        Public method called by Game to check what Pac-Man ate
        this frame (after _move has already run).

        Returns 'pellet', 'power_pellet', or None.
        """
        return game_map.get_tile(self.row, self.col)  # already eaten by _eat

    def _animate_mouth(self):
        """
        Toggle mouth between open and closed over time.
        mouth_angle cycles 45 → 0 → 45 repeatedly.
        """
        speed = 5  # degrees per frame
        if self.mouth_opening:
            self.mouth_angle += speed
            if self.mouth_angle >= 45:
                self.mouth_angle = 45
                self.mouth_opening = False
        else:
            self.mouth_angle -= speed
            if self.mouth_angle <= 0:
                self.mouth_angle = 0
                self.mouth_opening = True

    # ── Rendering ─────────────────────────────────────────

    def draw(self, screen):
        """
        Draw Pac-Man as a yellow pie/arc shape.

        pygame.draw.arc doesn't fill, so we use draw.polygon
        to approximate the mouth wedge via a circle of points.
        """
        import math

        cx, cy = self._center_pixels()
        radius = TILE_SIZE // 2 - 1

        # Determine facing angle for mouth direction
        dr, dc = self.direction
        if   dc ==  1: facing = 0       # right
        elif dc == -1: facing = 180     # left
        elif dr == -1: facing = 90      # up
        elif dr ==  1: facing = 270     # down
        else:          facing = 0       # default (stationary)

        angle = self.mouth_angle

        # Build polygon: center + arc points (excluding mouth wedge)
        start_angle = math.radians(facing + angle)
        end_angle   = math.radians(facing + 360 - angle)

        points = [(cx, cy)]
        steps  = 30
        step   = (end_angle - start_angle) / steps

        for i in range(steps + 1):
            a = start_angle + i * step
            points.append((
                cx + radius * math.cos(a),
                cy - radius * math.sin(a),
            ))

        pygame.draw.polygon(screen, YELLOW, points)

    def _center_pixels(self):
        """Return the pixel center of Pac-Man's current tile."""
        x = MAP_OFFSET_X + self.col * TILE_SIZE + TILE_SIZE // 2
        y = MAP_OFFSET_Y + self.row * TILE_SIZE + TILE_SIZE // 2
        return x, y

    # ── Helpers ───────────────────────────────────────────

    def get_position(self):
        """Return current (row, col) grid position."""
        return self.row, self.col