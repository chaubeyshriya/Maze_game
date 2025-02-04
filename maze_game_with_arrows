import pygame
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
TILE_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Clock
clock = pygame.time.Clock()
FPS = 10

# Generate random obstacles
def generate_obstacles():
    obstacles = set()
    for _ in range(GRID_SIZE * GRID_SIZE // 4):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (x, y) not in {(0, 0), (GRID_SIZE - 1, GRID_SIZE - 1)}:
            obstacles.add((x, y))
    return obstacles

# BFS to check if a path exists
def bfs_path_exists(start, end, obstacles):
    queue = deque([start])
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current = queue.popleft()
        if current == end:
            return True

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in visited and neighbor not in obstacles:
                visited.add(neighbor)
                queue.append(neighbor)

    return False

# Main game function
def main():
    start = (0, 0)
    end = (GRID_SIZE - 1, GRID_SIZE - 1)
    obstacles = generate_obstacles()

    # Ensure a valid path exists
    while not bfs_path_exists(start, end, obstacles):
        obstacles = generate_obstacles()

    player_pos = list(start)
    visited = [start]  # Store visited cells in order as a list
    lives = 3

    running = True
    while running:
        screen.fill(WHITE)

        # Draw grid
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if (x, y) in obstacles:
                    pygame.draw.rect(screen, BLACK, rect)
                elif (x, y) == start:
                    pygame.draw.rect(screen, GREEN, rect)
                elif (x, y) == end:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect, 1)

        # Draw the trace line
        for i in range(len(visited) - 1):
            start_pos = (visited[i][0] * TILE_SIZE + TILE_SIZE // 2, visited[i][1] * TILE_SIZE + TILE_SIZE // 2)
            end_pos = (visited[i + 1][0] * TILE_SIZE + TILE_SIZE // 2, visited[i + 1][1] * TILE_SIZE + TILE_SIZE // 2)
            pygame.draw.line(screen, YELLOW, start_pos, end_pos, 2)  # Slim line with thickness 2

        # Draw player
        player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, BLUE, player_rect)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            next_pos = (player_pos[0], player_pos[1] - 1)
        elif keys[pygame.K_DOWN]:
            next_pos = (player_pos[0], player_pos[1] + 1)
        elif keys[pygame.K_LEFT]:
            next_pos = (player_pos[0] - 1, player_pos[1])
        elif keys[pygame.K_RIGHT]:
            next_pos = (player_pos[0] + 1, player_pos[1])
        else:
            next_pos = tuple(player_pos)

        if 0 <= next_pos[0] < GRID_SIZE and 0 <= next_pos[1] < GRID_SIZE:
            if next_pos not in obstacles:
                player_pos[0], player_pos[1] = next_pos
                if tuple(player_pos) not in visited:
                    visited.append(tuple(player_pos))  # Add the new position to the trace
            else:
                lives -= 1
                player_pos = list(start)  # Restart from start point
                visited = [start]  # Reset the trace

                # Renew obstacles and ensure a valid path
                obstacles = generate_obstacles()
                while not bfs_path_exists(start, end, obstacles):
                    obstacles = generate_obstacles()

        # Check win condition
        if tuple(player_pos) == end:
            print("You win!")
            running = False

        # Check game over
        if lives <= 0:
            print("Game over!")
            running = False

        # Display lives
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
        screen.blit(lives_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
