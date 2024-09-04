import pygame
from pygame.locals import *
from pygame import mixer

# Initialize Pygame and the mixer for sound
pygame.init()
mixer.init()

# Screen settings
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Timer Rectangle')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FILL_COLOR = (255, 0, 0)  # Red color for the filling rectangle

# Font settings
pygame.font.init()
font = pygame.font.SysFont('Arial', 40)
button_font = pygame.font.SysFont('Arial', 30)
input_font = pygame.font.SysFont('Arial', 40)

# Timer settings
total_time = 0  # This will be set based on input
start_time = 0  # Will be set when the timer starts
timer_started = False

# Load the sound but don't play it immediately
try:
    mixer.music.load(r'C:\Users\corey\Downloads\mystic-logo-13493.mp3')
except pygame.error as e:
    print(f"Failed to load sound: {e}")

# Flag to indicate whether the music has been played
music_played = False

# Input box settings for minutes and seconds
input_box_minutes = pygame.Rect(screen_width // 2 - 120, screen_height // 2 - 60, 80, 50)
input_box_seconds = pygame.Rect(screen_width // 2 + 40, screen_height // 2 - 60, 80, 50)
input_minutes = ''
input_seconds = ''

# Start button settings
button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 20, 150, 50)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                minutes = int(input_minutes) if input_minutes.isdigit() else 0
                seconds = int(input_seconds) if input_seconds.isdigit() else 0

                total_time = minutes * 60 + seconds

                if total_time > 0:  # Ensure total_time is not zero
                    start_time = pygame.time.get_ticks()
                    timer_started = True
                    music_played = False
            elif input_box_minutes.collidepoint(event.pos):
                active_box = 'minutes'
            elif input_box_seconds.collidepoint(event.pos):
                active_box = 'seconds'
            else:
                active_box = None
        elif event.type == KEYDOWN:
            if active_box == 'minutes':
                if event.key == K_BACKSPACE:
                    input_minutes = input_minutes[:-1]
                elif event.unicode.isdigit():
                    input_minutes += event.unicode
            elif active_box == 'seconds':
                if event.key == K_BACKSPACE:
                    input_seconds = input_seconds[:-1]
                elif event.unicode.isdigit():
                    input_seconds += event.unicode

    # Clear the screen
    screen.fill(WHITE)

    if timer_started:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds
        time_left = max(0, total_time - int(elapsed_time))

        # Calculate drain percentage
        if total_time > 0:
            drain_percentage = min(elapsed_time / total_time, 1)  # Ensure percentage stays within 0 to 1
        
            # Rectangle size calculation
            rect_height = int(screen_height * (1 - drain_percentage))  # Drain from the top
            rect_top = screen_height - rect_height  # Start emptying from the top

            # Draw the drained portion of the rectangle
            pygame.draw.rect(screen, FILL_COLOR, (0, rect_top, screen_width, rect_height))

        # Render and display the timer text
        timer_text = font.render(str(time_left), True, BLACK)
        screen.blit(timer_text, (screen_width // 2 - timer_text.get_width() // 2, 50))  # Display above the rectangle

        if elapsed_time >= total_time:
            if not music_played:
                try:
                    mixer.music.play()  # Play the music when the timer ends
                except pygame.error as e:
                    print(f"Failed to play sound: {e}")
                music_played = True
            timer_started = False
    else:
        # Draw the input boxes for minutes and seconds
        pygame.draw.rect(screen, BLACK, input_box_minutes, 2)
        text_surface_minutes = input_font.render(input_minutes, True, BLACK)
        screen.blit(text_surface_minutes, (input_box_minutes.x + 5, input_box_minutes.y + 5))

        pygame.draw.rect(screen, BLACK, input_box_seconds, 2)
        text_surface_seconds = input_font.render(input_seconds, True, BLACK)
        screen.blit(text_surface_seconds, (input_box_seconds.x + 5, input_box_seconds.y + 5))
        
        # Draw labels for minutes and seconds
        minutes_label = button_font.render('Minutos', True, BLACK)
        seconds_label = button_font.render('Segundos', True, BLACK)
        screen.blit(minutes_label, (input_box_minutes.x, input_box_minutes.y - 30))
        screen.blit(seconds_label, (input_box_seconds.x, input_box_seconds.y - 30))
        
        # Draw the start button
        pygame.draw.rect(screen, BLACK, button_rect)
        button_text = button_font.render('Empezar', True, WHITE)
        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

    # Update the display
    pygame.display.flip()

# Quit Pygame and stop the music
mixer.music.stop()
pygame.quit()
