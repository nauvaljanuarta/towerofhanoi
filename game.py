import pygame
import sys
import time

# Constants for screen size and colors
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
TOWER_COLOR = (200, 200, 200)
DISK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]  # Additional colors for more disks

disk_count = 3
towers = []
base_x_positions = [200, 400, 600]
selected_disk = None
selected_tower = None
mouse_pos = (0, 0)
move_count = 0
game_solved = False
dragging = False

# game init 
def initialize_game():
    global towers, move_count, game_solved
    towers = [list(range(disk_count, 0, -1)), [], []]
    move_count = 0
    game_solved = False

def draw_towers(screen):
    screen.fill(BACKGROUND_COLOR)
    tower_width = 20
    base_y = HEIGHT - 100
    
    for x in base_x_positions:
        pygame.draw.rect(screen, TOWER_COLOR, (x - 10, 150, tower_width, 300))
    
    for i, tower in enumerate(towers):
        for j, disk in enumerate(tower):
            disk_width = 40 + disk * 30
            pygame.draw.rect(screen, DISK_COLORS[(disk - 1) % len(DISK_COLORS)],  
                             (base_x_positions[i] - disk_width // 2, base_y - j * 30, disk_width, 20))
    
    if dragging and selected_disk is not None:
        disk_width = 40 + selected_disk * 30
        pygame.draw.rect(screen, DISK_COLORS[(selected_disk - 1) % len(DISK_COLORS)], (mouse_pos[0] - disk_width // 2, mouse_pos[1] - 10, disk_width, 20))
    
    font = pygame.font.Font(None, 36)
    solve_button_rect = pygame.Rect(WIDTH - 150, 20, 100, 40)
    pygame.draw.rect(screen, (0, 255, 0), solve_button_rect)
    text = font.render("Solve", True, (0, 0, 0))
    screen.blit(text, (WIDTH - 130, 30))
    
    increase_button = pygame.Rect(50, 20, 40, 40)
    decrease_button = pygame.Rect(100, 20, 40, 40)
    pygame.draw.rect(screen, (0, 255, 255), increase_button)
    pygame.draw.rect(screen, (255, 165, 0), decrease_button)
    
    screen.blit(font.render("+", True, (0, 0, 0)), (65, 30))
    screen.blit(font.render("-", True, (0, 0, 0)), (115, 30))
    
    text = font.render(f"Moves: {move_count}", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - 50, HEIGHT - 50))
    
    if game_solved:
        text = font.render("Congratulations, you solved the game!", True, (255, 255, 0))
        screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2))

# towers init 
def get_tower_index(mouse_x):
    for i, x in enumerate(base_x_positions):
        if abs(mouse_x - x) < 50:
            return i
    return None

# inisiasi move disk 
def move_disk(from_tower, to_tower):
    global move_count, game_solved
    if towers[from_tower]:
        disk = towers[from_tower].pop()
        towers[to_tower].append(disk)
        move_count += 1
    
    if towers[1] == list(range(disk_count, 0, -1)) or towers[2] == list(range(disk_count, 0, -1)):
        game_solved = True

# logic solve hanoi 
def solve_hanoi(n, from_tower, to_tower, aux_tower, screen):
    if n == 1:
        move_disk(from_tower, to_tower)
        draw_towers(screen)
        pygame.display.flip()
        time.sleep(0.2)
        return
    solve_hanoi(n - 1, from_tower, aux_tower, to_tower, screen)
    move_disk(from_tower, to_tower)
    draw_towers(screen)
    pygame.display.flip()
    time.sleep(0.5)
    solve_hanoi(n - 1, aux_tower, to_tower, from_tower, screen)

# handle perpindahan cakram tarik turun
def handle_mouse_down(pos, screen):
    global selected_disk, selected_tower, dragging, disk_count
    solve_button_rect = pygame.Rect(WIDTH - 150, 20, 100, 40)
    increase_button = pygame.Rect(50, 20, 40, 40)
    decrease_button = pygame.Rect(100, 20, 40, 40)
    
    if solve_button_rect.collidepoint(pos):
        initialize_game()
        draw_towers(screen)
        pygame.display.flip()
        solve_hanoi(disk_count, 0, 2, 1, screen)
        return
    
    if increase_button.collidepoint(pos):
        disk_count += 1
        initialize_game()
        return
    
    if decrease_button.collidepoint(pos) and disk_count > 1:
        disk_count -= 1
        initialize_game()
        return
    
    tower_idx = get_tower_index(pos[0])
    if tower_idx is not None and towers[tower_idx]:
        selected_disk = towers[tower_idx].pop()
        selected_tower = tower_idx
        dragging = True

# handle perpindahan cakram angkat
def handle_mouse_up(pos):
    global selected_disk, selected_tower, dragging, move_count, game_solved
    dragging = False
    if selected_disk is not None:
        tower_idx = get_tower_index(pos[0])
        if tower_idx is not None:
            if not towers[tower_idx] or towers[tower_idx][-1] > selected_disk:
                towers[tower_idx].append(selected_disk)
                move_count += 1
                if towers[1] == list(range(disk_count, 0, -1)) or towers[2] == list(range(disk_count, 0, -1)):
                    game_solved = True
            else:
                towers[selected_tower].append(selected_disk)
        else:
            towers[selected_tower].append(selected_disk)
    selected_disk = None

# play game func 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tower of Hanoi")
    clock = pygame.time.Clock()
    initialize_game()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_down(event.pos, screen)
            elif event.type == pygame.MOUSEBUTTONUP:
                handle_mouse_up(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                global mouse_pos
                mouse_pos = event.pos
        
        draw_towers(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
