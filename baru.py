import pygame
import sys

# Konstanta ukuran layar dan warna
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
TOWER_COLOR = (200, 200, 200)
DISK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Warna hanya untuk 3 cakram

towers = [[3, 2, 1], [], []]  # Menggunakan hanya 3 cakram

def draw_towers(screen):
    screen.fill(BACKGROUND_COLOR)
    tower_width = 20
    base_y = HEIGHT - 100
    base_x_positions = [200, 400, 600]
    
    # Gambar tiang tower
    for x in base_x_positions:
        pygame.draw.rect(screen, TOWER_COLOR, (x - 10, 150, tower_width, 300))
    
    # Gambar cakram
    for i, tower in enumerate(towers):
        for j, disk in enumerate(tower):  # Urutan sudah benar dari bawah ke atas
            disk_width = 40 + disk * 30
            pygame.draw.rect(screen, DISK_COLORS[disk - 1],  
                             (base_x_positions[i] - disk_width // 2, base_y - j * 30, disk_width, 20))

def main():
    pygame.init()
    print("Game started")  # Debugging
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tower of Hanoi")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_towers(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()


