import os as os

import pygame as pygame

import Level as Level
import GameUI as GameUI

def stop_function():
    stop_animation = False

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                stop_animation = True
    while stop_animation:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stop_animation = False


def solveLevel(level: Level.Level, algorithm, UI):
    """Solve the given level using the given algorithm.

    ### Parameters
    @level: The level to solve.
    @algorithm: The algorithm to solve the level with.
    @UI: The UI object to draw the level and the success screen.
    """
    #condition to pause animation
    # stop_animation = False
    
    # Solve the level
    solution = algorithm(level)
    # If a solution is found, move the player according to the solution
    if solution:
        for move in solution:
            
            stop_function()
            # PAUSE ANIMATION WHEN ENTER SPACEBAR
            # for event in pygame.event.get():
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_SPACE:
            #             stop_animation = True
            # while stop_animation:
            #     for event in pygame.event.get():
            #         if event.type == pygame.KEYDOWN:
            #             if event.key == pygame.K_SPACE:
            #                 stop_animation = False


            movePlayer(move, level)
            UI.drawLevel(level.getMatrix())
            pygame.time.wait(100)

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_m:  # Option to return to menu
                        waiting = False
        # Draw the success screen when the level is completed
        #UI.drawSuccessScreen()
    # If no solution is found, print an announcement
    #else:
        #UI.drawSolutionNotFoundScreen()


def movePlayer(direction: tuple, level: Level.Level):
    """Move the player in the given direction.

    ### Parameters
    @direction: The direction to move the player.
    @level: The level to move the player in.
    """
    matrix = level.getMatrix()
    level.addToHistory(matrix)

    playerX, playerY = level.getPlayerPosition()

    moves = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1),
    }

    moveX = moves[direction][0]
    moveY = moves[direction][1]

    # Debug log for move direction
    print(
        "######### Moving",
        (
            "Left"
            if direction == "L"
            else "Right" if direction == "R" else "Up" if direction == "U" else "Down"
        ),
        "#########",
    )

    # if free space or a switch is in the move direction
    if (
        matrix[playerY + moveY][playerX + moveX] == " "
        or matrix[playerY + moveY][playerX + moveX] == "."
    ):
        # set the move position to + if Ares will step on a switch else @
        matrix[playerY + moveY][playerX + moveX] = (
            "+" if matrix[playerY + moveY][playerX + moveX] == "." else "@"
        )

        # set the player previous position to "." Ares was stepping on a switch else " "
        matrix[playerY][playerX] = "." if matrix[playerY][playerX] == "+" else " "

        # update player's and boxes' position
        level.playerPosition = [playerX + moveX, playerY + moveY]
        for box in level.boxes:
            if box == [playerX + moveX, playerY + moveY]:
                box[0] += moveX
                box[1] += moveY
                break

    # if box is in the move direction, box might be on a switch
    elif (
        matrix[playerY + moveY][playerX + moveX] == "$"
        or matrix[playerY + moveY][playerX + moveX] == "*"
    ):
        # # set the position that the box will be pushed to "*" if it is on a switch else "$"
        # matrix[playerY + 2 * moveY][playerX + 2 * moveX] = (
        #     "*" if matrix[playerY + 2 * moveY][playerX + 2 * moveX] == "." else "$"
        # )

        # # set the move position to + if Ares will step on a switch else @
        # matrix[playerY + moveY][playerX + moveX] = (
        #     "+" if matrix[playerY + moveY][playerX + moveX] == "*" else "@"
        # )

        # # set the player previous position to "." Ares was stepping on a switch else " "
        # matrix[playerY][playerX] = "." if matrix[playerY][playerX] == "+" else " "

        # # update player's position
        # level.playerPosition = [playerX + moveX, playerY + moveY]
        if(matrix[playerY + 2 * moveY][playerX + 2 * moveX] == "*"
           or matrix[playerY + 2 * moveY][playerX + 2 * moveX] == "#"
           or matrix[playerY + 2 * moveY][playerX + 2 * moveX] == "$"):
            pass
        else:
            if(matrix[playerY + 2 * moveY][playerX + 2 * moveX] == "."):
                matrix[playerY + 2 * moveY][playerX + 2 * moveX] = "*"
            else:
                matrix[playerY + 2 * moveY][playerX + 2 * moveX] = "$"
            
            matrix[playerY + moveY][playerX + moveX] = ("+" if matrix[playerY + moveY][playerX + moveX] == "*"
                                                        else "@")
            matrix[playerY][playerX] = (" " if matrix[playerY][playerX] == "@"
                                        else ".")
            level.playerPosition = [playerX + moveX, playerY + moveY]


    return matrix


def isDeadlock(matrix: list, boxPosition: list, move: list) -> bool:
    """Check if the given box position is in a deadlock.

    ### Parameters
    @matrix: The matrix representing the level.
    @boxPosition: The position of the box to check.

    ### Returns
    @bool: True if the box is in a deadlock, False otherwise.
    """
    x, y = boxPosition

    # Check for corner deadlock
    if matrix[y + move[1]][x + move[0]] == "#" and (
        matrix[y + move[0]][x + move[1]] == "#"
        or matrix[y - move[0]][x - move[1]] == "#"
    ):
        return True

    # Check for double box deadlock
    aroundPositions = {
        matrix[y + move[1]][x + move[0]]: (
            matrix[y + move[0]][x + move[1]] in ["#", "$", "*"]
            and (
                matrix[y - move[0]][x - move[1]] == "#"
                or matrix[y + move[1] + move[0]][x + move[0] + move[1]] == "#"
                or matrix[y + move[1] - move[0]][x + move[0] - move[1]] == "#"
            )
        )
        or (
            matrix[y - move[0]][x - move[1]]
            and (
                matrix[y + move[1] + move[0]][x + move[0] + move[1]] == "#"
                or matrix[y + move[1] - move[0]][x + move[0] - move[1]] == "#"
            )
        ),
        matrix[y + move[0]][x + move[1]]: matrix[y + move[1]][x + move[0]] == "#"
        and (
            matrix[y + move[1] + move[0]][x + move[0] + move[1]] == "#"
            or matrix[y - move[1] + move[0]][x - move[0] + move[1]] == "#"
        ),
        matrix[y - move[0]][x - move[1]]: matrix[y + move[1]][x + move[0]] == "#"
        and (
            matrix[y + move[1] - move[0]][x + move[0] - move[1]] == "#"
            or matrix[y - move[1] - move[0]][x - move[0] - move[1]] == "#"
        ),
    }

    for key in aroundPositions:
        if key in ["$", "*"] and aroundPositions[key]:
            return True

    return False
