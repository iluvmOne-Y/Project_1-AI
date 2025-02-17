import pygame
import sys

from Environment import Environment
from Level import Level
from algorithms import bfs_solve

from helper import reset_to_menu, show_success_screen
from Draw import algorithm_menu, level_menu, drawLevel, drawText
from player import movePlayer


def initLevel(level):
    myEnvironment.screen.fill((0, 0, 0))

    pygame.display.flip()
    drawText("Level " + str(level), (myEnvironment.size[1], 200))
    drawText("Algorithm: " + selected_algorithm.__name__, (myEnvironment.size[1], 250))
    drawText("Press S to solve", (myEnvironment.size[1], 300))
    drawText("Press M to return to menu", (myEnvironment.size[1], 350))
    # Create an instance of this Level
    global myLevel
    myLevel = Level(level)

    # Draw this level
    drawLevel(myLevel.getMatrix())

    global target_found
    target_found = False


# Create the environment
def solve_level():
    global myLevel, selected_algorithm
    solution = selected_algorithm(myLevel)
    if solution:
        for move in solution:
            movePlayer(move, myLevel)
            drawLevel(myLevel.getMatrix())
            pygame.display.flip()
            pygame.time.wait(100)
        show_success_screen()
    else:
        print("No solution found")


myEnvironment = Environment()


# Set the start Level
selected_algorithm = algorithm_menu()
current_level = level_menu()

# Initialize Level
initLevel(current_level)

target_found = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                movePlayer("L", myLevel)
            elif event.key == pygame.K_RIGHT:
                movePlayer("R", myLevel)
            elif event.key == pygame.K_DOWN:
                movePlayer("D", myLevel)
            elif event.key == pygame.K_UP:
                movePlayer("U", myLevel)
            elif event.key == pygame.K_u:
                drawLevel(myLevel.getLastMatrix())
            elif event.key == pygame.K_r:
                initLevel(current_level)
            elif event.key == pygame.K_m:
                reset_to_menu()
            elif event.key == pygame.K_s:
                solve_level()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
p
