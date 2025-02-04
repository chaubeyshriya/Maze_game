import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
ROWS = 20
CELL_SIZE = 20
SCREEN_SIZE = ROWS * CELL_SIZE
FPS = 20  

# Colors
RED = (255, 0, 0)  # Start1 color
BLUE = (0, 0, 255)  # Start2 color
BLACK = (0, 0, 0)  # Obstacles
WHITE = (245, 245, 245)  # Grid background
GREEN = (34, 177, 76)  # Fruit color
YELLOW = (255, 215, 0)  # Path from Start1
CYAN = (0, 255, 255)  # Path from Start2
FRUIT_HIGHLIGHT = (255, 140, 0)  # Meeting point

# Pygame setup
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Bidirectional DFS Game")
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, SCREEN_SIZE, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, SCREEN_SIZE), 1)
        pygame.draw.line(screen, (200, 200, 200), (0, x), (SCREEN_SIZE, x), 1)

def draw_cell(position, color, border_thickness=0):
    x, y = position
    rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    if border_thickness > 0:
        pygame.draw.rect(screen, (0, 0, 0), rect, border_thickness)

def get_neighbors(position):
    x, y = position
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx < ROWS and 0 <= ny < ROWS]

def place_obstacles(rows, num_obstacles, starts, fruit):
    obstacles = set()
    while len(obstacles) < num_obstacles:
        x, y = random.randint(0, rows - 1), random.randint(0, rows - 1)
        if (x, y) not in starts and (x, y) != fruit:
            obstacles.add((x, y))
    return obstacles

def dfs(start, fruit, obstacles):
    stack = [start]
    visited = set()
    parent = {}
    
    while stack:
        current = stack.pop()
        if current == fruit:
            break
        
        if current in visited:
            continue
        visited.add(current)
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited and neighbor not in obstacles:
                parent[neighbor] = current
                stack.append(neighbor)
    
    return reconstruct_path(parent, start, fruit)

def reconstruct_path(parent, start, fruit):
    path = []
    current = fruit
    while current != start:
        path.append(current)
        current = parent.get(current)
        if current is None:
            return []
    path.reverse()
    return path

def animate_snake_movement(path, color):
    for position in path:
        draw_cell(position, color)
        pygame.display.flip()
        clock.tick(FPS)

def show_fruit_found_message(fruit):
    font = pygame.font.SysFont(None, 48)
    message = f"Fruit found at {fruit}!"
    text = font.render(message, True, RED)
    
    message_screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    message_screen.fill(WHITE)
    
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    message_screen.blit(text, text_rect)
    pygame.display.flip()
    
    pygame.time.delay(2000)

def main():
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
        draw_cell(start1, RED, border_thickness=2)
        draw_cell(start2, BLUE, border_thickness=2)
        draw_cell(fruit, GREEN, border_thickness=2)
        for obs in obstacles:
            draw_cell(obs, BLACK)
        
        path1 = dfs(start1, fruit, obstacles)
        path2 = dfs(start2, fruit, obstacles)
        
        animate_snake_movement(path1, YELLOW)
        animate_snake_movement(path2, CYAN)
        draw_cell(fruit, FRUIT_HIGHLIGHT, border_thickness=3)
        
        show_fruit_found_message(fruit)
        
        pygame.display.flip()
        clock.tick(FPS)
        running = False

if __name__ == "__main__":
    main()