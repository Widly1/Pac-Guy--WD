# Ghosts, ghost.py file
import pygame
import math
import random
# from Ai import move_ghost

class Ghost:
    def __init__(self, x, y, target, speed, img, dead_img, edible_img, screen_width, screen_height, id):
        self.x, self.y = x, y
        self.speed = speed
        self.direction = random.choice([0, 1, 2, 3])  # random initial direction (newly added 2/13/25)
        self.img, self.dead_img, self.edible_img = img, dead_img, edible_img
        self.dead, self.is_scared, self.edible = False, False, False
        self.in_cage, self.released = True, False
        self.id, self.target = id, target
        self.path, self.counter = [], 0
        self.initial_x, self.initial_y = x, y
        self.screen_width, self.screen_height = screen_width, screen_height
        self.width, self.height = self.get_ghost_dimensions()
        # newly added (2.13.25, 6:15pm)
        self.hitbox = pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)
        self.is_moving = False
        # newly added (2.16.25)
        self.respawn_timer = 0 
        self.respawn_img = self.img     
    
    def get_ghost_dimensions(self):
        return self.img.get_width(), self.img.get_height()

    def draw(self, screen):
        """Draw the ghost based on its state (scared, dead, or normal)."""
        if self.dead:
            current_img = self.dead_img
        elif self.is_scared:
            current_img = self.edible_img
        else:
            current_img = self.img
        # flip the img based on direction
        if self.direction == 1:  # Left
            current_img = pygame.transform.flip(current_img, True, False)

        screen.blit(current_img, (self.x, self.y))

    # Beyond this point is everything dealing with ghost movements, collision, and location
    
    def check_ghost_location(self, level):
        """Determine which directions are valid for movement."""
        turns = [False, False, False, False]  # [Right, Left, Up, Down]
        num1 = (self.screen_height - 50) // 32  
        num2 = self.screen_width // 30  
        fudge = 3
        # increasing/decreasing this value would allow for more/less space between the ghosts and the walls.
        g_x = self.x + 15
        g_y = self.y + 15
        tile_x = max(0, min((g_x + fudge) // num2, len(level[0]) - 1))
        tile_y = max(0, min((g_y + fudge) // num1, len(level) - 1))
 
        # Checking all 4 directions
        if tile_x + 1 < len(level[0]) and (level[tile_y][tile_x + 1] < 3 or level[tile_y][tile_x + 1] == 9):
            turns[0] = True     # right

        if tile_x - 1 >= 0 and (level[tile_y][tile_x - 1] < 3 or level[tile_y][tile_x - 1] == 9):
            turns[1] = True     # left

        if tile_y - 1 >= 0 and (level[tile_y - 1][tile_x] < 3 or level[tile_y - 1][tile_x] == 9):
            turns[2] = True     # up

        if tile_y + 1 < len(level) and (level[tile_y + 1][tile_x] < 3 or level[tile_y + 1][tile_x] == 9):
            turns[3] = True     # down

        return turns
    
    def is_colliding_with_wall(self, level, next_x, next_y):
        """Check if ghost collides with a wall at the given position."""
        ghost_rect = pygame.Rect(next_x, next_y, self.width, self.height)
        num1 = (self.screen_height - 50) // 32  # Tile height
        num2 = self.screen_width // 30          # Tile width
        
        for i in range(0, self.width, self.width // 2):  # Check left/middle/right
            for j in range(0, self.height, self.height // 2):  # Check top/middle/bottom
                tile_x = (next_x + i) // num2
                tile_y = (next_y + j) // num1
                if level[tile_y][tile_x] >= 3 and level[tile_y][tile_x] != 9:  
                    return True  # Collides with a wall
        return False  
    
    # newly added for respawning ghosts (2.16.25)
    def respawn(self):
         if self.respawn_timer > 0:
            self.respawn_timer -= 1
            self.is_moving = False
            self.in_cage = True
            self.released = False
         else:
            self.dead = False
            self.is_scared = False
            self.released = True
            self.is_moving = True
            self.x, self.y = self.initial_x, self.initial_y
            # self.img = self.respawn_img

    def update(self, level, player, powered_up, powered_up_counter):
        """
        Update ghost movement to be random but ofc handle wall collisions.
        added a player and ghost collision for ghost:
         - call respawn function and be idle if eaten during powerup duration
         - kill pac guy if no powerup is activated
        """
        if self.dead: # respawn ghost if dead
            self.respawn()
            return

        # turn ghost scared if powerup is active, only for a limited time ofc
        if powered_up and powered_up_counter < 600 and not self.dead:
            self.is_scared = True
        else:
            self.is_scared = False

        valid_moves = self.check_ghost_location(level)

        # Mark ghost as released once it leaves the cage
        cage_x_range = (385, 450)  # Approximate x-range of the cage
        cage_y_exit = 295  # Approximate y-position of the gate
        if not self.released and self.y < cage_y_exit and (self.x > cage_x_range[0] and self.x < cage_x_range[1]):
            self.released = True

        # to stop living ghosts from going back into the cage
        if self.released and not self.dead:
            if level[self.y // 32][self.x // 32] == 9:  # Trying to go back into the cage (Gate Tile)
                self.direction = random.choice([0, 1, 2])  # Choose a new direction

        # newly added (2.17.25) 2% chance to pick a new direction at intersections
        if random.random() < 0.02:
            possible_directions = [i for i, can_move in enumerate(valid_moves) if can_move]
            if possible_directions:
                self.direction = random.choice(possible_directions)
        
        # choose a new random direction if the current one is blocked
        if not valid_moves[self.direction]:
            possible_directions = [i for i, can_move in enumerate(valid_moves) if can_move]
            if possible_directions:
                self.direction = random.choice(possible_directions)
            
        # Move the ghost based on the chosen direction
        if self.direction == 0:  # Right
            self.x += self.speed
        elif self.direction == 1:  # Left
            self.x -= self.speed
        elif self.direction == 2:  # Up
            self.y -= self.speed
        elif self.direction == 3:  # Down
            self.y += self.speed
        
        self.is_moving = True
        
        # check for collision with pac guy
        if self.hitbox.colliderect(player.hitbox):
            if self.is_scared:  
                self.dead = True            # If scared, ghost gets eaten and respawns
                self.respawn_timer = 240     #  4 sec respawn time inside cage
                self.is_moving = False
            else:
                player.lost_life()  # If not scared, pac guy loses a life
        # then we update hitbox after moving
        self.hitbox = pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)