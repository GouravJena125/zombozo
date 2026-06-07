import pygame
import random

pygame.init()

# Screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")

# Colors
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Player
player_width = 50
player_height = 30
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 60
player_speed = 7

# Game Stats
health = 100
ammo = 50
score = 0

# Lists
bullets = []
zombies = []
health_packs = []
ammo_boxes = []

running = True
spawn_timer = 0

while running:
    clock.tick(60)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ammo > 0:
                bullets.append([
                    player_x + player_width // 2,
                    player_y
                ])
                ammo -= 1

    # Movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    player_x = max(0, min(WIDTH - player_width, player_x))

    # Spawn Zombies
    spawn_timer += 1

    if spawn_timer > 40:
        spawn_timer = 0

        zombies.append([
            random.randint(20, WIDTH - 20),
            -40,
            random.randint(2, 5)
        ])

    # Random pickups
    if random.randint(1, 800) == 1:
        health_packs.append([
            random.randint(20, WIDTH - 20),
            random.randint(150, HEIGHT - 150)
        ])

    if random.randint(1, 800) == 1:
        ammo_boxes.append([
            random.randint(20, WIDTH - 20),
            random.randint(150, HEIGHT - 150)
        ])

    # Update bullets
    for bullet in bullets[:]:
        bullet[1] -= 10

        if bullet[1] < 0:
            bullets.remove(bullet)

    # Update zombies
    for zombie in zombies[:]:
        zombie[1] += zombie[2]

        # Reached player
        if zombie[1] > player_y:
            health -= 10

            if zombie in zombies:
                zombies.remove(zombie)

        # Bullet collisions
        for bullet in bullets[:]:
            if (
                abs(bullet[0] - zombie[0]) < 20
                and abs(bullet[1] - zombie[1]) < 20
            ):
                score += 10

                if bullet in bullets:
                    bullets.remove(bullet)

                if zombie in zombies:
                    zombies.remove(zombie)

                break

    # Health packs
    player_center_x = player_x + player_width // 2

    for pack in health_packs[:]:
        if (
            abs(player_center_x - pack[0]) < 30
            and abs(player_y - pack[1]) < 30
        ):
            health = min(100, health + 25)
            health_packs.remove(pack)

    # Ammo packs
    for box in ammo_boxes[:]:
        if (
            abs(player_center_x - box[0]) < 30
            and abs(player_y - box[1]) < 30
        ):
            ammo += 20
            ammo_boxes.remove(box)

    # Game Over
    if health <= 0:
        running = False

    # Draw
    screen.fill(BLACK)

    # Player
    pygame.draw.rect(
        screen,
        BLUE,
        (player_x, player_y,
         player_width, player_height)
    )

    # Bullets
    for bullet in bullets:
        pygame.draw.rect(
            screen,
            YELLOW,
            (bullet[0], bullet[1], 4, 12)
        )

    # Zombies
    for zombie in zombies:
        pygame.draw.circle(
            screen,
            GREEN,
            (int(zombie[0]), int(zombie[1])),
            18
        )

    # Health Packs
    for pack in health_packs:
        pygame.draw.rect(
            screen,
            RED,
            (pack[0] - 10, pack[1] - 10, 20, 20)
        )

    # Ammo Packs
    for box in ammo_boxes:
        pygame.draw.rect(
            screen,
            WHITE,
            (box[0] - 10, box[1] - 10, 20, 20)
        )

    # UI
    health_text = font.render(
        f"Health: {health}",
        True,
        WHITE
    )

    ammo_text = font.render(
        f"Ammo: {ammo}",
        True,
        WHITE
    )

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(health_text, (10, 10))
    screen.blit(ammo_text, (10, 45))
    screen.blit(score_text, (10, 80))

    pygame.display.flip()

# Game Over Screen
screen.fill(BLACK)

game_over = font.render(
    f"GAME OVER! Score: {score}",
    True,
    RED
)

screen.blit(
    game_over,
    (WIDTH // 2 - 160, HEIGHT // 2)
)

pygame.display.flip()
pygame.time.wait(4000)

pygame.quit()