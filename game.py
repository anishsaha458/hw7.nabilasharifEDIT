# game.py

"""
The Game class: central engine that owns and coordinates everything.

Responsibilities:
- Initialize all subsystems (map, Pac-Man, ghosts)
- Run the main loop (input → update → draw)
- Coordinate cross-entity logic:
    * Feed keypresses to Pac-Man
    * Trigger ghost frighten on power pellet
    * Detect ghost-Pac-Man collisions
    * Detect win condition (all pellets eaten)
- Render the HUD (score display)
"""

import pygame
from settings import (
    WIDTH, HEIGHT, FPS,
    BLACK, WHITE, YELLOW, RED,
    MAP_OFFSET_Y, NUM_GHOSTS
)
from map import Map
from pacman import Pacman
from ghost import Ghost


# Ghost spawn positions inside the ghost house (row 11, spread across cols)
GHOST_SPAWNS = [
    (11, 11),
    (11, 13),
    (11, 15),
    (11, 17),
]


class Game:
    def __init__(self):
        """
        Set up the window, clock, and all game entities.

        Entities created here:
            self.map     -> Map  (tile grid)
            self.pacman  -> Pacman
            self.ghosts  -> list of Ghost
            self.score   -> mirrored from pacman for HUD
            self.state   -> 'playing' | 'win' | 'dead'
            self.font    -> pygame font for HUD text
        """

        # ── Window + clock ────────────────────────────────
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man (OOP Build)")
        self.clock  = pygame.time.Clock()
        self.running = True

        # ── Font (for HUD) ────────────────────────────────
        self.font       = pygame.font.SysFont("monospace", 20, bold=True)
        self.big_font   = pygame.font.SysFont("monospace", 36, bold=True)

        # ── Game state ────────────────────────────────────
        self.state = "playing"   # 'playing' | 'win' | 'dead'

        # ── Map ───────────────────────────────────────────
        self.map = Map("pacman/level/level1.txt")

        # ── Pac-Man (spawns bottom-center, row 29 col 14) ─
        self.pacman = Pacman(row=29, col=14)

        # ── Ghosts ────────────────────────────────────────
        self.ghosts = [
            Ghost(row, col, ghost_id=i)
            for i, (row, col) in enumerate(GHOST_SPAWNS[:NUM_GHOSTS])
        ]

    # ── Main loop ─────────────────────────────────────────

    def run(self):
        """
        MAIN GAME LOOP

        Runs at FPS until self.running is False.
        Each iteration:
            1. handle_events  — read keyboard / window events
            2. update         — advance game logic by one frame
            3. draw           — render everything to screen
        """
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

    # ── Input ─────────────────────────────────────────────

    def handle_events(self):
        """
        Process pygame events.

        - QUIT closes the window
        - Arrow keys are forwarded to Pac-Man's input buffer
        - R key restarts after win/death
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            # Forward key events to Pac-Man (he buffers them)
            if self.state == "playing":
                self.pacman.handle_input(event)

            # Restart on R key when game is over
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if self.state in ("win", "dead"):
                    self.__init__()   # reset everything

    # ── Update ────────────────────────────────────────────

    def update(self):
        """
        Advance the game by one frame.

        Only runs when state == 'playing'.

        Steps:
            1. Move Pac-Man (he also eats pellets internally)
            2. Check what tile Pac-Man landed on
            3. If power pellet → frighten all ghosts
            4. Move all ghosts
            5. Check ghost collisions
            6. Check win condition
        """
        if self.state != "playing":
            return

        # 1. Update Pac-Man (moves + eats); returns what was eaten this frame
        eaten = self.pacman.update(self.map)

        # 2. React to what was eaten
        if eaten == "power_pellet":
            self._frighten_ghosts()

        # 3. Update all ghosts
        for ghost in self.ghosts:
            ghost.update(self.map)

        # 4. Ghost ↔ Pac-Man collision
        self._check_ghost_collision()

        # 5. Win condition
        self._check_win()

    def _frighten_ghosts(self):
        """Put all ghosts into FRIGHTENED mode."""
        for ghost in self.ghosts:
            ghost.frighten()

    def _check_ghost_collision(self):
        """
        Check if Pac-Man shares a tile with any ghost.

        - NORMAL ghost  → Pac-Man dies  (state = 'dead')
        - FRIGHTENED    → Ghost is eaten (+200 points, ghost respawns)
        """
        pr, pc = self.pacman.get_position()

        for i, ghost in enumerate(self.ghosts):
            gr, gc = ghost.get_position()
            if pr == gr and pc == gc:
                if ghost.is_frightened():
                    # Eat the ghost: respawn it at its original spawn
                    self.pacman.score += 200
                    spawn_row, spawn_col = GHOST_SPAWNS[i % len(GHOST_SPAWNS)]
                    self.ghosts[i] = Ghost(spawn_row, spawn_col, ghost_id=i)
                else:
                    # Pac-Man dies
                    self.state = "dead"
                    return

    def _check_win(self):
        """
        Win if every pellet and power pellet has been eaten.
        Counts remaining '.' and 'o' tiles in the grid.
        """
        remaining = sum(
            1 for row in self.map.grid for tile in row if tile in (".", "o")
        )
        if remaining == 0:
            self.state = "win"

    # ── Draw ──────────────────────────────────────────────

    def draw(self):
        """
        Render one frame.

        Order:
            1. Clear screen (black)
            2. Draw map (walls, pellets, power pellets)
            3. Draw Pac-Man
            4. Draw ghosts
            5. Draw HUD (score)
            6. Draw overlay if win/dead
            7. Flip display
        """
        self.screen.fill(BLACK)

        # Map tiles
        self.map.draw(self.screen)

        # Pac-Man
        self.pacman.draw(self.screen)

        # Ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen)

        # HUD
        self._draw_hud()

        # Overlay for end states
        if self.state == "win":
            self._draw_overlay("YOU WIN!", YELLOW)
        elif self.state == "dead":
            self._draw_overlay("GAME OVER", RED)

        pygame.display.flip()

    def _draw_hud(self):
        """
        Draw score at the top of the screen, above the maze.
        """
        score_text = self.font.render(
            f"SCORE: {self.pacman.score}", True, WHITE
        )
        # Vertically centered in the gap above the map
        y = (MAP_OFFSET_Y - score_text.get_height()) // 2
        self.screen.blit(score_text, (10, max(4, y)))

    def _draw_overlay(self, message, color):
        """
        Draw a semi-transparent overlay with a centered message.
        Shown on win or death.  Press R to restart.
        """
        # Semi-transparent dark rectangle over the whole screen
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # Big message
        msg_surf = self.big_font.render(message, True, color)
        mx = (WIDTH  - msg_surf.get_width())  // 2
        my = (HEIGHT - msg_surf.get_height()) // 2 - 20
        self.screen.blit(msg_surf, (mx, my))

        # Sub-text
        sub_surf = self.font.render("Press R to restart", True, WHITE)
        sx = (WIDTH  - sub_surf.get_width())  // 2
        sy = my + msg_surf.get_height() + 10
        self.screen.blit(sub_surf, (sx, sy))