import sys
import pygame
import GameUI as GUI
import Utilities as Utilities
import json
from datetime import datetime
import os
from stats import StatsVisualizer


sample_data = """\
| Level | BFS Storage | BFS States | BFS Time | DFS Storage | DFS States | DFS Time | UCS Storage | UCS States | UCS Time | A* Storage | A* States | A* Time |
|-------|-------------|------------|----------|-------------|------------|----------|-------------|------------|----------|------------|-----------|---------|
| 1     | 0.14        | 204        | 0.01     | 0.05        | 92         | 0.00     | 0.03        | 200        | 0.00     | 0.02       | 146       | 0.01    |
| 2     | 61.06       | 65767      | 3.29     | 0.02        | 11382      | 0.20     | 15.11       | 66363      | 1.37     | 1.30       | 14762     | 0.79    |
| 3     | 0.00        | 977        | 0.04     | 0.00        | 496        | 0.01     | 0.61        | 975        | 0.01     | 0.00       | 606       | 0.03    |
| 4     | 0.00        | 407        | 0.02     | 0.00        | 305        | 0.00     | 0.00        | 407        | 0.01     | 0.00       | 362       | 0.02    |
| 5     | 3.45        | 1683       | 0.07     | 0.00        | 715        | 0.01     | 4.61        | 1694       | 0.03     | 0.02       | 667       | 0.03    |
| 6     | 5.78        | 11052      | 0.54     | 0.59        | 6716       | 0.13     | 3.36        | 10976      | 0.20     | 48.59      | 5582      | 0.34    |
| 7     | 9.89        | 27067      | 1.42     | 22.14       | 26362      | 0.96     | 7.80        | 27022      | 0.56     | 2.42       | 14384     | 0.89    |
| 8     | 1.64        | 9456       | 0.48     | 1.70        | 8098       | 0.16     | 2.25        | 9389       | 0.19     | 3.67       | 6112      | 0.34    |
| 9     | 5.75        | 8572       | 0.48     | 2.83        | 1663       | 0.04     | 7.22        | 8581       | 0.20     | 4.11       | 4215      | 0.28    |
| 10    | 7.41        | 15007      | 0.83     | 53.03       | 12577      | 0.32     | 4.38        | 15065      | 0.30     | 1.14       | 12571     | 0.84    |
"""

# Create instance and generate PDF
""""
visualizer = StatsVisualizer(sample_data)
visualizer.generate_pdf()
stats_visualizer = StatsVisualizer(sample_data)
"""




# Modify the save_algorithm_stats function
def save_algorithm_stats(algorithm_name, level_number, stats):
    """Save algorithm performance data and update visualization"""
    performance_data = {
        "algorithm": algorithm_name,
        "level": level_number,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **stats
    }
    
    if not os.path.exists('results'):
        os.makedirs('results')
        
    filename = f"results/level{level_number}_{algorithm_name}_{datetime.now().strftime('%Y%m%d')}.json"
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
        
    data.append(performance_data)
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    # Generate updated PDF report
    # stats_visualizer.generate_pdf()

# Initialize Pygame
UI = GUI.UI()

# Get the moves corresponding to the keys
moves = {
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
}

# Initialize the level variable
level = None

while True:
    # Set the start Level
    selectedAlgorithm, selectedLevel = UI.drawSelectionMenu()

    # Delete the previous level if it exists
    if level:
        del level
    # Initialize Level
    level = UI.initLevel(selectedLevel, selectedAlgorithm)
    print("\n", level.getPlayerPosition(), level.getBoxes(), level.getSwitches(), "\n")

    levelFinished = False

    while not levelFinished:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in moves:
                    Utilities.movePlayer(level, moves[event.key])
                    UI.drawLevel(level.getMatrix())
                elif event.key == pygame.K_r:
                    UI.initLevel(selectedLevel, selectedAlgorithm)
                elif event.key == pygame.K_s:
                    Utilities.solveLevel(level, selectedAlgorithm, UI)
                    final_stats = {
                        
                        'time': UI.current_stats.get('time', '0.00s') if hasattr(UI, 'current_stats') else '0.00s',
                        'nodes': UI.current_stats.get('nodes', '0') if hasattr(UI, 'current_stats') else 0,
                        'steps': UI.current_stats.get('steps', '0') if hasattr(UI, 'current_stats') else 0,
                        'memory': UI.current_stats.get('memory', '0.00MB') if hasattr(UI, 'current_stats') else '0.00MB'
                    }
                    save_algorithm_stats(selectedAlgorithm.__name__, selectedLevel, final_stats)
                    levelFinished = True
                elif event.key == pygame.K_m:
                    break
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  
            elif event.type == pygame.VIDEORESIZE:
                    UI.resizeWindow(event.size)
                    if level:
                        UI.drawLevel(level.getMatrix())
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
