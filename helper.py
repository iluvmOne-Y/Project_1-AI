import numpy as np
import pygame as pygame
import sys as sys

from heapq import heappop, heappush

from Environment import Environment
from Draw import drawMenu

myEnvironment = Environment()


def reset_to_menu():
    global current_level, selected_algorithm
    myEnvironment.screen.fill((0, 0, 0))
    pygame.display.flip()
    selected_algorithm = drawMenu.algorithm_menu()
    current_level = drawMenu.level_menu()
    drawMenu.initLevel(current_level)


def show_success_screen():
    myEnvironment.screen.fill((0, 0, 0))
    drawMenu("Level Completed", (myEnvironment.size[0] / 2, myEnvironment.size[1] / 2))
    drawMenu(
        "Press any key to continue",
        (myEnvironment.size[0] / 2, myEnvironment.size[1] / 2 + 50),
    )
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
