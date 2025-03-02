class StateStats:
    """A class to represent statistics of the current state.

    ### Attributes
    - path: The path to the current state.
    - nodesExpanded: The total number of nodes expanded.
    - timeTaken: The time taken until this state.
    - memoryUsage: The peak memory usage until this state.
    """

    def __init__(
        self,
        path: str,
        nodesExpanded: int,
        timeTaken: float,
        memoryUsage: float,
    ):
        """Initialize the Solution class.

        ### Parameters
        - path: The path to the current state.
        - nodesExpanded: The total number of nodes expanded.
        - timeTaken: The time taken until this state.
        - memoryUsage: The peak memory usage until this state.
        """
        self.path = path
        self.nodesExpanded = nodesExpanded
        self.timeTaken = timeTaken
        self.memoryUsage = memoryUsage
