class Solution:
    """A class to represent a solution to a level.

    ### Attributes
    - steps: The number of steps to solve the level.
    - weight: The weight of the solution.
    - nodesExpanded: The total number of nodes expanded.
    - timeTaken: The time taken to solve the level.
    - memoryUsage: The memory usage of the algorithm.
    - path: The path to the solution.
    """

    def __init__(
        self,
        steps: int,
        weight: int,
        nodesExpanded: int,
        timeTaken: float,
        memoryUsage: float,
        path: str,
    ):
        """Initialize the Solution class.

        ### Parameters
        - steps: The number of steps to solve the level.
        - weight: The weight of the solution.
        - nodesExpanded: The total number of nodes expanded.
        - timeTaken: The time taken to solve the level.
        - memoryUsage: The memory usage of the algorithm.
        - path: The path to the solution.
        """
        self.steps = steps
        self.weight = weight
        self.nodesExpanded = nodesExpanded
        self.timeTaken = timeTaken
        self.memoryUsage = memoryUsage
        self.path = path

    def __str__(self) -> str:
        """Return the string representation of the solution."""
        return f"Steps: {self.steps}, Weight: {self.weight}, Node: {self.nodesExpanded}, Time (ms): {self.timeTaken:.2f}, Memory (MB): {self.memoryUsage:.2f}\n{self.path}"
