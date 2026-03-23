# map.py

"""
Handles the tile-based game map.

Responsibilities:
- Load level from a .txt file into a 2D grid
- Render walls, pellets, and power pellets
- Allow tiles to be removed (pellet collection)
- Expose tile lookups for collision detection

Tile key:
  '#'  -> Wall
  '.'  -> Pellet
  'o'  -> Power pellet
  ' '  -> Empty space
"""

import pygame
from settings import TILE_SIZE, MAP_OFFSET_X, MAP_OFFSET_Y, BLUE, WHITE, PINK


class Map:
    def __init__(self, filepath):
        """
        Load the map from a text file.

        self.grid is a list of *lists* (not strings) so individual
        tiles can be mutated when Pac-Man eats a pellet.
        """
        self.grid = self._load(filepath)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.grid else 0

        # Count total pellets + power pellets for win condition
        self.total_pellets = sum(
            1 for row in self.grid for tile in row if tile in ('.', 'o')
        )

    def _load(self, filepath):
        """
        Read the file and return a 2D list of characters.

        Each row is a list so tiles can be overwritten later.
        rstrip('\\n') preserves spaces (ghost house / tunnels).
        """
        with open(filepath, "r") as f:
            return [list(line.rstrip("\n")) for line in f.readlines()]

    # ── Tile access ───────────────────────────────────────

    def get_tile(self, row, col):
        """
        Return the tile character at (row, col).
        Returns ' ' if the position is out of bounds.
        """
        if 0 <= row < self.rows and 0 <= col < len(self.grid[row]):
            return self.grid[row][col]
        return " "

    def set_tile(self, row, col, value):
        """
        Overwrite the tile at (row, col) with value.
        Used by Pac-Man to erase pellets after eating them.
        """
        if 0 <= row < self.rows and 0 <= col < len(self.grid[row]):
            self.grid[row][col] = value

    def is_wall(self, row, col):
        """Return True if the tile is a wall. Used for collision."""
        return self.get_tile(row, col) == "#"

    # ── Pixel helpers ─────────────────────────────────────

    @staticmethod
    def pixel_to_tile(px, py):
        """
        Convert pixel coordinates to (row, col).
        Useful for checking which tile an entity occupies.
        """
        col = (px - MAP_OFFSET_X) // TILE_SIZE
        row = (py - MAP_OFFSET_Y) // TILE_SIZE
        return row, col

    @staticmethod
    def tile_to_pixel(row, col):
        """
        Return the pixel coordinates of a tile's top-left corner.
        """
        x = MAP_OFFSET_X + col * TILE_SIZE
        y = MAP_OFFSET_Y + row * TILE_SIZE
        return x, y

    @staticmethod
    def tile_center(row, col):
        """Return the pixel coordinates of a tile's center."""
        x = MAP_OFFSET_X + col * TILE_SIZE + TILE_SIZE // 2
        y = MAP_OFFSET_Y + row * TILE_SIZE + TILE_SIZE // 2
        return x, y

    # ── Rendering ─────────────────────────────────────────

    def draw(self, screen):
        """
        Draw every tile to the screen.
        Called once per frame from Game.draw().
        """
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.get_tile(row, col)
                x, y = self.tile_to_pixel(row, col)

                if tile == "#":
                    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))

                elif tile == ".":
                    cx, cy = self.tile_center(row, col)
                    pygame.draw.circle(screen, WHITE, (cx, cy), 2)

                elif tile == "o":
                    cx, cy = self.tile_center(row, col)
                    pygame.draw.circle(screen, PINK, (cx, cy), 5)