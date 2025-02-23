import time

from collections import deque
from copy import deepcopy
from heapq import heappush, heappop

import Utilities as Utilities


class State:
    def __init__(self, matrix, playerPosition, boxes, path):
        self.matrix = matrix
        self.playerPosition = playerPosition
        self.boxes = boxes
        self.path = path
    
    def __lt__(self, other):
        # Compare by path length (or any other relevant metric)
        return len(self.path) < len(other.path)


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

    # Initalize the initial path of the level
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
    queue = deque([State(level.getMatrix(), level.getPlayerPosition(), boxes, path)])
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
                "steps": str(len(currentState.path)),
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
                    "steps": str(len(currentState.path)),
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
            if Utilities.movePlayer(level, move, True) != 0:
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
    # Store the initial state of the level
    initialMatrix = level.getMatrix()
    initialPosition = level.getPlayerPosition()
    initialBoxes = level.getBoxes()
    # Start measuring time and initialise node counter
    totalNodes = 0
    start_time = time.time()

    # Initalize the initial path of the level
    path = []

    directions = ["D", "U", "R", "L"]
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
    stack = deque([State(level.getMatrix(), level.getPlayerPosition(), boxes, path)])
    # Iterate through the stack
    while stack:
        currentState = deepcopy(stack.pop())
        # Increment the total number of nodes
        totalNodes += 1
        # Update GUI stats every 1000 nodes
        if ui and totalNodes % 1000 == 0:
            current_time = time.time() - start_time
            stats = {
                "path": "".join(currentState.path),
                "time": f"{current_time:.2f}s",
                "nodes": str(totalNodes),
                "steps": str(len(currentState.path)),
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
                    "steps": str(len(currentState.path)),
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
            if Utilities.movePlayer(level, move, True) != 0:
                # Check if the current matrix has been visited
                currentMatrix = str(level.matrix)
                if currentMatrix in visited:
                    continue
                # Add this matrix to the stack if new
                visited.add(currentMatrix)
                stack.append(
                    (
                        State(
                            level.matrix,
                            level.playerPosition,
                            level.boxes,
                            currentState.path + [direction],
                        )
                    )
                )

    # Return level to its original state
    level.matrix = initialMatrix
    level.playerPosition = initialPosition
    level.boxes = initialBoxes

    return None


def AStar(level, ui = None):
    # Get the initial state of the level
    initialMatrix = level.getMatrix()
    initialPosition = level.getPlayerPosition()
    initialBoxes = level.getBoxes()

    totalNodes = 0
    start_time = time.time()
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
    
    intialCost = currDepth = 0
    currCost = Utilities.Manhattan_sum(level)
    priority_queue = []
    visited = set()

    heappush(priority_queue, (intialCost, currCost, 
                              State(level.getMatrix(), level.getPlayerPosition(), boxes, path), currDepth))

    while priority_queue:
        """pop the smallest cost node"""
        _, curr_cost, currentState, curr_depth= deepcopy(heappop(priority_queue))
        # Increment the total number of nodes
        totalNodes += 1
        # Update GUI stats every 1000 nodes
        if ui and totalNodes % 1000 == 0:
            current_time = time.time() - start_time
            stats = {
                "path": "".join(currentState.path),
                "time": f"{current_time:.2f}s",
                "nodes": str(totalNodes),
                "steps": str(len(currentState.path)),
            }
            ui.drawStats(stats)

        # check if all switches are activated
        if all(currentState.matrix[y][x] == "*" for x, y in level.getSwitches()):
            end_time = time.time()
            if ui:
                stats = {
                    "path": "".join(currentState.path),
                    "time": f"{end_time - start_time:.2f}s",
                    "nodes": str(totalNodes),
                    "steps": str(len(currentState.path)),
                    "status": "Solved",
                }
                ui.drawStats(stats)
            # Return level to its original state
            level.matrix = initialMatrix
            level.playerPosition = initialPosition
            level.boxes = initialBoxes
            return currentState.path
        
        for direction in directions:
            move = moves[direction]
            # Update level state
            level.matrix = currentState.matrix
            level.playerPosition = currentState.playerPosition
            level.boxes = currentState.boxes
            # Check if payer can move in the given direction

            moveCost = Utilities.movePlayer(level, move, True)
            if moveCost != 0:
                # Check if the current matrix has been visited
                currentMatrix = str(level.matrix)
                if currentMatrix in visited:
                    continue
                visited.add(currentMatrix)
                newCost = Utilities.Manhattan_sum(level)
                heappush(priority_queue, (
                            moveCost + curr_cost,
                            newCost,
                            State(
                                level.matrix,
                                level.playerPosition,
                                level.boxes,
                                currentState.path + [direction]
                            ),
                            curr_depth + 1,
                ))
    # Return level to its original state
    level.matrix = initialMatrix
    level.playerPosition = initialPosition
    level.boxes = initialBoxes

    print("Can't found the wae")
    return None


def UCS(level):
    return None


algorithms = {
    "Breadth First Search": BFS,
    "Depth First Search": DFS,
    "A*": AStar,
    "Uniform Cost Search": UCS,
}
