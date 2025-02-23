import sys
import pygame
import GameUI as GUI
import Utilities as Utilities

# Initialize Pygame
UI = GUI.UI()

# Get the moves corresponding to the keys
moves = {
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
}

# Initialize the level variable
level = None

while True:
    # Set the start Level
    selectedAlgorithm, selectedLevel = UI.drawSelectionMenu()

    # Delete the previous level if it exists
    if level:
        del level
    # Initialize Level
    level = UI.initLevel(selectedLevel, selectedAlgorithm)
    print("\n", level.getPlayerPosition(), level.getBoxes(), level.getSwitches(), "\n")

    levelFinished = False

    while not levelFinished:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in moves:
                    Utilities.movePlayer(level, moves[event.key])
                    UI.drawLevel(level.getMatrix())
                elif event.key == pygame.K_r:
                    UI.initLevel(selectedLevel, selectedAlgorithm)
                elif event.key == pygame.K_s:
                    Utilities.solveLevel(level, selectedAlgorithm, UI)

                    levelFinished = True
                elif event.key == pygame.K_m:
                    break
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
