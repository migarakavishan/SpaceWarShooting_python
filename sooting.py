import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space War")

# Load images
background_img = pygame.image.load("background.png")
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")
menu_background_img = pygame.image.load("menu_background.png")
game_over_background_img = pygame.image.load("game_over_background.png")

# Scale images
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 30))
menu_background_img = pygame.transform.scale(menu_background_img, (WIDTH, HEIGHT))
game_over_background_img = pygame.transform.scale(game_over_background_img, (WIDTH, HEIGHT))

# Set up the player
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 70, 50, 50)
player_speed = 5

# Set up bullets
bullets = []

# Set up the enemy
enemies = []

# Set up font for UI
font = pygame.font.SysFont(None, 36)

# Set up score
score = 0

# Set up game state
state = "menu"

# Clock to control the frame rate
clock = pygame.time.Clock()

# Function to reset game variables
def reset_game():
    global player, bullets, enemies, score
    player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 70, 50, 50)
    bullets = []
    enemies = []
    score = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Menu state
    if state == "menu":
        screen.blit(menu_background_img, (0, 0))
        start_text = font.render("Press SPACE to start", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - 150, HEIGHT // 2))

        if keys[pygame.K_SPACE]:
            state = "playing"
            reset_game()

    # Playing state
    elif state == "playing":
        # Move player
        if keys[pygame.K_LEFT] and player.x - player_speed > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x + player_speed + player.width < WIDTH:
            player.x += player_speed

        # Shoot bullets
        if keys[pygame.K_SPACE]:
            bullet = pygame.Rect(player.x + player.width // 2 - 5, player.y, 10, 30)
            bullets.append(bullet)

        # Move bullets
        for bullet in bullets:
            bullet.y -= 10
            if bullet.y < 0:
                bullets.remove(bullet)

        # Create enemies
        if random.randint(0, 100) < 5:
            enemy = pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50)
            enemies.append(enemy)

        # Move enemies
        for enemy in enemies:
            enemy.y += 5
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                score -= 10  # Deduct score for each missed enemy

        # Check for collisions between bullets and enemies
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 20  # Increase score for each hit enemy

        # Check for collisions between player and enemies
        for enemy in enemies:
            if player.colliderect(enemy):
                state = "game_over"

        # Draw everything
        screen.blit(background_img, (0, 0))
        screen.blit(player_img, player)

        for bullet in bullets:
            screen.blit(bullet_img, bullet)

        for enemy in enemies:
            screen.blit(enemy_img, enemy)

        # Draw UI
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    # Game over state
    elif state == "game_over":
        screen.blit(game_over_background_img, (0, 0))
        game_over_text = font.render(f"Game Over - Your Score: {score}", True, WHITE)
        restart_text = font.render("Press R to restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 30))
        screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 30))

        if keys[pygame.K_r]:
            state = "playing"
            reset_game()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
