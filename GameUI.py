import os as os
import sys as sys
import pygame as pygame

import Algorithms as Algorithms
import Level as Level


class UI:
    """Class to handle the UI of the game."""

    screenSurface: pygame.Surface = None
    """The surface of the screen."""
    screenSize: tuple = None
    """The size of the screen."""

    sprites: dict = {}
    """Dictionary to store the sprites."""
    imageSize: int = 20
    """The size of the images."""

    def __init__(self):
        """Initialize the UI, including the display, font, and sprites."""
        # Initialize the display for all platforms
        pygame.display.init()
        pygame.display.set_caption("Project 1 AI")  # Window title
        self.screenSize = (1000, 800)  # Window size
        self.screenSurface = pygame.display.set_mode(self.screenSize)

        # Clear the screen to white
        self.screenSurface.fill((255, 255, 255))
        # Initialize font support
        pygame.font.init()
        # Hide the mouse cursor
        pygame.mouse.set_visible(True)
        # Update the display
        pygame.display.update()

        # Define a helper function to get the path of the current file
        def getPath():
            """Return the path of the current file."""
            return os.path.dirname(os.path.abspath(__file__))

        # Load all sprites
        self.sprites["@"] = pygame.image.load(
            getPath() + "/themes/" + "/images/player.png"
        ).convert()  # Player
        self.sprites["+"] = pygame.image.load(
            getPath() + "/themes/" + "/images/player.png"
        ).convert()  # Player on target
        self.sprites[" "] = pygame.image.load(
            getPath() + "/themes/" + "/images/space.png"
        ).convert()  # Space
        self.sprites["#"] = pygame.image.load(
            getPath() + "/themes/" + "/images/wall.png"
        ).convert()  # Wall
        self.sprites["$"] = pygame.image.load(
            getPath() + "/themes/" + "/images/box.png"
        ).convert()  # Box
        self.sprites["."] = pygame.image.load(
            getPath() + "/themes/" + "/images/target.png"
        ).convert()  # Target
        self.sprites["*"] = pygame.image.load(
            getPath() + "/themes/" + "/images/box_on_target.png"
        ).convert()  # Box on target

        # Get image size
        self.imageSize = self.sprites["#"].get_width()

    def drawMenu(self, text: str, position: list, selected: bool = False):
        """Draw the menu with the given text at the specified position.

        ### Parameters
        @text: The text to be displayed.
        @position: The position where the text should be displayed.
        @selected: Whether the menu item is selected.
        """
        font = pygame.font.Font(None, 36)
        color = (255, 255, 0) if selected else (255, 255, 255)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect(center=position)
        self.screenSurface.blit(textSurface, textRect)

    def drawText(
        self, text: str, position: list, size: int = 26, color: tuple = (255, 255, 255)
    ):
        """Draw the text at the specified position.

        ### Parameters
        @text: The text to be displayed.
        @position: The position where the text should be displayed.
        @size: The size of the font.
        @color: The color of the text.
        """
        font = pygame.font.Font(None, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect(center=position)
        self.screenSurface.blit(textSurface, textRect)
        pygame.display.flip()

    def drawAlgorithmSelectionMenu(self):
        """Draw the algorithm selection menu and return the selected algorithm."""
        # Get all algorithms and their names
        algorithms = Algorithms.algorithms
        algorithmNames = list(algorithms.keys())

        algorithmSelected = 0

        while True:
            # Clear the screen
            self.screenSurface.fill((0, 0, 0))
            # Draw the title
            self.drawMenu(
                "Select an algorithm",
                (self.screenSize[0] / 2, self.screenSize[1] / 2 - 50),
            )
            # Draw every algorithm names for selection
            for i, algorithm in enumerate(algorithmNames):
                self.drawMenu(
                    algorithm,
                    (self.screenSize[0] / 2, self.screenSize[1] / 2 + 50 + 50 * i),
                    i == algorithmSelected,
                )

            pygame.display.flip()

            # Track movement events
            for event in pygame.event.get():
                # Update algorithm selected based on key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        algorithmSelected = (algorithmSelected - 1) % len(algorithms)
                    elif event.key == pygame.K_DOWN:
                        algorithmSelected = (algorithmSelected + 1) % len(algorithms)
                    # Return the selected algorithm
                    elif event.key == pygame.K_RETURN:
                        return algorithms[algorithmNames[algorithmSelected]]
                # Exit the game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def drawLevelSelectionMenu(self):
        """Draw the level selection menu and return the selected level."""
        levels = [f"Level {i}" for i in range(1, 11)]

        levelSelected = 0

        while True:
            # Clear the screen
            self.screenSurface.fill((0, 0, 0))
            # Draw the title
            self.drawMenu("Select a level", (self.screenSize[0] / 2, 50))
            # Draw every level for selection
            for i, level in enumerate(levels):
                self.drawMenu(
                    level, (self.screenSize[0] / 2, 100 + 50 * i), i == levelSelected
                )

            pygame.display.flip()

            # Track movement events
            for event in pygame.event.get():
                # Update level selected based on key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        levelSelected = (levelSelected - 1) % len(levels)
                    elif event.key == pygame.K_DOWN:
                        levelSelected = (levelSelected + 1) % len(levels)
                    # Return the selected level
                    elif event.key == pygame.K_RETURN:
                        return levelSelected + 1
                # Exit the game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def drawLevel(self, matrix: list):
        """Draw the level on the screen.

        ### Parameters
        @matrix: The matrix representing the level.
        """
        # Iterate all Rows
        for i in range(0, len(matrix)):
            # Iterate all columns of the row and draw the corresponding sprite
            for c in range(0, len(matrix[i])):
                self.screenSurface.blit(
                    self.sprites[matrix[i][c]], (c * self.imageSize, i * self.imageSize)
                )
        # Update the display
        pygame.display.update()

    def drawSuccessScreen(self):
        """Draw the success screen when a level is completed."""
        # Clear the screen
        self.screenSurface.fill((0, 0, 0))
        # Draw the success message
        self.drawMenu(
            "Level Completed", (self.screenSize[0] / 2, self.screenSize[1] / 2)
        )
        # Draw the message to continue
        self.drawMenu(
            "Press any key to continue",
            (self.screenSize[0] / 2, self.screenSize[1] / 2 + 50),
        )

        pygame.display.flip()

        # Wait for any key to be pressed
        while True:
            for event in pygame.event.get():
                # Return if any key is pressed
                if event.type == pygame.KEYDOWN:
                    return
                # Exit the game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def drawSolutionNotFoundScreen(self):
        """Draw the success screen when a level is completed."""
        # Clear the screen
        self.screenSurface.fill((0, 0, 0))
        # Draw the success message
        self.drawMenu(
            "Solution not found", (self.screenSize[0] / 2, self.screenSize[1] / 2)
        )
        # Draw the message to continue
        self.drawMenu(
            "Press any key to continue",
            (self.screenSize[0] / 2, self.screenSize[1] / 2 + 50),
        )

        pygame.display.flip()

        # Wait for any key to be pressed
        while True:
            for event in pygame.event.get():
                # Return if any key is pressed
                if event.type == pygame.KEYDOWN:
                    return
                # Exit the game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def initLevel(self, levelNumber: int, algorithm) -> Level.Level:
        """Initialize the level and draw it on the screen.

        ### Parameters
        @levelNumber: The number of the level to be initialized.
        @algorithm: The algorithm to be used for solving the level.

        ### Returns
        @level: The initialized level.
        """
        # Clear the screen
        self.screenSurface.fill((0, 0, 0))

        # Draw the menu
        pygame.display.flip()
        self.drawText("Level " + str(levelNumber), (self.screenSize[1], 200))
        self.drawText("Algorithm: " + algorithm.__name__, (self.screenSize[1], 250))
        self.drawText("Press S to solve", (self.screenSize[1], 300))
        self.drawText("Press M to return to menu", (self.screenSize[1], 350))

        # Create an instance of this Level and draw it
        level = Level.Level(levelNumber)
        self.drawLevel(level.getMatrix())

        return level
