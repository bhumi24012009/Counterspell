import pygame
from collections import deque

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echo Racer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game settings
FPS = 60
clock = pygame.time.Clock()

# Player settings
player_size = 30
player_pos = [WIDTH // 2, HEIGHT - 100]
player_speed = 5

# Echo settings
echo_spawn_delay = 200  # Frames before the first echo spawns
echo_interval = 150  # Frames between subsequent echoes
echo_queue = deque(maxlen=300)  # Records player positions
echoes = []

# Game loop
running = True
frame_count = 0

while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running =  False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += player_speed

    # Add player position to the echo queue
    echo_queue.append(tuple(player_pos))

    # Spawn echoes only after the delay
    if frame_count > echo_spawn_delay and frame_count % echo_interval == 0:
        # Add echo at an old position (further back in time)
        if len(echo_queue) > 50:  # Ensure enough data exists for echoes
            echoes.append(list(echo_queue[-50]))  # Echo spawns at older position

    # Move echoes (replaying recorded positions)
    for echo in echoes:
        if len(echo_queue) > 50:  # Ensure enough history to move echoes
            echo[:] = list(echo_queue.popleft())  # Update echo position

    # Collision detection with echoes
    for echo in echoes:
        if abs(echo[0] - player_pos[0]) < player_size and \
           abs(echo[1] - player_pos[1]) < player_size:
            print("Collided with echo!")
            running = False

    # Draw player
    pygame.draw.rect(screen, BLUE, (*player_pos, player_size, player_size))

    # Draw echoes
    for echo in echoes:
        pygame.draw.rect(screen, RED, (*echo, player_size, player_size))

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1

# Quit Pygame
pygame.quit()
