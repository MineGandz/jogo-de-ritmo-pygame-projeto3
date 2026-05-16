import pygame
import os
import sys
from animacoes import fade_in, fade_out

def menu_pausa(screen, clock, font):
    pygame.mixer.music.pause()  # pausa música

    paused = True
    sair_do_jogo = False

    while paused:
        screen.fill((20, 20, 20))
        texto = font.render("Jogo Pausado", True, (255, 255, 255))
        continuar = font.render("Pressione C para continuar", True, (200, 200, 200))
        sair = font.render("Pressione Q para sair", True, (200, 200, 200))

        screen.blit(texto, (400, 150))
        screen.blit(continuar, (400, 250))
        screen.blit(sair, (400, 300))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair_do_jogo = True
                paused = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # continuar
                    pygame.mixer.music.unpause()  # retoma música
                    paused = False
                elif event.key == pygame.K_q:  # sair
                    sair_do_jogo = True
                    paused = False


    return sair_do_jogo

def rodando(screen, clock, font, velocidade, musica, dificuldade, voltar_menu):
    fade_in(screen, clock)
    # diretório dos assets do jogo
    ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "Songs", musica)

    # diretório da música
    dir_musica = os.path.join(ASSETS_DIR, musica + ".mp3")
    #carregando e dando play na música
    pygame.mixer.music.load(dir_musica)
    pygame.mixer.music.play()


    # definindo fonte do combo/pontuação/precisão
    font = pygame.font.SysFont("Consolas", 32)

    # definição das lanes(circulos vazios)
    lanes = [
        {"x": 768, "y": 800, "key": pygame.K_d},
        {"x": 896, "y": 800, "key": pygame.K_f},
        {"x": 1024, "y": 800, "key": pygame.K_j},
        {"x": 1152, "y": 800, "key": pygame.K_k},
    ]

    # definindo o que é uma nota
    class Note:
        def __init__(self, time, lane):
            self.time = time # tempo relação à música
            self.lane = lane # linha
            self.hit = False # acertada ou não

    # ler e traduzir arquivo .osu(mapa da música)
    def parse_osu_file(path, num_lanes=4):
        notes = []
        # definindo formatação do arquivo
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        hit_objects_section = False
        # passando pelas linhas do arquivo
        for line in lines:
            line = line.strip()
            # se for uma nota, a define
            if line == "[HitObjects]":
                hit_objects_section = True
                continue
            if hit_objects_section:
                # ignora linhas que não sejam notas
                if line == "" or line.startswith("["):
                    break
    # separando os aspectos da nota e definindo-os com base nos requisito da classe nota
                parts = line.split(",")
                if len(parts) >= 3:
                    x = int(parts[0])
                    time = int(parts[2])
                    lane = int(x / (512 / num_lanes))
                    notes.append(Note(time, lane))
        return notes
    # pegando o mapa das notas

    dir_mapa   = os.path.join(ASSETS_DIR, dificuldade + ".osu")
    notes = parse_osu_file(dir_mapa, num_lanes=4)
    
    # definindo variáveis essenciais
    running = True
    feedback_text = None
    feedback_timer = 0
    feedback_color = (255, 255, 255)
    combo_color = (255, 255, 255)

    # definindo valores iniciais
    combo = 0
    score = 0

    # definindo valores de pontuação
    total_notas = len(notes)
    # pontuação para cada julgamento(excellent, great, etc...)
    excellent = 1000000 // total_notas
    great = int(excellent * 0.5)
    good = int(excellent * 0.25)
    bad = int(excellent * 0.1)

    # totais de cada julgamento inicialmente
    total_excellent = total_great = total_good = total_bad = total_miss = 0

    # lane piscar quando aperta sem nota
    lane_flash = {i:0 for i in range(len(lanes))}

    # tamanho da música
    music_length = pygame.mixer.Sound(dir_musica).get_length()  # duração em segundos
    # loop do jogo geral
    while running:
        screen.fill((0,0,0))
        # posição atual na música
        current_time = pygame.mixer.music.get_pos() / 1000.0  # posição em segundos

        # posição atual na música
        current_time = pygame.mixer.music.get_pos() / 1000.0  # posição em segundos

        # desenhando lanes
        for i, lane in enumerate(lanes):
            fill_color = (255,255,255) if pygame.time.get_ticks() - lane_flash[i] < 150 else (48,48,48)
            pygame.draw.circle(screen, fill_color, (lane["x"], lane["y"]), 40)
            pygame.draw.circle(screen, (0,0,0), (lane["x"], lane["y"]), 40, 3)
        # desenhando notas
        appear_time = 1000-(velocidade*20) # tempo para notas aparecer
        for note in notes:
            if note.hit: 
                continue
            dt = note.time/1000.0 - current_time  # nota.time está em ms -> converter para segundos
            if dt < -0.2:  # passou da janela
                feedback_text = "Miss!"
                feedback_color = (139,0,0)
                feedback_timer = pygame.time.get_ticks()
                note.hit = True
                combo = 0
                total_miss += 1
                continue
            progress = 1 - (dt / (appear_time/1000.0)) # onde a nota tá na tela
            if 0 <= progress <= 1.2:
                y = -50 + progress * (lanes[note.lane]["y"] + 50) # nota caindo
                pygame.draw.circle(screen, (93,136,150), (lanes[note.lane]["x"], int(y)), 40) # desenha a nota na nova posição

        # input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                #Tecla para dar reset (tecla de aspas: ' )
                if event.key == pygame.K_QUOTE:
                    #reset para a música e a roda de novo
                    pygame.mixer.music.stop()
                    rodando(screen, clock, font, velocidade, musica, dificuldade, voltar_menu)
                if event.key == pygame.K_ESCAPE:
                    if menu_pausa(screen, clock, font):
                        voltar_menu(screen, clock, font, velocidade)
                for lane_index, lane in enumerate(lanes):
                    if event.key == lane["key"]:
                        found_note = False
                        for note in notes:
                            if note.lane == lane_index and not note.hit:
                                delta = note.time/1000.0 - current_time
                                if -0.3 <= delta <= 0.250:
                                    found_note = True
                                    delta_abs = abs(delta*1000)  # em ms para julgamento
                                    # vendo qual julgamento atribuir baseado no delta
                                    if delta_abs < 30:
                                        feedback_text, feedback_color = "Excellent", (173,216,230)
                                        score += excellent
                                        combo += 1
                                        note.hit = True
                                        total_excellent += 1
                                    elif delta_abs < 60:
                                        feedback_text, feedback_color = "Great", (144,238,144)
                                        score += great
                                        combo += 1 
                                        note.hit = True
                                        total_great += 1
                                    elif delta_abs < 100:
                                        feedback_text, feedback_color = "Good", (70,130,180)
                                        score += good
                                        combo += 1
                                        note.hit = True
                                        total_good += 1
                                    elif delta_abs < 150:
                                        feedback_text, feedback_color = "Bad", (138,43,226)
                                        score += bad
                                        combo += 1
                                        note.hit = True
                                        total_bad += 1
                                    else:
                                        feedback_text, feedback_color = "Miss", (139,0,0)
                                        combo = 0
                                        note.hit = True
                                        total_miss += 1
                                    feedback_timer = pygame.time.get_ticks()
                                    lane_flash[lane_index] = pygame.time.get_ticks()
                                    break
                                # fazer lane piscar
                                elif delta < -0.3:
                                    found_note = True
                                    lane_flash[lane_index] = pygame.time.get_ticks()
                                    break
                        # lane piscar
                        if not found_note:
                            lane_flash[lane_index] = pygame.time.get_ticks()

        # centro
        center_x = screen.get_width()//2
        center_y = screen.get_height()//2
        left_lane_x = lanes[0]["x"]-100

        # combo colorido (se chegou 1/4 da música ele colore o combo dependendo do seu desempenho)
        if combo >= len(notes)*0.25:
            if total_great==0 and total_good==0 and total_bad==0 and total_miss==0:
                combo_color = (173,216,230)
            elif total_good==0 and total_bad==0 and total_miss==0:
                combo_color = (144,238,144)
            elif total_miss==0:
                combo_color = (200,200,0)

        combo_surface = font.render(f"{combo}", True, combo_color)
        screen.blit(combo_surface, (center_x - combo_surface.get_width()//2, center_y - 40))

        # quantos acertos até agora
        total_hits = total_excellent + total_great + total_good + total_bad + total_miss

        # precisão calculos avançados chatos demais
        max_points = (total_hits + total_miss) * excellent

        # precisão baseada em pontos
        accuracy = (score / max_points * 100) if max_points > 0 else 100

        accuracy_surface = font.render(f"{accuracy:.2f}%", True, (255,255,255))
        screen.blit(accuracy_surface, (1400, 200))

        # feedback
        if feedback_text:
            if pygame.time.get_ticks() - feedback_timer < 500:
                text_surface = font.render(feedback_text, True, feedback_color)
                screen.blit(text_surface, (center_x - text_surface.get_width()//2, center_y + 10))
            else:
                feedback_text = None

        # score
        score_surface = font.render(f"{score:,}".replace(",", "'"), True, (255,255,255))
        screen.blit(score_surface, (left_lane_x - 150, center_y))

        # barra de progresso inferior central
        progress = current_time / music_length
        bar_width, bar_height = 600, 10
        bar_x = 660
        bar_y = 900
        pygame.draw.rect(screen, (80,80,80), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0,150,150), (bar_x, bar_y, int(bar_width*progress), bar_height))

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()
