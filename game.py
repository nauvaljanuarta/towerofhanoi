import pygame
import sys
import time

# Konstanta Warna
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
TOWER_COLOR = (200, 200, 200)
DISK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]

class TowerOfHanoi:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tower of Hanoi")
        self.clock = pygame.time.Clock()
        self.disk_count = 3  # inisiasi disk ada 3 disk
        self.initialize_game()

    def initialize_game(self):
        self.towers = [list(range(self.disk_count, 0, -1)), [], []] #inisialisasi caakram sesuai diskcount contoh 3 berarti 
        self.selected_disk = None
        self.selected_tower = None
        self.mouse_pos = (0, 0)
        self.move_count = 0
        self.game_solved = False
        self.dragging = False

    def draw_towers(self):
        self.screen.fill(BACKGROUND_COLOR)
        base_x_positions = [200, 400, 600]
        base_y = HEIGHT - 100
        tower_width = 20
        
        font = pygame.font.Font(None, 48)
        tower_labels = ["A", "B", "C"]
        
        for i, x in enumerate(base_x_positions):
            pygame.draw.rect(self.screen, TOWER_COLOR, (x - 10, 150, tower_width, 300))
            text = font.render(tower_labels[i], True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, 100))  # Posisi di atas tower
            self.screen.blit(text, text_rect)
        
        for i, tower in enumerate(self.towers):
            for j, disk in enumerate(tower):
                disk_width = 40 + disk * 30
                pygame.draw.rect(self.screen, DISK_COLORS[disk % len(DISK_COLORS)],  
                                 (base_x_positions[i] - disk_width // 2, base_y - j * 30, disk_width, 20))
        
        if self.dragging and self.selected_disk is not None:
            disk_width = 40 + self.selected_disk * 30
            pygame.draw.rect(self.screen, DISK_COLORS[self.selected_disk % len(DISK_COLORS)],
                             (self.mouse_pos[0] - disk_width // 2, self.mouse_pos[1] - 10, disk_width, 20))
        
        font = pygame.font.Font(None, 36)
        self.draw_buttons(font)
        
        if self.game_solved:
            text = font.render("Game Berhasil!", True, (255, 255, 0))
            self.screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))

        pygame.display.flip()

    def draw_buttons(self, font):
        pygame.draw.rect(self.screen, (0, 255, 0), (WIDTH - 150, 20, 100, 40))
        self.screen.blit(font.render("Solve", True, (0, 0, 0)), (WIDTH - 130, 30))
        
        pygame.draw.rect(self.screen, (0, 255, 255), (50, 20, 40, 40))
        pygame.draw.rect(self.screen, (255, 165, 0), (100, 20, 40, 40))
        
        self.screen.blit(font.render("+", True, (0, 0, 0)), (65, 30))
        self.screen.blit(font.render("-", True, (0, 0, 0)), (115, 30))
        self.screen.blit(font.render(f"Moves: {self.move_count}", True, (255, 255, 255)), (WIDTH // 2 - 50, HEIGHT - 50))
    
    def get_tower_index(self, mouse_x):
        base_x_positions = [200, 400, 600]
        for i, x in enumerate(base_x_positions):
            if abs(mouse_x - x) < 50:
                return i
        return None

    def move_disk(self, from_tower, to_tower):
        if self.towers[from_tower]:
            disk = self.towers[from_tower].pop()
            self.towers[to_tower].append(disk)
            self.move_count += 1
            if self.towers[1] == list(range(self.disk_count, 0, -1)) or self.towers[2] == list(range(self.disk_count, 0, -1)):
                self.game_solved = True

    def solve_hanoi(self, n, from_tower, to_tower, aux_tower): #pakai stack untuk dfs searchnya
        stack = [(n, from_tower, to_tower, aux_tower)] 
        while stack:
            n, from_tower, to_tower, aux_tower = stack.pop() #last in first out untuk pop (mengambil stack yang paling akhir)
            if n == 1:
                self.move_disk(from_tower, to_tower)
                self.draw_towers()
                time.sleep(0.9)
            else:
                stack.append((n - 1, aux_tower, to_tower, from_tower))
                stack.append((1, from_tower, to_tower, aux_tower))
                stack.append((n - 1, from_tower, aux_tower, to_tower))
    
    # def solve_hanoi(self, n, from_tower, to_tower, aux_tower):
    #   if n == 1:
    #       self.move_disk(from_tower, to_tower)
    #       self.draw_towers()
    #       time.sleep(0.2)
    #       return

    #   self.solve_hanoi(n - 1, from_tower, aux_tower, to_tower)

    #   self.move_disk(from_tower, to_tower)
    #   self.draw_towers()
    #   time.sleep(0.2)

    #   self.solve_hanoi(n - 1, aux_tower, to_tower, from_tower)

    def handle_mouse_down(self, pos):
        solve_button_rect = pygame.Rect(WIDTH - 150, 20, 100, 40)
        increase_button = pygame.Rect(50, 20, 40, 40)
        decrease_button = pygame.Rect(100, 20, 40, 40)
        
        if solve_button_rect.collidepoint(pos):
            self.initialize_game()
            self.solve_hanoi(self.disk_count, 0, 2, 1)
            return
        if increase_button.collidepoint(pos):
            self.disk_count += 1
            self.initialize_game()
            return
        if decrease_button.collidepoint(pos) and self.disk_count > 1:
            self.disk_count -= 1
            self.initialize_game()
            return
        
        tower_idx = self.get_tower_index(pos[0])
        if tower_idx is not None and self.towers[tower_idx]:
            self.selected_disk = self.towers[tower_idx].pop()
            self.selected_tower = tower_idx
            self.dragging = True

    def handle_mouse_up(self, pos):
        self.dragging = False
        if self.selected_disk is not None:
            tower_idx = self.get_tower_index(pos[0])
            if tower_idx is not None and (not self.towers[tower_idx] or self.towers[tower_idx][-1] > self.selected_disk):
                self.towers[tower_idx].append(self.selected_disk)
                self.move_count += 1
            else:
                self.towers[self.selected_tower].append(self.selected_disk)
        self.selected_disk = None

    def run(self):
        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_mouse_down(event.pos)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.handle_mouse_up(event.pos)
                    elif event.type == pygame.MOUSEMOTION:
                        self.mouse_pos = event.pos
                self.draw_towers()
                self.clock.tick(60)
            except Exception as e:
                print(f"Terjadi error: {e}")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    TowerOfHanoi().run()