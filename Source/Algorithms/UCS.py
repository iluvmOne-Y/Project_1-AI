import _TYPES as _TYPES

# Intergrated modules
import time as time
from heapq import heappush

# Custom modules
from Controller.InterfaceController import DrawStats
from Utilities import GetMemoryUsage, IsDeadlock, MovePlayer


def UCS(level: _TYPES.Level) -> _TYPES.Solution:
    """A function to solve a level using the Uniformed Cost Search algorithm.

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
    )  # A priority queue of the states to explore ordered by their traversal cost

    # Initialize the frontier
    # Format: (pathCost, path, playerPostion, boxes)
    heappush(
        frontier,
        (0, "", playerPosition, boxes),
    )

    while frontier:
        # Get the current state
        currentPathCost, currentPath, currentPlayerPosition, currentBoxes = (
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

        # Add the current state to the explored set
        exploredStates.add((currentPlayerPosition, tuple(currentBoxes.keys())))

        # Check if all switches are activated
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

            # Check if the new state has already been explored
            explored = False
            if (newPlayerPosition, tuple(newBoxes.keys())) in exploredStates:
                explored = True

            # Loop through the frontier and find any states that match the new state
            for i, state in enumerate(frontier):
                # Skip if the state is not the same as the new state
                if state[2] != newPlayerPosition or state[3] != newBoxes:
                    continue

                # Update the frontier if the new state has a lower path cost
                if not explored and currentPathCost + moveCost < state[0]:
                    # Remove the old state from the frontier
                    frontier.pop(i)

            # Skip if the new state has already been explored
            if explored:
                continue

            # Add the new state to the frontier
            heappush(
                frontier,
                (
                    currentPathCost + moveCost,
                    currentPath + moveType,
                    newPlayerPosition,
                    newBoxes,
                ),
            )

    # Return None if no solution is found
    return None
