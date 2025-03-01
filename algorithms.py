import time
import heapq
from heapq import heappush, heappop
from collections import deque
from copy import deepcopy
from itertools import count
import Utilities as Utilities
import psutil
import os
import random
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



"""Solving by using Dijkstra's Algorithm"""
def Dijkstra(level, ui=None):
    """
    ### Parameters
    @level: The level to solve.
    """
    # Start measuring time
    start_time = time.time()
    expanded_nodes = 0
    start_memory = get_memory_usage()

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
            if Utilities.isDeadlock(level.getMatrix(), box, moves[direction]):
                print("The level is in a deadlock state.")
                return None

    # Set to keep track of visited states
    visited = set()
    
    # Priority queue for Dijkstra's algorithm
    # Format: (cost, counter, matrix, position, path)
    counter = count()  # Unique sequence to break ties consistently
    priority_queue = []
    heapq.heappush(priority_queue, (0, next(counter), deepcopy(initialMatrix), initialPosition, []))

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
        # Get the state with the lowest cost
        cost, _, currentMatrix, currentPosition, currentPath = heapq.heappop(priority_queue)
        
        expanded_nodes += 1

        # Update GUI stats every 1000 nodes
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
            
        # Check if all switches are activated (goal state)
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
            
        # Skip if we've already visited this state
        state_str = str(currentMatrix)
        if state_str in visited:
            continue
        visited.add(state_str)
        
        # Try each possible move
        for direction in directions:
            move = moves[direction]
            
            # Try the move and get results
            newMatrix, newPosition, moveCost, moveIsValid = tryMove(
                currentMatrix, currentPosition, move
            )
            
            if moveIsValid:
                # Calculate new cost (Dijkstra uses actual cost from start)
                newCost = cost + moveCost
                
                # Add to priority queue
                heapq.heappush(priority_queue, 
                              (newCost, next(counter), newMatrix, newPosition, currentPath + [direction]))
    
    return None


   



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
                    new_box_pos,  # instead of using this, use box_pos = dictionary{(x, y): weight}
                    path + [direction],
                ))

    print("Can't found the way")
    return None

def ACO(level, ui=None):
    """Ant Colony Optimization algorithm for solving Sokoban puzzles.
    
    ### Parameters
    @level: The level to solve.
    @ui: The UI object to display statistics.
    
    ### Returns
    @list: The path to solve the level, or None if no solution is found.
    """
    # Parameters for ACO
    n_ants = 200                # Number of ants per iteration
    n_iterations = 300          # Number of iterations
    evaporation_rate = 0.5     # Rate of pheromone evaporation
    alpha = 1.0                # Pheromone importance
    beta = 2.0                 # Heuristic importance
    
    # Start measuring time and memory
    start_time = time.time()
    start_memory = get_memory_usage()
    generated_nodes = 0
    
    # Get the initial state
    initialMatrix = level.getMatrix()
    initialPosition = level.getPlayerPosition()
    switchPosition = level.getSwitches()
    boxes = level.getBoxes()
    
    # Directions and moves
    directions = ["L", "R", "U", "D"]
    moves = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1),
    }
    
    # Check for initial deadlock
    for box in boxes:
        for direction in directions:
            if Utilities.isDeadlock(level.getMatrix(), box, moves[direction]):
                print("The level is in a deadlock state.")
                return None
    
    # Pheromone initialization - use a dictionary to store state-action pheromones
    pheromones = {}  # {state_str: {direction: pheromone_value}}
    
    # Function to try a move and get the new state
    def try_move(matrix, position, box_positions, direction):
        move = moves[direction]
        newMatrix = [row[:] for row in matrix]
        new_position = [position[0] + move[0], position[1] + move[1]]
        new_box_positions = deepcopy(box_positions)
        
        # Check if new position is empty space or target
        if newMatrix[new_position[1]][new_position[0]] in [" ", "."]:
            # Move player
            newMatrix[position[1]][position[0]] = " " if newMatrix[position[1]][position[0]] == "@" else "."
            newMatrix[new_position[1]][new_position[0]] = "@" if newMatrix[new_position[1]][new_position[0]] == " " else "+"
            return newMatrix, new_position, new_box_positions, 1, True
        
        # Check if new position has a box
        elif newMatrix[new_position[1]][new_position[0]] in ["$", "*"]:
            box_new_pos = [new_position[0] + move[0], new_position[1] + move[1]]
            
            # Check if box can be pushed
            if newMatrix[box_new_pos[1]][box_new_pos[0]] in ["#", "$", "*"]:
                return matrix, position, box_positions, 0, False
            
            # Move player and box
            newMatrix[position[1]][position[0]] = " " if newMatrix[position[1]][position[0]] == "@" else "."
            newMatrix[new_position[1]][new_position[0]] = "@" if newMatrix[new_position[1]][new_position[0]] == "$" else "+"
            newMatrix[box_new_pos[1]][box_new_pos[0]] = "$" if newMatrix[box_new_pos[1]][box_new_pos[0]] == " " else "*"
            
            # Check for deadlock
            if newMatrix[box_new_pos[1]][box_new_pos[0]] == "$" and Utilities.isDeadlock(newMatrix, box_new_pos, move):
                return matrix, position, box_positions, 0, False
            
            # Update box positions
            box_cost = new_box_positions.pop((new_position[0], new_position[1]))
            new_box_positions[(box_new_pos[0], box_new_pos[1])] = box_cost
            
            return newMatrix, new_position, new_box_positions, box_cost, True
        
        return matrix, position, box_positions, 0, False
    
    # Function to calculate heuristic value
    def calculate_heuristic(matrix, box_positions, player_pos):
        return Utilities.Manhattan_Sum(matrix, switchPosition, box_positions, player_pos)
    
    # Main ACO algorithm
    best_solution = None
    best_solution_length = float('inf')
    
    for iteration in range(n_iterations):
        ant_solutions = []
        
        # Generate solutions with n_ants
        for ant in range(n_ants):
            current_matrix = deepcopy(initialMatrix)
            current_position = initialPosition.copy()
            current_boxes = deepcopy(boxes)
            path = []
            visited = {str(current_matrix)}
            
            # Build solution
            max_steps = 3000  # Prevent infinite loops
            step = 0
            
            while step < max_steps:
                step += 1
                generated_nodes += 1
                
                # Check if solution found
                if all(current_matrix[y][x] == "*" for x, y in switchPosition):
                    ant_solutions.append((path, calculate_heuristic(current_matrix, current_boxes, current_position)))
                    if len(path) < best_solution_length:
                        best_solution = path
                        best_solution_length = len(path)
                    break
                
                # Calculate probability for each direction
                state_str = str(current_matrix)
                valid_moves = {}
                total_weight = 0
                
                for direction in directions:
                    new_matrix, new_position, new_boxes, move_cost, is_valid = try_move(
                        current_matrix, current_position, current_boxes, direction)
                    
                    if is_valid and str(new_matrix) not in visited:
                        # Get pheromone level (default to 1.0 if not present)
                        pheromone = pheromones.get(state_str, {}).get(direction, 1.0)
                        
                        # Get heuristic value (lower is better, so invert)
                        heuristic = 1.0 / (calculate_heuristic(new_matrix, new_boxes, new_position) + 1.0)
                        
                        # Calculate weight
                        weight = (pheromone ** alpha) * (heuristic ** beta)
                        valid_moves[direction] = weight
                        total_weight += weight
                
                # No valid moves
                if not valid_moves:
                    break
                
                # Choose direction based on probabilities
                choice = random.random() * total_weight
                current_weight = 0
                chosen_direction = None
                
                for direction, weight in valid_moves.items():
                    current_weight += weight
                    if current_weight >= choice:
                        chosen_direction = direction
                        break
                
                if not chosen_direction:  # Just in case, pick the first
                    chosen_direction = list(valid_moves.keys())[0]
                
                # Apply chosen move
                new_matrix, new_position, new_boxes, _, _ = try_move(
                    current_matrix, current_position, current_boxes, chosen_direction)
                
                current_matrix = new_matrix
                current_position = new_position
                current_boxes = new_boxes
                path.append(chosen_direction)
                visited.add(str(current_matrix))
            
            # Update UI every few nodes
            if ui and generated_nodes % 1000 == 0:
                current_time = time.time() - start_time
                current_memory = get_memory_usage() - start_memory
                stats = {
                    "path": "".join(path if path else []),
                    "time": f"{current_time:.2f}s",
                    "nodes": str(generated_nodes),
                    "steps": str(len(path)),
                    "memory": f"{current_memory:.2f}MB",
                    "iteration": f"{iteration+1}/{n_iterations}"
                }
                ui.drawStats(stats)
        
        # Update pheromones
        # First, evaporate all pheromones
        for state in pheromones:
            for direction in pheromones[state]:
                pheromones[state][direction] *= (1 - evaporation_rate)
        
        # Then deposit new pheromones from solutions
        for solution, quality in ant_solutions:
            # Adjust deposit amount based on solution quality (lower quality = higher deposit)
            deposit = 1.0 / (quality + 1.0)
            
            # Reconstruct the solution to update pheromones
            current_matrix = deepcopy(initialMatrix)
            current_position = initialPosition.copy()
            current_boxes = deepcopy(boxes)
            
            for i, direction in enumerate(solution):
                state_str = str(current_matrix)
                if state_str not in pheromones:
                    pheromones[state_str] = {}
                if direction not in pheromones[state_str]:
                    pheromones[state_str][direction] = 0.0
                    
                # Deposit pheromone
                pheromones[state_str][direction] += deposit
                
                # Apply move
                current_matrix, current_position, current_boxes, _, _ = try_move(
                    current_matrix, current_position, current_boxes, direction)
    
    # Return the best solution found
    if best_solution:
        end_time = time.time() - start_time
        memory_usage = get_memory_usage() - start_memory
        if ui:
            stats = {
                "path": "".join(best_solution),
                "time": f"{end_time:.2f}s",
                "nodes": str(generated_nodes),
                "steps": str(len(best_solution)),
                'memory': f"{memory_usage:.2f}MB",
                "status": "Solved"
            }
            ui.drawStats(stats)
        return best_solution
    
    return None

algorithms = {
    "Breadth-First Search": BFS,
    "Depth-First Search": DFS,
    "Uniform Cost Search": UCS,
    "A*": AStar,
    "Dijkstra": Dijkstra,
    "ACO": ACO
}


