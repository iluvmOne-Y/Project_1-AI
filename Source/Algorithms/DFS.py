import _TYPES as _TYPES

# Intergrated modules
import time as time

# Custom modules
from Controller.InterfaceController import DrawStats
from Utilities import GetMemoryUsage, IsDeadlock, MovePlayer


def DFS(level: _TYPES.Level) -> _TYPES.Solution:
    """A function to solve a level using the Depth First Search algorithm.

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

    exploredStates = set()
    # Format: (playerPostion, boxes, path, pathCost)
    frontier = [
        (playerPosition, boxes, "", 0),
    ]  # A stack of the states to explore
    frontierSet = {
        (playerPosition, tuple(boxes.keys()))
    }  # Set for constant-time membership checking

    # Iterate through the frontier
    while frontier:
        # Get the current state
        currentPlayerPosition, currentBoxes, currentPath, currentPathCost = (
            frontier.pop()
        )
        frontierSet.remove((currentPlayerPosition, tuple(currentBoxes.keys())))

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

        # Iterate through the directions
        for direction in directions:
            # Move the player in the given direction
            move = moves[direction]
            newPlayerPosition, newBoxes, moveCost = MovePlayer(
                level, currentPlayerPosition, currentBoxes, move, True
            )

            # Skip if the player can't move in the given direction
            if moveCost == 0:
                continue

            # Skip if the new state has already been explored or is in the frontier
            newState = (newPlayerPosition, tuple(newBoxes.keys()))
            if newState in exploredStates or newState in frontierSet:
                continue

            # Get the correct move type
            # (lowercase for ordinary move, uppercase for box pushing action)
            moveType = direction if moveCost == 1 else direction.upper()

            # Append this new state to the end of the frontier
            frontier.append(
                (
                    newPlayerPosition,
                    newBoxes,
                    currentPath + moveType,
                    currentPathCost + moveCost,
                )
            )
            # Add the new state to the frontier set
            frontierSet.add(newState)

    # Return None if no solution is found
    return None
