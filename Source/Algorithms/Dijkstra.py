import _TYPES as _TYPES

# Intergrated modules
import time as time
from itertools import count
from heapq import heappush

# Custom modules
from Controller.InterfaceController import DrawStats
from Utilities import GetMemoryUsage, IsDeadlock, MovePlayer


def Dijkstra(level: _TYPES.Level) -> _TYPES.Solution:
    """A function to solve a level using the Dijkstra algorithm.

    ### Parameters
    - level: The level to solve.

    ### Returns
    - _TYPES.Solution: The solution to the level.
    """
    # Initialize mesurments
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

    # Get the inital state of the level
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
    )  # A priority queue of states to explore orderd by their traversal cost

    counter = count()  # Unique sequence to break ties consistently
    # Format: (cost, counter, path, playerPostion, boxes)
    heappush(frontier, (0, next(counter), "", playerPosition, boxes))

    while frontier:
        # Get the state with the lowest cost
        currentPathCost, _, currentPath, currentPlayerPosition, currentBoxes = (
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

        # Return solution and relevant datas if all switches are activated
        if all(switchPostion in currentBoxes for switchPostion in switches):
            return _TYPES.Solution(
                len(currentPath),
                currentPathCost - len(currentPath),
                totalNodes,
                time.time() - startTime,
                max(peakMemory, GetMemoryUsage() - startMemory),
                currentPath,
            )

        # Skip if current state is already explored
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

            # Return if the player can't move in the given direction
            if moveCost == 0:
                continue

            # Get the correct move type (lowercase for ordinary move, uppercase for box pushing action)
            moveType = direction if moveCost == 1 else direction.upper()

            # Add to frontier
            heappush(
                frontier,
                (
                    currentPathCost + moveCost,
                    next(counter),
                    currentPath + moveType,
                    newPlayerPosition,
                    newBoxes,
                ),
            )

    return None
