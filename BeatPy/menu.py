import pygame
import sys
import os

from jogar import rodando
from animacoes import fade_in, fade_out

def carregar_musicas(assets_dir):
    # pega todas as pastas dentro de assets_dir
    lista_musicas = []
    for item in os.listdir(assets_dir):
        caminho = os.path.join(assets_dir, item)
        if os.path.isdir(caminho):  # verifica se é pasta
            lista_musicas.append(item)
    return lista_musicas

def menu_musicas(screen, clock, font, velocidade):
    fade_in(screen, clock)
    # diretório assets
    ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
    MSC_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", 'Songs')
    
    lista_musicas = carregar_musicas(MSC_DIR)
    music_index = 0
    running_musica = True

    while running_musica:
        screen.fill((30,30,30))
        title_surface = font.render("Seleção de Música", True, (255,255,0))
        screen.blit(title_surface, (screen.get_width()//2 - title_surface.get_width()//2, 150))

        # mostrar músicas
        for i, option in enumerate(lista_musicas + ["Voltar"]):
            color = (255,255,255)
            if i == music_index:
                color = (0,255,0)
            text_surface = font.render(option, True, color)
            screen.blit(text_surface, (screen.get_width()//2 - text_surface.get_width()//2, 300 + i*80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    music_index = (music_index - 1) % (len(lista_musicas)+1)
                elif event.key == pygame.K_DOWN:
                    music_index = (music_index + 1) % (len(lista_musicas)+1)
                elif event.key == pygame.K_RETURN:
                    fade_out(screen, clock)
                    if music_index < len(lista_musicas):
                        musica_escolhida = lista_musicas[music_index]
                        dificuldade = escolher_dificuldade(screen, clock, font, musica_escolhida)
                        if dificuldade:  # se escolheu uma dificuldade válida
                            print(musica_escolhida, dificuldade)
                            rodando(screen, clock, font, velocidade, musica_escolhida, dificuldade)
                    else:
                        running_musica = False
        clock.tick(60)


def escolher_dificuldade(screen, clock, font, musica):
    diff_options = ["Iniciante", "Intermediário", "Avançado", "Veterano", "Voltar"]
    diff_index = 0
    running_diff = True
    dificuldade = None

    while running_diff:
        screen.fill((40,40,40))
        title_surface = font.render(f"Dificuldade - {musica}", True, (255,255,0))
        screen.blit(title_surface, (screen.get_width()//2 - title_surface.get_width()//2, 150))

        for i, option in enumerate(diff_options):
            color = (255,255,255)
            if i == diff_index:
                color = (0,255,0)
            text_surface = font.render(option, True, color)
            screen.blit(text_surface, (screen.get_width()//2 - text_surface.get_width()//2, 300 + i*80))

        pygame.display.flip()

        lista_dificuldades = ["Iniciante", "Intermediario", "Avancado", "Veterano", "Voltar"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    diff_index = (diff_index - 1) % len(diff_options)
                elif event.key == pygame.K_DOWN:
                    diff_index = (diff_index + 1) % len(diff_options)
                elif event.key == pygame.K_RETURN:
                    chosen = lista_dificuldades[diff_index]
                    if chosen in ["Iniciante", "Intermediario", "Avancado", "Veterano"]:
                        dificuldade = chosen
                        running_diff = False
                    elif chosen == "Voltar":
                        running_diff = False

        clock.tick(60)

    return dificuldade