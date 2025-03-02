import _TYPES as _TYPES

# Intergrated modules
import os as os
import sys as sys
import copy as copy
import pathlib as pathlib

# External modules
import pygame as pygame

# Get the fonts
HeaderFont = "Data/Assets/Fonts/Header-font3.otf"
TextFont1 = "Data/Assets/Fonts/Text-font2.ttf"
TextFont2 = "Data/Assets/Fonts/Text-font1.ttf"


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

# Get the number of input files
inputNumber = 0

currentDirectory = pathlib.Path("Inputs")
for item in currentDirectory.iterdir():
    if item.is_file() and item.name[:5] == "input" and item.suffix == ".txt":
        inputNumber += 1

# Initialize the levels
levels: list = [_TYPES.Level(i) for i in range(1, inputNumber + 1)]

# Set the screen size
screenSize = (
    max(max(level.matrixSize[0] for level in levels) * imageSize + 250, screenSize[0]),
    max(max(level.matrixSize[1] for level in levels) * imageSize + 400, screenSize[1]),
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
previewOffset = screenSize[1] / 3
solvingOffset = screenSize[1] / 3 - 45


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


def DrawSelectionScreen(level: _TYPES.Level, algorithmName: str):
    """Draw the selection screen.

    ### Parameters
    - level: The selected level.
    - algorithmName: The name of the algorithm.
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
    levelText = "Level " + str(level.number)
    font = pygame.font.Font(None, 40)
    textSurface = font.render(levelText, True, (255, 255, 255))
    textRect = textSurface.get_rect(center=(screenSize[0] / 2, 200))
    borderRect = textRect.inflate(20, 20)
    pygame.draw.rect(screenSurface, (255, 255, 255), borderRect, 4)
    centeredTextRect = textSurface.get_rect(center=borderRect.center)
    screenSurface.blit(textSurface, centeredTextRect)

    # Draw the border box for the current algorithm
    algorithmText = algorithmName
    font = pygame.font.Font(None, 44)
    textSurface = font.render(algorithmText, True, (255, 255, 255))
    textRect = textSurface.get_rect(center=(screenSize[0] / 2, screenSize[1] - 70))
    borderRect = textRect.inflate(20, 20)
    pygame.draw.rect(screenSurface, (255, 255, 255), borderRect, 4)
    centeredTextRect = textSurface.get_rect(center=borderRect.center)
    screenSurface.blit(textSurface, centeredTextRect)

    # Draw the level
    DrawMatrix(
        level.getMatrix(),
        level.matrixSize,
        previewOffset,
    )

    pygame.display.flip()


def DrawSelectionMenu(
    algorithms: list[_TYPES.Algorithm],
) -> tuple[_TYPES.Level, _TYPES.Algorithm]:
    """Draw the combined algorithm and level selection menu.

    ### Parameters
    - algorithms: The list of algorithms to select from.

    ### Returns
    - tuple: The selected level and algorithm.
    """
    # Initialize the selected level and algorithm
    levelSelected: int = 0
    algorithmSelected: int = 0

    # Draw the selection screen
    DrawSelectionScreen(levels[levelSelected], algorithms[algorithmSelected].__name__)

    while True:
        # Track movement events
        for event in pygame.event.get():
            # Update level or algorithm selected based on key pressed
            if event.type == pygame.KEYDOWN:
                # Update level selected with left and right key
                if event.key == pygame.K_LEFT:
                    levelSelected = (levelSelected - 1) % len(levels)
                    DrawSelectionScreen(
                        levels[levelSelected], algorithms[algorithmSelected].__name__
                    )

                elif event.key == pygame.K_RIGHT:
                    levelSelected = (levelSelected + 1) % len(levels)
                    DrawSelectionScreen(
                        levels[levelSelected], algorithms[algorithmSelected].__name__
                    )

                # Update algorithm selected with up and down key
                elif event.key == pygame.K_UP:
                    algorithmSelected = (algorithmSelected - 1) % len(algorithms)
                    DrawSelectionScreen(
                        levels[levelSelected], algorithms[algorithmSelected].__name__
                    )
                elif event.key == pygame.K_DOWN:
                    algorithmSelected = (algorithmSelected + 1) % len(algorithms)
                    DrawSelectionScreen(
                        levels[levelSelected], algorithms[algorithmSelected].__name__
                    )

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


def DrawSuccessScreen(
    level: _TYPES.Level, algorithmName: str, solution: _TYPES.Solution
):
    """Draw the success screen when a level is completed.

    ### Parameters
    - level: The level that is completed.
    - algorithmName: The name of the algorithm used to solve the level.
    - solution: The solution to the level.
    """
    # Clear the screen
    screenSurface.fill((0, 0, 0))

    # Redraw the background
    DrawText("Level " + str(level.number), (screenSize[0] / 2, 50), 50)
    DrawText(
        "Algorithm: " + algorithmName,
        (screenSize[0] / 2, 95),
        45,
    )

    #
    DrawText("Press 'Space' to (un)pause", (screenSize[0] / 2, 130), 30)
    DrawText(
        "Press 'Left'/'Right' to change matrix to previous/next state",
        (screenSize[0] / 2, 150),
        30,
    )
    DrawText("Press 'R' to restart", (screenSize[0] / 2, 170), 30)
    DrawText("Press 'M' to return to menu", (screenSize[0] / 2, 190), 30)

    # Redraw the matrix
    DrawMatrix(level.getMatrix(), level.matrixSize, solvingOffset)

    # Draw the solution statistics
    stats = _TYPES.StateStats(
        solution.path,
        solution.nodesExpanded,
        solution.timeTaken,
        solution.memoryUsage,
    )
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
    DrawText("Level " + str(level.number), (screenSize[0] / 2, 50), 50)
    DrawText(
        "Algorithm: " + algorithmName,
        (screenSize[0] / 2, 95),
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


def DrawStats(stats: _TYPES.StateStats):
    """Draw the state statistics on the screen.

    ### Parameters
    - stats: The statistics to be displayed
    """
    # Clear the stats area with a semi-transparent black
    statsAreaWidth = screenSize[0] * 0.98  # 98% of screen width
    statsAreaHeight = screenSize[1] * 0.15  # 15% of screen height
    statsAreaOffsetX = (screenSize[0] - statsAreaWidth) / 2  # Centered horizontally
    statsAreaOffsetY = (
        screenSize[1] - statsAreaHeight - 20
    )  # Position at bottom with 10px padding

    # Clear the stats area with a semi-transparent black
    statsSurface = pygame.Surface((statsAreaWidth, statsAreaHeight), pygame.SRCALPHA)
    statsSurface.fill((0, 0, 0, 255))  # Pitch black
    screenSurface.blit(statsSurface, (statsAreaOffsetX, statsAreaOffsetY))

    # First display the path at the top if it exists
    if stats.path:
        # Position path at top of stats area
        pathOffsetY = statsAreaOffsetY + statsAreaHeight * 0.25

        # Add ellipsis if path is longer than what we can show
        maxCharPerLine = min(40, int(statsAreaWidth / 10))
        pathDisplay = stats.path

        if len(stats.path) > maxCharPerLine:
            pathDisplay = pathDisplay[: maxCharPerLine - 3] + "..."

        # Draw the path with larger font size
        font = pygame.font.Font(None, 30)
        statText = f"Path: {pathDisplay}"
        statSurface = font.render(statText, True, (255, 255, 255))
        statRect = statSurface.get_rect(center=(screenSize[0] / 2, pathOffsetY))
        screenSurface.blit(statSurface, statRect)

    # Display the core stats on a single line at the bottom
    bottomStatsY = statsAreaOffsetY + statsAreaHeight * 0.6

    # Calculate horizontal positions for each stat
    statWidth = statsAreaWidth / 4
    timeX = statsAreaOffsetX + statWidth / 2
    nodesX = statsAreaOffsetX + statWidth + statWidth / 2
    stepsX = statsAreaOffsetX + statWidth * 2 + statWidth / 2
    memoryX = statsAreaOffsetX + statWidth * 3 + statWidth / 2

    # Draw the core stats with custom colors
    fontSize = 40
    font = pygame.font.Font(None, fontSize)

    # Time stat (green)
    statText = f"Time: {stats.timeTaken:.2f}s"
    statSurface = font.render(statText, True, (100, 255, 100))
    statRect = statSurface.get_rect(center=(timeX, bottomStatsY))
    screenSurface.blit(statSurface, statRect)

    # Nodes stat (blue)
    statText = f"Nodes: {stats.nodesExpanded}"
    statSurface = font.render(statText, True, (100, 100, 255))
    statRect = statSurface.get_rect(center=(nodesX, bottomStatsY))
    screenSurface.blit(statSurface, statRect)

    # Steps stat (red)
    statText = f"Steps: {len(stats.path)}"
    statSurface = font.render(statText, True, (255, 100, 100))
    statRect = statSurface.get_rect(center=(stepsX, bottomStatsY))
    screenSurface.blit(statSurface, statRect)

    # Memory stat (yellow)
    statText = f"Memory: {stats.memoryUsage:.2f}MB"
    statSurface = font.render(statText, True, (255, 255, 100))
    statRect = statSurface.get_rect(center=(memoryX, bottomStatsY))
    screenSurface.blit(statSurface, statRect)

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
