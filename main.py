# main.py, main game file
import pygame
from player import Player
from game_map import GameMap
from movement import check_location, handle_collisions_and_powerups, check_collision_man_ghost
from scoreboard import draw_score, draw_lives, draw_powerup_event, show_time, show_game_over_screen, save_scores, load_scores, reset_game
from ghost import Ghost
import copy
import time

# Screen dimensions
s_width = 900
s_height = 850
# Cell dimensions
num1 = (s_height - 50) // 32  # Cell height
num2 = s_width // 30  # Cell width

# Initialize player
player_images = [pygame.transform.scale(pygame.image.load(f'assets/images/player_images/{i}.png'), (34, 34)) for i in range(1, 4)]
player = Player(x = 430, y = 595, speed = 2, images = player_images, lives = 3)
counter = 0

# Initialize ghosts
greeny_image = pygame.transform.scale(pygame.image.load("assets/images/ghosts/1.png"), (29, 29))
pinky_image = pygame.transform.scale(pygame.image.load("assets/images/ghosts/2.png"), (33, 33))
blinky_image = pygame.transform.scale(pygame.image.load("assets/images/ghosts/3.png"), (33, 33))
cyanky_image = pygame.transform.scale(pygame.image.load("assets/images/ghosts/4.png"), (33, 33))

# Edible or Dead Ghosts
edible_img = pygame.transform.scale(pygame.image.load("assets/images/ghosts/edible.png"), (48, 48))
dead_img = pygame.transform.scale(pygame.image.load("assets/images/ghosts/eyes-dead.png"), (40, 40))

# Creating ghost objects
ghosts = [
    Ghost(x = 434, y = 350, target = player, speed = 2, img = blinky_image, dead_img = dead_img, edible_img= edible_img, screen_width = s_width, screen_height = s_height, id = "blinky"),
    Ghost(x = 400, y = 392, target = player, speed = 2, img = greeny_image, dead_img = dead_img, edible_img= edible_img, screen_width = s_width, screen_height = s_height, id = "greeny"),
    Ghost(x = 400, y = 360, target = player, speed = 2, img = pinky_image, dead_img = dead_img, edible_img= edible_img, screen_width = s_width, screen_height = s_height, id = "pinky"),
    Ghost(x = 445, y = 360, target = player, speed = 2, img = cyanky_image, dead_img = dead_img, edible_img= edible_img, screen_width = s_width, screen_height = s_height, id = "cyanky")
]


# Star (power-up) indicator
star_img = pygame.image.load("assets/images/extras/star.png")
star_img = pygame.transform.scale(star_img, (53, 53))

# Lives indicator
hearts_img = pygame.image.load("assets/images/extras/lives.png")
hearts_img = pygame.transform.scale(hearts_img, (35, 35))

def main():
    pygame.init()
    screen = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption("W Pac-Guy")
    clock = pygame.time.Clock()

    score = 0  # Initialize score
    prev_score, high_score = load_scores()  # load scores when game begins

    powered_up = False
    powered_up_counter = 0
    ghosts_eaten = [False, False, False, False]
    lives = 3
    player.lives = lives
   
    game_map = GameMap(s_width, s_height)   # map for gameplay
    og_game_map = GameMap(s_width, s_height)    # map for reset (new game)
    frame_counter = 0  #will be used for something sooner or later

    start_time = time.time()

    run = True
    while run:
        clock.tick(60)  # Cap the frame rate
        frame_counter += 1  # Increment frame counter
        
        elapsed_time = time.time() - start_time

        screen.fill((0, 0, 0))

        # Draw player and game map
        player.draw(screen)
        game_map.draw(screen, frame_counter, flashing=True)

        # Player collision and movement logic
        player_width, player_height = player.get_dimensions()
        c_x = player.x + player_width // 2
        c_y = player.y + player_height // 2

        valid_turns = check_location(c_x, c_y, game_map.level, player.direction, s_width, s_height)
        player.move(valid_turns)

        # Handle collisions and powerups
        score, powered_up, powered_up_counter, ghosts_eaten = handle_collisions_and_powerups(
            c_x, c_y, game_map.level, num1, num2, score, powered_up, powered_up_counter, ghosts_eaten
        )

        score, collision = check_collision_man_ghost(player, ghosts, score, ghosts_eaten)

        # Draw UI elements
        draw_lives(screen, player.lives, hearts_img)
        draw_score(screen, score, prev_score, high_score)
        draw_powerup_event(screen, powered_up, star_img, powered_up_counter)
        show_time(screen, elapsed_time)

        for ghost in ghosts:
            ghost.draw(screen)  # Draw each ghost
            ghost.update(game_map.level, player, powered_up, powered_up_counter)
        
        
        # show the game over text and let the user restart or close the game 
        if player.lives <= 0:
            # first save the scores
            prev_score = score
            high_score = max(high_score, score)
            save_scores(prev_score, high_score)
            # then show game options during game-over sequence
            show_game_over_screen(screen, s_width, s_height)
            player.is_moving = False
            player.respawn()
            start_time = time.time()
            elapsed_time = 0
 
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.update_direction(0)
                    player.is_moving = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.update_direction(1) 
                    player.is_moving = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.update_direction(2)
                    player.is_moving = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.update_direction(3)
                    player.is_moving = True
                elif event.key == pygame.K_SPACE or event.key == pygame.K_n:
                    run = False
                elif event.key == pygame.K_y or event.key == pygame.K_r:  # to restart and reset game attributes
                    reset_game(player, ghosts, prev_score, high_score)
                    game_map = copy.deepcopy(og_game_map)  # reset gamemap by reinitializing it with the og_game_map     
                    score = 0
        """ 
        Screen wrapping logic for pacman and ghosts
        doesn't work well in functions for some reason
        """
        if player.x > s_width:  
            player.x = -47  # Wrap to the left
        elif player.x < -50:  
            player.x = s_width - 11  # Wrap to the right
        
        for ghost in ghosts:
            if ghost.x > s_width:  
                ghost.x = -47  
            elif ghost.x < -50:  
                ghost.x = s_width - 11 
        
        # Update display
        pygame.display.flip()

    pygame.quit()
main()