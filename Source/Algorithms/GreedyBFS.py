import _TYPES as _TYPES

# Integrated modules
import time as time
from heapq import heappush

# Custom modules
from Controller.InterfaceController import DrawStats
from Utilities import GetMemoryUsage, IsDeadlock, MovePlayer, CalculateHeuristicValue


def GreedyBFS(level: _TYPES.Level) -> _TYPES.Solution:
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
    directions = ["l", "r", "u", "d"]
    moves = {
        "l": (-1, 0),
        "r": (1, 0),
        "u": (0, -1),
        "d": (0, 1),
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
    frontier = (
        []
    )  # A priority queue of states to explore ordered by their heuristic cost

    # Initialize the frontier
    # Format: (heuristicCost, pathCost, path, playerPosition, boxes)
    heappush(frontier, (0, 0, "", playerPosition, boxes))

    while frontier:
        # Get the state with the lowest heuristic value
        _, currentPathCost, currentPath, currentPlayerPosition, currentBoxes = (
            frontier.pop(0)
        )

        # Increment the total number of nodes
        totalNodes += 1

        # Show stats every 5000 nodes
        if totalNodes % 5000 == 0:
            # Calculate the peak memory usage
            peakMemory = max(peakMemory, GetMemoryUsage() - startMemory)

            stats = _TYPES.StateStats(
                currentPath,
                totalNodes,
                time.time() - startTime,
                peakMemory,
            )
            DrawStats(stats)

        # Return solution if all switches are activated
        if all(switchPosition in currentBoxes for switchPosition in switches):
            return _TYPES.Solution(
                len(currentPath),
                currentPathCost - len(currentPath),
                totalNodes,
                time.time() - startTime,
                max(peakMemory, GetMemoryUsage() - startMemory),
                currentPath,
            )

        # Skip if the state is already explored
        if (currentPlayerPosition, tuple(currentBoxes.keys())) in exploredStates:
            continue

        # Add the current state to the explored set
        exploredStates.add((currentPlayerPosition, tuple(currentBoxes.keys())))

        # Iterate through the directions
        for direction in directions:
            # Move the player in the given direction
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

            # Get the correct move type (lowercase for ordinary move, uppercase for box pushing action)
            moveType = direction if moveCost == 1 else direction.upper()

            # Add to frontier
            heappush(
                frontier,
                (
                    CalculateHeuristicValue(newPlayerPosition, newBoxes, switches),
                    currentPathCost + moveCost,
                    currentPath + moveType,
                    newPlayerPosition,
                    newBoxes,
                ),
            )

    # Return None if no solution is found
    return None
