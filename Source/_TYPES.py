from typing import Callable

from Data.Types.Level import Level
from Data.Types.Solution import Solution
from Data.Types.StateStats import StateStats

Algorithm = Callable[[Level], Solution]

__all__ = ["Level", "Solution", "StateStats", "Algorithm"]
