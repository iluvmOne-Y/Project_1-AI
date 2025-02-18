import sys
import pygame

import GameUI as GUI
import Utilities as Utilities

# Initialize Pygame
UI = GUI.UI()

# Get the moves corresponding to the keys
moves = {
    pygame.K_LEFT: "L",
    pygame.K_RIGHT: "R",
    pygame.K_UP: "U",
    pygame.K_DOWN: "D",
}

while True:
    # Set the start Level
    selectedLevel = UI.drawLevelSelectionMenu()
    selectedAlgorithm = UI.drawAlgorithmSelectionMenu()

    # Initialize Level
    level = UI.initLevel(selectedLevel, selectedAlgorithm)

    levelFinished = False

    while not levelFinished:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in moves:
                    Utilities.movePlayer(moves[event.key], level)
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
