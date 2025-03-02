import _TYPES as _TYPES

# Intergrated modules
import os as os
import sys as sys
import copy as copy

# External modules
import pygame as pygame
import psutil as psutil


def MovePlayer(
    level: _TYPES.Level,
    playerPosition: tuple,
    boxes: dict,
    move: tuple,
    mode: bool = False,
) -> tuple[tuple, dict, int]:
    """Move the player in the given direction.

    ### Parameters
    - level: The level to move the player in.
    - playerPosition: The current position of the player.
    - boxes: The current positions of the boxes and their weights.
    - move: The direction to move the player.
    - mode: The mode to run this function. True for algorithm mode, False for manual mode.

    ### Returns
    - tuple: The new position of the player, the new positions of the boxes, and the cost of the move (0 if move is unsuccessful).
    """
    matrix = level.matrix
    newPosition = (
        playerPosition[0] + move[0],
        playerPosition[1] + move[1],
    )
    # Check if the new position is a free space or a switch
    if newPosition not in boxes and matrix[newPosition[1]][newPosition[0]] != "#":
        return newPosition, boxes, 1
    # Check if the new position is a box
    elif newPosition in boxes:
        boxNewPosition = (newPosition[0] + move[0], newPosition[1] + move[1])
        # Check if the box can be moved
        if (
            matrix[boxNewPosition[1]][boxNewPosition[0]] == "#"
            or boxNewPosition in boxes
        ):
            return playerPosition, boxes, 0
        # Return if the box is in a deadlock
        if (
            mode
            and boxNewPosition not in level.switches
            and IsDeadlock(matrix, boxes, boxNewPosition, move)
        ):
            return playerPosition, boxes, 0

        # Update the box's position
        newBoxes: dict = {}
        for box in boxes:
            if box == tuple(newPosition):
                newBoxes.update({boxNewPosition: int(boxes[box])})
            else:
                newBoxes.update({box: int(boxes[box])})

        return newPosition, newBoxes, newBoxes[boxNewPosition]

    return playerPosition, boxes, 0


def IsDeadlock(matrix: list, boxes: list, boxPosition: tuple, move: tuple) -> bool:
    """Check if the given box position is in a deadlock.

    ### Parameters
    - matrix: The matrix representing the level.
    - boxes: The positions of the boxes and their weights.
    - boxPosition: The position of the box to check.
    - move: The move direction of the box.

    ### Returns
    - bool: True if the box is in a deadlock, False otherwise.
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
        (x + move[0], y + move[1]): (  # Forward
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
        (x + move[1], y + move[0]): (  # Relatively left
            matrix[y + move[1]][x + move[0]] == "#"
            and (
                matrix[y + move[1] + move[0]][x + move[0] + move[1]] == "#"
                or matrix[y - move[1] + move[0]][x - move[0] + move[1]] == "#"
            )
        ),
        (x - move[1], y - move[0]): (  # Relatively right
            matrix[y + move[1]][x + move[0]] == "#"
            and (
                matrix[y + move[1] - move[0]][x + move[0] - move[1]] == "#"
                or matrix[y - move[1] - move[0]][x - move[0] - move[1]] == "#"
            )
        ),
    }

    for position in aroundPositions:
        if position in boxes and aroundPositions[position]:
            return True

    return False


def CalculateHeuristicValue(playerPosition: tuple, boxes: dict, switches: list) -> int:
    """Calculate the heuristic cost based on the sum of Manhattan distances between boxes with their nearest switch.

    ### Parameters
    - playerPosition: The position of the player.
    - boxes: The positions of the boxes and their weights.
    - switches: The positions of the switches.

    ### Returns
    - int: The heuristic cost.
    """
    heuristicDistances: dict = {}
    boxWithMinDistance = None

    heuristicValue = 0

    # Loop through all boxes
    for box in boxes:
        # Calculate the Mahattan distance of the box to the nearest switch
        mahattanDistance = (
            min(
                abs(box[0] - switch[0]) + abs(box[1] - switch[1]) for switch in switches
            )
            * boxes[box]
        )

        # Update the heuristic distances and the heuristic value
        heuristicDistances.update({box: mahattanDistance})
        heuristicValue += mahattanDistance

        # Update the box with the minimum distance
        if (
            not boxWithMinDistance
            or heuristicDistances[boxWithMinDistance] > mahattanDistance
        ):
            boxWithMinDistance = box

    # Return the heuristic value with the Manhattan distance of the box with the minimum distance to the player
    return (
        heuristicValue
        + abs(boxWithMinDistance[0] - playerPosition[0])
        + abs(boxWithMinDistance[1] - playerPosition[1])
    )

def GetMemoryUsage():
    """Get current memory usage in MB

    ### Returns
    - int: Current memory usage (in MBs).
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Convert bytes to MB


__all__ = ["MovePlayer", "IsDeadlock", "CalculateHeuristicValue", "GetMemoryUsage"]
