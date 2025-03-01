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
def UCS(level, ui=None):
    """
    ### Parameters
    @level: The level to solve.
    """
    initialMatrix = level.getMatrix()
    initialPosition = level.getPlayerPosition()
    initialBoxes = level.getBoxes()

    totalNodes = 0
    start_time = time.time()
    start_memory = get_memory_usage()
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

    intialCost = 0
    priority_queue = []
    visited = set()
    counter = count()
    heapq.heappush(priority_queue, (intialCost, next(counter),
                              State(level.getMatrix(), level.getPlayerPosition(), boxes, path)))

    while priority_queue:
        """pop the smallest cost node"""
        curr_cost, _, currentState= deepcopy(heappop(priority_queue))
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

        # check if all switches are activated
        if all(currentState.matrix[y][x] == "*" for x, y in level.getSwitches()):
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
                heappush(priority_queue, (
                    moveCost + curr_cost, #priority
                    next(counter), #tie-break
                    State(
                        level.matrix,
                        level.playerPosition,
                        level.boxes,
                        currentState.path + [direction]
                    )
                ))
    # Return level to its original state
    level.matrix = initialMatrix
    level.playerPosition = initialPosition
    level.boxes = initialBoxes
    return None


"""Solving by using A* Algorithm"""
def AStar(level, ui=None):
    # Get the initial state of the level
    initialMatrix = level.getMatrix()
    initialPosition = level.getPlayerPosition()
    initialBoxes = level.getBoxes()

    totalNodes = 0
    start_time = time.time()
    start_memory = get_memory_usage()
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
    counter = count()
    heapq.heappush(priority_queue, (intialCost, currCost,next(counter),
                              State(level.getMatrix(), level.getPlayerPosition(), boxes, path), currDepth))

    while priority_queue:
        """pop the smallest cost node"""
        _, curr_cost,_, currentState, curr_depth = deepcopy(heappop(priority_queue))
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

        # check if all switches are activated
        if all(currentState.matrix[y][x] == "*" for x, y in level.getSwitches()):
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
                    moveCost + curr_cost, #priority
                    newCost, #heuristic cost
                    next(counter), #tie-break
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

    print("Can't find the wae")
    return None



def Dijkstra(level, ui=None):
    # Get the initial state of the level
    initialMatrix = level.getMatrix()
    initialPosition = level.getPlayerPosition()
    initialBoxes = level.getBoxes()

    totalNodes = 0
    start_time = time.time()
    start_memory = get_memory_usage()
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

    intialCost = 0
    dijkstra_cost = Utilities.dijkstra_sum(level)
    priority_queue = []
    visited = set()
    counter = count()
    heapq.heappush(priority_queue, (intialCost, dijkstra_cost, next(counter),
                              State(level.getMatrix(), level.getPlayerPosition(), boxes, path)))

    while priority_queue:
        """pop the smallest cost node"""
        _, curr_cost, _, currentState = deepcopy(heappop(priority_queue))
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

        # check if all switches are activated
        if all(currentState.matrix[y][x] == "*" for x, y in level.getSwitches()):
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
                newCost = Utilities.dijkstra_sum(level)
                heappush(priority_queue, (
                    moveCost + curr_cost,
                    newCost,
                    next(counter),
                    State(
                        level.matrix,
                        level.playerPosition,
                        level.boxes,
                        currentState.path + [direction]
                    )
                ))
    # Return level to its original state
    level.matrix = initialMatrix
    level.playerPosition = initialPosition
    level.boxes = initialBoxes

    print("Can't find the wae")
    return None


# ...existing algorithms dictionary...
algorithms = {
    "Breadth-First Search": BFS,
    "Depth-First Search": DFS,
    "Uniform Cost Search": UCS,
    "A*": AStar
}

