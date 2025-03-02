import _TYPES as _TYPES

# Intergated modules
import pathlib as pathlib

# Custom modules
import Controller.InterfaceController as InterfaceController
import Controller.LevelController as LevelController

# Custom modules
from Algorithms.BFS import BFS
from Algorithms.DFS import DFS
from Algorithms.UCS import UCS
from Algorithms.AStar import AStar
from Algorithms.Dijkstra import Dijkstra
from Algorithms.GreedyBFS import GreedyBFS

# Get the algorithms
algorithms: list = [BFS, DFS, UCS, AStar, Dijkstra, GreedyBFS]

while True:
    level, algorithm = InterfaceController.DrawSelectionMenu(algorithms)
    LevelController.InitLevel(level, algorithm)
