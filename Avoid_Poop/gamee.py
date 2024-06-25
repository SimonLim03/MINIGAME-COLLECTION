import random
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Enhanced Game")
clock = pygame.time.Clock()

# Load images
background = pygame.image.load("background.png")
character = pygame.image.load("kid.png")
enemy_image = pygame.image.load("enemy.png")

# Load sounds
try:
    pygame.mixer.init()
    game_over_sound = pygame.mixer.Sound("game_over.wav")  # Ensure you have a 'game_over.wav' file
except Exception as e:
    print("Error loading sound: ", e)

# Character setup
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height
character_speed = 10
to_x = 0
lives = 3  # Number of lives the character has

# Enemies setup
enemies = []
enemy_speed = 7  

def add_enemy():
    enemies.append({
        "x_pos": random.randint(0, screen_width - ddong_width),
        "y_pos": 0,
        "speed": enemy_speed
    })

ddong_width = enemy_image.get_rect().size[0]
ddong_height = enemy_image.get_rect().size[1]
add_enemy()  # Add the first enemy

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Countdown before the game starts
def countdown():
    countdown_font = pygame.font.SysFont(None, 72)
    for i in range(3, 0, -1):
        screen.blit(background, (0, 0))
        countdown_text = countdown_font.render(str(i), True, (255, 255, 255))
        text_rect = countdown_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(countdown_text, text_rect)
        pygame.display.update()
        pygame.time.wait(1000)

countdown()

# Game loop
running = True
while running:
    dt = clock.tick(30)  # FPS
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    # Update character position
    character_x_pos += to_x * dt / 10
    character_x_pos = max(0, min(screen_width - character_width, character_x_pos))

    # Update enemies
    for enemy in enemies:
        enemy['y_pos'] += enemy['speed'] * dt / 10
        if enemy['y_pos'] > screen_height:
            enemy['y_pos'] = 0
            enemy['x_pos'] = random.randint(0, screen_width - ddong_width)
            score += 10  # Increase score when dodging an enemy

    # Check for collisions
    character_rect = character.get_rect(topleft=(character_x_pos, character_y_pos))
    for enemy in enemies:
        enemy_rect = enemy_image.get_rect(topleft=(enemy['x_pos'], enemy['y_pos']))
        if character_rect.colliderect(enemy_rect):
            lives -= 1
            if lives <= 0:
                game_over_sound.play()
                print("GAME OVER")
                pygame.time.wait(2000)  # Wait two seconds after game over
                running = False
            enemy['y_pos'] = 0  # Reset enemy position

    # Draw everything
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    for enemy in enemies:
        screen.blit(enemy_image, (enemy['x_pos'], enemy['y_pos']))
    score_text = font.render(f"Score: {score} Lives: {lives}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()