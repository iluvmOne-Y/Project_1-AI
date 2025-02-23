import time

from collections import deque
from copy import deepcopy

import Utilities as Utilities


class State:
    def __init__(self, matrix, playerPosition, boxes, totalStep, path):
        self.matrix = matrix
        self.playerPosition = playerPosition
        self.boxes = boxes
        self.totalStep = totalStep
        self.path = path


def BFS(level, ui=None):
    """Solve the level using the Breadth First Search algorithm.

    ### Parameters
    @level: The level to solve.
    """
    # Store the initial state of the level
    initialMatrix = level.getMatrix()
    initialPosition = level.getPlayerPosition()
    initialBoxes = level.getBoxes()
    # Start measuring time and initialise node counter
    totalNodes = 0
    start_time = time.time()

    # Get the initial state of the level
    totalStep = 0
    path = []

    directions = ["L", "R", "U", "D"]
    moves = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1),
    }

    # Check if the level is in a deadlock state
    boxes = level.getBoxes()
    for box in boxes:
        for direction in directions:
            if Utilities.isDeadlock(level.getMatrix(), box, moves[direction]):
                print("The level is in a deadlock state.")
                return None

    visited = set(str(level.getMatrix()))
    queue = deque(
        [State(level.getMatrix(), level.getPlayerPosition(), boxes, totalStep, path)]
    )
    # Iterate through the queue
    while queue:
        currentState = deepcopy(queue.popleft())
        # Increment the total number of nodes
        totalNodes += 1
        # Update GUI stats every 1000 nodes
        if ui and totalNodes % 1000 == 0:
            current_time = time.time() - start_time
            stats = {
                "path": "".join(currentState.path),
                "time": f"{current_time:.2f}s",
                "nodes": str(totalNodes),
                "steps": str(currentState.totalStep),
            }
            ui.drawStats(stats)
        # Check if all switches are activated
        if all(currentState.matrix[y][x] == "*" for x, y in level.switches):
            end_time = time.time()
            if ui:
                stats = {
                    "path": "".join(currentState.path),
                    "time": f"{end_time - start_time:.2f}s",
                    "nodes": str(totalNodes),
                    "steps": str(currentState.totalStep),
                    "status": "Solved",
                }
                ui.drawStats(stats)
            # Return level to its original state
            level.matrix = initialMatrix
            level.playerPosition = initialPosition
            level.boxes = initialBoxes

            return currentState.path
        # Iterate through the directions
        for direction in directions:
            move = moves[direction]
            # Update level state
            level.matrix = currentState.matrix
            level.playerPosition = currentState.playerPosition
            level.boxes = currentState.boxes
            # Check if the player can move in the given direction
            cost = Utilities.movePlayer(level, move, True)
            # Add the new state to the queue
            if cost != 0:
                # Check if the current matrix has been visited
                currentMatrix = str(level.matrix)
                if currentMatrix in visited:
                    continue
                # Add this matrix to the queue if new
                visited.add(currentMatrix)
                queue.append(
                    (
                        State(
                            level.matrix,
                            level.playerPosition,
                            level.boxes,
                            currentState.totalStep + 1,
                            currentState.path + [direction],
                        )
                    )
                )

    # Return level to its original state
    level.matrix = initialMatrix
    level.playerPosition = initialPosition
    level.boxes = initialBoxes

    return None


def DFS(level, ui=None):
    """Solve the level using the Depth First Search algorithm.

    ### Parameters
    @level: The level to solve.
    """
    # # Get the initial state of the level
    # initialMatrix = level.getMatrix()
    # initialPosition = level.getPlayerPosition()
    # boxes = level.getBoxes()

    # directions = ["L", "R", "U", "D"]
    # moves = {
    #     "D": (0, 1),
    #     "U": (0, -1),
    #     "R": (1, 0),
    #     "L": (-1, 0),
    # }
    # start_time = time.time()
    # expanded_nodes = 0

    # # Check if the level is in a deadlock state
    # for box in boxes:
    #     for direction in directions:
    #         if Utilities.isDeadlock(level.getMatrix(), box, moves[direction]):
    #             print("The level is in a deadlock state.")
    #             return None

    # visited = set()
    # stack = deque([(deepcopy(initialMatrix), initialPosition, [])])

    # # Iterate through the queue
    # while stack:
    #     currentMatrix, currentPosition, currentPath = stack.pop()
    #     # Check if all switches are activated
    #     expanded_nodes += 1
    #     # Update GUI stats every 1000 nodes
    #     if ui and expanded_nodes % 1000 == 0:
    #         current_time = time.time() - start_time
    #         stats = {
    #             "path": "".join(currentPath),
    #             "time": f"{current_time:.2f}s",
    #             "nodes": str(expanded_nodes),
    #         }
    #         ui.drawStats(stats)
    #     # Check if all switches are activated
    #     if all(currentMatrix[y][x] == "*" for x, y in level.getSwitches()):
    #         end_time = time.time()
    #         if ui:
    #             stats = {
    #                 "path": "".join(currentPath),
    #                 "time": f"{end_time - start_time:.2f}s",
    #                 "nodes": str(expanded_nodes),
    #                 "status": "Solved",
    #             }
    #             ui.drawStats(stats)

    #         return currentPath
    #     # Iterate through the directions
    #     for direction in directions:
    #         move = moves[direction]
    #         # Check if the player can move in the given direction
    #         newMatrix, newPosition, moveIsValid = tryMove(
    #             currentMatrix, currentPosition, move
    #         )
    #         # Add the new state to the queue
    #         if moveIsValid:
    #             # Check if the current state has been visited
    #             state = str(newMatrix)
    #             if state in visited:
    #                 continue
    #             # Add the new state to the queue
    #             visited.add(state)
    #             stack.append((newMatrix, newPosition, currentPath + [direction]))

    return None


def AStar(level):
    return None


def UCS(level):
    return None


algorithms = {
    "Breadth First Search": BFS,
    "Depth First Search": DFS,
    "A*": AStar,
    "Uniform Cost Search": UCS,
}
