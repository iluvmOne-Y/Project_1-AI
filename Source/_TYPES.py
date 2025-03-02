from typing import Callable

from Data.Types.Level import Level
from Data.Types.Solution import Solution

Algorithm = Callable[[Level], Solution]

__all__ = ["Level", "Solution", "Algorithm"]
