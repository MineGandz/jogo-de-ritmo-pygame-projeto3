import pygame
import sys
import os

#importacao de funcoes
from jogar import rodando
from animacoes import fade_in, fade_out
from leaderboard import leaderboard

def carregar_musicas(assets_dir):
    # pega todas as pastas dentro de assets_dir
    lista_musicas = []
    for item in os.listdir(assets_dir):
        caminho = os.path.join(assets_dir, item)
        if os.path.isdir(caminho):  # verifica se é pasta
            lista_musicas.append(item)
    return lista_musicas


def carregar_osu(msc_dir):
    # pega todos os arquivos .osu dentro de msc_dir
    lista_osu = []
    for item in os.listdir(msc_dir):
        caminho = os.path.join(msc_dir, item)
        if os.path.isfile(caminho) and item.lower().endswith(".osu"):
            lista_osu.append(item)
    return lista_osu

def menu_musicas(screen, clock, font, velocidade, nome):
    fade_in(screen, clock)
    # diretório assets
    MSC_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "Songs")
    
    lista_musicas = carregar_musicas(MSC_DIR)
    music_index = 0
    scroll_offset = 0   # deslocamento vertical da lista
    running_musica = True

    while running_musica:
        screen.fill((0,0,0))  # fundo preto uniforme
        title_surface = font.render("Seleção de Música", True, (255,255,0))
        screen.blit(title_surface, (screen.get_width()//2 - title_surface.get_width()//2, 150))

        # mostrar músicas + opção Voltar
        opcoes = lista_musicas + ["Voltar"]
        for i, option in enumerate(opcoes):
            y = 300 + i*80 - scroll_offset   # posição ajustada pelo scroll
            if 200 < y < screen.get_height()-100:  # só desenha se estiver visível
                color = (0,255,0) if i == music_index else (255,255,255)
                text_surface = font.render(option, True, color)
                screen.blit(text_surface, (screen.get_width()//2 - text_surface.get_width()//2, y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    music_index += 1
                    if music_index > len(opcoes)-1:  # passou da última opção
                        music_index = 0
                        scroll_offset = 0  # volta a lista pro topo
                    elif 300 + music_index*80 - scroll_offset > screen.get_height()-150:
                        scroll_offset += 80

                elif event.key == pygame.K_UP:
                    music_index -= 1
                    if music_index < 0:  # passou do topo
                        music_index = len(opcoes)-1  # vai pra última opção
                        # ajusta scroll para mostrar o fim da lista
                        scroll_offset = max(0, (len(opcoes))*80 - (screen.get_height()-450))
                    elif 300 + music_index*80 - scroll_offset < 250:
                        scroll_offset -= 80

                elif event.key == pygame.K_RETURN:
                    fade_out(screen, clock)
                    if music_index < len(lista_musicas):
                        musica_escolhida = lista_musicas[music_index]
                        dificuldade = escolher_dificuldade(screen, clock, font, musica_escolhida)
                        if dificuldade:  # se escolheu uma dificuldade válida
                            acao = painel_opcoes(screen, clock, font, musica_escolhida, dificuldade)
                            #se escolheu jogar, abre o jogo
                            if acao == "jogar":
                                rodando(screen, clock, font, velocidade, musica_escolhida, dificuldade, nome, voltar_menu=menu_musicas)
                            #mostra as melhores pontuacoes
                            elif acao == "leaderboard":
                                leaderboard(screen, clock, font, musica_escolhida, dificuldade)
                            #volta pra selecao de dificuldade
                            elif acao == "voltar":
                                # volta para seleção de dificuldade
                                dificuldade = escolher_dificuldade(screen, clock, font, musica_escolhida)
                                if dificuldade:
                                    acao = painel_opcoes(screen, clock, font, musica_escolhida, dificuldade)
                    else:
                        # opção "Voltar"
                        running_musica = False
                        return "voltar"   # <-- retorna para o main

        clock.tick(60)


def escolher_dificuldade(screen, clock, font, musica):
    diff_index = 0
    running_diff = True
    dificuldade = None

    dir_diff = os.path.join(os.path.dirname(__file__), "..", "assets", "Songs", musica)
    diff_options=carregar_osu(dir_diff)
    diff_options = [arq.replace(".osu", "") for arq in diff_options]

    item = diff_options.pop(0) 
    diff_options.insert(2, item)  # insere na posição 2arquivos = ["Avancado.osu", "Iniciante.osu", "Intermediario.osu", "Veterano.osu"]
    lista_dificuldades = diff_options
    

    while running_diff:
        screen.fill((0,0,0))  # fundo preto uniforme
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
                    chosen = lista_dificuldades[diff_index]
                    if chosen in ["Iniciante", "Intermediario", "Avançado", "Veterano"]:
                        dificuldade = chosen
                        running_diff = False
                    elif chosen == "Voltar":
                        running_diff = False

        clock.tick(60)

    return dificuldade

#opcao de jogar ou abrir leaderboard
def painel_opcoes(screen, clock, font, musica, dificuldade):
    opcoes = ["Jogar", "Leaderboard", "Voltar"]
    selecionado = 0
    ativo = True

    while ativo:
        screen.fill((30,30,30))

        # título fora da caixa (azul, mais baixo)
        titulo = font.render(f"{musica} - {dificuldade}", True, (0,128,255))
        screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 160))

        # painel central (subindo um pouco pra ficar perto do título)
        panel_width, panel_height = 600, 400
        panel_x = screen.get_width()//2 - panel_width//2
        panel_y = screen.get_height()//2 - panel_height//2 + 40
        pygame.draw.rect(screen, (50,50,50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (200,0,0), (panel_x, panel_y, panel_width, panel_height), 4)

        # opções centralizadas dentro da caixa
        for i, opcao in enumerate(opcoes):
            cor = (255,255,0) if i == selecionado else (200,200,200)
            texto = font.render(opcao, True, cor)
            screen.blit(texto, (screen.get_width()//2 - texto.get_width()//2, panel_y + 100 + i*60))

        # instrução
        instr_font = pygame.font.SysFont("Consolas", 24)
        sair_text = instr_font.render("ENTER para confirmar", True, (180,180,180))
        screen.blit(sair_text, (screen.get_width()//2 - sair_text.get_width()//2, panel_y + panel_height - 40))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif event.key == pygame.K_RETURN:
                    return opcoes[selecionado].lower()