import _TYPES as _TYPES

# Integrated modules
import time as time
from heapq import heappush

# Custom modules
from Utilities import GetMemoryUsage, IsDeadlock, MovePlayer, CalculateHeuristicValue


def GreedyBFS(level: _TYPES.Level, ui=None) -> _TYPES.Solution:
    """A function to solve a level using the Greedy Best-First Search algorithm.

    ### Parameters
    - level: The level to solve.

    ### Returns
    - _TYPES.Solution: The solution to the level.
    """
    # Initialize measurements
    totalNodes = 0
    startTime = time.time()
    startMemory = GetMemoryUsage()
    peakMemory = 0
    # Get the moves and directions
    directions = ["L", "R", "U", "D"]
    moves = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1),
    }

    # Get the initial state of the level
    matrix = level.matrix
    playerPosition = level.playerPosition
    boxes = level.boxes
    switches = level.switches

    # Return none if the level is in a deadlock state
    for box in boxes:
        for direction in directions:
            if IsDeadlock(matrix, boxes, box, moves[direction]):
                return None

    exploredStates = set()
    frontier = []  # A priority queue based only on heuristic value

    # Calculate initial heuristic
    initialHeuristic = CalculateHeuristicValue(playerPosition, boxes, switches)

    # Initialize the frontier with (heuristic, path, playerPosition, boxes)
    heappush(frontier, (initialHeuristic, [], playerPosition, boxes))

    while frontier:
        # Get the state with the lowest heuristic value
        currentHeuristic, currentPath, currentPlayerPosition, currentBoxes = frontier.pop(0)
        
        current_memory = GetMemoryUsage() - startMemory
        peakMemory = max(peakMemory, current_memory)
        # Increment the total number of nodes
        totalNodes += 1
        if ui and totalNodes % 1000 == 0:
            current_time = time.time() - startTime
            current_memory = GetMemoryUsage() - startMemory

            stats = {
                "path": "".join(currentPath),
                "time": f"{current_time:.2f}s",
                "nodes": str(totalNodes),
                "steps": str(len(currentPath)),
                "memory": f"{current_memory:.2f}MB"
            }
            ui.DrawStats(stats)

        # Return solution if all switches are activated
        if all(switchPosition in currentBoxes for switchPosition in switches):
            # Calculate total cost of the path
            totalCost = sum(1 if move.islower() else int(currentBoxes.get((0, 0), 1)) for move in currentPath)
            
            return _TYPES.Solution(
                len(currentPath),
                totalCost,
                totalNodes,
                time.time() - startTime,
                peakMemory ,
                currentPath,
            )

        # Skip if the state is already explored
        if (currentPlayerPosition, tuple(currentBoxes.keys())) in exploredStates:
            continue

        # Add the current state to the explored set
        exploredStates.add((currentPlayerPosition, tuple(currentBoxes.keys())))

        # Try all possible moves
        nextStates = []
        for direction in directions:
            move = moves[direction]
            newPlayerPosition, newBoxes, moveCost = MovePlayer(
                level, currentPlayerPosition, currentBoxes, move, True
            )

            # Skip if the move is invalid
            if moveCost == 0:
                continue

            # Skip if the new state is already explored
            if (newPlayerPosition, tuple(newBoxes.keys())) in exploredStates:
                continue

            # Get move type (lowercase for player move, uppercase for box push)
            moveType = direction.lower() if moveCost == 1 else direction
            
            # Calculate heuristic for the new state
            newHeuristic = CalculateHeuristicValue(newPlayerPosition, newBoxes, switches)
            
            # Add to list of next states
            nextStates.append((newHeuristic, currentPath + [moveType], newPlayerPosition, newBoxes))
        
        # Sort next states by heuristic and add to frontier
        nextStates.sort(key=lambda x: x[0])
        for state in nextStates:
            heappush(frontier, state)

    # Return None if no solution is found
    return None