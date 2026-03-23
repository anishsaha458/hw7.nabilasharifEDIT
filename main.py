# main.py

"""
Entry point of the program.

Responsibilities (only):
- Initialize pygame
- Create and run the Game object
- Quit pygame cleanly on exit

Nothing game-specific lives here — all logic is in Game.
"""

import pygame
from game import Game


def main():
    """
    Bootstrap sequence:
        1. pygame.init()  — must come before any pygame calls
        2. Game()         — sets up window, map, entities
        3. game.run()     — blocks until window is closed
        4. pygame.quit()  — clean shutdown
    """
    pygame.init()

    game = Game()
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()