import _TYPES as _TYPES

# Intergrated modules
import time as time
from heapq import heappush, heappop

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
    startMemory = GetMemoryUsage()
    startTime = time.time()
    totalNodes = 0
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

    # Initialize the frontier
    exploredStates = set()
    frontierDict = {
        (playerPosition, tuple(boxes.keys())): [0]
    }  # A dict for constant-time traversal cost lookup
    # Format: ([pathCost], path, playerPostion, boxes)
    frontier = [
        (frontierDict[(playerPosition, tuple(boxes.keys()))], "", playerPosition, boxes)
    ]  # A priority queue of the states to explore ordered by their traversal cost

    while frontier:
        # Get the current state
        currentPathCost, currentPath, currentPlayerPosition, currentBoxes = heappop(
            frontier
        )
        frontierDict.pop((currentPlayerPosition, tuple(currentBoxes.keys())))

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
                currentPathCost[0] - len(currentPath),
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

            # Skip if the player can't move in the given direction
            if moveCost == 0:
                continue

            # ALso skip if the state is already explored
            newState = (newPlayerPosition, tuple(newBoxes.keys()))
            if newState in exploredStates:
                continue

            # Update new path cost and get the correct move type
            # (lowercase for ordinary move, uppercase for box pushing action)
            newPathCost = currentPathCost[0] + moveCost
            moveType = direction if moveCost == 1 else direction.upper()

            # Check for new state in the frontier dict
            if newState in frontierDict:
                # Replace the path cost if the new path cost is lower
                # Update this will also update the path cost of the same state in the frontier (built-in list acts as a reference)
                if frontierDict[newState][0] > newPathCost:
                    frontierDict[newState][0] = newPathCost

                continue

            # Add the new state to the frontier and also update the frontier dict
            frontierDict.update({newState: [newPathCost]})
            heappush(
                frontier,
                (
                    frontierDict[newState],
                    currentPath + moveType,
                    newPlayerPosition,
                    newBoxes,
                ),
            )

    # Return None if no solution is found
    return None
