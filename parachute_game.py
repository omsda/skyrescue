import pygame, random

# Initialize
pygame.init()
WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)

# Boat
boat_img = pygame.image.load("boat.png").convert_alpha()
boat_img = pygame.transform.scale(boat_img, (50, 20))  # Reduced length
boat_rect = boat_img.get_rect(midbottom=(WIDTH//2, HEIGHT - 20))

# Load parachute image
parachute_img = pygame.image.load("parachute.png").convert_alpha()
parachute_img = pygame.transform.scale(parachute_img, (20, 20))

# Parachutist
class Parachutist:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 20), 0, 20, 20)
    def fall(self):
        self.rect.y += 5

# Game variables
parachutists = []
spawn_timer = 0
score = 0
missed = 0
font = pygame.font.SysFont(None, 36)

# Game loop
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move boat
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: boat_rect.x -= 5
    if keys[pygame.K_RIGHT]: boat_rect.x += 5
    boat_rect.clamp_ip(screen.get_rect())

    # Spawn parachutists
    spawn_timer += 1
    if spawn_timer > 30:
        parachutists.append(Parachutist())
        spawn_timer = 0

    # Update parachutists
    for p in parachutists[:]:
        p.fall()
        # Draw parachute image instead of rectangle
        screen.blit(parachute_img, p.rect)
        if p.rect.colliderect(boat_rect):
            parachutists.remove(p)
            score += 1
        elif p.rect.top > HEIGHT:
            parachutists.remove(p)
            missed += 1

    # Draw boat
    screen.blit(boat_img, boat_rect)

    # Display score
    score_text = font.render(f"Score: {score}  Missed: {missed}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Check game over
    if missed >= 5:
        game_over = font.render("Game Over", True, (200, 0, 0))
        screen.blit(game_over, (WIDTH//2 - 80, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()