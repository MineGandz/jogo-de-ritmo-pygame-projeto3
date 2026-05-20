import pygame
import os
import sys
from animacoes import fade_in, fade_out

#funcao que mostra a pontuacao obtida
def resultado(screen, clock, font, score, accuracy,
              total_excellent, total_great, total_good, total_bad, total_miss,
              replay_callback, voltar_menu_callback, max_combo):
    showing = True
    while showing:
        screen.fill((30, 30, 30))  # fundo escuro

        # painel central
        panel_width, panel_height = 600, 520
        panel_x = screen.get_width()//2 - panel_width//2
        panel_y = screen.get_height()//2 - panel_height//2
        pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))  # retângulo cinza
        pygame.draw.rect(screen, (200, 0, 0), (panel_x, panel_y, panel_width, panel_height), 4)  # borda vermelha

        # título
        titulo = font.render("Resultado", True, (255, 255, 255))
        screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, panel_y + 40))

        # pontuação
        score_text = font.render(f"Pontuação: {score:,}".replace(",", "."), True, (255, 255, 255))
        screen.blit(score_text, (screen.get_width()//2 - score_text.get_width()//2, panel_y + 120))

        # precisão
        acc_text = font.render(f"Precisão: {accuracy:.2f}%", True, (255, 255, 255))
        screen.blit(acc_text, (screen.get_width()//2 - acc_text.get_width()//2, panel_y + 170))

        # combo máximo (com espaço próprio)
        combo_text = font.render(f"Combo Máximo: {max_combo}", True, (255, 255, 0))
        screen.blit(combo_text, (screen.get_width()//2 - combo_text.get_width()//2, panel_y + 220))

        # estatísticas (descem um pouco para não colar no combo)
        stats = [
            (f"Excellent: {total_excellent}", (173,216,230)),
            (f"Great: {total_great}", (144,238,144)),
            (f"Good: {total_good}", (70,130,180)),
            (f"Bad: {total_bad}", (138,43,226)),
            (f"Miss: {total_miss}", (139,0,0))
        ]
        for i, (texto, cor) in enumerate(stats):
            surf = font.render(texto, True, cor)
            screen.blit(surf, (screen.get_width()//2 - surf.get_width()//2, panel_y + 270 + i*40))

        # instruções em quadradinhos
        instr_font = pygame.font.SysFont("Consolas", 24)
        options = [
            ("Menu - ENTER", (200,200,200)),
            ("Replay - R", (200,200,200)),
            ("Sair do Jogo - Q", (200,200,200))
        ]

        rendered = [instr_font.render(txt, True, cor) for txt, cor in options]
        rects = [surf.get_rect() for surf in rendered]
        total_width = sum(r.width for r in rects) + (len(rects)-1)*40 + len(rects)*20
        start_x = screen.get_width()//2 - total_width//2
        y = panel_y + panel_height + 40

        # desenhar centralizado
        x = start_x
        for surf in rendered:
            rect = surf.get_rect(topleft=(x+10, y+5))
            box_rect = pygame.Rect(x, y, rect.width+20, rect.height+10)
            pygame.draw.rect(screen, (50,50,50), box_rect, border_radius=8)
            pygame.draw.rect(screen, (200,0,0), box_rect, 2, border_radius=8)
            screen.blit(surf, rect)
            x += rect.width + 60

        pygame.display.flip()
        clock.tick(60)

        # entradas do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showing = False
                return "sair"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    voltar_menu_callback(screen, clock, font, 1.0)
                    return "menu"
                elif event.key == pygame.K_r:
                    replay_callback()
                    return "replay"
                elif event.key == pygame.K_q:
                    return "sair"



#funcao de pause durante a musica
def menu_pausa(screen, clock, font):
    pygame.mixer.music.pause()  # pausa música

    paused = True
    sair_do_jogo = False
    resetar = False

    while paused:
        screen.fill((30, 30, 30))  # fundo escuro

        # painel central
        panel_width, panel_height = 500, 400
        panel_x = screen.get_width()//2 - panel_width//2
        panel_y = screen.get_height()//2 - panel_height//2
        pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (200, 0, 0), (panel_x, panel_y, panel_width, panel_height), 4)

        # título
        titulo = font.render("Jogo Pausado", True, (255, 255, 255))
        screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, panel_y + 40))

        # botões com atalhos
        opcoes = [
            ("Continuar [C]", (200, 200, 200)),
            ("Sair [Q]", (200, 200, 200)),
            ("Resetar [R]", (200, 200, 200))
        ]

        button_width, button_height = 300, 60
        spacing = 80
        for i, (texto, cor) in enumerate(opcoes):
            bx = screen.get_width()//2 - button_width//2
            by = panel_y + 120 + i*spacing

            pygame.draw.rect(screen, (80, 80, 80), (bx, by, button_width, button_height))
            pygame.draw.rect(screen, (255, 255, 255), (bx, by, button_width, button_height), 2)

            surf = font.render(texto, True, cor)
            screen.blit(surf, (bx + button_width//2 - surf.get_width()//2,
                               by + button_height//2 - surf.get_height()//2))

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
                elif event.key == pygame.K_r:  # resetar
                    resetar = True
                    paused = False

    #retorna a opcao escolhida
    if sair_do_jogo:
        return "sair"
    elif resetar:
        return "reset"
    else:
        return "continuar"

#funcao principal do jogo que mantém rodando
def rodando(screen, clock, font, velocidade, musica, dificuldade, voltar_menu):
    fade_in(screen, clock)
    ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "Songs", musica)
    dir_musica = os.path.join(ASSETS_DIR, musica + ".mp3")
    pygame.mixer.music.load(dir_musica)

    font = pygame.font.SysFont("Consolas", 32)

    lanes = [
        {"x": 768, "y": 800, "key": pygame.K_d},
        {"x": 896, "y": 800, "key": pygame.K_f},
        {"x": 1024, "y": 800, "key": pygame.K_j},
        {"x": 1152, "y": 800, "key": pygame.K_k},
    ]
    lane_flash = {i:0 for i in range(len(lanes))}

    # valores iniciais
    combo = 0
    max_combo = 0
    score = 0
    total_excellent = total_great = total_good = total_bad = total_miss = 0
    accuracy = 100.0
    feedback_text = None
    feedback_color = (255,255,255)
    feedback_timer = 0
    combo_color = (255,255,255)
    music_length = pygame.mixer.Sound(dir_musica).get_length()

    # --- Delay de 2 segundos com HUD e lanes ---
    start_ticks = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_ticks < 2000:
        screen.fill((0,0,0))

        # desenhar lanes
        for i, lane in enumerate(lanes):
            fill_color = (255,255,255) if pygame.time.get_ticks() - lane_flash[i] < 150 else (48,48,48)
            pygame.draw.circle(screen, fill_color, (lane["x"], lane["y"]), 40)
            pygame.draw.circle(screen, (0,0,0), (lane["x"], lane["y"]), 40, 3)

        # centro
        center_x = screen.get_width()//2
        center_y = screen.get_height()//2
        left_lane_x = lanes[0]["x"]-100

        # combo
        combo_surface = font.render(f"{combo}", True, combo_color)
        screen.blit(combo_surface, (center_x - combo_surface.get_width()//2, center_y - 40))

        # precisão
        accuracy_surface = font.render(f"{accuracy:.2f}%", True, (255,255,255))
        screen.blit(accuracy_surface, (1400, 200))

        # feedback (se houver)
        if feedback_text:
            if pygame.time.get_ticks() - feedback_timer < 500:
                text_surface = font.render(feedback_text, True, feedback_color)
                screen.blit(text_surface, (center_x - text_surface.get_width()//2, center_y + 10))
            else:
                feedback_text = None

        # score
        score_surface = font.render(f"{score:,}".replace(",", "'"), True, (255,255,255))
        screen.blit(score_surface, (left_lane_x - 150, center_y))

        # barra de progresso inferior central (fica zerada no delay)
        progress = 0
        bar_width, bar_height = 600, 10
        bar_x = 660
        bar_y = 900
        pygame.draw.rect(screen, (80,80,80), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0,150,150), (bar_x, bar_y, int(bar_width*progress), bar_height))

        pygame.display.flip()
        clock.tick(60)

        # permitir flash das lanes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                for lane_index, lane in enumerate(lanes):
                    if event.key == lane["key"]:
                        lane_flash[lane_index] = pygame.time.get_ticks()

    # só depois do delay toca a música
    pygame.mixer.music.play()

    # carregar notas
    class Note:
        def __init__(self, time, lane):
            self.time = time
            self.lane = lane
            self.hit = False

    def parse_osu_file(path, num_lanes=4):
        notes = []
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        hit_objects_section = False
        for line in lines:
            line = line.strip()
            if line == "[HitObjects]":
                hit_objects_section = True
                continue
            if hit_objects_section:
                if line == "" or line.startswith("["):
                    break
                parts = line.split(",")
                if len(parts) >= 3:
                    x = int(parts[0])
                    time = int(parts[2])
                    lane = int(x / (512 / num_lanes))
                    notes.append(Note(time, lane))
        return notes

    dir_mapa = os.path.join(ASSETS_DIR, dificuldade + ".osu")
    notes = parse_osu_file(dir_mapa, num_lanes=4)

    # --- Ajuste para sincronizar notas com o delay ---
    delay_ms = 2000
    for note in notes:
        note.time += delay_ms
    
    # definindo variáveis essenciais
    running = True
    feedback_text = None
    feedback_timer = 0
    feedback_color = (255, 255, 255)
    combo_color = (255, 255, 255)

    # definindo valores iniciais
    combo = 0
    max_combo = 0
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
        posicao = pygame.mixer.music.get_pos()
        if posicao == -1:
            current_time = music_length  # força como se tivesse acabado
        else:
            current_time = posicao / 1000.0  # posição em segundos

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
                    acao = menu_pausa(screen, clock, font)
                    if acao == "sair":
                        pygame.mixer.music.stop()
                        return  # volta para o menu principal
                    elif acao == "reset":
                        pygame.mixer.music.stop()
                        #chama a musica para rodar denovo
                        return rodando(screen, clock, font, velocidade, musica, dificuldade, voltar_menu)
                    elif acao == "continuar":
                        # não faz nada, apenas segue o loop normalmente
                        continue
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
                                    if delta_abs < 40:
                                        feedback_text, feedback_color = "Excellent", (173,216,230)
                                        score += excellent
                                        combo += 1
                                        if combo > max_combo:
                                            max_combo = combo
                                        note.hit = True
                                        total_excellent += 1
                                    elif delta_abs < 75:
                                        feedback_text, feedback_color = "Great", (144,238,144)
                                        score += great
                                        combo += 1 
                                        note.hit = True
                                        total_great += 1
                                    elif delta_abs < 120:
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

        #checagem do fim da música para exibir a pontuacao
        if current_time == -1 or current_time >= music_length:
            acao = resultado(screen, clock, font, score, accuracy,
                     total_excellent, total_great, total_good, total_bad, total_miss,
                     lambda: rodando(screen, clock, font, velocidade, musica, dificuldade, voltar_menu),
                     voltar_menu,
                     max_combo)

            if acao == "sair":
                pygame.quit()
                return  # fecha jogo
            elif acao == "menu":
                return voltar_menu(screen, clock, font, 1.0)  # volta pro menu principal
            elif acao == "replay":
                return rodando(screen, clock, font, velocidade, musica, dificuldade, voltar_menu) #toca a musica de novo

