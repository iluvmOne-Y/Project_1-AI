# Sokoban Solver

A Python implementation of various search algorithms to solve Sokoban puzzles. This project visualizes how different algorithms navigate through puzzles, offering real-time statistics and solution analysis.

## Overview

The project implements multiple search algorithms to solve Sokoban puzzles, where the player must push boxes onto target locations. Each algorithm uses different strategies to find optimal or near-optimal solutions.

## Algorithms

The project implements the following search algorithms:

1. **BFS (Breadth-First Search)** - Explores all nodes at a given depth before moving to nodes at the next depth level. Guarantees the shortest path in terms of steps but may not be optimal for weighted puzzles.

2. **DFS (Depth-First Search)** - Explores as far as possible along each branch before backtracking. Fast for finding any solution but does not guarantee optimality.

3. **UCS (Uniform Cost Search)** - Similar to BFS but prioritizes paths with lower cumulative costs. Guarantees the cheapest path.

4. **A* (A-Star)** - Combines path cost with a heuristic function to guide the search more efficiently. Guarantees optimal solutions if the heuristic is admissible.

5. **Dijkstra** - A special case of UCS that finds the shortest path in a weighted graph.

6. **Greedy BFS** - Uses only the heuristic function to decide which node to expand next. Very efficient but does not guarantee optimal solutions.

7. **Swarm** - A collaborative approach where multiple simulated agents explore the state space using pheromone-based strategies inspired by ant colony optimization.

## Requirements

The following Python libraries are required:

- pygame - For visualization
- psutil - For memory tracking
- pandas - For data analysis in the stats report
- reportlab - For PDF report generation
- matplotlib - For generating charts

## Installation

### Using the install script:

```bash
cd Scripts
chmod +x install.sh
./install.sh
```
### Using requirement.txt
```bash
cd source 
pip install -r requirement.txt
```

### Manual installation:

```bash
pip install pygame psutil pandas reportlab matplotlib
```

## How to Run

Navigate to the Source directory and run main.py:

```bash
cd Source
python main.py
```

## Game Controls

### Main Menu:
- **Arrow Keys** - Navigate between levels and algorithms
- **Enter** - Select level and algorithm
- **Escape** - Exit the game

### During Gameplay:
- **S** - Solve the level with the selected algorithm
- **Arrow Keys** - Move the player manually
- **R** - Reset the level
- **M/Escape** - Return to the menu

### After Solution:
- **Space** - Play/pause the solution playback
- **Left/Right Arrow** - Step through solution states
- **R** - Restart the solution
- **M/Escape** - Return to the menu

## Project Structure

```
.
├── Scripts/
│   └── install.sh              # Installation script
├── Source/
│   ├── Algorithms/             # Implementation of all search algorithms
│   │   ├── AStar.py
│   │   ├── BFS.py
│   │   ├── DFS.py
│   │   ├── Dijkstra.py
│   │   ├── GreedyBFS.py
│   │   ├── Swarm.py
│   │   └── UCS.py
│   ├── Controller/             # Game control logic
│   ├── Data/                   # Game assets and data types
│   │   ├── Assets/             # Graphics and fonts
│   │   └── Types/              # Data structure definitions
│   ├── Inputs/                 # Puzzle level definitions
│   ├── outputs/                # Solution outputs and statistics
│   ├── _TYPES.py               # Type definitions
│   ├── main.py                 # Main entry point
│   ├── requirements.txt        # Python dependencies
│   └── Utilities.py            # Helper functions
```

## Solution Analysis

After running the algorithms, you can generate a comprehensive report comparing their performance:

```bash
cd Source/outputs
python stats.py
```

This will create a PDF report with tables and charts comparing the algorithms based on:
- Execution time
- Number of nodes expanded
- Memory usage
- Solution steps
- Solution weights

## Input Format

Level files follow this format:
- First line: Box weights (space-separated integers)
- Remaining lines: Level layout using these symbols:
  - `@` - Player
  - `+` - Player on target
  - `#` - Wall
  - ` ` - Empty space
  - `$` - Box
  - `.` - Target/switch
  - `*` - Box on target

## Output Format

Solution files include:
- Algorithm name
- Statistics (Steps, Weight, Nodes, Time, Memory)
- Solution path (sequence of moves)
