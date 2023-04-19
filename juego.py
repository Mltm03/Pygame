import pygame
import random
import threading
import sys
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Definir constantes del juego
WIDTH = 800
HEIGHT = 600
FPS = 60

# Definir colores
# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Crear la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ejemplo de juego con hilos en Python")

#meter sonido
sound=pygame.mixer.Sound("musica.ogg")

enemies_out_of_screen = 0

# Clase para representar a los enemigos del juego
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.speed = random.randint(1, 5)

    def update(self):
        global enemies_out_of_screen
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -50)
            self.speed = random.randint(1, 5)
            enemies_out_of_screen += 1  # aumenta la variable global


# Clase para representar al jugador del juego
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Función para crear enemigos de forma continua
def create_enemies():
    while True:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        pygame.time.wait(random.randint(500, 3000))

# Crea una función para mostrar el menú de "muerte"
def death_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    restart_game()
                    
        # Dibuja el fondo y los botones del menú de "muerte"
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        text = font.render("Has perdido. ¿Quieres reiniciar el juego?", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
        screen.blit(text, text_rect)
        restart_button = pygame.draw.rect(screen, (0, 255, 0), (WIDTH/2 - 50, HEIGHT/2 + 50, 100, 50))
        font = pygame.font.Font(None, 24)
        text = font.render("Reiniciar", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 75))
        screen.blit(text, text_rect)
        
        pygame.display.flip()

# Crea una función para reiniciar el juego
def restart_game():
    # Restablece las variables del juego a sus valores iniciales
    # ...
    main_game_loop()

# Inicializar grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Crear jugador y agregarlo al grupo de sprites
player = Player()
all_sprites.add(player)

# Crear hilos para crear enemigos
enemy_thread = threading.Thread(target=create_enemies)
enemy_thread.start()

# Iniciar el bucle principal del juego
#marcador 
score=0
running = True
clock = pygame.time.Clock()
while running:
    # Mantener el bucle al ritmo deseado
    sound.play()
    clock.tick(FPS)

    # Procesar eventos del juego
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

    # Actualizar sprites
    all_sprites.update()
    # Detectar colisiones entre el jugador y los enemigos
    hits = pygame.sprite.spritecollide(player, enemies, False)    
    if hits:
        death_menu()
        running = False
        

        

    # Dibujar todo en la pantalla
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Dibujar puntajes
    font = pygame.font.Font(None, 36)
    missed_text = font.render(f"Esquivados: {enemies_out_of_screen}", True, WHITE)
    screen.blit(missed_text, (10, 50))

    pygame.display.flip()

# Cerrar Pygame
pygame.quit()
