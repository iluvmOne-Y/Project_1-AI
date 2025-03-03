=====================================================================
                 SOKOBAN SOLVER - HOW TO RUN
=====================================================================

This guide provides step-by-step instructions to set up and run the 
Sokoban Solver application.

---------------------------------------------------------------------
SETUP INSTRUCTIONS
---------------------------------------------------------------------

1. INSTALL DEPENDENCIES:
   
   Option 1: Using the install script
   $ cd Scripts
   $ chmod +x install.sh
   $ ./install.sh
   
   Option 2: Using pip
   $ pip install pygame psutil pandas reportlab matplotlib
   
   Option 3: Using requirements.txt
   $ cd Source
   $ pip install -r requirements.txt

2. VERIFY INSTALLATION:
   Make sure all libraries are installed correctly:
   $ python -c "import pygame, psutil, pandas, reportlab, matplotlib; print('All dependencies installed!')"

---------------------------------------------------------------------
RUNNING THE APPLICATION
---------------------------------------------------------------------

1. STARTING THE PROGRAM:
   $ cd Source
   $ python main.py

2. MAIN MENU NAVIGATION:
   - Use Up/Down arrows to select algorithm
   - Use Left/Right arrows to select puzzle level
   - Press Enter to start with selected options
   - Press Escape to exit

3. SOLVING OPTIONS:
   - Manual play: Use arrow keys to move the player
   - Automatic solve: Press 'S' to solve with selected algorithm
   - Reset level: Press 'R'
   - Return to main menu: Press 'M' or Escape

4. SOLUTION PLAYBACK:
   - Play/Pause: Space bar
   - Step forward/backward: Right/Left arrows
   - Reset solution: 'R' key
   - Return to menu: 'M' or Escape

---------------------------------------------------------------------
GENERATING SOLUTION REPORTS
---------------------------------------------------------------------

After running algorithms, generate a performance comparison report:
$ cd Source/outputs
$ python stats.py

The report will be saved as a PDF in the outputs directory.

---------------------------------------------------------------------
FILE STRUCTURE (EXECUTION-RELEVANT)
---------------------------------------------------------------------

Source/
├── main.py                 # Main entry point
├── Algorithms/             # Contains all solver algorithms
├── Inputs/                 # Puzzle level definitions
└── outputs/                # Solution outputs and statistics

---------------------------------------------------------------------
COMMON ISSUES
---------------------------------------------------------------------

1. "ModuleNotFoundError":
   - Verify all dependencies are installed correctly
   - Make sure you're running from the correct directory

2. "No such file or directory":
   - Check that you're in the correct directory
   - Verify that file paths haven't been changed

3. Display issues:
   - Pygame requires a graphical environment
   - If running remotely, ensure X11 forwarding is enabled
p
---------------------------------------------------------------------
EXAMPLE WORKFLOW
---------------------------------------------------------------------

$ cd Source
$ python main.py
  (Select algorithm and level from menu)
  (Press Enter)
  (Press 'S' to solve automatically)
  (Watch solution or use Space to control playback)
  (Press 'M' to return to menu)
$ cd outputs
$ python stats.py
  (View generated performance report)

---------------------------------------------------------------------
For more information, refer to the project documentation or contact
the development team.
---------------------------------------------------------------------