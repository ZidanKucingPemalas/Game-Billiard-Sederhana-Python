import pygame
import sys
import subprocess
import pygame.mixer

# Inisialisasi Pygame
pygame.init()

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
DARK_YELLOW = (204, 204, 0)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)

# Load musik latar belakang
background_music = pygame.mixer.Sound("f:\Game Billiard Sederhana Python\Asset Game Billiard Python\Music dan Sound Effect\TakeFive.wav")
background_music.play() # untuk memutar musik secara terus-menerus
background_music.set_volume(0.3) # Atur volume suara

# Ukuran layar
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 565

# Font
TITLE_FONT = pygame.font.SysFont("comicsansms", 60)
BUTTON_FONT = pygame.font.SysFont("comicsansms", 40)
NAMA_FONT = pygame.font.SysFont("comicsansms", 20)
KELAS_FONT = pygame.font.SysFont("comicsansms", 20)

# Judul dan tombol
TITLE = "Game Billiard Sederhana"
START_BUTTON = "Mulai"
EXIT_BUTTON = "Keluar"
NAMA = "Muhammad Zidan Hikayatuloh"
KELAS = "X PPLG A"

# Membuat layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Fungsi untuk menggambar tombol
def draw_button(surface, text, font, color, rect):
    pygame.draw.rect(surface, color, rect)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# Fungsi utama untuk main menu
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    # Menghentikan musik latar belakang sebelum menjalankan permainan
                    background_music.stop()
                    # Jalankan game saat tombol mulai ditekan
                    subprocess.run(["python", "main.py"])
                elif exit_button_rect.collidepoint(event.pos):
                    # Keluar dari permainan saat tombol keluar ditekan
                    pygame.quit()
                    sys.exit()

        screen.fill(GREEN)

        # Judul game
        title_text = TITLE_FONT.render(TITLE, True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Tombol Mulai
        start_button_rect = pygame.Rect(0, 0, 200, 80)
        start_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_button(screen, START_BUTTON, BUTTON_FONT, ORANGE, start_button_rect)

        # Tombol Keluar
        exit_button_rect = pygame.Rect(0, 0, 200, 80)
        exit_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        draw_button(screen, EXIT_BUTTON, BUTTON_FONT, ORANGE, exit_button_rect)
        
        # Teks nama
        name_text = NAMA_FONT.render(NAMA, True, WHITE)
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2))
        screen.blit(name_text, name_rect)
        
        # Teks kelas
        class_text = KELAS_FONT.render(KELAS, True, WHITE)
        class_rect = class_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.12))
        screen.blit(class_text, class_rect)

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()