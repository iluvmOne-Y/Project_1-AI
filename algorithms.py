import time

from collections import deque
from copy import deepcopy

import Utilities as Utilities


class State:
    def __init__(self, matrix, playerPosition, boxes, path):
        self.matrix = matrix
        self.playerPosition = playerPosition
        self.boxes = boxes
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
    # # Get the initial state of the level
    initialMatrix = level.getMatrix()
    initialPosition = level.getPlayerPosition()
    boxes = level.getBoxes()

    directions = ["L", "R", "U", "D"]
    moves = {
        "D": (0, 1),
        "U": (0, -1),
        "R": (1, 0),
        "L": (-1, 0),
    }
    start_time = time.time()
    expanded_nodes = 0

    # Check if the level is in a deadlock state
    for box in boxes:
        for direction in directions:
            if Utilities.isDeadlock(level.getMatrix(), box, moves[direction]):
                print("The level is in a deadlock state.")
                return None

    visited = set()
    stack = deque([(deepcopy(initialMatrix), initialPosition, [])])

    # Iterate through the queue
    while stack:
        currentMatrix, currentPosition, currentPath = stack.pop()
        # Check if all switches are activated
        expanded_nodes += 1
        #Update GUI stats every 1000 nodes 
        if ui and expanded_nodes % 1000 ==0:
            current_time = time.time() - start_time
            stats = {
                'path': ''.join(currentPath),
                'time': f"{current_time:.2f}s",
                'nodes': str(expanded_nodes)
            }
            ui.drawStats(stats)
        # Check if all switches are activated
        if all(currentMatrix[y][x] == "*" for x, y in level.getSwitches()):
            end_time = time.time()
            if ui:
                stats = {
                    'path': ''.join(currentPath),
                    'time': f"{end_time - start_time:.2f}s",
                    'nodes': str(expanded_nodes),
                    'status': 'Solved'
                }
                ui.drawStats(stats)
       
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
                stack.append((newMatrix, newPosition, currentPath + [direction]))

    return None


def AStar(level, ui = None):
    return None

def UCS(level, ui = None):
    """Solve the level using the Uniform Cost Search algorithm."""

    #Start measuring time
    start_time = time.time()

    #Initialise node counter
    expanded_nodes = 0

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

    for box in boxes:
        for direction in directions:
            if isDeadlock(level.getMatrix(), box, moves[direction]):
                print("The level is in a deadlock state.")
                return None

    visited = set()
    priority_queue = []
    initialCost = calculateCost(initialPosition, boxes)
    heapq.heappush(priority_queue, (initialCost, 0, deepcopy(initialMatrix), initialPosition, []))

    def tryMove(matrix, currentPosition, move):
        newMatrix = [row[:] for row in matrix]
        newPosition = [
            currentPosition[0] + move[0],
            currentPosition[1] + move[1],
        ]

        if newMatrix[newPosition[1]][newPosition[0]] in [" ", "."]:
            newMatrix[currentPosition[1]][currentPosition[0]] = (
                " " if newMatrix[currentPosition[1]][currentPosition[0]] == "@" else "."
            )
            newMatrix[newPosition[1]][newPosition[0]] = (
                "@" if newMatrix[newPosition[1]][newPosition[0]] == " " else "+"
            )
            return newMatrix, newPosition, 1, True
        elif newMatrix[newPosition[1]][newPosition[0]] in ["$", "*"]:
            boxNewPosition = [newPosition[0] + move[0], newPosition[1] + move[1]]
            if newMatrix[boxNewPosition[1]][boxNewPosition[0]] in ["#", "$", "*"]:
                return matrix, currentPosition, 0, False
            newMatrix[currentPosition[1]][currentPosition[0]] = (
                " " if newMatrix[currentPosition[1]][currentPosition[0]] == "@" else "."
            )
            newMatrix[newPosition[1]][newPosition[0]] = (
                "@" if newMatrix[newPosition[1]][newPosition[0]] == "$" else "+"
            )
            newMatrix[boxNewPosition[1]][boxNewPosition[0]] = (
                "$" if newMatrix[boxNewPosition[1]][boxNewPosition[0]] == " " else "*"
            )
            if newMatrix[boxNewPosition[1]][boxNewPosition[0]] == "$" and isDeadlock(
                newMatrix, boxNewPosition, move
            ):
                return matrix, currentPosition, 0, False
            return newMatrix, newPosition, 2, True

        return newMatrix, newPosition, 0, False

    while priority_queue:
        heuristic, cost, currentMatrix, currentPosition, currentPath = heapq.heappop(priority_queue)
        
        expanded_nodes += 1

        if ui and expanded_nodes % 1000 == 0:
            current_time = time.time() - start_time
            stats = {
                'path': ''.join(currentPath),
                'time': f"{current_time:.2f}s",
                'nodes': str(expanded_nodes)
            }
            ui.drawStats(stats)
        # Check if all switches are activated
        if all(currentMatrix[y][x] == "*" for x, y in level.getSwitches()):
            end_time = time.time()
            if ui:
                stats = {
                    'path': ''.join(currentPath),
                    'time': f"{end_time - start_time:.2f}s",
                    'nodes': str(expanded_nodes),
                    'status': 'Solved'
                }
                ui.drawStats(stats)
            return currentPath

        # Check if all switches are activated
        for direction in directions:
            move = moves[direction]
            newMatrix, newPosition, moveCost, moveIsValid = tryMove(
                currentMatrix, currentPosition, move
            )
            
            if moveIsValid:
                state = str(newMatrix)
                if state in visited:
                    continue
                visited.add(state)
                newCost = cost + moveCost
                heuristicCost = calculateCost(newPosition, level.getBoxes())
                heapq.heappush(priority_queue, (heuristicCost + newCost, newCost, newMatrix, newPosition, currentPath + [direction]))
    
    return None


algorithms = {
    "Breadth First Search": BFS,
    "Depth First Search": DFS,
    "A*": AStar,
    "Uniform Cost Search": UCS,
}
