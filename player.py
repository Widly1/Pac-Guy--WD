# Player (player.py) File
import pygame
import math

class Player:
    def __init__(self, x, y, speed, images, lives):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = 0
        self.counter = 0
        self.images = images
        self.is_moving = False
        self.width, self.height = self.get_dimensions()
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.lives = lives
        self.dead = False
        self.initial_x, self.initial_y, self.initial_direction = x, y, self.direction

    def get_dimensions(self):
        """get the player width and height from the images"""
        return self.images[0].get_width(), self.images[0].get_height()

    def draw(self, screen):
        """Draw the player based on its direction and animate."""
        self.counter += 1  # Increment animation frame counter

        if self.direction == 0:
            screen.blit(self.images[(self.counter // 7) % len(self.images)], (self.x, self.y))
        elif self.direction == 1:
            screen.blit(pygame.transform.flip(self.images[(self.counter // 7) % len(self.images)], True, False), (self.x, self.y))
        elif self.direction == 2:
            screen.blit(pygame.transform.rotate(self.images[(self.counter // 7) % len(self.images)], 90), (self.x, self.y))
        elif self.direction == 3:
            screen.blit(pygame.transform.rotate(self.images[(self.counter // 7) % len(self.images)], 270), (self.x, self.y))

    def move(self, valid_turns):
        if not self.is_moving: # This allows pacman to be stationary as soon as the game starts
            return              
        """Move the player in the current direction if the move is valid."""
        if self.direction == 0 and valid_turns[0]:  # Right
            self.x += self.speed
        elif self.direction == 1 and valid_turns[1]:  # Left
            self.x -= self.speed
        elif self.direction == 2 and valid_turns[2]:  # Up
            self.y -= self.speed
        elif self.direction == 3 and valid_turns[3]:  # Down
            self.y += self.speed
            
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_direction(self, new_direction):
        """Update the player's direction."""
        self.direction = new_direction

    def lost_life(self):
        if self.lives > 0: # as long as we have more than 0 lives, respawn pacman location
            self.lives -= 1
            self.dead = True
            self.respawn()     # respawn pac guy
            self.is_moving = False                              # make pac guy still after respawning 
            self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def respawn(self):
        self.x, self.y = self.initial_x, self.initial_y
        self.is_moving = False 
        self.initial_direction = 0
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)