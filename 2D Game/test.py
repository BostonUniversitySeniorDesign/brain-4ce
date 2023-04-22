import pygame

pygame.init()

# Set up the window and screen surface
window_width = 640
window_height = 480
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pygame Text Demo")

# Set up the font
font_size = 36
font = pygame.font.Font(None, font_size)

# Render the text
text = font.render("Hello, World!", True, (255, 255, 255))

# Blit the text onto the screen surface
text_rect = text.get_rect()
text_rect.center = (window_width // 2, window_height // 2)
screen.blit(text, text_rect)

# Update the display
pygame.display.flip()

# Wait for the user to close the window
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

pygame.quit()
