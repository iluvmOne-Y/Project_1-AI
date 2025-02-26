import time
import heapq
from heapq import heappush, heappop
from collections import deque
from copy import deepcopy
from itertools import count
import Utilities as Utilities
import psutil
import os
class State:
    def __init__(self, matrix, playerPosition, boxes, path):
        self.matrix = matrix
        self.playerPosition = playerPosition
        self.boxes = boxes
        self.path = path
    
"""Solving by using Breadth-First Search Algorithm"""
def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Convert bytes to MB

def BFS(level, ui=None):
    """### Parameters
    @level: The level to solve.
    """
    
    # Store the initial state of the level
    initialMatrix = level.getMatrix()
    initialPosition = level.getPlayerPosition()
    initialBoxes = level.getBoxes()
    
    # Start measuring time and initialise node counter
    totalNodes = 0
    start_time = time.time()
    start_memory = get_memory_usage()
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
            current_memory = get_memory_usage() - start_memory
            stats = {
                "path": "".join(currentState.path),
                "time": f"{current_time:.2f}s",
                "nodes": str(totalNodes),
                "steps": str(len(currentState.path)),
                'memory': f"{current_memory:.2f}MB"
            }
            ui.drawStats(stats)

        # Check if all switches are activated
        if all(currentState.matrix[y][x] == "*" for x, y in level.switches):
            end_time = time.time()
            memory_used = get_memory_usage() - start_memory
            if ui:
                stats = {
                    "path": "".join(currentState.path),
                    "time": f"{end_time - start_time:.2f}s",
                    "nodes": str(totalNodes),
                    "steps": str(len(currentState.path)),
                    'memory': f"{memory_used:.2f}MB",
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

"""Solving by using Depth-First Search Algorithm"""
def DFS(level, ui=None):
    """
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
    start_memory = get_memory_usage()
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
            current_memory = get_memory_usage() - start_memory
            stats = {
                'path': ''.join(currentPath),
                'time': f"{current_time:.2f}s",
                'nodes': str(expanded_nodes),
                "steps": str(len(currentPath)),
                'memory': f"{current_memory:.2f}MB"
            }
            ui.drawStats(stats)
        # Check if all switches are activated
        if all(currentMatrix[y][x] == "*" for x, y in level.getSwitches()):
            end_time = time.time()
            memory_used = get_memory_usage() - start_memory
            if ui:
                stats = {
                    'path': ''.join(currentPath),
                    'time': f"{end_time - start_time:.2f}s",
                    'nodes': str(expanded_nodes),
                    "steps": str(len(currentPath)),
                    'memory': f"{memory_used:.2f}MB",
                    'status': 'Solved'
                }
                ui.drawStats(stats)
            
            return currentPath
        # Iterate through the directions
        for direction in directions:
            move = moves[direction]
            # Check if the player can move in the given direction
            newMatrix, newPosition, moveIsValid = Utilities.tryMove(
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

"""Solving by using Uniform Cost Search Algorithm"""
def UCS(level, ui = None):
    """Solve the level using the Uniform Cost Search algorithm."""

    #Start measuring time
    start_time = time.time()

    #Initialise node counter
    expanded_nodes = 0
    start_memory = get_memory_usage()

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
            if Utilities.isDeadlock(level.getMatrix(), box, moves[direction]):
                print("The level is in a deadlock state.")
                return None

    visited = set()
    priority_queue = []
    initialCost = Utilities.calculateCost(initialPosition, boxes)
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
            if newMatrix[boxNewPosition[1]][boxNewPosition[0]] == "$" and Utilities.isDeadlock(
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
            current_memory = get_memory_usage() - start_memory
            stats = {
                'path': ''.join(currentPath),
                'time': f"{current_time:.2f}s",
                'nodes': str(expanded_nodes),
                "steps": str(len(currentPath)),
                'memory': f"{current_memory:.2f}MB"
            }
            ui.drawStats(stats)
        # Check if all switches are activated
        if all(currentMatrix[y][x] == "*" for x, y in level.getSwitches()):
            end_time = time.time()
            memory_used = get_memory_usage() - start_memory 
            if ui:
                stats = {
                    'path': ''.join(currentPath),
                    'time': f"{end_time - start_time:.2f}s",
                    'nodes': str(expanded_nodes),
                    "steps": str(len(currentPath)),
                    'memory': f"{memory_used:.2f}MB",
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
                heuristicCost = Utilities.calculateCost(newPosition, level.getBoxes())
                heapq.heappush(priority_queue, (heuristicCost + newCost, newCost, newMatrix, newPosition, currentPath + [direction]))
    
    return None


"""Solving by using A* Algorithm"""

"""Solving by using A* Algorithm"""


def AStar(level, ui=None):
    start_time = time.time()
    generated_nodes = 0
    start_memory = get_memory_usage()
    # Get the initial state of the level
    initialMatrix = level.getMatrix()
    initialPosition = level.getPlayerPosition()
    switchPosition = level.getSwitches()
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
            if Utilities.isDeadlock(level.getMatrix(), box, moves[direction]):
                print("The level is in a deadlock state.")
                return None

    intialCost = 0
    currCost = Utilities.Manhattan_Sum(initialMatrix, switchPosition, boxes, initialPosition)
    priority_queue = []
    visited = set()

    heapq.heappush(priority_queue, (intialCost, currCost, initialMatrix, initialPosition, boxes, []))

    def tryMove(matrix, currentPosition, boxPosition, move):
        newMatrix = [row[:] for row in matrix]
        newPosition = [
            currentPosition[0] + move[0],
            currentPosition[1] + move[1],
        ]
        new_boxPosition = deepcopy(boxPosition)
        the_cost = 1
        # Check if the new position is a free space or a switch
        if newMatrix[newPosition[1]][newPosition[0]] in [" ", "."]:
            # Move the player
            newMatrix[currentPosition[1]][currentPosition[0]] = (
                " " if newMatrix[currentPosition[1]][currentPosition[0]] == "@" else "."
            )
            newMatrix[newPosition[1]][newPosition[0]] = (
                "@" if newMatrix[newPosition[1]][newPosition[0]] == " " else "+"
            )
            return newMatrix, newPosition, the_cost, new_boxPosition, True
        # Check if the new position is a box
        elif newMatrix[newPosition[1]][newPosition[0]] in ["$", "*"]:
            boxNewPosition = [newPosition[0] + move[0], newPosition[1] + move[1]]
            # Check if the box can be moved
            if newMatrix[boxNewPosition[1]][boxNewPosition[0]] in [
                "#",
                "$",
                "*",
            ]:
                return matrix, currentPosition, the_cost, new_boxPosition, False
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
            if newMatrix[boxNewPosition[1]][boxNewPosition[0]] == "$" and Utilities.isDeadlock(
                    newMatrix, boxNewPosition, move
            ):
                return matrix, currentPosition, the_cost, new_boxPosition, False
            new_boxPosition[(boxNewPosition[0], boxNewPosition[1])] = new_boxPosition.pop(
                (newPosition[0], newPosition[1]))
            return newMatrix, newPosition, new_boxPosition[
                (boxNewPosition[0], boxNewPosition[1])], new_boxPosition, True

        return newMatrix, newPosition, the_cost, new_boxPosition, False

    while priority_queue:
        """pop the smallest cost node"""
        generated_nodes += 1
        _, curr_cost, currentMatrix, currentPosition, box_pos, path = heapq.heappop(priority_queue)
        if ui and generated_nodes % 1000 == 0:
            current_time = time.time() - start_time
            current_memory = get_memory_usage() - start_memory
            stats = {
                "path":"".join(path),
                'time': f"{current_time:.2f}s",
                'nodes': str(generated_nodes),
                "steps":str(len(path)),
                "memory": f"{current_memory:.2f}M",

            }
            ui.drawStats(stats)

        # check if all switches are activated
        if all(currentMatrix[y][x] == "*" for x, y in level.getSwitches()):
            end_time = time.time() - start_time
            memory_usage = get_memory_usage() -start_memory
            if ui:
                stats = {
                    "path": "".join(path),
                    "time": f"{end_time:.2f}s",
                    "nodes": str(generated_nodes),
                    "steps": str(len(path)),
                    'memory': f"{memory_usage:.2f}MB"
                }
                ui.drawStats(stats)
            return path

        for direction in directions:
            move = moves[direction]

            newMatrix, newPosition, moveCost, new_box_pos, moveIsValid = tryMove(
                currentMatrix, currentPosition, box_pos, move)

            if moveIsValid:
                state = str(newMatrix)
                if state in visited:
                    continue
                visited.add(state)

                new_cost = Utilities.Manhattan_Sum(newMatrix, switchPosition, new_box_pos, newPosition)
                heapq.heappush(priority_queue, (
                    moveCost + curr_cost,
                    new_cost,
                    newMatrix,
                    newPosition,
                    new_box_pos,  # instead of using this, let's use box_pos = dictionary{(x, y): weight}
                    path + [direction],
                ))

    print("Can't found the wae")
    return None



# ...existing algorithms dictionary...
algorithms = {
    "Breadth-First Search": BFS,
    "Depth-First Search": DFS,
    "Uniform Cost Search": UCS,
    "A*": AStar
}

