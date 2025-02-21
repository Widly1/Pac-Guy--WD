# scoreboard.py file 
import pygame
pygame.font.init()
# import os
import json     # for reading in the json file containing the scores.
import time

global my_font
my_font = "assets/fonts/SuperCartoon.ttf"
# my_font = os.path.abspath("assets/fonts/SuperCartoon.ttf")
# my_font = os.path.join(os.getcwd(), "assets/fonts/SuperCartoon.ttf")

def draw_score(screen, score, prev_score, high_score):
    """Draw the score text on the screen."""
    # Defined positions
    outside_x_pos, outside_y_pos = 10, 820
    side_x_pos, side_y_pos = 150, 820
    h_side_x_pos, h_side_y_pos = 320, 820
    
    font_size = 18                 
    font = pygame.font.Font(my_font, font_size)  

    # Create rendered text
    text_score = font.render(f'Score: {score}', True, 'White')  
    text_pscore = font.render(f'Prev. Score: {prev_score}', True, 'White')  
    text_hscore = font.render(f'Highest: {high_score}', True, 'White')  

    # Draw text on screen
    screen.blit(text_score, (outside_x_pos, outside_y_pos))  
    screen.blit(text_pscore, (side_x_pos, side_y_pos))  
    screen.blit(text_hscore, (h_side_x_pos, h_side_y_pos))


# newly added function for loading scores from json file (better formatting + more common)
SCORE_FILE = "highscores.json"

def load_scores():
    """Loads previous and high scores from a file."""
    try:
        with open(SCORE_FILE, "r") as file:
            data = json.load(file)
            return data.get("prev_score", 0), data.get("high_score", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0, 0  # Default scores if file is missing or corrupted

def save_scores(prev_score, high_score):
    """Saves the previous and high score to the file."""
    with open(SCORE_FILE, "w") as file:
        json.dump({"prev_score": prev_score, "high_score": high_score}, file)

    
def show_time(screen, elapsed_time):
    """Draw the timer on the screen."""
    outside_x_pos = 500
    outside_y_pos = 817
    font_size = 25
    font = pygame.font.Font(my_font, font_size)
    
    # # Convert elapsed time to minutes and seconds
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    timer_text = font.render(f'Timer: {minutes:02}: {seconds:02}', True, 'White')
    screen.blit(timer_text, (outside_x_pos, outside_y_pos))


def draw_powerup_event(screen, powered_up, star_img, powered_up_counter):
    outside_x_pos = 670
    outside_y_pos = 806
    powerup_time = 600  # 10 seconds (600 frames at 60 FPS)

    if powered_up:
        flash_threshold = powerup_time // 2  # halfway point (5 secs)
        
        if powered_up_counter >= flash_threshold:  # Only start flashing AFTER halfway
            if (powered_up_counter // 10) % 3  == 0:  # flashing effect
                screen.blit(star_img, (outside_x_pos, outside_y_pos))
        else:
            screen.blit(star_img, (outside_x_pos, outside_y_pos))  # Show normally before flashing


def draw_lives(screen, lives, hearts_img):
    img_height, img_width = 35, 35
    img_padding = 15

    outside_x_pos = 755
    outside_y_pos = 815    

    for i in range(lives):
        screen.blit(pygame.transform.scale(hearts_img, (img_width, img_height)), 
                    (outside_x_pos + i * (img_width + img_padding), outside_y_pos)) # img width + padding, adds space between them

#  newly added function (2.17.25) still need to add game menu

def show_game_over_screen(screen, s_width, s_height):
    new_font = "assets/fonts/RETRO-DISPLAY.ttf"
    
    # show the "Game Over" text
    font = pygame.font.Font(new_font, 100)
    g_o_text = font.render('Game Over', True, (255, 0, 0))  
    screen.blit(g_o_text, (s_width // 2 - g_o_text.get_width() // 2, s_height // 2))

    # show Restart Prompt
    font = pygame.font.Font(my_font, 50)
    restart_text = font.render('Want To Play Again ?', True, (255, 255, 255))  
    screen.blit(restart_text, ((s_width // 2) - (restart_text.get_width() // 2), (s_height // 2) + 90))

    # show "Press Y or R" to restart
    font = pygame.font.Font(my_font, 30)
    instruction_text = font.render('Press Y or R', True, (255, 255, 255))  
    screen.blit(instruction_text, ((s_width // 2) - (instruction_text.get_width() // 2), (s_height // 2) + 130))

    # show  "Press N or SpaceBar" to Quit
    font = pygame.font.Font(my_font, 30)
    quit_text = font.render( 'Press N or SpaceBar to Quit', True, (144, 238, 144))  
    screen.blit(quit_text, ((s_width // 2) - (quit_text.get_width() // 2), (s_height // 2) + 205))


# newly added file (2.20.25) could be deleted soon or tweaked, we'll see
def reset_game(player, ghosts, prev_score, high_score):
    global  powered_up, powered_up_counter, ghosts_eaten, lives, start_time
    powered_up = False
    powered_up_counter = 0
    ghosts_eaten = [False, False, False, False]
    lives = 3
    player.lives = lives
    player.respawn()
    for ghost in ghosts:
        ghost.respawn()
    
    start_time = time.time()  # Reset timer

    prev_score, high_score = load_scores()  # Reload scores