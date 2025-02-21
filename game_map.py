# GameMap (game_map.py) File
import pygame
import math
# from mazes import maze
import copy

class GameMap:
    def __init__(self, screen_width, screen_height, color='blue'):
        from mazes import maze
        self.level = copy.deepcopy(maze)  # working maze copy (for gameplay)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = color
        self.num1 = (screen_height - 50) // 32  # Cell height
        self.num2 = screen_width // 30  # Cell width
        self.pi = math.pi

    def draw(self, screen, frame_counter ,flashing=False):
        """Draw the entire map."""
        for row_index, row in enumerate(self.level):
            for col_index, cell in enumerate(row):
                self._draw_cell(screen, row_index, col_index, cell, flashing, frame_counter)
    
    def _draw_cell(self, screen, row, col, cell, flashing, frame_counter):
        """Draw an individual cell based on its type."""
        x_center = col * self.num2 + (0.5 * self.num2)
        y_center = row * self.num1 + (0.5 * self.num1)

        if cell == 1:  # Small dots
            pygame.draw.circle(screen, 'white', (x_center, y_center), 3)
        elif cell == 2:  # Power-ups with flashing effect
            if flashing:  # Only flash if 'flashing' is True
                if frame_counter % 50 < 15:  # Flash every 30 frames = 0.5 secs
                    pygame.draw.circle(screen, 'white', (x_center, y_center), 9)
            else:
                pygame.draw.circle(screen, 'white', (x_center, y_center), 9)

        elif cell == 3:  # Vertical line
            pygame.draw.line(screen, self.color, 
                             (x_center, row * self.num1), 
                             (x_center, row * self.num1 + self.num1), 3)
        elif cell == 4:  # Horizontal line
            pygame.draw.line(screen, self.color, 
                             (col * self.num2, y_center), 
                             (col * self.num2 + self.num2, y_center), 3)
        elif cell == 5:  # Top-right arc
            pygame.draw.arc(screen, self.color, 
                            [col * self.num2 - (self.num2 * 0.4) - 2, y_center, self.num2, self.num1], 
                            0, self.pi / 2, 3)
        elif cell == 6:  # Top-left arc
            pygame.draw.arc(screen, self.color, 
                            [col * self.num2 + (self.num2 * 0.5), y_center, self.num2, self.num1], 
                            self.pi / 2, self.pi, 3)
        elif cell == 7:  # Bottom-left arc
            pygame.draw.arc(screen, self.color, 
                            [col * self.num2 + (self.num2 * 0.5), row * self.num1 - (0.4 * self.num1), self.num2, self.num1], 
                            self.pi, 3 * self.pi / 2, 3)
        elif cell == 8:  # Bottom-right arc
            pygame.draw.arc(screen, self.color, 
                            [col * self.num2 - (self.num2 * 0.4) - 2, row * self.num1 - (0.4 * self.num1), self.num2, self.num1], 
                            3 * self.pi / 2, 2 * self.pi, 3)
        elif cell == 9:  # Cage door
            pygame.draw.line(screen, 'white', 
                             (col * self.num2, y_center), 
                             (col * self.num2 + self.num2, y_center), 3)