import pygame
import pymunk
import pymunk.pygame_util
import math
import subprocess
import sys

pygame.init()

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
background_music = pygame.mixer.Sound("e:\Game Billiard Python dan Constructs 3\Asset Game Billiard Python\Music dan Sound Effect\TakeFive.wav")
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

# kode dari "main.py" dimulai di sini
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 565
BOTTOM_PANEL = 50

# layar game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BOTTOM_PANEL))
pygame.display.set_caption("Billiard Sederhana")

# ruang pymunk
space = pymunk.Space()
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

# fps
clock = pygame.time.Clock()
FPS = 120

# variabel game
lives = 3
dia = 32
pocket_dia = 60
force = 0
max_force = 10000
force_direction = 1
game_running = True
cue_ball_potted = False
taking_shot = True
powering_up = False
potted_balls = []
score = 0  # Variabel score untuk menyimpan waktu

# warna
BG = (50, 50, 50)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# fonts
font = pygame.font.SysFont("Lato", 30)
large_font = pygame.font.SysFont("Lato", 60)

# asset gambar
cue_image = pygame.image.load("e:\Game Billiard Python dan Constructs 3\Asset Game Billiard Python\Asset Game New\cue 2.png").convert_alpha()
table_image = pygame.image.load("e:\Game Billiard Python dan Constructs 3\Asset Game Billiard Python\Asset Game New/table 2.png").convert_alpha()
ball_images = []
for i in range(1, 17):
    ball_image = pygame.image.load(f"e:\Game Billiard Python dan Constructs 3\Asset Game Billiard Python\Asset Game New/ball_{i}.png").convert_alpha()
    ball_images.append(ball_image)

# teks di layar
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Load efek suara saat bola dipukul
hit_sound = pygame.mixer.Sound("e:\Game Billiard Python dan Constructs 3\Asset Game Billiard Python\Music dan Sound Effect/billiards+2.wav")

# bola
def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    shape.elasticity = 0.8
    # pivot untuk menambah gesekan
    pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0  # nonaktifkan koreksi
    pivot.max_force = 1000  # gesekan linier

    space.add(body, shape, pivot)
    return shape

# setup bola game
balls = []
rows = 5
# lubang masuk bola
for col in range(5):
    for row in range(rows):
        pos = (250 + (col * (dia + 1)), 220 + (row * (dia + 1)) + (col * dia / 2))
        new_ball = create_ball(dia / 2, pos)
        balls.append(new_ball)
    rows -= 1

# Mengatur collision handler untuk mendeteksi tabrakan antara bola-bola
def ball_collision_handler(arbiter, space, data):
    hit_sound.set_volume(0.05) # Atur volume suara
    hit_sound.play()  # Memainkan efek suara saat bola bertabrakan

# Menambahkan collision handler ke ruang PyMunk
collision_handler = space.add_default_collision_handler()
collision_handler.pre_solve = ball_collision_handler

# tongkat bola
pos = (744, SCREEN_HEIGHT / 2)
cue_ball = create_ball(dia / 2, pos)
balls.append(cue_ball)

# enam lubang di atas meja
pockets = [
    (55, 63),
    (492, 48),
    (934, 64),
    (55, 516),
    (492, 529),
    (934, 516)
]

# penghalang atau batas meja
cushions = [
    [(78, 56), (99, 77), (445, 77), (454, 56)],
    [(511, 56), (520, 77), (971, 77), (992, 56)],
    [(79, 511), (100, 490), (446, 490), (454, 511)],
    [(512, 511), (521, 490), (972, 490), (993, 511)],
    [(56, 86), (77, 107), (77, 450), (56, 471)],
    [(923, 86), (902, 107), (902, 450), (923, 471)]
]

# berfungsi untuk membuat penghalang atau batas
def create_cushion(poly_dims):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = ((0, 0))
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.8

    space.add(body, shape)

for c in cushions:
    create_cushion(c)

# membuat tongkat biliar
class Cue():
    def __init__(self, pos):
        self.original_image = cue_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, angle):
        self.angle = angle

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image,
                     (self.rect.centerx - self.image.get_width() / 2,
                      self.rect.centery - self.image.get_height() / 2)
                     )

cue = Cue(balls[-1].body.position)

# bar kekuatan untuk menunjukkan seberapa keras bola putih akan dipukul
power_bar = pygame.Surface((10, 20))
power_bar.fill(RED)

# game loop
run = True
while run:

    clock.tick(FPS)
    space.step(1 / FPS)

    # fill background
    screen.fill(BG)

    # meja blliard
    screen.blit(table_image, (0, 0))

    # periksa apakah ada bola yang dimasukkan ke dalam lubang
    for i, ball in enumerate(balls):
        for pocket in pockets:
            ball_x_dist = abs(ball.body.position[0] - pocket[0])
            ball_y_dist = abs(ball.body.position[1] - pocket[1])
            ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
            if ball_dist <= pocket_dia / 2:
                # periksa apakah bola dalam lubang adalah bola billiard
                if i == len(balls) - 1:
                    lives -= 1
                    cue_ball_potted = True
                    ball.body.position = (-100, -100)
                    ball.body.velocity = (0.0, 0.0)
                else:
                    space.remove(ball.body)
                    balls.remove(ball)
                    potted_balls.append(ball_images[i])
                    ball_images.pop(i)

    # menggambar bola biliar
    for i, ball in enumerate(balls):
        screen.blit(ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

    # periksa apakah semua bola sudah berhenti bergerak
    taking_shot = True
    for ball in balls:
        if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
            taking_shot = False

    # menggambar tongkat biliar
    if taking_shot and game_running:
        if cue_ball_potted:
            # reposisi bola
            balls[-1].body.position = (744, SCREEN_HEIGHT / 2)
            cue_ball_potted = False
        # menghitung sudut tongkat biliar
        mouse_pos = pygame.mouse.get_pos()
        cue.rect.center = balls[-1].body.position
        x_dist = balls[-1].body.position[0] - mouse_pos[0]
        y_dist = -(balls[-1].body.position[1] - mouse_pos[1])  # -ve karena koordinat pygame y bertambah di bagian bawah layar
        cue_angle = math.degrees(math.atan2(y_dist, x_dist))
        cue.update(cue_angle)
        cue.draw(screen)

    # menyalakan tongkat biliar
    if powering_up and game_running:
        force += 100 * force_direction
        if force >= max_force or force <= 0:
            force_direction *= -1
        # power bar
        for b in range(math.ceil(force / 2000)):
            screen.blit(power_bar,
                        (balls[-1].body.position[0] - 30 + (b * 15),
                         balls[-1].body.position[1] + 30))
    elif not powering_up and taking_shot:
        x_impulse = math.cos(math.radians(cue_angle))
        y_impulse = math.sin(math.radians(cue_angle))
        balls[-1].body.apply_impulse_at_local_point((force * -x_impulse, force * y_impulse), (0, 0))
        force = 0
        force_direction = 1

    # panel bawah
    pygame.draw.rect(screen, BG, (0, SCREEN_HEIGHT, SCREEN_WIDTH, BOTTOM_PANEL))
    draw_text("LIVES: " + str(lives), font, WHITE, SCREEN_WIDTH - 150, SCREEN_HEIGHT + 10)
    # Perbarui score (waktu) jika permainan masih berlangsung
    if game_running:
        score += 1 / FPS  # Tambahkan waktu yang telah berlalu
    else:
        score = 0  # Set score ke 0 saat game over
    # Tampilkan score
    draw_text("SCORE: " + str(round(score, 2)), font, WHITE, SCREEN_WIDTH - 300, SCREEN_HEIGHT + 10)

    # bola masuk di panel bawah
    for i, ball in enumerate(potted_balls):
        screen.blit(ball, (10 + (i * 50), SCREEN_HEIGHT + 10))

    # periksa game over
    if lives <= 0:
        draw_text("GAME OVER", large_font, WHITE, SCREEN_WIDTH / 1.91 - 160, SCREEN_HEIGHT / 1.55 - 100)
        game_running = False

    # periksa apakah semua bola sudah dimasukkan ke dalam lubang
    if len(balls) == 1:
        draw_text("YOU WIN!", large_font, WHITE, SCREEN_WIDTH / 1.91 - 160, SCREEN_HEIGHT / 1.55 - 100)
        game_running = False

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and taking_shot:
            powering_up = True
        if event.type == pygame.MOUSEBUTTONUP and taking_shot:
            powering_up = False
        if event.type == pygame.QUIT:
            run = False

    # space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()