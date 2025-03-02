import _TYPES as _TYPES

# Intergrated modules
import time as time
from heapq import heappush

# Custom modules
from Utilities import GetMemoryUsage, IsDeadlock, MovePlayer, CalculateHeuristicValue


def AStar(level: _TYPES.Level) -> _TYPES.Solution:
    """A function to solve a level using the A* algorithm.

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

    # Initialize the frontier
    # Format: (weight, pathCost, path, playerPostion, boxes)
    heappush(
        frontier,
        (0, 0, "", playerPosition, boxes),
    )

    while frontier:
        # Get the current state
        _, currentCost, currentPath, currentPlayerPosition, currentBoxes = frontier.pop(
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

        # Add the current state to the explored set
        exploredStates.add((currentPlayerPosition, tuple(currentBoxes.keys())))

        # Check if all switches are activated
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

                # Check if the new state has already been explored
                explored = False
                if (newPlayerPosition, tuple(newBoxes.keys())) in exploredStates:
                    explored = True

                # Calculate the weight of the new state
                # by adding heuristic value to the true travel cost and the current path cost
                weight = (
                    currentCost
                    + moveCost
                    + CalculateHeuristicValue(newPlayerPosition, newBoxes, switches)
                )

                # Loop through the frontier and find any states that match the new state
                for i, state in enumerate(frontier):
                    # Skip if the state is not the same as the new state
                    if state[3] != newPlayerPosition or state[4] != newBoxes:
                        continue

                    # Update the frontier if the new state has a lower weight
                    if not explored and weight < state[0]:
                        # Remove the old state and path from the frontier
                        frontier.pop(i)

                # Skip if the new state has already been explored
                if explored:
                    continue

                # Add the new state and path to the frontier
                heappush(
                    frontier,
                    (
                        weight,
                        currentCost + moveCost,
                        currentPath + moveType,
                        newPlayerPosition,
                        newBoxes,
                    ),
                )

    # Return None if no solution is found
    return None
