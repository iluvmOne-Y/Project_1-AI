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
    imageSize: int 
    """The size of the images."""


    def getPath(self):
        """Return the path of the current file."""
        return os.path.dirname(os.path.abspath(__file__))
    

    def __init__(self):
        """Initialize the UI, including the display, font, and sprites."""
        # Initialize the display for all platforms
        pygame.display.init()
        pygame.display.set_caption("Ares' adventure")  # Window title
        display_info = pygame.display.Info()
        monitor_width, monitor_height = display_info.current_w, display_info.current_h
        self.default_size = (550*2, 700*2)  # Window size
        self.screenSize = (min(int(monitor_width * 0.8), self.default_size[0]), 
                       min(int(monitor_height * 0.8), self.default_size[1]))
        self.scale_factor = min(self.screenSize[0] / self.default_size[0], 
                           self.screenSize[1] / self.default_size[1])
        
        
        self.screenSurface = pygame.display.set_mode(self.screenSize, pygame.RESIZABLE)  # resize

        # Clear the screen to white
        self.screenSurface.fill((255, 255, 255))
        # Initialize font support
        pygame.font.init()
        # Hide the mouse cursor
        pygame.mouse.set_visible(True)
        # Update the display
        pygame.display.update()
        self.loadSprites()
        '''
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
        '''
    def loadSprites(self):
        """Load and scale game sprites based on current screen size."""
        sprite_paths = {
            "@": "themes/images/player.png",
            "+": "themes/images/player_on_target.png", 
            " ": "themes/images/space.png",
            "#": "themes/images/wall.png",
            "$": "themes/images/box.png",
            ".": "themes/images/target.png",
            "*": "themes/images/box_on_target.png"
        }
        
        # Store original size (assuming all tiles are square)
        base_size = 32  # Default size if loading fails
        
        # Load and scale sprites based on current window size
        optimal_size = min(
            self.screenSize[0] // 20,  # Approximate level width
            self.screenSize[1] // 15   # Approximate level height
        )
        self.imageSize = max(optimal_size, 16)  # Minimum size threshold
        
        self.sprites = {}
        for key, path in sprite_paths.items():
            try:
                original = pygame.image.load(path).convert_alpha()
                self.sprites[key] = pygame.transform.scale(original, (self.imageSize, self.imageSize))
            except (pygame.error, FileNotFoundError):
                # Create a colored rectangle as fallback
                surface = pygame.Surface((self.imageSize, self.imageSize))
                if key == "@":  # Player
                    surface.fill((255, 0, 0))  # Red
                elif key in ["$", "*"]:  # Box
                    surface.fill((165, 42, 42))  # Brown
                elif key in [".", "+"]:  # Target
                    surface.fill((0, 255, 0))  # Green
                elif key == "#":  # Wall
                    surface.fill((128, 128, 128))  # Gray
                else:  # Space
                    surface.fill((0, 0, 0))  # Black
                self.sprites[key] = surface

    def handleResize(self, new_size):
        """Handle window resize events."""
        self.screenSize = new_size
        self.scale_factor = min(self.screenSize[0] / self.default_size[0], 
                               self.screenSize[1] / self.default_size[1])
        
        # Reload and rescale sprites
        self.loadSprites()
        if hasattr(self, 'current_level_number'):
        # Redraw current screen
            if hasattr(self, 'current_algorithm'):
                level = Level.Level(self.current_level_number)
                self.draw_gameplay_screen(level, self.current_algorithm)
        # Redraw the screen
        pygame.display.update()
        
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

    def drawText(self, text: str, position: list, size: int = 36, color: tuple = (255, 255, 255), textFont: str = None):
        """Draw the text at the specified position with proper scaling."""
        # Scale font size proportionally to screen size
        scaled_size = int(size * self.scale_factor)
        font = pygame.font.Font(textFont, scaled_size)
        textSurface = font.render(text, True, color)
        # Scale position values based on current screen dimensions
        scaled_position = (
            position[0] * (self.screenSize[0] / self.default_size[0]),
            position[1] * (self.screenSize[1] / self.default_size[1])
        )
        textRect = textSurface.get_rect(center=scaled_position)
        self.screenSurface.blit(textSurface, textRect)
    
    def drawSelectionMenu(self):
        """Draw the combined algorithm and level selection menu and return the selected algorithm and level."""

        levels = [f"Level {i}" for i in range(1, 11)]
        algorithms = Algorithms.algorithms
        algorithmNames = list(algorithms.keys())
        preview_offset = 245
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
            title_y = self.default_size[1] * 0.1
            level_selection_y = self.default_size[1] * 0.15
            level_box_y = self.default_size[1] * 0.2
            algo_box_y = self.default_size[1] * 0.65
            preview_offset = self.default_size[1] * 0.25
            # Draw game's title
            self.drawMenu("Ares' Adventure", (self.screenSize[0] / 2, 50), True, HeaderFont)

            # Draw the level selection title
            self.drawText("Select your level", (self.screenSize[0] / 2, 150), 40, (255, 123, 255), TextFont2)
            
            # Draw the border box for the current level
            levelText = levels[levelSelected]
            font = pygame.font.Font(None, 40)
            textSurface = font.render(levelText, True, (255, 255, 255))
            textRect = textSurface.get_rect(center=(self.screenSize[0] / 2, 150))
            borderRect = textRect.inflate(20, 20)
            pygame.draw.rect(self.screenSurface, (255, 255, 255), borderRect, 4)
            centeredTextRect = textSurface.get_rect(center=borderRect.center)
            self.screenSurface.blit(textSurface, centeredTextRect)

            # Draw the border box for the current algorithm
            algorithmText = algorithmNames[algorithmSelected]
            font = pygame.font.Font(None, 44)
            textSurface = font.render(algorithmText, True, (255, 255, 255))
            textRect = textSurface.get_rect(center=(self.screenSize[0] / 2, 750))
            borderRect = textRect.inflate(20, 20)
            pygame.draw.rect(self.screenSurface, (255, 255, 255), borderRect, 4)
            centeredTextRect = textSurface.get_rect(center=borderRect.center)
            self.screenSurface.blit(textSurface, centeredTextRect)

            # Draw the level
            level = Level.Level(levelSelected + 1)
            self.drawLevel(level.getMatrix(), offsetY=preview_offset)
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
                elif event.type == pygame.VIDEORESIZE:
                    self.handleResize(event.size)
        # Redraw the current screen
                    level = Level.Level(levelSelected + 1)
                    self.drawLevel(level.getMatrix(), offsetY=preview_offset)
                    del level
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def drawLevel(self, matrix: list, offsetY: int = 150):
        """Draw the level on the screen.

        ### Parameters
        @matrix: The matrix representing the level.
        """
        scaled_offsetY = int(offsetY * self.scale_factor)
        # Calculate the offset to center the level
        levelWidth = len(matrix[0]) * self.imageSize
        levelHeight = len(matrix) * self.imageSize
        offsetX = (self.screenSize[0] - levelWidth) // 2  
        
        
        # Iterate all Rows
        for i in range(0, len(matrix)):
            # Iterate all columns of the row and draw the corresponding sprite
            for c in range(0, len(matrix[i])):
                self.screenSurface.blit(
                    self.sprites[matrix[i][c]], (c * self.imageSize + offsetX, i * self.imageSize + scaled_offsetY)
                )
        # Update the display
        pygame.display.update()
    '''
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
    '''
    '''
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
    '''
    def drawStats(self, stats):
        """Draw the algorithm statistics on the screen."""
        self.current_stats = stats
        
        # Calculate stats area dimensions based on screen size
        stats_area_width = self.screenSize[0] * 0.98  # 98% of screen width
        stats_area_height = self.screenSize[1] * 0.15  # 15% of screen height
        stats_area_x = (self.screenSize[0] - stats_area_width) / 2  # Centered horizontally
        stats_area_y = self.screenSize[1] - stats_area_height - 20  # Position at bottom with 10px padding
        
        # Clear the stats area with a semi-transparent black
        stats_surface = pygame.Surface((stats_area_width, stats_area_height), pygame.SRCALPHA)
        stats_surface.fill((0, 0, 0, 180))  # Semi-transparent black
        self.screenSurface.blit(stats_surface, (stats_area_x, stats_area_y))
        
        # Extract the core stats (to display on the same line)
        time_value = stats.get('time', '0.00s')
        nodes_value = stats.get('nodes', '0')
        steps_value = stats.get('steps', '0')
        memory_value = stats.get('memory', '0.00MB')
        path_value = stats.get('path', '')
        
        # First display the path at the top if it exists
        if path_value:
            # Position path at top of stats area
            path_y = stats_area_y + stats_area_height * 0.25
            
            # Calculate max characters based on screen width
            chars_per_line = max(40, int(stats_area_width / (10 * self.scale_factor)))
            path_display = path_value[:chars_per_line]
            
            # Add ellipsis if path is longer than what we can show
            if len(path_value) > chars_per_line:
                path_display = path_display[:-3] + "..."
            
            # Draw the path with larger font size
            scaled_path_size = int(30 * self.scale_factor)  # Larger font size for path
            path_font = pygame.font.Font(None, scaled_path_size)
            path_text = f"Path: {path_display}"
            path_surface = path_font.render(path_text, True, (255, 255, 255))
            path_rect = path_surface.get_rect(center=(self.screenSize[0]/2, path_y))
            self.screenSurface.blit(path_surface, path_rect)
        
        # Display the core stats on a single line at the bottom
        bottom_stats_y = self.screenSize[1] - stats_area_height * 0.6  # Move stats down to leave room for path
        
        # Calculate horizontal positions for each stat
        stat_width = stats_area_width / 4
        time_x = stats_area_x + stat_width/2
        nodes_x = stats_area_x + stat_width + stat_width/2
        steps_x = stats_area_x + stat_width*2 + stat_width/2
        memory_x = stats_area_x + stat_width*3 + stat_width/2
        
        # Draw the core stats with custom colors
        scaled_size = int(40 * self.scale_factor)
        
        # Time stat (green)
        time_font = pygame.font.Font(None, scaled_size)
        time_text = f"Time: {time_value}"
        time_surface = time_font.render(time_text, True, (100, 255, 100))
        time_rect = time_surface.get_rect(center=(time_x, bottom_stats_y))
        self.screenSurface.blit(time_surface, time_rect)
        
        # Nodes stat (blue)
        nodes_font = pygame.font.Font(None, scaled_size)
        nodes_text = f"Nodes: {nodes_value}"
        nodes_surface = nodes_font.render(nodes_text, True, (100, 100, 255))
        nodes_rect = nodes_surface.get_rect(center=(nodes_x, bottom_stats_y))
        self.screenSurface.blit(nodes_surface, nodes_rect)
        
        # Steps stat (red)
        steps_font = pygame.font.Font(None, scaled_size)
        steps_text = f"Steps: {steps_value}"
        steps_surface = steps_font.render(steps_text, True, (255, 100, 100))
        steps_rect = steps_surface.get_rect(center=(steps_x, bottom_stats_y))
        self.screenSurface.blit(steps_surface, steps_rect)
        
        # Memory stat (yellow)
        memory_font = pygame.font.Font(None, scaled_size)
        memory_text = f"Memory: {memory_value}"
        memory_surface = memory_font.render(memory_text, True, (255, 255, 100))
        memory_rect = memory_surface.get_rect(center=(memory_x, bottom_stats_y))
        self.screenSurface.blit(memory_surface, memory_rect)
        
        # Update the display
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
    
        # Create an instance of this Level
        level = Level.Level(levelNumber)
        
        # Store current level and algorithm info for redrawing
        self.current_level_number = levelNumber
        self.current_algorithm = algorithm
        
        # Draw the level and menu
        self.draw_gameplay_screen(level, algorithm)
        
        return level
    
    def draw_gameplay_screen(self, level, algorithm):
        """Draw the gameplay screen with level and UI elements."""
        # Clear the screen
        self.screenSurface.fill((0, 0, 0))
        
        # Use relative positioning based on default screen size
        header_y_base = 50
        y_spacing = 20
        
        # Draw the menu text using default_size coordinates which will be scaled by drawText
        self.drawText(f"Level {self.current_level_number}", (self.default_size[0]/2, header_y_base))
        self.drawText(f"Algorithm: {algorithm.__name__}", (self.default_size[0]/2, header_y_base + y_spacing))
        self.drawText("Press S to solve", (self.default_size[0]/2, header_y_base + y_spacing*2))
        self.drawText("Press M to return to menu", (self.default_size[0]/2, header_y_base + y_spacing*3))
        self.drawText("Press SPACE to pause animation", (self.default_size[0]/2, header_y_base + y_spacing*4))
        # Draw the level with proportional padding
        gameplay_offset = self.default_size[1] * 0.15  # 15% of height
        self.drawLevel(level.getMatrix(), offsetY=gameplay_offset)
        
        # Update the display
        pygame.display.flip()