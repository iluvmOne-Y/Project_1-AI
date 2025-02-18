from collections import deque
from copy import deepcopy
from Utilities import isDeadlock


def BFS(level):
    """Solve the level using the Breadth First Search algorithm.

    ### Parameters
    @level: The level to solve.
    """
    # Get the initial state of the level
    initialMatrix = level.getMatrix()
    initialPosition = level.getPlayerPosition()
    boxes = level.getBoxes()

    directions = ["L", "R", "U", "D"]
    moves = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1),
    }

    # Check if the level is in a deadlock state
    for box in boxes:
        for direction in directions:
            if isDeadlock(level.getMatrix(), box, moves[direction]):
                print("The level is in a deadlock state.")
                return None

    visited = set()
    queue = deque([(deepcopy(initialMatrix), initialPosition, [])])

    # Check if the player can move in the given direction and return the new state
    def tryMove(matrix, currentPosition, move):
        newMatrix = [row[:] for row in matrix]
        newPosition = [
            currentPosition[0] + move[0],
            currentPosition[1] + move[1],
        ]

        # Check if the new position is a free space or a switch
        if newMatrix[newPosition[1]][newPosition[0]] in [" ", "."]:
            # Move the player
            newMatrix[currentPosition[1]][currentPosition[0]] = (
                " " if newMatrix[currentPosition[1]][currentPosition[0]] == "@" else "."
            )
            newMatrix[newPosition[1]][newPosition[0]] = (
                "@" if newMatrix[newPosition[1]][newPosition[0]] == " " else "+"
            )
            return newMatrix, newPosition, True
        # Check if the new position is a box
        elif newMatrix[newPosition[1]][newPosition[0]] in ["$", "*"]:
            boxNewPosition = [newPosition[0] + move[0], newPosition[1] + move[1]]
            # Check if the box can be moved
            if newMatrix[boxNewPosition[1]][boxNewPosition[0]] in [
                "#",
                "$",
                "*",
            ]:
                return matrix, currentPosition, False
            # Move the player and the box
            newMatrix[currentPosition[1]][currentPosition[0]] = (
                " " if newMatrix[currentPosition[1]][currentPosition[0]] == "@" else "."
            )
            newMatrix[newPosition[1]][newPosition[0]] = (
                "@" if newMatrix[newPosition[1]][newPosition[0]] == "$" else "+"
            )
            newMatrix[boxNewPosition[1]][boxNewPosition[0]] = (
                "$" if newMatrix[boxNewPosition[1]][boxNewPosition[0]] == " " else "*"
            )
            # Check if the new state is in a deadlock
            if newMatrix[boxNewPosition[1]][boxNewPosition[0]] == "$" and isDeadlock(
                newMatrix, boxNewPosition, move
            ):
                return matrix, currentPosition, False
            return newMatrix, newPosition, True

        return newMatrix, newPosition, False

    # Iterate through the queue
    while queue:
        currentMatrix, currentPosition, currentPath = queue.popleft()
        # Check if all switches are activated
        if all(currentMatrix[y][x] == "*" for x, y in level.getSwitches()):
            return currentPath
        # Iterate through the directions
        for direction in directions:
            move = moves[direction]
            # Check if the player can move in the given direction
            newMatrix, newPosition, moveIsValid = tryMove(
                currentMatrix, currentPosition, move
            )
            # Add the new state to the queue
            if moveIsValid:
                # Check if the current state has been visited
                state = str(newMatrix)
                if state in visited:
                    continue
                # Add the new state to the queue
                visited.add(state)
                queue.append((newMatrix, newPosition, currentPath + [direction]))

    return None


algorithms = {"Breadth First Search": BFS}
