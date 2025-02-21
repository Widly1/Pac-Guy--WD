# movement.py 
import pygame
from game_map import GameMap

def check_location(c_x, c_y, level, direction, screen_width, screen_height):
    turns = [False, False, False, False]  # [Right, Left, Up, Down]
    num1 = (screen_height - 50) // 32  # Tile height
    num2 = screen_width // 30  # Tile width
    fudge = 13 
    # adjusts for slight overlaps to smooth movement near boundaries.
    # increasing/decreasing this value would allow for more/less space between the player and the walls.

    # Wrap-around for horizontal movement
    if c_x < 0:  
        c_x = screen_width - num2  # Wrap to right side
    elif c_x >= screen_width:  
        c_x = 0  # Wrap to left side

    # Ensure c_x and c_y remain within valid map indices
    tile_x = (c_x + fudge) // num2 % len(level[0])  # used modulo to prevents out-of-bounds errors 4 the array
    tile_y = (c_y + fudge) // num1 % len(level)  

    # Check Right movement
    if direction == 0 and level[c_y // num1][tile_x] < 3:
        turns[0] = True

    # Check Left movement
    if direction == 1 and level[c_y // num1][(c_x - fudge) // num2 % len(level[0])] < 3:
        turns[1] = True

    # Check Up movement
    if direction == 2 and level[(c_y - fudge) // num1 % len(level)][c_x // num2] < 3:
        turns[2] = True

    # Check Down movement
    if direction == 3 and level[(c_y + fudge) // num1 % len(level)][c_x // num2] < 3:
        turns[3] = True

    return turns


def calculate_map_cell_dimensions(screen_width, screen_height):
    num1 = (screen_height - 50) // 32  # {Cell} height
    num2 = screen_width // 30  # {Cell} width
    return num1, num2

def handle_collisions_and_powerups(c_x, c_y, level, num1, num2, score, powered_up, powered_up_counter, eaten_ghosts):
    # Collision with regular dots
    """
    ✰ c_x // num2:
        -  gives us the tile index in the map by converting the pixel coordinate
    ✰ min(c_x // num2, len(level[0]) - 1):
        - grid_x doesn’t go beyond the right edge of the map.
        - len(level[0]) - 1 is the maximum valid column index in the 2D level array.
    ✰ max(0, min(...)): 
        - grid_x doesn’t go below 0, preventing negative indexing
    ✰ Overall: 
        - level[grid_y][grid_x] makes sure accessing  grid_x and grid_y always stays between 0 and the last row/column index.
        - preventing any crash when trying to wrap around screen 
    ^^^ same logic for grid_y 
    """
    grid_x = max(0, min(c_x // num2, len(level[0]) - 1))  
    grid_y = max(0, min(c_y // num1, len(level) - 1))

    # now we correctly access level[grid_y][grid_x]
    if level[grid_y][grid_x] == 1:
        score += 10
        level[grid_y][grid_x] = 0  # Remove dot after eating

    # Collision with power-up dots
    elif level[grid_y][grid_x] == 2:
        score += 50
        powered_up = True
        powered_up_counter = 0
        eaten_ghosts = [False, False, False, False]
        level[grid_y][grid_x] = 0  # Remove power pellet after eating

    # Power-up timer logic
    if powered_up:
        if powered_up_counter < 600:
            powered_up_counter += 1
        else:
            powered_up = False
            powered_up_counter = 0
            eaten_ghosts = [False, False, False, False]

    return score, powered_up, powered_up_counter, eaten_ghosts

def check_collision_man_ghost(player, ghosts, score, eaten_ghosts):
    """
    Check if the player collides with any ghost.
    If the ghost is scared, it gets eaten and the player gets extra points
    If the ghost is normal, the player loses a life.
    """
    for i, ghost in enumerate(ghosts):
        if player.hitbox.colliderect(ghost.hitbox):
            if ghost.is_scared and not eaten_ghosts[i]:
                ghost.dead = True    # ghost is eaten, respawn it
                score += 600         # bonus points for eating a ghost
                ghost.respawn()
                ghost.img = ghost.respawn_img  
                eaten_ghosts[i] = True 
            elif not ghost.is_scared:
                player.lost_life()
            return score, True  # Collision happened
    return score, False  # No collision