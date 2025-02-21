import pygame
from collections import deque
from game_map import GameMap
import random

# File not being used because ghost calculation causes lag
# and using manhattan distance doesn't properly allow ghosts to move at all sometimes

s_width = 900
s_height = 850

# initialize GameMap instance
game_map = GameMap(s_width, s_height)
level = game_map.level

# Directions: Right (0), Left (1), Up (2), Down (3)
DIRECTIONS = [(1, 0), (-1, 0), (0, -1), (0, 1)]  # Right, Left, Up, Down

def bfs_movement(level, start, goal, is_scared):
    """
    use BFS to find the shortest path for the ghost.
    If is_scared is True, it will avoid the player (run away), else it will chase the player.
    """
    queue = deque([(start[0], start[1], [])])  # (x, y, path)
    visited = set()
    visited.add(start)
    
    while queue:
        x, y, path = queue.popleft()
        
        if (x, y) == goal:
            return path  # Return the path to the goal
        
        for i, (dx, dy) in enumerate(DIRECTIONS):
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(level[0]) and 0 <= ny < len(level):
                if level[ny][nx] < 3 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [i]))  
    return []  # No path found

def move_ghost(ghost, level, player, is_scared):
    """
    Move the ghost using BFS either toward or away from the player.
    If Pac-Man is far, move randomly instead.
    """
    start = (ghost.x // ghost.width, ghost.y // ghost.height)  
    goal = (player.x // ghost.width, player.y // ghost.height)  
    
    manhattan_distance = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    
    if manhattan_distance > 6:
        # If far away, move randomly
        possible_moves = [i for i, can_move in enumerate(ghost.check_ghost_location(level)) if can_move]
        return random.choice(possible_moves) if possible_moves else ghost.direction
    
    if is_scared:
        goal = (len(level[0]) - 1 - goal[0], len(level) - 1 - goal[1])
    
    path = bfs_movement(level, start, goal, is_scared)
    
    if path:
        return path[0]  # Follow the first step of the path
    return ghost.direction
