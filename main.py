import pygame
import sys
import os
from jogar import rodando


pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
dir_fonte = os.path.join(ASSETS_DIR, "Exo2.ttf")
font = pygame.font.Font(dir_fonte, 32)

menu_options = ["Jogar", "Preferências", "Ajuda", "Sair"]
selected_index = 0

# variáveis globais de configuração
num_teclas = 4
velocidade = 20 # padrão
dificuldade = "Iniciante"

def draw_menu():
    screen.fill((0,0,0))
    title_surface = font.render("Menu Principal", True, (255,255,0))
    screen.blit(title_surface, (screen.get_width()//2 - title_surface.get_width()//2, 150))

    for i, option in enumerate(menu_options):
        color = (255,255,255)
        if i == selected_index:
            color = (0,255,0)
        text_surface = font.render(option, True, color)
        screen.blit(text_surface, (screen.get_width()//2 - text_surface.get_width()//2, 300 + i*80))

    pygame.display.flip()

running = True
while running:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                chosen = menu_options[selected_index]
                if chosen == "Jogar":
                    rodando(screen, clock, num_teclas, velocidade)
                    # rodando(screen, clock, num_teclas, velocidade)  # passa configs
                elif chosen == "Preferências":
                    #add dps
                elif chosen == "Ajuda":
                    #add dps
                elif chosen == "Sair":
                    pygame.quit()
                    sys.exit()

    clock.tick(60)
