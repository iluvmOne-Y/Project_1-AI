from collections import deque 
from copy import deepcopy
from Level import Level
import pygame
def bfs_solve(level):
    visited = set()
    initial_matrix = level.getMatrix()
    initial_position = level.getPlayerPosition()
    target_count = len(level.getBoxes())
    queue = deque([(deepcopy(initial_matrix), initial_position, [])])
    
    def try_move(matrix, position, direction):
        x, y=position
        new_matrix = deepcopy(matrix)

        dx = -1 if direction == "L" else 1 if direction == "R" else 0
        dy = -1 if direction == "U" else 1 if direction == "D" else 0

        if not (0 <= x + dx < len(new_matrix[y]) and 0 <= y + dy < len(new_matrix)):
            return matrix,position,False

        next_pos = (x + dx, y + dy)
        next_cell = new_matrix[y+dy][x+dx]
        #move to free space or switch
        if next_cell in [" ", ".","+"]:
            new_matrix[y][x] = " "  if new_matrix[y][x] != "+" else "."
            new_matrix[y+dy][x+dx] = "@" if next_cell !="+" else "+"
            return new_matrix, next_pos,True
        #move box
        elif next_cell in ["$","*"]:
            if (0 <= x + 2*dx < len(new_matrix[y]) and 
                0 <= y + 2*dy < len(new_matrix) and 
                new_matrix[y+2*dy][x+2*dx] in [" ", ".","+"]):
                new_matrix[y][x] = " " if new_matrix[y][x] != "+" else "." 
                new_matrix[y+dy][x+dx] = "@" if next_cell !="*" else "+"
                new_matrix[y+2*dy][x+2*dx] = "$" if new_matrix[y+2*dy][x+2*dx] == " " else "*"
                return new_matrix, next_pos, True
        return new_matrix, next_pos, False
   
    while queue:
        current_matrix, current_position, current_path = queue.popleft()
        

        boxes_on_target = sum(row.count("*") for row in current_matrix)
        
        if boxes_on_target == target_count:
            return current_path
        
        state_key = str(current_matrix)
        if state_key in visited:
            continue
        visited.add(state_key)

        for direction in ["L", "R", "U", "D"]:
            new_matrix, new_position, valid_move = try_move(current_matrix, current_position, direction)
            if valid_move:
                queue.append((new_matrix, new_position, current_path + [direction]))
                
    return None