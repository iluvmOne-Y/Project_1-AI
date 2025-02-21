from collections import deque
from copy import deepcopy
from Utilities import isDeadlock 
import time

def BFS(level,ui=None):
    """Solve the level using the Breadth First Search algorithm.

    ### Parameters
    @level: The level to solve.
    """
    #Start measuring time
    start_time = time.time()

    #Initialise node counter
    expanded_nodes = 0

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
                queue.append((newMatrix, newPosition, currentPath + [direction]))

    return None

def DFS(level,ui=None):
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
            if isDeadlock(level.getMatrix(), box, moves[direction]):
                print("The level is in a deadlock state.")
                return None

    visited = set()
    stack = deque([(deepcopy(initialMatrix), initialPosition, [])])

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

def AStar(level):
    return None

def UCS(level):
    return None 


algorithms = {"Breadth First Search": BFS, "Depth First Search": DFS, "A*": AStar,"Uniform Cost Search": UCS}
