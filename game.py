# game.py

"""
This file contains the Game class.

Think of Game as:
- The "engine" of your program
- The thing that controls everything
"""

import pygame
from settings import WIDTH, HEIGHT, FPS, BLACK


class Game:
    def __init__(self):
        """
        Constructor: runs once when the Game object is created.

        We initialize:
        - screen (window)
        - clock (controls speed)
        - running flag (controls loop)
        """

        # Create the game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man (OOP Build)")

        # Clock controls how fast the loop runs
        self.clock = pygame.time.Clock()

        # This determines whether the game loop continues running
        self.running = True

    def run(self):
        """
        MAIN GAME LOOP

        This runs forever (until self.running = False)

        Structure:
        1. Handle input
        2. Update game logic
        3. Draw everything
        """

        while self.running:
            # Limit the loop to FPS (prevents insane speeds)
            self.clock.tick(FPS)

            # Step 1: Input
            self.handle_events()

            # Step 2: Logic
            self.update()

            # Step 3: Rendering
            self.draw()

    def handle_events(self):
        """
        Handles all user input and system events.

        Example events:
        - Closing window
        - Key presses (later)
        """

        for event in pygame.event.get():

            # If user clicks the close button
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """
        Game logic goes here.

        Right now:
        - Nothing happens yet

        Later:
        - Move Pac-Man
        - Move ghosts
        - Check collisions
        """
        pass

    def draw(self):
        """
        Draw everything to the screen.

        Every frame:
        - Clear screen
        - Draw objects
        - Update display
        """

        # Fill the screen with black (clears previous frame)
        self.screen.fill(BLACK)

        # This actually updates what the player sees
        pygame.display.flip()