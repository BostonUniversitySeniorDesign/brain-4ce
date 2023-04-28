import pygame
import time
import random
from tkinter import Tk, Label

# Initialize Pygame
pygame.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h


# set display size to fit within screen resolution
width = min(500, screen_width)
height = min(screen_height - 100, 1000)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple 2D Game")

# Set up the colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Set up the player
player_size = 50
player_x = width / 2 - player_size / 2
player_y = height - player_size - 10
player_speed = 0.7

# Set up the game loop
start_time = None
timer_started = False

box_start_time = None
box_timer_started = False
rand_num = height
box_bottom = height/2 - 50
box_top = height/2 - 60 + 0.1*height


font = pygame.font.Font(None, 36)

time_text = "Score: 0"
text = font.render(time_text, True, black)
elapsed_time = 0
box_elapsed_time = 0
total = 0
score = 0

countdown_font = pygame.font.Font(None, 36)
countdown_time = 30
countdown_text = "Time: {:.0f}s".format(countdown_time)
countdown = countdown_font.render(countdown_text, True, black)

countdown_start = time.time()

pygame.draw.rect(screen, 'green', (width/2 - 25, rand_num/2-50, player_size, 0.1*height))
pygame.draw.rect(screen, black, (player_x, player_y, player_size, player_size/2.5))
pygame.display.update()

def gen_rand():
    rand = random.uniform(0, height*2-50)
    if rand > (height*2-50)/2:
        rand += 50
    else:
        rand -= 50
    return int(rand)


while True:

    screen.fill('yellow')

    if time.time() - countdown_start >= 1:
        countdown_time -= 1
        countdown_text = "Time: {}s".format(countdown_time)
        countdown = countdown_font.render(countdown_text, True, black)
        countdown_start = time.time()
        if countdown_time == 0:
            break


    # Display the countdown timer
    screen.blit(countdown, (380, 10))    
    
    # checks if the user tried to quit the window
    if len(pygame.event.get(eventtype=pygame.QUIT)):
        break # ends game
    
    screen.blit(text, (10, 10))

    # Handle player movement

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and  player_y <= height-50/2.5:
        player_y += player_speed

    if player_y >= box_bottom and player_y <= box_top:
        if not timer_started:
            start_time = time.time()
            timer_started = True
        
        elapsed_time = time.time() - start_time + total

        score = int(elapsed_time / 0.5)     

        time_text = "Score: {:.0f}".format(score)
        text = font.render(time_text, True, black)
        screen.blit(text, (10, 10))
    else:
        timer_started = False
        total = elapsed_time

    # Draw the screen
    pygame.draw.rect(screen, red, (width/2 - 25, 0, player_size, height))
    


    if not box_timer_started:
        box_start_time = time.time()

        box_timer_started = True
    
    if box_elapsed_time >= 5:
        rand_num = gen_rand()
        
        box_start_time = time.time()
        box_elapsed_time = 0
        box_top = rand_num/2 - 60 + 0.1*height
        box_bottom = rand_num/2 - 50

    else:
        box_elapsed_time = time.time() - box_start_time

    pygame.draw.rect(screen, 'green', (width/2 - 25, rand_num/2-50, player_size, 0.1*height))
    pygame.draw.rect(screen, black, (player_x, player_y, player_size, player_size/2.5))
    pygame.display.update()

    pygame.display.update()

pygame.quit()

root = Tk()
root.title("Game Over")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 200
window_height = 100
x_pos = (screen_width - window_width) // 2
y_pos = (screen_height - window_height) // 2
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_pos, y_pos))
label = Label(root, text="You finished!")
label.pack()

label2 = Label(root, text="Your final score is " + str(score))
label2.pack()

root.mainloop()    