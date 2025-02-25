# scoreboard.py file 
import pygame
pygame.font.init()
# import os
import json     # for reading in the json file containing the scores.
import time

global my_font
my_font = "assets/fonts/SuperCartoon.ttf"

def draw_score(screen, score, prev_score, high_score):
    """Draw the score text on the screen."""
    # positions
    outside_x_pos, outside_y_pos = 10, 820
    side_x_pos, side_y_pos = 150, 820
    h_side_x_pos, h_side_y_pos = 320, 820
    
    font_size = 18                 
    font = pygame.font.Font(my_font, font_size)  

    # create text
    text_score = font.render(f'Score: {score}', True, 'White')  
    text_pscore = font.render(f'Prev. Score: {prev_score}', True, 'White')  
    text_hscore = font.render(f'Highest: {high_score}', True, 'White')  

    # Draw text on screen
    screen.blit(text_score, (outside_x_pos, outside_y_pos))  
    screen.blit(text_pscore, (side_x_pos, side_y_pos))  
    screen.blit(text_hscore, (h_side_x_pos, h_side_y_pos))


# newly added (2.21.25) function for saving and loading scores from json file (better formatting + more common)
SCORE_FILE = "highscores.json"

def load_scores():
    """Loads previous and high scores from a file."""
    try:
        with open(SCORE_FILE, "r") as file:
            data = json.load(file)
            return data.get("prev_score", 0), data.get("high_score", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0, 0  # blank or default scores if file is missing or damaged

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


# newly (2.21.25) added function for resetting the game
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


# newly added (2.22.25) function for pausing or continuing the game 
def paused_screen(screen):
    """ show a pause menu with 'Continue' and 'Quit' buttons """
    font = pygame.font.Font(my_font, 60)
    button_font = pygame.font.Font(my_font, 50)

    # show "Paused" text
    text = font.render("GAME PAUSED", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))  # positions the text in the center of the screen

    # button rectangles creation (the words will be inside of these rects)
    button_width, button_height = 210, 70
    
    # create two rectangular button areas, "continue" and "quit" 
    # subtract 100 from screen.get_width() // 2 to shift the buttons to center it
    # screen.get_width() // 2 alone would only place the left edge of the buttons at the center of the screen
    
    continue_button = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 40, button_width, button_height) 
    quit_button = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 50, button_width, button_height)

    # creating the transparent dark overlay to darken the game screen
    transparent_bg = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    transparent_bg.fill((0, 0, 0, 180)) 

    # now draw the actual buttons (blue for "Continue", red for "Quit") inside the transparent background
    pygame.draw.rect(transparent_bg, (0, 125, 255), continue_button, border_radius=15) 
    pygame.draw.rect(transparent_bg, (255,0,0), quit_button, border_radius=15)

    # create the texts
    continue_text = button_font.render("Continue", True, (255, 255, 255))
    quit_text = button_font.render("Quit", True, (255, 255, 255))

    # now position the button texts inside the buttons (rectangles created earlier)
    continue_text_rect = continue_text.get_rect(center = continue_button.center)
    quit_text_rect = quit_text.get_rect(center = quit_button.center)

    # now draw everything
    screen.blit(transparent_bg, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(continue_text, continue_text_rect)
    screen.blit(quit_text, quit_text_rect)
    pygame.display.flip()

    return continue_button, quit_button  # return buttons for user interaction

# newly added (2.22.25) function for winning the game showing a "You Win" message 
# allowing player to choose from "restart" or "quit" 
# reused code from paused menu
def you_win(screen, prev_score, high_score):
    font = pygame.font.Font(my_font, 85)
    button_font = pygame.font.Font(my_font, 19)


    text = font.render("YOU WIN !!", True, (255, 215, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))  # positions the text in the center of the screen

    # button rectangles creation (the words will be inside of these rects)
    button_width, button_height = 220, 60
    
    restart_button = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 40, button_width, button_height) 
    quit_button = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 50, button_width, button_height)

    # creating the transparent dark overlay to darken the game screen
    transparent_bg = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    transparent_bg.fill((0, 0, 0, 180)) 

    pygame.draw.rect(transparent_bg, (0, 128, 0), restart_button, border_radius=15) 
    pygame.draw.rect(transparent_bg, (255,0,0), quit_button, border_radius=15)

    # create the texts
    restart_text = button_font.render("Restart ", True, (255, 255, 255))
    quit_text = button_font.render("Quit ", True, (255, 255, 255))

    restart_text_rect = restart_text.get_rect(center = restart_button.center)
    quit_text_rect = quit_text.get_rect(center = quit_button.center)

    screen.blit(transparent_bg, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(restart_text, restart_text_rect)
    screen.blit(quit_text, quit_text_rect)
    pygame.display.flip()

    save_scores(prev_score, high_score)     # save the scores
    prev_score, high_score = load_scores()  # Reload scores (will be useful in main.py
    return restart_button, quit_button  # return buttons for user interaction