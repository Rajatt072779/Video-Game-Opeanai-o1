import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ICON_SIZE = 40
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BG = (18, 18, 18)
FPS = 60

# Load images and resize them
koala_img = pygame.image.load("koala.webp")
koala_img = pygame.transform.scale(koala_img, (ICON_SIZE, ICON_SIZE))

strawberry_img = pygame.image.load("strawberry.jpg")
strawberry_img = pygame.transform.scale(strawberry_img, (ICON_SIZE, ICON_SIZE))

squirrel_img = pygame.image.load("squirrel.jpeg")
squirrel_img = pygame.transform.scale(squirrel_img, (ICON_SIZE, ICON_SIZE))

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Squirrel Finder')

# Font settings
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Timer setup
start_ticks = pygame.time.get_ticks()

# Classes
class Koala(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = koala_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep the koala on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Strawberry(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = strawberry_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - ICON_SIZE), 
                             random.randint(0, SCREEN_HEIGHT - ICON_SIZE))
        self.speed_x = random.choice([-speed, speed])
        self.speed_y = random.choice([-speed, speed])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce the strawberry off the screen edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

class Squirrel(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = squirrel_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - ICON_SIZE), 
                             random.randint(0, SCREEN_HEIGHT - ICON_SIZE))
        self.speed_x = random.choice([-speed, speed])
        self.speed_y = random.choice([-speed, speed])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce the squirrel off the screen edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

# Display instructions
def show_instructions():
    screen.fill(DARK_BG)
    title_text = font.render("Squirrel Finder", True, WHITE)
    instructions = small_font.render("Avoid the strawberries and find the squirrel!", True, WHITE)
    start_text = small_font.render("Press any key to start...", True, WHITE)

    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

    pygame.display.flip()
    wait_for_key()

# Wait for key press
def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Main game loop
def game(win_count):
    koala = Koala()
    strawberries = []
    squirrel_speed = 3 + win_count  # Squirrel speed increases every round
    strawberry_speed = 4 + win_count  # Strawberry speed increases every round

    all_sprites = pygame.sprite.Group()

    # Generate initial number of strawberries (4-6) and increase number by 3-4 each round
    num_strawberries = random.randint(4, 6) + win_count * random.randint(3, 4)

    for _ in range(num_strawberries):
        strawberry = Strawberry(strawberry_speed)
        strawberries.append(strawberry)
        all_sprites.add(strawberry)

    squirrel = Squirrel(squirrel_speed)
    all_sprites.add(squirrel)

    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update Koala separately (since it needs key input)
        keys = pygame.key.get_pressed()
        koala.update(keys)

        # Update other sprites (strawberries and squirrel) without keys
        all_sprites.update()

        # Check for collisions with any strawberry
        for strawberry in strawberries:
            if pygame.sprite.collide_rect(koala, strawberry):
                game_over = True
                result = "You Died!"
                break

        # Check for collision with squirrel
        if not game_over and pygame.sprite.collide_rect(koala, squirrel):
            game_over = True
            result = "You Win!"
            win_count += 1  # Increase win count after each win

        # Drawing
        screen.fill(DARK_BG)
        screen.blit(koala.image, koala.rect)  # Manually draw koala
        all_sprites.draw(screen)

        # Display timer
        time_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        timer_text = font.render(f"Time: {time_passed}s", True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

        # Display "openai"
        openai_text = font.render("openai", True, GREEN)
        screen.blit(openai_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    # Game over message
    screen.fill(DARK_BG)
    result_text = font.render(result, True, RED if result == "You Died!" else GREEN)
    screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    # Wait for 2 seconds before restarting
    time.sleep(2)

    if result == "You Win!":
        game(win_count)  # Restart the game with increased difficulty
    else:
        game(0)  # Restart the game with default values if you lose

if __name__ == "__main__":
    show_instructions()
    game(0)  # Start the game with 0 wins