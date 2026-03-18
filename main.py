# main.py

"""
This is the entry point of the program.

Think of this file as:
"Start the game"
"""

import pygame
from game import Game


def main():
    """
    Initializes pygame and starts the game.
    """

    # Initialize pygame (REQUIRED before using anything)
    pygame.init()

    # Create the Game object (our core controller)
    game = Game()

    # Start the main loop
    game.run()

    # Clean exit
    pygame.quit()


# Ensures this runs only when you execute this file directly
if __name__ == "__main__":
    main()