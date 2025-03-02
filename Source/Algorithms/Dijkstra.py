import _TYPES as _TYPES

# Intergrated modules
import time as time
from itertools import count
from heapq import heappush

# Custom modules
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

    # Get the moves and directions
    directions = ["L", "R", "U", "D"]
    moves = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1),
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
    )  # A priority queue of the current state and the path to the current state

    counter = count()  # Unique sequence to break ties consistently
    # Format: (cost, counter, path, playerPostion, boxes)
    heappush(frontier, (0, next(counter), [], playerPosition, boxes))

    while frontier:
        # Get the state with the lowest cost
        currentCost, _, currentPath, currentPlayerPosition, currentBoxes = frontier.pop(
            0
        )

        # Increment the total number of nodes
        totalNodes += 1

        # Return solution and relevant datas if all switches are activated
        if all(switchPostion in currentBoxes for switchPostion in switches):
            return _TYPES.Solution(
                len(currentPath),
                currentCost,
                totalNodes,
                time.time() - startTime,
                GetMemoryUsage() - startMemory,
                currentPath,
            )

        # Skip if current state is already explored
        if (currentPlayerPosition, tuple(currentBoxes.keys())) in exploredStates:
            continue

        # Add the current state to the explored set
        exploredStates.add((currentPlayerPosition, tuple(currentBoxes.keys())))

        # Try each possible move
        for direction in directions:
            # Move the player in the given direction
            move = moves[direction]
            newPlayerPosition, newBoxes, moveCost = MovePlayer(
                level, currentPlayerPosition, currentBoxes, move, True
            )

            # Check if the player can move in the given direction
            if moveCost != 0:
                # Get the correct move type
                moveType = direction.lower() if moveCost == 1 else direction

                # Add to priority queue
                heappush(
                    frontier,
                    (
                        currentCost + moveCost,
                        next(counter),
                        currentPath + [moveType],
                        newPlayerPosition,
                        newBoxes,
                    ),
                )

    return None
