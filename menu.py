import pygame
import sys
from jogar import rodando

def menu_musicas(screen, clock, font, num_teclas, velocidade):
    # lista de músicas disponíveis
    lista_musicas = ["Song A", "Song B", "Song C"]
    music_index = 0
    running_music = True

    while running_music:
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
                    if music_index < len(lista_musicas):
                        musica_escolhida = lista_musicas[music_index]
                        dificuldade = escolher_dificuldade(screen, clock, font, musica_escolhida)
                        if dificuldade:  # se escolheu uma dificuldade válida
                            rodando(screen, clock, num_teclas, velocidade, dificuldade, musica_escolhida)
                    else:
                        running_music = False

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
                    chosen = diff_options[diff_index]
                    if chosen in ["Iniciante", "Intermediário", "Avançado", "Veterano"]:
                        dificuldade = chosen
                        running_diff = False
                    elif chosen == "Voltar":
                        running_diff = False

        clock.tick(60)

    return dificuldade
