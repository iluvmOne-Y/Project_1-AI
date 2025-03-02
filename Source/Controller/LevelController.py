import _TYPES as _TYPES

# Intergrated modules
import os as os
import sys as sys
import copy as copy
from threading import Thread, Event

# External modules
import pygame as pygame

# Custom modules
import Utilities as Utilities
import Controller.InterfaceController as InterfaceController


# Get the moves corresponding to the keys
moves = {
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
}


def InitLevel(level: _TYPES.Level, algorithm: _TYPES.Algorithm):
    """Handle actions taking place on level screen.

    ### Parameters
    - level: The level to be managed.
    - algorithm: The algorithm to solve the level.
    """
    originalLevel = copy.deepcopy(level)

    while True:
        for event in pygame.event.get():
            # Check if the event is a key press
            if not event.type == pygame.KEYDOWN:
                # Exit if the event is a quit event
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                # Continue to the next event if the event is not a key press
                continue

            # Move the player in the given direction if direction key is pressed
            if event.key in moves:
                level.playerPosition, level.boxes, _ = Utilities.MovePlayer(
                    level, level.playerPosition, level.boxes, moves[event.key]
                )
                InterfaceController.DrawMatrix(level.getMatrix(), level.matrixSize)

            # Reset the level if 'r' key is pressed
            elif event.key == pygame.K_r:
                InterfaceController.DrawMatrix(
                    originalLevel.getMatrix(), originalLevel.matrixSize
                )
                level = copy.deepcopy(originalLevel)

            # Solve the level if 's' key is pressed
            elif event.key == pygame.K_s:
                SolveLevel(level, algorithm)
                return

            # Return to the main menu if 'm' or 'esc' key is pressed
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                return


def SolveLevel(
    level: _TYPES.Level,
    algorithm: _TYPES.Algorithm,
):
    """Solve the given level using the given algorithm and control post-solving input actions.

    ### Parameters
    - level: The level to solve.
    - algorithm: The algorithm to solve the level with.
    """
    # Solve the level
    solution: _TYPES.Solution = algorithm(level,InterfaceController)
    

    # Return if no solution is found
    if not solution:
        # Draw the fail screen when the level could not be solved
        InterfaceController.DrawFailScreen(level, algorithm.__name__)

        # Wait for a key press
        while True:
            for event in pygame.event.get():
                # Check if the event is a quit event
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                # Return if the event is a key press
                elif event.type == pygame.KEYDOWN:
                    return

        return
    
    SaveSolutionToFile(level, algorithm.__name__, solution)
    # Draw the success screen when the level is completed
    InterfaceController.DrawSuccessScreen(level, algorithm.__name__,solution)

    moves = {
        "l": (-1, 0),
        "r": (1, 0),
        "u": (0, -1),
        "d": (0, 1),
    }

    # Initialize the list of mazes
    solutionStates = [level.getMatrix()]

    # Generate list of mazes according to the solution path
    for direction in solution.path:
        level.playerPosition, level.boxes, _ = Utilities.MovePlayer(
            level, level.playerPosition, level.boxes, moves[direction.lower()]
        )
        solutionStates.append(level.getMatrix())

    # Draw the solution path
    global index
    index = 0
    InterfaceController.DrawMatrix(solutionStates[0], level.matrixSize)

    # Initialize the movement events
    moveRightEvent = Event()
    moveLeftEvent = Event()

    # Define functions to move to the next and previous mazes
    def moveToNextMatrix():
        global index

        # Keep moving to the next maze while the right key is being pressed
        while True:
            index += 1
            # Check if the index is out of bounds
            if index >= len(solutionStates):
                index = len(solutionStates) - 1
            else:
                InterfaceController.DrawMatrix(solutionStates[index], level.matrixSize)

            # Wait for a while before moving to the next maze
            pygame.time.wait(100)

            # Check if the right key is released
            if not moveRightEvent.is_set():
                break

    def moveToPreviousMatrix():
        global index

        # Keep moving to the previous maze while the left key is being pressed
        while True:
            index -= 1
            # Check if the index is out of bounds
            if index < 0:
                index = 0
            else:
                InterfaceController.DrawMatrix(solutionStates[index], level.matrixSize)

            # Wait for a while before moving to the next maze
            pygame.time.wait(100)

            # Check if the left key is released
            if not moveLeftEvent.is_set():
                break

    # Initialize the threads for maze change
    moveLeftThread: Thread = None
    moveRightThread: Thread = None

    paused = True

    while True:
        for event in pygame.event.get():
            # Check if the event is a quit event
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            # Check if the event is a key press
            elif event.type == pygame.KEYDOWN:
                # Return to the main menu if 'm' or 'esc' key is pressed
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                    return

                # Reset the level if 'r' key is pressed
                elif event.key == pygame.K_r:
                    index = 0
                    InterfaceController.DrawMatrix(
                        solutionStates[index], level.matrixSize
                    )

                    # Also pause the game
                    paused = True

                # Toggle game pause if 'space' key is pressed
                elif event.key == pygame.K_SPACE:
                    paused = not paused

                elif paused and event.key == pygame.K_LEFT:
                    moveLeftEvent.set()

                    # Also stop the thread to move to the next maze
                    if moveRightThread:
                        moveRightEvent.clear()
                        moveRightThread.join()

                    # Start the thread to move to the previous maze
                    moveLeftThread = Thread(target=moveToPreviousMatrix)
                    moveLeftThread.start()

                elif paused and event.key == pygame.K_RIGHT:
                    moveRightEvent.set()

                    # Also stop the thread to move to the previous maze
                    if moveLeftThread:
                        moveLeftEvent.clear()
                        moveLeftThread.join()

                    # Start the thread to move to the next maze
                    moveRightThread = Thread(target=moveToNextMatrix)
                    moveRightThread.start()

            elif event.type == pygame.KEYUP:
                # Check if the event is a key release
                if event.key == pygame.K_LEFT:
                    # Stop the thread to move to the previous maze
                    if moveLeftThread:
                        moveLeftEvent.clear()
                        moveLeftThread.join()

                elif event.key == pygame.K_RIGHT:
                    # Stop the thread to move to the next maze
                    if moveRightThread:
                        moveRightEvent.clear()
                        moveRightThread.join()

        # Check if the game is paused
        if not paused:
            # Increment the index to show the next maze
            index += 1

            # Check if the index is out of bounds
            if index >= len(solutionStates):
                # Reset the index and pause the game
                index = -1
                paused = True
            else:
                InterfaceController.DrawMatrix(solutionStates[index], level.matrixSize)
                pygame.time.wait(200)



def SaveSolutionToFile(level: _TYPES.Level, algorithmName: str, solution: _TYPES.Solution):
    """Save the solution statistics to an output file according to the specified format.
    
    Format:
    - Line 1: Algorithm name
    - Line 2: Statistics (Steps, Weight, Node, Time (ms), Memory (MB))
    - Line 3: Solution path as a string
    
    ### Parameters
    - level: The solved level
    - algorithmName: Name of the algorithm used
    - solution: The solution data
    """
    # Format level number with zero padding
    formatted_level = f"{level.number:02d}"  # 01, 02, etc.
    
    # Generate filename based on required format
    filename = f"outputs/output-{formatted_level}.txt"
    
    # Check if file exists - if so, we'll append to it rather than overwrite
    file_exists = os.path.exists(filename)
    
    # Open file in append mode if it exists, otherwise create new
    with open(filename, "a" if file_exists else "w") as f:
        # If this is a new file, no newline needed
        # If we're appending, add a newline before the algorithm name
        if file_exists:
            f.write("\n")
            
        # Line 1: Algorithm name
        f.write(f"{algorithmName}\n")
        
        # Line 2: Statistics (convert time to milliseconds)
        time_ms = solution.timeTaken * 1000  # Convert seconds to milliseconds
        f.write(f"Steps: {solution.steps}, Weight: {solution.weight}, ")
        f.write(f"Node: {solution.nodesExpanded}, Time (ms): {time_ms:.2f}, ")
        f.write(f"Memory (MB): {solution.memoryUsage:.2f}\n")
        
        # Line 3: Solution path as a string
        f.write(f"{''.join(solution.path)}")
        
    print(f"Solution saved to {filename}")
__all__ = ["InitLevel"]
