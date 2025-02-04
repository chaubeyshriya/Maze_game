import pygame
from collections import deque
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
ROWS = 20
CELL_SIZE = 20
SCREEN_SIZE = ROWS * CELL_SIZE

# Colors
RED = (255, 0, 0)         # Start1 color
BLUE = (0, 0, 255)        # Start2 color
BLACK = (0, 0, 0)         # Obstacles
WHITE = (245, 245, 245)   # Grid background (off-white for better contrast)
GREEN = (34, 177, 76)     # Fruit color
YELLOW = (255, 215, 0)    # Path from Start1 (a gold yellow)
CYAN = (0, 255, 255)      # Path from Start2 (a bright cyan)
FRUIT_HIGHLIGHT = (255, 140, 0)  # Meeting point (distinct orange)

# Pygame setup
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Bidirectional BFS Game")
clock = pygame.time.Clock()


def draw_grid():
    """Draws the grid with a lighter grid line for better contrast."""
    for x in range(0, SCREEN_SIZE, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, SCREEN_SIZE), 1)
        pygame.draw.line(screen, (200, 200, 200), (0, x), (SCREEN_SIZE, x), 1)


def draw_cell(position, color, border_thickness=0):
    """Draws a single cell with optional border thickness for styling."""
    x, y = position
    rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    if border_thickness > 0:
        pygame.draw.rect(screen, (0, 0, 0), rect, border_thickness)


def get_neighbors(position, rows):
    """Returns valid neighboring cells."""
    x, y = position
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < rows - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < rows - 1:
        neighbors.append((x, y + 1))
    return neighbors


def place_obstacles(rows, num_obstacles, starts, fruit):
    """Randomly places obstacles on the grid."""
    obstacles = set()
    while len(obstacles) < num_obstacles:
        x, y = random.randint(0, rows - 1), random.randint(0, rows - 1)
        if (x, y) not in starts and (x, y) != fruit:
            obstacles.add((x, y))
    return obstacles


def bidirectional_bfs(start1, start2, fruit, obstacles):
    """Bidirectional BFS to find shortest paths from start1 and start2 to fruit."""
    queue1 = deque([start1])
    queue2 = deque([start2])
    visited1 = {start1}
    visited2 = {start2}
    parent1 = {}
    parent2 = {}

    while queue1 or queue2:
        # Expand from start1
        if queue1:
            current = queue1.popleft()
            for neighbor in get_neighbors(current, ROWS):
                if neighbor not in visited1 and neighbor not in obstacles:
                    visited1.add(neighbor)
                    parent1[neighbor] = current
                    queue1.append(neighbor)
                    if neighbor == fruit:
                        break

        # Expand from start2
        if queue2:
            current = queue2.popleft()
            for neighbor in get_neighbors(current, ROWS):
                if neighbor not in visited2 and neighbor not in obstacles:
                    visited2.add(neighbor)
                    parent2[neighbor] = current
                    queue2.append(neighbor)
                    if neighbor == fruit:
                        break

    # Reconstruct paths
    path1 = reconstruct_path(parent1, start1, fruit)
    path2 = reconstruct_path(parent2, start2, fruit)

    return path1, path2


def reconstruct_path(parent, start, fruit):
    """Reconstructs a path from start to the fruit."""
    path = []
    current = fruit
    while current != start:
        path.append(current)
        current = parent.get(current)
        if current is None:
            break
    path.reverse()
    return path


def animate_snake_movement(path, color, delay=100):
    """Animates the snake moving along the given path."""
    for position in path:
        draw_cell(position, color)
        pygame.display.flip()
        pygame.time.delay(delay)


def show_fruit_found_message(fruit):
    """Displays a new window with a message when the fruit is found."""
    font = pygame.font.SysFont(None, 48)
    message = f"Fruit found at {fruit}!"
    text = font.render(message, True, RED)
    
    # Create a new window for the message
    message_screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    message_screen.fill(WHITE)
    
    # Center the text on the screen
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    message_screen.blit(text, text_rect)
    pygame.display.flip()
    
    # Wait for user to close or continue
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # Exit message window on any key press
                waiting = False


def main():
    # Randomly place start points, fruit, and obstacles
    start1 = (0, 0)
    start2 = (ROWS - 1, ROWS - 1)
    fruit = (random.randint(0, ROWS - 1), random.randint(0, ROWS - 1))
    while fruit == start1 or fruit == start2:
        fruit = (random.randint(0, ROWS - 1), random.randint(0, ROWS - 1))

    obstacles = place_obstacles(ROWS, 30, {start1, start2}, fruit)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_grid()

        # Draw start points, fruit, and obstacles
        draw_cell(start1, RED, border_thickness=2)
        draw_cell(start2, BLUE, border_thickness=2)
        draw_cell(fruit, GREEN, border_thickness=2)
        for obs in obstacles:
            draw_cell(obs, BLACK)

        # Perform bidirectional BFS
        path1, path2 = bidirectional_bfs(start1, start2, fruit, obstacles)

        # Animate snakes moving toward the fruit
        animate_snake_movement(path1, YELLOW)
        animate_snake_movement(path2, CYAN)

        # Highlight the fruit
        draw_cell(fruit, FRUIT_HIGHLIGHT, border_thickness=3)

        # Show message after reaching the fruit
        if path1 and path2:
            show_fruit_found_message(fruit)
            running = False

        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
