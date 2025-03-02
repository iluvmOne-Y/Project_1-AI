import _TYPES as _TYPES

# Intergrated modules
import time as time

# Custom modules
from Utilities import GetMemoryUsage, IsDeadlock, MovePlayer


def DFS(level: _TYPES.Level,ui=None) -> _TYPES.Solution:
    """A function to solve a level using the Depth First Search algorithm.

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
    # Format: (playerPostion, boxes, path, pathCost)
    frontier = [
        (playerPosition, boxes, [], 0),
    ]  # A stack of the current state and the path to the current state

    # Iterate through the frontier
    while frontier:
        # Get the current state
        currentPlayerPosition, currentBoxes, currentPath, currentCost = frontier.pop()
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
        # Return solution and relevant datas if all switches are activated
        if all(switchPostion in currentBoxes for switchPostion in switches):
            return _TYPES.Solution(
                len(currentPath),
                currentCost,
                totalNodes,
                time.time() - startTime,
                peakMemory,
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

            # Check if the player can move in the given direction
            if moveCost != 0:
                # Skip if the new state has already been explored
                if (newPlayerPosition, tuple(newBoxes.keys())) in exploredStates:
                    continue

                # Check if the new state is in the frontier
                isInFrontier = False
                for state in frontier:
                    if state[0] == newPlayerPosition and state[1] == newBoxes:
                        isInFrontier = True
                        break

                # Also skip if the new state is in the frontier
                if isInFrontier:
                    continue

                # Get the correct move type
                moveType = direction.lower() if moveCost == 1 else direction

                # Append this new state to the end of the frontier
                frontier.append(
                    (
                        newPlayerPosition,
                        newBoxes,
                        currentPath + [moveType],
                        currentCost + moveCost,
                    )
                )

    # Return None if no solution is found
    return None
