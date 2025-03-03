import _TYPES as _TYPES

# Intergrated modules
import time as time
from heapq import heappush, heappop

# Custom modules
from Controller.InterfaceController import DrawStats
from Utilities import GetMemoryUsage, IsDeadlock, MovePlayer, CalculateHeuristicValue

def SwarmAlgorithm(level: _TYPES.Level) -> _TYPES.Solution:
    """A function to solve a level using a Swarm Intelligence algorithm.
    
    ### Parameters
    - level: The level to solve.
    
    ### Returns
    - _TYPES.Solution: The solution to the level.
    """
    # Initialize measurements
    startMemory = GetMemoryUsage()
    startTime = time.time()
    totalNodes = 0
    peakMemory = 0
    
    # Get the moves and directions
    directions = ["l", "r", "u", "d"]
    moves = {
        "l": (-1, 0),
        "r": (1, 0),
        "u": (0, -1),
        "d": (0, 1),
    }
    
    # Check for initial deadlocks
    for box in level.boxes:
        for direction in directions:
            if IsDeadlock(level.matrix, level.boxes, box, moves[direction]):
                return None
    
    # Initialize agents (multiple exploration paths)
    agentCount = 100  
    
    # Create initial pheromone map (state attractiveness)
    pheromoneMap = {}
    globalExplored = set()
    #bestSolution = None
    
    # Initialize frontiers for each agent
    frontiers = []
    for i in range(agentCount):
        # Format: (playerPosition, boxes, path, pathCost)
        frontiers.append([(level.playerPosition, level.boxes, "", 0)])
    
    # Agent-specific explored sets
    exploredSets = [set() for _ in range(agentCount)]
    
    # Factors for heuristic calculation
    alpha = 1.0  # Pheromone importance
    beta = 2.0   # Heuristic importance
    evapRate = 0.95  # Pheromone evaporation rate (5% per iteration)
    
    # Main iteration loop
    iterations = 0
    max_iterations = 20000  # Reduced from 1000 to improve efficiency
    
    while iterations < max_iterations:
        # Skip iteration if we're out of states to explore
        if all(len(frontier) == 0 for frontier in frontiers):
            break
            
        totalNodesThisIteration = 0
        
        # Move each agent
        for agentId, frontier in enumerate(frontiers):
            if not frontier:
                continue
                
            # Get the states this agent will explore this iteration (limited to prevent one agent doing all work)
            statesToExplore = min(len(frontier), 200)
            
            for _ in range(statesToExplore):
                if not frontier:
                    break
                    
                # Get current state
                currentPlayerPos, currentBoxes, currentPath, currentCost = frontier.pop(0)
                currentState = (currentPlayerPos, tuple(sorted(currentBoxes.keys())))
                
                # Skip if already explored globally
                if currentState in globalExplored:
                    continue
                    
                # Add to explored sets
                exploredSets[agentId].add(currentState)
                globalExplored.add(currentState)
                totalNodes += 1
                totalNodesThisIteration += 1
                
                # Check if goal state
                if all(switchPos in currentBoxes for switchPos in level.switches):
                    solution = _TYPES.Solution(
                        len(currentPath),
                        currentCost - len(currentPath),
                        totalNodes,
                        time.time() - startTime,
                        max(peakMemory, GetMemoryUsage() - startMemory),
                        currentPath,
                    )
                    '''
                    # Update best solution if this is better
                    if not bestSolution or len(currentPath) < len(bestSolution.path):
                        bestSolution = solution
                        
                    continue
                    '''
                    return solution
                # Show stats periodically
                if totalNodes % 5000 == 0:
                    peakMemory = max(peakMemory, GetMemoryUsage() - startMemory)
                    stats = _TYPES.StateStats(
                        currentPath,
                        totalNodes,
                        time.time() - startTime,
                        peakMemory,
                    )
                    DrawStats(stats)
                
                # Deposit pheromone - more if closer to goal
                heuristic = CalculateHeuristicValue(currentPlayerPos, currentBoxes, level.switches)
                pheromone = 100.0 / (1.0 + heuristic)  # Higher pheromone for better states
                pheromoneMap[currentState] = pheromoneMap.get(currentState, 0) + pheromone
                
                # Explore neighbors
                nextStates = []
                for direction in directions:
                    move = moves[direction]
                    newPlayerPos, newBoxes, moveCost = MovePlayer(
                        level, currentPlayerPos, currentBoxes, move, True
                    )
                    
                    if moveCost == 0:
                        continue
                        
                    newState = (newPlayerPos, tuple(sorted(newBoxes.keys())))
                    if newState in globalExplored:
                        continue
                        
                    moveType = direction if moveCost == 1 else direction.upper()
                    newPath = currentPath + moveType
                    newCost = currentCost + moveCost
                    
                    # Calculate priority based on pheromone and heuristic
                    newHeuristic = CalculateHeuristicValue(newPlayerPos, newBoxes, level.switches)
                    statePheromone = pheromoneMap.get(newState, 0.1)
                    
                    # Calculate priority: more pheromone = higher priority, lower heuristic = higher priority
                    priority = (statePheromone ** alpha) * ((1.0 / (1.0 + newHeuristic)) ** beta)
                    
                    nextStates.append((priority, newPlayerPos, newBoxes, newPath, newCost))
                
                # Sort next states by priority (highest first)
                nextStates.sort(reverse=True)
                
                # Add to frontier
                for _, newPos, newBoxes, newPath, newCost in nextStates:
                    frontier.append((newPos, newBoxes, newPath, newCost))
        
        # Evaporate pheromones
        for state in pheromoneMap:
            pheromoneMap[state] *= evapRate
        
        # Knowledge sharing - share promising states between agents
        if iterations % 10 == 0 and iterations > 0:
            # Find states with high pheromone
            highPheromoneStates = sorted(
                [(state, pheromone) for state, pheromone in pheromoneMap.items()],
                key=lambda x: x[1],
                reverse=True
            )[:10]  # Top 10 states
            
            # Share these states by adding them to other agents' frontiers
            for agentId, frontier in enumerate(frontiers):
                for (playerPos, boxKeys), _ in highPheromoneStates:
                    # Recreate the boxes dictionary
                    boxes = {box: level.boxes[box] if box in level.boxes else 1 for box in boxKeys}
                    
                    # Only add if not in this agent's explored set
                    if (playerPos, boxKeys) not in exploredSets[agentId]:
                        # Use the shared knowledge with a small path penalty
                        frontier.append((playerPos, boxes, f"S{iterations}", 2))
        
        # Show progress
        if iterations % 20 == 0:
            peakMemory = max(peakMemory, GetMemoryUsage() - startMemory)
            stats = _TYPES.StateStats(
                f"Iteration {iterations}, Agents: {agentCount}, Nodes: {totalNodes}",
                totalNodes,
                time.time() - startTime,
                peakMemory,
            )
            DrawStats(stats)
            
        iterations += 1
    
    # Return best solution found, if any
    #return bestSolution