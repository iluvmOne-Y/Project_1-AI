import os as os
import sys as sys
import pygame as pygame

import Algorithms as Algorithms
import Level as Level

HeaderFont = 'themes/Header-font3.otf'
TextFont1 = 'themes/Text-font2.ttf'
TextFont2 = 'themes/Text-font1.ttf'

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


    def getPath(self):
        """Return the path of the current file."""
        return os.path.dirname(os.path.abspath(__file__))
    

    def __init__(self):
        """Initialize the UI, including the display, font, and sprites."""
        # Initialize the display for all platforms
        pygame.display.init()
        pygame.display.set_caption("Ares' adventure")  # Window title
        self.screenSize = (550, 700)  # Window size
        self.screenSurface = pygame.display.set_mode(self.screenSize, pygame.RESIZABLE)  # Window

        # Clear the screen to white
        self.screenSurface.fill((255, 255, 255))
        # Initialize font support
        pygame.font.init()
        # Hide the mouse cursor
        pygame.mouse.set_visible(True)
        # Update the display
        pygame.display.update()

        # Load all sprites
        self.sprites["@"] = pygame.image.load(
            self.getPath() + "/themes/images/player.png"
        ).convert()  # Player
        self.sprites["+"] = pygame.image.load(
            self.getPath() + "/themes/images/player.png"
        ).convert()  # Player on target
        self.sprites[" "] = pygame.image.load(
            self.getPath() + "/themes/images/space.png"
        ).convert()  # Space
        self.sprites["#"] = pygame.image.load(
            self.getPath() + "/themes/images/wall.png"
        ).convert()  # Wall
        self.sprites["$"] = pygame.image.load(
            self.getPath() + "/themes/images/box.png"
        ).convert()  # Box
        self.sprites["."] = pygame.image.load(
            self.getPath() + "/themes/images/target.png"
        ).convert()  # Target
        self.sprites["*"] = pygame.image.load(
            self.getPath() + "/themes/images/box_on_target.png"
        ).convert()  # Box on target

        # Get image size
        self.imageSize = self.sprites["#"].get_width()

    def drawMenu(self, text: str, position: list, selected: bool = False, textFont: str = None):
        """Draw the menu with the given text at the specified position.

        ### Parameters
        @text: The text to be displayed.
        @position: The position where the text should be displayed.
        @selected: Whether the menu item is selected.
        @textFont: Set the text font.
        """
        font = pygame.font.Font(textFont, 50)  # Updated font path
        color = (255, 255, 0) if selected else (255, 255, 255)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect(center=position)
        self.screenSurface.blit(textSurface, textRect)

    def drawText(
        self, text: str, position: list, size: int = 36, color: tuple = (255, 255, 255), textFont: str = None):
        """Draw the text at the specified position.

        ### Parameters
        @text: The text to be displayed.
        @position: The position where the text should be displayed.
        @size: The size of the font.
        @color: The color of the text.
        @textFont: Set the text font.
        """
        font = pygame.font.Font(textFont, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect(center=position)
        self.screenSurface.blit(textSurface, textRect)

    def drawSelectionMenu(self):
        """Draw the combined algorithm and level selection menu and return the selected algorithm and level."""

        levels = [f"Level {i}" for i in range(1, 11)]
        algorithms = Algorithms.algorithms
        algorithmNames = list(algorithms.keys())

        levelSelected = 0
        algorithmSelected = 0
        
        while True:
            # Clear the screen
            self.screenSurface.fill((0, 0, 0))
            # Draw background
            background = pygame.image.load(os.path.join(self.getPath(), "themes/images/background2.png"))
            self.screenSurface.blit(background, (0, 0))

            try:
                # Try to load and draw background
                background = pygame.image.load("themes/images/background2.png")
                self.screenSurface.blit(background, (0, 0))
            except (pygame.error, FileNotFoundError):
                # If background image is missing, draw a gradient or pattern
                for y in range(0, self.screenSize[1], 2):
                    color = (max(0, 40 - y//10), 0, max(0, 20 - y//20))
                    pygame.draw.line(self.screenSurface, color, 
                                (0, y), (self.screenSize[0], y))
            # Draw game's title
            self.drawMenu("Ares' Adventure", (self.screenSize[0] / 2, 90), True, HeaderFont)

            # Draw the level selection title
            self.drawText("Select your level", (self.screenSize[0] / 2, 150), 29, (255, 123, 255), TextFont2)
            
            # Draw the border box for the current level
            levelText = levels[levelSelected]
            font = pygame.font.Font(None, 40)
            textSurface = font.render(levelText, True, (255, 255, 255))
            textRect = textSurface.get_rect(center=(self.screenSize[0] / 2, 200))
            borderRect = textRect.inflate(20, 20)
            pygame.draw.rect(self.screenSurface, (255, 255, 255), borderRect, 4)
            centeredTextRect = textSurface.get_rect(center=borderRect.center)
            self.screenSurface.blit(textSurface, centeredTextRect)

            # Draw the border box for the current algorithm
            algorithmText = algorithmNames[algorithmSelected]
            font = pygame.font.Font(None, 44)
            textSurface = font.render(algorithmText, True, (255, 255, 255))
            textRect = textSurface.get_rect(center=(self.screenSize[0] / 2, 600))
            borderRect = textRect.inflate(20, 20)
            pygame.draw.rect(self.screenSurface, (255, 255, 255), borderRect, 4)
            centeredTextRect = textSurface.get_rect(center=borderRect.center)
            self.screenSurface.blit(textSurface, centeredTextRect)

            # Draw the level
            level = Level.Level(levelSelected + 1)
            self.drawLevel(level.getMatrix())
            del level

            pygame.display.flip()

            # Track movement events
            for event in pygame.event.get():
                # Update level or algorithm selected based on key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        levelSelected = (levelSelected - 1) % len(levels)
                    elif event.key == pygame.K_RIGHT:
                        levelSelected = (levelSelected + 1) % len(levels)
                    elif event.key == pygame.K_UP:
                        algorithmSelected = (algorithmSelected - 1) % len(algorithms)
                    elif event.key == pygame.K_DOWN:
                        algorithmSelected = (algorithmSelected + 1) % len(algorithms)
                    elif event.key == pygame.K_RETURN:
                        return algorithms[algorithmNames[algorithmSelected]], levelSelected + 1
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                # Exit the game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def drawLevel(self, matrix: list):
        """Draw the level on the screen.

        ### Parameters
        @matrix: The matrix representing the level.
        """
        # Calculate the offset to center the level
        levelWidth = len(matrix[0]) * self.imageSize
        levelHeight = len(matrix) * self.imageSize
        offsetX = (self.screenSize[0] - levelWidth) // 2
        offsetY = (self.screenSize[1] - levelHeight) // 2

        # Iterate all Rows
        for i in range(0, len(matrix)):
            # Iterate all columns of the row and draw the corresponding sprite
            for c in range(0, len(matrix[i])):
                self.screenSurface.blit(
                    self.sprites[matrix[i][c]], (c * self.imageSize + offsetX, i * self.imageSize + 245)
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
    def drawStats(self, stats):
        """Draw the algorithm statistics on the screen.
    
        ### Parameters
        @stats: Dictionary containing path, time and nodes statistics
        """
        # Clear the stats area
        pygame.draw.rect(self.screenSurface, (0, 0, 0), 
                    (self.screenSize[0]-500, 500, 500, 200))
    
        # Draw statistics
        y_pos = 500
        for key, value in stats.items():
            if key == 'path':
                path_chunks = [value[i:i+20] for i in range(0, len(value), 20)]
                self.drawText(f"Path", (self.screenSize[0]/2, y_pos))
                y_pos += 20
                for chunk in path_chunks:
                    self.drawText(chunk, (self.screenSize[0]/2, y_pos),size=20)
                    y_pos += 20
            else:
                self.drawText(f"{key}: {value}", (self.screenSize[0]/2, y_pos))
                y_pos += 40
        pygame.display.update()
        
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
        self.drawText("Level " + str(levelNumber), (self.screenSize[0]/2, 50))
        self.drawText("Algorithm: " + algorithm.__name__, (self.screenSize[0]/2, 100))
        self.drawText("Press S to solve", (self.screenSize[0]/2, 150))
        self.drawText("Press M to return to menu", (self.screenSize[0]/2, 200))

        # Create an instance of this Level and draw it
        level = Level.Level(levelNumber)
        self.drawLevel(level.getMatrix())
        return level
