import os as os
from copy import deepcopy


class Level:
    """The class that represents the level of the game."""

    def __init__(self, levelNumber: int):
        """Initialize the level and getting the player position, boxes, and switches.

        ### Parameters
        @levelNumber: The level number to be loaded.
        """
        self.matrix = []
        self.matrixSize = [0, 0]
        self.playerPosition = []
        self.boxes = {}
        self.switches = []
        # Create level
        weights = []
        with open(
            os.path.dirname(os.path.abspath(__file__))
            + "/levels/"
            + "/level"
            + str(levelNumber),
            "r",
        ) as f:
            # Get the weights of the boxes
            weights = f.readline().split()
            # Get the size while parsing the matrix
            largestRowLength = 0
            # Iterate all rows
            for row in f.read().splitlines():
                self.matrix.append(list(row))
                # Update the largest row length
                largestRowLength = (
                    len(self.matrix[self.matrixSize[1]])
                    if len(self.matrix[self.matrixSize[1]]) > largestRowLength
                    else largestRowLength
                )
                self.matrixSize[1] += 1
            # Set the row length of the matrix
            self.matrixSize[0] = largestRowLength

        # Get player position, boxes and switches
        for i in range(0, len(self.matrix)):
            # Iterate all columns
            for k in range(0, len(self.matrix[i]) - 1):
                if self.matrix[i][k] == "@" or self.matrix[i][k] == "+":
                    self.playerPosition = [k, i]
                elif self.matrix[i][k] == "$":
                    self.boxes.update({(k, i): int(weights[len(self.boxes)])})
                elif self.matrix[i][k] == ".":
                    self.switches.append([k, i])
                elif self.matrix[i][k] == "*":
                    self.boxes.update({(k, i): int(weights[len(self.boxes)])})
                    self.switches.append([k, i])

    def getMatrix(self):
        """Return the current matrix of the level."""
        return self.matrix

    def getPlayerPosition(self):
        """Return the current position of the player."""
        return self.playerPosition

    def getBoxes(self):
        """Return the list of box positions."""
        return self.boxes

    def getSwitches(self):
        """Return the list of switch positions."""
        return self.switches

    def getSize(self):
        """Return the size of the matrix."""
        return self.matrixSize

    def printMatrix(self):
        """Print the matrix of the level."""
        for row in self.matrix:
            print("".join(row))
        print("\n")
