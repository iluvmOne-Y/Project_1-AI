import os as os
import sys as sys
import copy
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
    # condition to pause animation
    # stop_animation = False

    # Solve the level
    solution = algorithm(level, UI)
    # If a solution is found, move the player according to the solution
    if solution:
        moves = {
            "L": (-1, 0),
            "R": (1, 0),
            "U": (0, -1),
            "D": (0, 1),
        }
        for direction in solution:

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

            movePlayer(level, moves[direction], True)
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
        # UI.drawSuccessScreen()
    # If no solution is found, print an announcement
    # else:
    # UI.drawSolutionNotFoundScreen()


def movePlayer(level: Level, move: tuple, mode: bool = False) -> int:
    """Move the player in the given direction.

    ### Parameters
    @level: The level to move the player in.
    @move: The direction to move the player.
    @mode: The mode to run this function.

    ### Returns
    @int: The cost of the move.
    """
    matrix = level.getMatrix()
    # Create a new matrix to store the new state
    newMatrix = [row[:] for row in matrix]

    currentPosition = level.getPlayerPosition()
    newPosition = [
        currentPosition[0] + move[0],
        currentPosition[1] + move[1],
    ]
    # Check if the new position is a free space or a switch
    if matrix[newPosition[1]][newPosition[0]] in [" ", "."]:
        # Move the player
        newMatrix[currentPosition[1]][currentPosition[0]] = (
            " " if matrix[currentPosition[1]][currentPosition[0]] == "@" else "."
        )
        newMatrix[newPosition[1]][newPosition[0]] = (
            "@" if matrix[newPosition[1]][newPosition[0]] == " " else "+"
        )
        # Update the player's position
        level.matrix = newMatrix
        level.playerPosition = newPosition

        return 1
    # Check if the new position is a box
    elif matrix[newPosition[1]][newPosition[0]] in ["$", "*"]:
        boxNewPosition = [newPosition[0] + move[0], newPosition[1] + move[1]]
        # Check if the box can be moved
        if matrix[boxNewPosition[1]][boxNewPosition[0]] in [
            "#",
            "$",
            "*",
        ]:
            return 0
        # Move the player and the box
        newMatrix[currentPosition[1]][currentPosition[0]] = (
            " " if matrix[currentPosition[1]][currentPosition[0]] == "@" else "."
        )
        newMatrix[newPosition[1]][newPosition[0]] = (
            "@" if matrix[newPosition[1]][newPosition[0]] == "$" else "+"
        )
        newMatrix[boxNewPosition[1]][boxNewPosition[0]] = (
            "$" if matrix[boxNewPosition[1]][boxNewPosition[0]] == " " else "*"
        )
        # Check if the new state is in a deadlock
        if (
            mode
            and newMatrix[boxNewPosition[1]][boxNewPosition[0]] != "*"
            and isDeadlock(newMatrix, boxNewPosition, move)
        ):
            return 0
        # Update the matrix and the player's position
        level.matrix = newMatrix
        level.playerPosition = newPosition
        # Update the cost
        boxes = copy.deepcopy(level.boxes)
        cost = boxes[tuple(newPosition)]
        # Update the box's position
        del boxes[tuple(newPosition)]
        boxes[tuple(boxNewPosition)] = cost
        level.boxes = boxes

        return cost

    return 0


def isDeadlock(matrix: list, boxPosition: list, move: tuple) -> bool:
    """Check if the given box position is in a deadlock.

    ### Parameters
    @matrix: The matrix representing the level.
    @boxPosition: The position of the box to check.
    @move: The move direction of the box.

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
            (
                matrix[y + move[0]][x + move[1]] == "#"
                and (
                    matrix[y + move[1] + move[0]][x + move[0] + move[1]] == "#"
                    or matrix[y + move[1] - move[0]][x + move[0] - move[1]] == "#"
                )
            )
            or (
                matrix[y - move[0]][x - move[1]] == "#"
                and (
                    matrix[y + move[1] + move[0]][x + move[0] + move[1]] == "#"
                    or matrix[y + move[1] - move[0]][x + move[0] - move[1]] == "#"
                )
            )
        ),
        matrix[y + move[0]][x + move[1]]: (
            matrix[y + move[1]][x + move[0]] == "#"
            and (
                matrix[y + move[1] + move[0]][x + move[0] + move[1]] == "#"
                or matrix[y - move[1] + move[0]][x - move[0] + move[1]] == "#"
            )
        ),
        matrix[y - move[0]][x - move[1]]: (
            matrix[y + move[1]][x + move[0]] == "#"
            and (
                matrix[y + move[1] - move[0]][x + move[0] - move[1]] == "#"
                or matrix[y - move[1] - move[0]][x - move[0] - move[1]] == "#"
            )
        ),
    }

    for key in aroundPositions:
        if key in ["$", "*"] and aroundPositions[key]:
            return True

    return False
