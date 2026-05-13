import pygame
import sys
import os

# importando funções dos outros arquivos
from opções import preferencias
from menu import menu_musicas
from animacoes import fade_in, fade_out

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

# diretório assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
# definindo fonte
dir_fonte = os.path.join(ASSETS_DIR, "fonte.ttf")
font = pygame.font.Font(dir_fonte, 32)

# opções do menu
menu_options = ["Jogar", "Preferências", "Ajuda", "Sair"]
selected_index = 0

# variáveis globais de configuração
velocidade = 20 # padrão
dificuldade = "Iniciante"

def draw_menu(clicked_index=None, click_animation_progress=0):
    screen.fill((0,0,0))
    
    # título grande na lateral esquerda
    title_font = pygame.font.Font(dir_fonte, 80)
    title_surface = title_font.render("BeatPy", True, (128,0,32))  # vinho
    screen.blit(title_surface, (400, screen.get_height()//2 - title_surface.get_height()//2))

    # fundo cinza na lateral direita
    right_rect = pygame.Rect(screen.get_width()//2, 0, screen.get_width()//2, screen.get_height())
    pygame.draw.rect(screen, (50,50,50), right_rect)

    # barra vinho divisória
    pygame.draw.rect(screen, (128,0,32), (screen.get_width()//2 - 10, 0, 20, screen.get_height()))

    # dimensões fixas para os botões
    button_width = 300
    button_height = 70
    button_x = screen.get_width()//2 + 150

    # calcular posição inicial para centralizar verticalmente
    total_height = len(menu_options) * (button_height + 30) - 30
    start_y = screen.get_height()//2 - total_height//2

    # exibir opções
    for i, option in enumerate(menu_options):
        # animação de clique (reduz tamanho temporariamente)
        scale = 1.0
        if clicked_index == i and click_animation_progress > 0:
            scale = 1.0 - 0.1 * click_animation_progress  # encolhe até 90%

        bw = int(button_width * scale)
        bh = int(button_height * scale)
        bx = button_x + (button_width - bw)//2
        by = start_y + i*(button_height+30) + (button_height - bh)//2

        # cor da caixa
        box_color = (128,0,32)
        if i == selected_index:
            box_color = (200,80,100)

        # desenhar caixa
        box_rect = pygame.Rect(bx, by, bw, bh)
        pygame.draw.rect(screen, box_color, box_rect, border_radius=20)

        # texto centralizado
        text_surface = font.render(option, True, (255,255,255))
        text_rect = text_surface.get_rect(center=box_rect.center)
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

clicked_index = None
click_animation_progress = 0

running = True
while running:
    draw_menu(clicked_index, click_animation_progress)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                clicked_index = selected_index
                click_animation_progress = 1  # inicia animação

    # atualizar animação
    if click_animation_progress > 0:
        click_animation_progress -= 0.1
        if click_animation_progress <= 0:
            # fim da animação → executa ação
            chosen = menu_options[clicked_index]
            fade_out(screen, clock)  # escurece antes de mudar
            if chosen == "Jogar":
                menu_musicas(screen, clock, font, velocidade)
            elif chosen == "Preferências":
                velocidade=preferencias(screen, clock, font, velocidade)
            elif chosen == "Ajuda":
                pass
            elif chosen == "Sair":
                pygame.quit()
                sys.exit()
            fade_in(screen, clock)
            clicked_index = None
    clock.tick(60)
if __name__ == "__main__":
    menu_musicas()