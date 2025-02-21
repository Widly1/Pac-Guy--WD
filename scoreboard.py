# scoreboard.py file 
import pygame
pygame.font.init()
import os

global my_font
my_font = "assets/fonts/SuperCartoon.ttf"
# my_font = os.path.abspath("assets/fonts/SuperCartoon.ttf")
# my_font = os.path.join(os.getcwd(), "assets/fonts/SuperCartoon.ttf")

def draw_score(screen, score, prev_score, high_score):
    """Draw the score text on the screen."""
    outside_x_pos = 10
    outside_y_pos = 820
    font_size = 18                 
    # Load the custom font
    font = pygame.font.Font( my_font, font_size)                # Using the custom font
    text_score = font.render(f'Score: {score}', True, 'White')  # create the score
    screen.blit(text_score, (outside_x_pos, outside_y_pos))  # Draw the score text on the screen at the given position
    
    side_x_pos = 150
    side_y_pos = 820
    s_font_size = 18  
    font = pygame.font.Font( my_font, s_font_size) 
    text_pscore = font.render(f'Prev.Score: {prev_score}', True, 'White')  
    screen.blit(text_pscore, (side_x_pos, side_y_pos))  

    h_side_x_pos = 320
    h_side_y_pos = 820
    h_font_size = 18
    font = pygame.font.Font( my_font, h_font_size)
    text_hscore = font.render(f'Highest: {high_score}', True, 'White')  
    screen.blit(text_hscore, (h_side_x_pos, h_side_y_pos))  
    
    
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
    global game_over 
    new_font = "assets/fonts/RETRO-DISPLAY.ttf"
    
    # Display Game Over text
    font = pygame.font.Font(new_font, 100)
    g_o_text = font.render('Game Over', True, (255, 0, 0))  
    screen.blit(g_o_text, (s_width // 2 - g_o_text.get_width() // 2, s_height // 2))

    # Display Restart Prompt
    font = pygame.font.Font(my_font, 50)
    restart_text = font.render('Want To Play Again ?', True, (255, 255, 255))  
    screen.blit(restart_text, ((s_width // 2) - (restart_text.get_width() // 2), (s_height // 2) + 90))

    # Display "Press Y or R" to restart
    font = pygame.font.Font(my_font, 30)
    instruction_text = font.render('Press Y or R', True, (255, 255, 255))  
    screen.blit(instruction_text, ((s_width // 2) - (instruction_text.get_width() // 2), (s_height // 2) + 130))

    # Display "Press N or SpaceBar" to Quit
    font = pygame.font.Font(my_font, 30)
    quit_text = font.render( 'Press N or SpaceBar to Quit', True, (144, 238, 144))  
    screen.blit(quit_text, ((s_width // 2) - (quit_text.get_width() // 2), (s_height // 2) + 205))