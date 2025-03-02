import _TYPES as _TYPES

# Intergrated modules
import os as os
import sys as sys
import copy as copy
import pathlib as pathlib

# External modules
import pygame as pygame

# Custom modules
from Algorithms.BFS import BFS
from Algorithms.DFS import DFS
from Algorithms.UCS import UCS
from Algorithms.AStar import AStar
from Algorithms.Dijkstra import Dijkstra
from Algorithms.GreedyBFS import GreedyBFS
# Get the fonts
HeaderFont = "Data/Assets/Fonts/Header-font3.otf"
TextFont1 = "Data/Assets/Fonts/Text-font2.ttf"
TextFont2 = "Data/Assets/Fonts/Text-font1.ttf"


# Get the number of input files
inputNumber = 0

currentDirectory = pathlib.Path("Inputs")
for item in currentDirectory.iterdir():
    if item.is_file() and item.name[:5] == "input" and item.suffix == ".txt":
        inputNumber += 1

# Initialize the levels
levels: list = [_TYPES.Level(i) for i in range(1, inputNumber + 1)]

# Get the algorithms
algorithms: list = [BFS, DFS, UCS, AStar, Dijkstra, GreedyBFS]

# Set the display to be centered
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Initialize the display for the game
pygame.display.init()
pygame.display.set_caption("Ares' adventure")  # Window title

# Initialize the sprites
sprites: dict = {}

# Set the screen size
screenSize: tuple = (550, 700)
screenSurface: pygame.Surface = pygame.display.set_mode(screenSize, pygame.RESIZABLE)

# Load all sprites
sprites["@"] = pygame.image.load(
    "Data/Assets/Images/Icons/player.png"
).convert()  # Player
sprites["+"] = pygame.image.load(
    "Data/Assets/Images/Icons/player.png"
).convert()  # Player on target
sprites[" "] = pygame.image.load(
    "Data/Assets/Images/Icons/space.png"
).convert()  # Space
sprites["#"] = pygame.image.load("Data/Assets/Images/Icons/wall.png").convert()  # Wall
sprites["$"] = pygame.image.load("Data/Assets/Images/Icons/box.png").convert()  # Box
sprites["."] = pygame.image.load(
    "Data/Assets/Images/Icons/target.png"
).convert()  # Target
sprites["*"] = pygame.image.load(
    "Data/Assets/Images/Icons/box_on_target.png"
).convert()  # Box on target

# Get the size of the sprites
imageSize = sprites["#"].get_width()

# Set the screen size
screenSize = (
    max(level.matrixSize[0] for level in levels) * imageSize + 200,
    max(level.matrixSize[1] for level in levels) * imageSize + 350,
)

# Quit the display and reinitialize it
pygame.display.quit()
screenSurface = pygame.display.set_mode(screenSize, pygame.RESIZABLE)

# Update some settings
pygame.font.init()
pygame.mouse.set_visible(True)

# Clear the screen to white
screenSurface.fill((255, 255, 255))
pygame.display.update()

# Set the preview offset
previewOffset = screenSize[1] / 3 + 20
solvingOffset = 200


def DrawText(
    text: str,
    position: tuple,
    size: int = 36,
    color: tuple = (255, 255, 255),
    textFont: str = None,
):
    """Draw the text at the specified position.

    ### Parameters
    - text: The text to be displayed.
    - position: The position where the text should be displayed.
    - size: The size of the font.
    - color: The color of the text.
    - textFont: Set the text font.
    """
    font = pygame.font.Font(textFont, size)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect(center=position)
    screenSurface.blit(textSurface, textRect)


def DrawMatrix(matrix: list, matrixSize: tuple, offsetY: int = solvingOffset):
    """Draw the maze on the screen.

    ### Parameters
    - matrix: The matrix to draw.
    - matrixSize: The size of the matrix.
    - offsetY: The offset in Y axis (height) to draw at. By default, it is 160.
    """
    # Calculate the offset to center the level
    offsetX = (screenSize[0] - matrixSize[0] * imageSize) // 2

    # Iterate all Rows
    for i in range(0, len(matrix)):
        isVoid: bool = True
        # Iterate all objects of the row and draw the corresponding sprite
        for c in range(0, len(matrix[i])):
            # Skip if the character is a void space
            if matrix[i][c] == " " and isVoid:
                continue
            else:
                isVoid = False

            screenSurface.blit(
                sprites[matrix[i][c]],
                (c * imageSize + offsetX, i * imageSize + offsetY),
            )

    # Update the display
    pygame.display.update()


def DrawSelectionScreen(levelSelected: int, algorithmSelected: int):
    """Draw the selection screen.

    ### Parameters
    - levelSelected: The selected level.
    - algorithmSelected: The selected algorithm.
    """
    # Clear the screen
    screenSurface.fill((0, 0, 0))
    # Draw background
    background = pygame.image.load(
        os.path.join("Data/Assets/Images/Background/background2.png")
    )
    screenSurface.blit(background, (0, 0))

    # Try to load and draw background
    try:
        background = pygame.image.load("Data/Assets/Images/Background/background2.png")
        screenSurface.blit(background, (0, 0))
    except (pygame.error, FileNotFoundError):
        # If background image is missing, draw a gradient or pattern
        for y in range(0, screenSize[1], 2):
            color = (max(0, 40 - y // 10), 0, max(0, 20 - y // 20))
            pygame.draw.line(screenSurface, color, (0, y), (screenSize[0], y))

    # Draw game's title
    DrawText(
        "Ares' Adventure", (screenSize[0] / 2, 90), 50, (255, 255, 255), HeaderFont
    )

    # Draw the level selection title
    DrawText(
        "Select your level",
        (screenSize[0] / 2, 150),
        29,
        (255, 123, 255),
        TextFont2,
    )

    # Draw the border box for the current level
    levelText = "Level " + str(levels[levelSelected].number)
    font = pygame.font.Font(None, 40)
    textSurface = font.render(levelText, True, (255, 255, 255))
    textRect = textSurface.get_rect(center=(screenSize[0] / 2, 200))
    borderRect = textRect.inflate(20, 20)
    pygame.draw.rect(screenSurface, (255, 255, 255), borderRect, 4)
    centeredTextRect = textSurface.get_rect(center=borderRect.center)
    screenSurface.blit(textSurface, centeredTextRect)

    # Draw the border box for the current algorithm
    algorithmText = algorithms[algorithmSelected].__name__
    font = pygame.font.Font(None, 44)
    textSurface = font.render(algorithmText, True, (255, 255, 255))
    textRect = textSurface.get_rect(center=(screenSize[0] / 2, screenSize[1] - 70))
    borderRect = textRect.inflate(20, 20)
    pygame.draw.rect(screenSurface, (255, 255, 255), borderRect, 4)
    centeredTextRect = textSurface.get_rect(center=borderRect.center)
    screenSurface.blit(textSurface, centeredTextRect)

    # Draw the level
    DrawMatrix(
        levels[levelSelected].getMatrix(),
        levels[levelSelected].matrixSize,
        previewOffset,
    )

    pygame.display.flip()


def DrawSelectionScreen(levelSelected: int, algorithmSelected: int):
    """Draw the selection screen.

    ### Parameters
    - levelSelected: The selected level.
    - algorithmSelected: The selected algorithm.
    """
    # Clear the screen
    screenSurface.fill((0, 0, 0))
    # Draw background
    background = pygame.image.load(
        os.path.join("Data/Assets/Images/Background/background2.png")
    )
    screenSurface.blit(background, (0, 0))

    # Try to load and draw background
    try:
        background = pygame.image.load("Data/Assets/Images/Background/background2.png")
        screenSurface.blit(background, (0, 0))
    except (pygame.error, FileNotFoundError):
        # If background image is missing, draw a gradient or pattern
        for y in range(0, screenSize[1], 2):
            color = (max(0, 40 - y // 10), 0, max(0, 20 - y // 20))
            pygame.draw.line(screenSurface, color, (0, y), (screenSize[0], y))

    # Draw game's title
    DrawText(
        "Ares' Adventure", (screenSize[0] / 2, 90), 50, (255, 255, 255), HeaderFont
    )

    # Draw the level selection title
    DrawText(
        "Select your level",
        (screenSize[0] / 2, 150),
        29,
        (255, 123, 255),
        TextFont2,
    )

    # Draw the border box for the current level
    levelText = "Level " + str(levels[levelSelected].number)
    font = pygame.font.Font(None, 40)
    textSurface = font.render(levelText, True, (255, 255, 255))
    textRect = textSurface.get_rect(center=(screenSize[0] / 2, 200))
    borderRect = textRect.inflate(20, 20)
    pygame.draw.rect(screenSurface, (255, 255, 255), borderRect, 4)
    centeredTextRect = textSurface.get_rect(center=borderRect.center)
    screenSurface.blit(textSurface, centeredTextRect)

    # Draw the border box for the current algorithm
    algorithmText = algorithms[algorithmSelected].__name__
    font = pygame.font.Font(None, 44)
    textSurface = font.render(algorithmText, True, (255, 255, 255))
    textRect = textSurface.get_rect(center=(screenSize[0] / 2, screenSize[1] - 60))
    borderRect = textRect.inflate(20, 20)
    pygame.draw.rect(screenSurface, (255, 255, 255), borderRect, 4)
    centeredTextRect = textSurface.get_rect(center=borderRect.center)
    screenSurface.blit(textSurface, centeredTextRect)

    # Draw the level
    DrawMatrix(
        levels[levelSelected].getMatrix(),
        levels[levelSelected].matrixSize,
        previewOffset,
    )

    pygame.display.flip()


def DrawSelectionMenu() -> tuple[_TYPES.Level, _TYPES.Algorithm]:
    """Draw the combined algorithm and level selection menu.

    ### Returns
    - tuple: The selected level and algorithm.
    """
    # Initialize the selected level and algorithm
    levelSelected: int = 0
    algorithmSelected: int = 0

    # Draw the selection screen
    DrawSelectionScreen(levelSelected, algorithmSelected)

    while True:
        # Track movement events
        for event in pygame.event.get():
            # Update level or algorithm selected based on key pressed
            if event.type == pygame.KEYDOWN:
                # Update level selected with left and right key
                if event.key == pygame.K_LEFT:
                    levelSelected = (levelSelected - 1) % len(levels)
                    DrawSelectionScreen(levelSelected, algorithmSelected)

                elif event.key == pygame.K_RIGHT:
                    levelSelected = (levelSelected + 1) % len(levels)
                    DrawSelectionScreen(levelSelected, algorithmSelected)

                # Update algorithm selected with up and down key
                elif event.key == pygame.K_UP:
                    algorithmSelected = (algorithmSelected - 1) % len(algorithms)
                    DrawSelectionScreen(levelSelected, algorithmSelected)
                elif event.key == pygame.K_DOWN:
                    algorithmSelected = (algorithmSelected + 1) % len(algorithms)
                    DrawSelectionScreen(levelSelected, algorithmSelected)

                # Return the selected level and algorithm
                elif event.key == pygame.K_RETURN:
                    # Clear the screen
                    screenSurface.fill((0, 0, 0))

                    # Draw the display for the selected level and algorithm
                    DrawText(
                        "Level " + str(levelSelected + 1), (screenSize[0] / 2, 50), 50
                    )
                    DrawText(
                        "Algorithm: " + algorithms[algorithmSelected].__name__,
                        (screenSize[0] / 2, 95),
                        45,
                    )
                    DrawText(
                        "Press 'S' to solve",
                        (screenSize[0] / 2, screenSize[1] - 90),
                        40,
                    )
                    DrawText(
                        "Press 'M' to return to menu",
                        (screenSize[0] / 2, screenSize[1] - 50),
                        40,
                    )

                    # Create an instance of this Level and draw it
                    level = _TYPES.Level(levelSelected + 1)
                    DrawMatrix(level.getMatrix(), level.matrixSize, solvingOffset)

                    # Return the selected level instance and algorithm
                    return (
                        copy.deepcopy(level),
                        algorithms[algorithmSelected],
                    )

                # Exit the game if escape key is pressed
                elif event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                    return None

            # Also exit the game if the window is closed
            elif event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

                return None


def DrawSuccessScreen(level: _TYPES.Level, algorithmName: str,solution: _TYPES.Solution= None):
    """Draw the success screen when a level is completed.

    ### Parameters
    - level: The level that is completed.
    - algorithmName: The name of the algorithm used to solve the level.
    """
    # Clear the screen
    screenSurface.fill((0, 0, 0))

    # Redraw the background
    DrawText("Level " + str(level.number) + ": Solved!", (screenSize[0] / 2, 40), 40)
    DrawText(
        "Algorithm: " + algorithmName,
        (screenSize[0] / 2, 60),
        40,
    )

    #
    DrawText("Press 'Space' to (un)pause", (screenSize[0] / 2,100),30 )
    DrawText(
        "Press 'Left'/'Right' to change matrix to previous/next state",
        (screenSize[0] / 2, 120),30
    )
    DrawText(
        "Press 'R' to restart",
        (screenSize[0] / 2, 140),30
    )
    DrawText(
        "Press 'M' to return to menu",
        (screenSize[0] / 2, 160),30
    )

    # Create an instance of this Level and draw it
    DrawMatrix(level.getMatrix(), level.matrixSize, solvingOffset)
    if solution:
        stats = {
            "path": "".join(solution.path),
            "time": f"{solution.timeTaken:.2f}s",
            "nodes": str(solution.nodesExpanded),
            "steps": str(solution.steps),
            "memory": f"{solution.memoryUsage:.2f}MB",
            "status": "Solved"
        }
        DrawStats(stats)

def DrawFailScreen(level: _TYPES.Level, algorithmName: str):
    """Draw the success screen when a level is completed.

    ### Parameters
    - level: The level that is completed.
    - algorithmName: The name of the algorithm used to solve the level.
    """
    # Clear the screen
    screenSurface.fill((0, 0, 0))

    # Redraw the background
    DrawText("Level " + str(level.number), (screenSize[0] / 2, 60), 50)
    DrawText(
        "Algorithm: " + algorithmName,
        (screenSize[0] / 2, 115),
        45,
    )

    #
    DrawText("No solution found!", (screenSize[0] / 2, screenSize[1] - 90), 50)
    DrawText(
        "Press 'M' to return to menu",
        (screenSize[0] / 2, screenSize[1] - 50),
    )

    # Create an instance of this Level and draw it
    DrawMatrix(level.getMatrix(), level.matrixSize, solvingOffset)
    
def DrawStats(stats):
    """Draw the algorithm statistics on the screen."""
    # Clear the stats area with a semi-transparent black
    stats_area_width = screenSize[0] * 0.98  # 98% of screen width
    stats_area_height = screenSize[1] * 0.15  # 15% of screen height
    stats_area_x = (screenSize[0] - stats_area_width) / 2  # Centered horizontally
    stats_area_y = screenSize[1] - stats_area_height - 20  # Position at bottom with 10px padding
    
    # Clear the stats area with a semi-transparent black
    stats_surface = pygame.Surface((stats_area_width, stats_area_height), pygame.SRCALPHA)
    stats_surface.fill((0, 0, 0, 180))  # Semi-transparent black
    screenSurface.blit(stats_surface, (stats_area_x, stats_area_y))
    
    # Extract the core stats (to display on the same line)
    time_value = stats.get('time', '0.00s')
    nodes_value = stats.get('nodes', '0')
    steps_value = stats.get('steps', '0')
    memory_value = stats.get('memory', '0.00MB')
    path_value = stats.get('path', '')
    status_value = stats.get('status', '')
    
    # First display the path at the top if it exists
    if path_value:
        # Position path at top of stats area
        path_y = stats_area_y + stats_area_height * 0.25
        
        # Calculate max characters based on screen width
        chars_per_line = max(40, int(stats_area_width / 10))
        path_display = path_value[:chars_per_line]
        
        # Add ellipsis if path is longer than what we can show
        if len(path_value) > chars_per_line:
            path_display = path_display[:-3] + "..."
        
        # Draw the path with larger font size
        path_font = pygame.font.Font(None, 30)
        path_text = f"Path: {path_display}"
        path_surface = path_font.render(path_text, True, (255, 255, 255))
        path_rect = path_surface.get_rect(center=(screenSize[0]/2, path_y))
        screenSurface.blit(path_surface, path_rect)
    
    # Display the core stats on a single line at the bottom
    bottom_stats_y = stats_area_y + stats_area_height * 0.6
    
    # Calculate horizontal positions for each stat
    stat_width = stats_area_width / 4
    time_x = stats_area_x + stat_width/2
    nodes_x = stats_area_x + stat_width + stat_width/2
    steps_x = stats_area_x + stat_width*2 + stat_width/2
    memory_x = stats_area_x + stat_width*3 + stat_width/2
    
    # Draw the core stats with custom colors
    font_size = 40
    
    # Time stat (green)
    time_font = pygame.font.Font(None, font_size)
    time_text = f"Time: {time_value}"
    time_surface = time_font.render(time_text, True, (100, 255, 100))
    time_rect = time_surface.get_rect(center=(time_x, bottom_stats_y))
    screenSurface.blit(time_surface, time_rect)
    
    # Nodes stat (blue)
    nodes_font = pygame.font.Font(None, font_size)
    nodes_text = f"Nodes: {nodes_value}"
    nodes_surface = nodes_font.render(nodes_text, True, (100, 100, 255))
    nodes_rect = nodes_surface.get_rect(center=(nodes_x, bottom_stats_y))
    screenSurface.blit(nodes_surface, nodes_rect)
    
    # Steps stat (red)
    steps_font = pygame.font.Font(None, font_size)
    steps_text = f"Steps: {steps_value}"
    steps_surface = steps_font.render(steps_text, True, (255, 100, 100))
    steps_rect = steps_surface.get_rect(center=(steps_x, bottom_stats_y))
    screenSurface.blit(steps_surface, steps_rect)
    
    # Memory stat (yellow)
    memory_font = pygame.font.Font(None, font_size)
    memory_text = f"Memory: {memory_value}"
    memory_surface = memory_font.render(memory_text, True, (255, 255, 100))
    memory_rect = memory_surface.get_rect(center=(memory_x, bottom_stats_y))
    screenSurface.blit(memory_surface, memory_rect)
    
    # Add status if present
    if status_value:
        status_y = stats_area_y + stats_area_height * 0.9
        status_font = pygame.font.Font(None, 36)
        status_text = f"Status: {status_value}"
        status_surface = status_font.render(status_text, True, (255, 255, 255))
        status_rect = status_surface.get_rect(center=(screenSize[0]/2, status_y))
        screenSurface.blit(status_surface, status_rect)
    
    # Update the display
    pygame.display.update()

__all__ = [
    "DrawText",
    "DrawMatrix",
    "DrawSelectionMenu",
    "DrawSuccessScreen",
    "DrawFailScreen",
    "DrawStats",
]
