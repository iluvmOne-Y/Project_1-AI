# Intergrated modules
from os.path import dirname, abspath
from copy import deepcopy


class Level:
    """The class that represents the level of the game.

    ### Attributes
    - number: The order number of the level.
    - matrix: The matrix of the level.
    - matrixSize: The size of the matrix.
    - playerPosition: The position of the player.
    - boxes: The positions of the boxes and their weights.
    - switches: The positions of the switches.
    """

    def __init__(self, levelNumber: int):
        """Initialize the level and getting the player position, boxes, and switches.

        ### Parameters
        @levelNumber: The level order number to be loaded.
        """
        # Set the level order number
        self.number = levelNumber

        # Initialize the attributes
        self.matrix: list = []
        self.matrixSize: tuple = ()
        self.playerPosition: tuple = ()
        self.boxes: dict = {}
        self.switches: list = []

        weights = []

        # Open input file and read the level
        with open(
            (
                dirname(dirname(dirname(abspath(__file__))))
                + "/Inputs/input-"
                + (str(levelNumber) if levelNumber > 9 else "0" + str(levelNumber))
                + ".txt"
            ),
            "r",
        ) as f:
            # Get the weights of the boxes
            weights = f.readline().split()

            # Initialize the matrix size
            rowCount = 0
            columnCount = 0

            # Iterate and get single row each iteration from the file
            for row in f.read().splitlines():
                # Remove the trailing whitespaces on the right side of the row
                row.rstrip()

                # Append the row to the matrix
                self.matrix.append(list(row))

                # Update the row length if the current row is longer
                if len(row) > columnCount:
                    columnCount = len(row)

                # Update the row count
                rowCount += 1

            # Update the matrix size
            self.matrixSize = (columnCount, rowCount)

        # Get player position, boxes and switches as well as remove character and boxes from the matrix
        for i in range(0, len(self.matrix)):
            # Iterate all columns
            for k in range(0, len(self.matrix[i]) - 1):
                if self.matrix[i][k] == "@":
                    self.playerPosition = (k, i)
                    self.matrix[i][k] = " " if self.matrix[i][k] == "@" else "."
                elif self.matrix[i][k] == "$":
                    self.boxes.update({(k, i): int(weights[len(self.boxes)])})
                    self.matrix[i][k] = " "
                elif self.matrix[i][k] == ".":
                    self.switches.append((k, i))
                elif self.matrix[i][k] == "+":
                    self.playerPosition = (k, i)
                    self.switches.append((k, i))
                    self.matrix[i][k] = "."
                elif self.matrix[i][k] == "*":
                    self.boxes.update({(k, i): int(weights[len(self.boxes)])})
                    self.switches.append((k, i))
                    self.matrix[i][k] = "."

    def getMatrix(self):
        """Return the current matrix state of the level."""
        matrix = deepcopy(self.matrix)

        # Add the boxes to the matrix
        for box in self.boxes:
            matrix[box[1]][box[0]] = "$" if matrix[box[1]][box[0]] == " " else "*"

        # Add the player to the matrix
        matrix[self.playerPosition[1]][self.playerPosition[0]] = (
            "@"
            if matrix[self.playerPosition[1]][self.playerPosition[0]] == " "
            else "+"
        )

        return matrix
