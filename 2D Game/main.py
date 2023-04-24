import pygame
import time

# Initialize Pygame
pygame.init()

# Set up the display
width = 500
height = 1000
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
player_speed = 1

# Set up the game loop
game_over = False
start_time = None
timer_started = False

font = pygame.font.Font(None, 36)

time_text = "Time: 0.0s"
text = font.render(time_text, True, black)
elapsed_time = 0
total = 0

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
    
    screen.blit(text, (10, 10))

    # Handle player movement

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_x < width - player_size and player_y <= 1000-50/2.5:
        player_y += player_speed

    if player_y >= 400 and player_y <= 390 + 0.1*1000:
        if not timer_started:
            start_time = time.time()
            timer_started = True
        
        elapsed_time = time.time() - start_time + total
        time_text = "Time: {:.1f}s".format(elapsed_time)
        text = font.render(time_text, True, black)
        screen.blit(text, (10, 10))
    else:
        timer_started = False
        total = elapsed_time


            
    if keys[pygame.K_ESCAPE]:
        try:
            event.type = pygame.QUIT
    
        except AttributeError:
            exit(0)

    # Draw the screen
    pygame.draw.rect(screen, red, (width/2 - 25, 0, player_size, 1000))
    pygame.draw.rect(screen, 'green', (width/2 - 25, 400, player_size, 0.1*1000))
    pygame.draw.rect(screen, black, (player_x, player_y, player_size, player_size/2.5))

    pygame.display.update()
    screen.fill('yellow')

    

# Quit Pygame
#pygame.quit()
