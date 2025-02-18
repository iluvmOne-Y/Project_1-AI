import os as os
from copy import deepcopy


class Level:
    """The class that represents the level of the game."""

    matrix = []
    """The matrix of the level."""
    matrixHistories = []
    """The storage to older versions of the level matrix."""

    playerPosition = [0, 0]
    """The position of the player."""

    boxes = []
    """The positions of the boxes."""
    switches = []
    """The positions of the switches."""

    def __init__(self, levelNumber: int):
        """Initialize the level and getting the player position, boxes, and switches.

        ### Parameters
        @levelNumber: The level number to be loaded.
        """
        del self.matrix[:]
        del self.matrixHistories[:]

        # Create level
        with open(
            os.path.dirname(os.path.abspath(__file__))
            + "/levels/"
            + "/level"
            + str(levelNumber),
            "r",
        ) as f:
            for row in f.read().splitlines():
                self.matrix.append(list(row))

        # Get player position
        for i in range(0, len(self.matrix)):
            # Iterate all columns
            for k in range(0, len(self.matrix[i]) - 1):
                if self.matrix[i][k] == "@" or self.matrix[i][k] == "+":
                    self.playerPosition = [k, i]
                    break

        # Get boxes and switches
        for i in range(0, len(self.matrix)):
            # Iterate all columns
            for k in range(0, len(self.matrix[i]) - 1):
                if self.matrix[i][k] == "$":
                    self.boxes.append([k, i])
                elif self.matrix[i][k] == ".":
                    self.switches.append([k, i])
                elif self.matrix[i][k] == "*":
                    self.boxes.append([k, i])
                    self.switches.append([k, i])

    def getMatrix(self):
        """Return the current matrix of the level."""
        return self.matrix

    def getLastMatrix(self):
        """Return the last matrix from the history and set it as the current matrix.
        If no history is available, return the current matrix.
        """
        if len(self.matrixHistories) > 0:
            lastMatrix = self.matrixHistories.pop()
            self.matrix = lastMatrix
            return lastMatrix
        else:
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
        largestRowLength = 0
        # Iterate all rows
        for i in range(0, len(self.matrix)):
            # Get the length of each row
            rowLength = len(self.matrix[i])
            # Update the largest row length if the current row length is larger
            if rowLength > largestRowLength:
                largestRowLength = rowLength
        return [largestRowLength, len(self.matrix)]

    def addToHistory(self, matrix: list):
        """Store the provided matrix to the history list.

        ### Parameters
        @matrix: The matrix to be stored in the history list.
        """
        self.matrixHistories.append(deepcopy(matrix))
