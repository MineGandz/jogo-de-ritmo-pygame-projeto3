import pygame
import os
import sys
from animacoes import fade_in, fade_out
from leaderboard import salvar_resultado, leaderboard


# exibe a tela de resultado ao final da música
def resultado(screen, clock, font, score, accuracy,
              total_excellent, total_great, total_good, total_bad, total_miss,
              replay_callback, voltar_menu_callback, max_combo, dificuldade, musica, nome):

    # salva o resultado no leaderboard
    salvar_resultado(nome, musica, dificuldade, score, accuracy, max_combo)

    showing = True
    while showing:
        # preenche o fundo
        screen.fill((30, 30, 30))

        # calcula posição do painel central
        panel_width, panel_height = 600, 520
        panel_x = screen.get_width() // 2 - panel_width // 2
        panel_y = screen.get_height() // 2 - panel_height // 2

        # desenha o painel e sua borda
        pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (200, 0, 0), (panel_x, panel_y, panel_width, panel_height), 4)

        # título do painel
        titulo = font.render("Resultado", True, (255, 255, 255))
        screen.blit(titulo, (screen.get_width() // 2 - titulo.get_width() // 2, panel_y + 40))

        # exibe pontuação formatada
        score_text = font.render(f"Pontuação: {score:,}".replace(",", "."), True, (255, 255, 255))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, panel_y + 120))

        # exibe precisão percentual
        acc_text = font.render(f"Precisão: {accuracy:.2f}%", True, (255, 255, 255))
        screen.blit(acc_text, (screen.get_width() // 2 - acc_text.get_width() // 2, panel_y + 170))

        # exibe combo máximo
        combo_text = font.render(f"Combo Máximo: {max_combo}", True, (255, 255, 0))
        screen.blit(combo_text, (screen.get_width() // 2 - combo_text.get_width() // 2, panel_y + 220))

        # lista de estatísticas com cores por julgamento
        stats = [
            (f"Excellent: {total_excellent}", (173, 216, 230)),
            (f"Great: {total_great}", (144, 238, 144)),
            (f"Good: {total_good}", (70, 130, 180)),
            (f"Bad: {total_bad}", (138, 43, 226)),
            (f"Miss: {total_miss}", (139, 0, 0))
        ]
        for i, (texto, cor) in enumerate(stats):
            surf = font.render(texto, True, cor)
            screen.blit(surf, (screen.get_width() // 2 - surf.get_width() // 2, panel_y + 270 + i * 40))

        # fonte menor para os botões de ação
        instr_font = pygame.font.SysFont("Consolas", 24)
        options = [
            ("Menu - ENTER", (200, 200, 200)),
            ("Replay - R", (200, 200, 200)),
            ("Sair do Jogo - Q", (200, 200, 200))
        ]

        # renderiza os textos dos botões
        rendered = [instr_font.render(txt, True, cor) for txt, cor in options]
        rects = [surf.get_rect() for surf in rendered]
        total_width = sum(r.width for r in rects) + (len(rects) - 1) * 40 + len(rects) * 20
        start_x = screen.get_width() // 2 - total_width // 2
        y = panel_y + panel_height + 40

        # desenha cada botão com borda
        x = start_x
        for surf in rendered:
            rect = surf.get_rect(topleft=(x + 10, y + 5))
            box_rect = pygame.Rect(x, y, rect.width + 20, rect.height + 10)
            pygame.draw.rect(screen, (50, 50, 50), box_rect, border_radius=8)
            pygame.draw.rect(screen, (200, 0, 0), box_rect, 2, border_radius=8)
            screen.blit(surf, rect)
            x += rect.width + 60

        pygame.display.flip()
        clock.tick(60)

        # lida com eventos da tela de resultado
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


# exibe o menu de pausa e aguarda ação do jogador
def menu_pausa(screen, clock, font):

    # pausa o áudio imediatamente
    pygame.mixer.music.pause()

    paused = True
    sair_do_jogo = False
    resetar = False

    while paused:
        # fundo escuro
        screen.fill((30, 30, 30))

        # calcula posição do painel central
        panel_width, panel_height = 500, 400
        panel_x = screen.get_width() // 2 - panel_width // 2
        panel_y = screen.get_height() // 2 - panel_height // 2

        # desenha o painel e sua borda
        pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (200, 0, 0), (panel_x, panel_y, panel_width, panel_height), 4)

        # título do painel
        titulo = font.render("Jogo Pausado", True, (255, 255, 255))
        screen.blit(titulo, (screen.get_width() // 2 - titulo.get_width() // 2, panel_y + 40))

        # opções do menu de pausa
        opcoes = [
            ("Continuar [C]", (200, 200, 200)),
            ("Sair [Q]", (200, 200, 200)),
            ("Resetar [R]", (200, 200, 200))
        ]

        # desenha os botões das opções
        button_width, button_height = 300, 60
        spacing = 80
        for i, (texto, cor) in enumerate(opcoes):
            bx = screen.get_width() // 2 - button_width // 2
            by = panel_y + 120 + i * spacing
            pygame.draw.rect(screen, (80, 80, 80), (bx, by, button_width, button_height))
            pygame.draw.rect(screen, (255, 255, 255), (bx, by, button_width, button_height), 2)
            surf = font.render(texto, True, cor)
            screen.blit(surf, (bx + button_width // 2 - surf.get_width() // 2,
                               by + button_height // 2 - surf.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

        # lida com eventos do menu de pausa
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair_do_jogo = True
                paused = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pygame.mixer.music.unpause()
                    paused = False
                elif event.key == pygame.K_q:
                    sair_do_jogo = True
                    paused = False
                elif event.key == pygame.K_r:
                    resetar = True
                    paused = False

    # retorna a ação escolhida pelo jogador
    if sair_do_jogo:
        return "sair"
    elif resetar:
        return "reset"
    else:
        return "continuar"


# exibe a tela de ajuda com instruções do jogo
def ajuda(screen, clock, font):
    showing = True
    while showing:
        # fundo escuro
        screen.fill((30, 30, 30))

        # calcula posição do painel central
        panel_width, panel_height = 700, 500
        panel_x = screen.get_width()//2 - panel_width//2
        panel_y = screen.get_height()//2 - panel_height//2

        # desenha o painel e sua borda
        pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (200, 0, 0), (panel_x, panel_y, panel_width, panel_height), 4)

        # título do painel
        titulo = font.render("Ajuda", True, (255, 255, 255))
        screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, panel_y + 40))

        # fonte menor para instruções
        instr_font = pygame.font.SysFont("Consolas", 26)

        # texto explicando as teclas
        texto_teclas = instr_font.render("Teclas para jogar:", True, (255,255,0))
        screen.blit(texto_teclas, (screen.get_width()//2 - texto_teclas.get_width()//2, panel_y + 100))

        # círculos representando as lanes com as teclas correspondentes
        lanes = [
            {"x": screen.get_width()//2 - 150, "y": panel_y + 180, "key": "D"},
            {"x": screen.get_width()//2 - 50,  "y": panel_y + 180, "key": "F"},
            {"x": screen.get_width()//2 + 50,  "y": panel_y + 180, "key": "J"},
            {"x": screen.get_width()//2 + 150, "y": panel_y + 180, "key": "K"},
        ]
        for lane in lanes:
            pygame.draw.circle(screen, (93,136,150), (lane["x"], lane["y"]), 40)
            pygame.draw.circle(screen, (0,0,0), (lane["x"], lane["y"]), 40, 3)
            letra = font.render(lane["key"], True, (255,255,255))
            screen.blit(letra, (lane["x"] - letra.get_width()//2, lane["y"] - letra.get_height()//2))

        # instrução de pausa
        esc_text = instr_font.render("ESC → Pausar o jogo", True, (200,200,200))
        screen.blit(esc_text, (screen.get_width()//2 - esc_text.get_width()//2, panel_y + 250))

        # dicas em duas linhas
        dica1 = instr_font.render("Dica: Acerte no tempo certo", True, (200,200,200))
        dica2 = instr_font.render("para ganhar mais pontos!", True, (200,200,200))
        screen.blit(dica1, (screen.get_width()//2 - dica1.get_width()//2, panel_y + 300))
        screen.blit(dica2, (screen.get_width()//2 - dica2.get_width()//2, panel_y + 330))

        # instrução para fechar a ajuda
        sair_text = instr_font.render("ENTER para voltar", True, (180,180,180))
        screen.blit(sair_text, (panel_x + panel_width - sair_text.get_width() - 20,
                                panel_y + panel_height - 30))

        pygame.display.flip()
        clock.tick(60)

        # lida com eventos da tela de ajuda
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showing = False
                return "sair"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    return "menu"


# loop principal do jogo: carrega mapa, toca música e processa notas
def rodando(screen, clock, font, velocidade, musica, dificuldade, nome, voltar_menu):
    while True:
        fade_in(screen, clock)

        # monta caminhos para o arquivo de música e o mapa .osu
        ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "Songs", musica)
        dir_musica = os.path.join(ASSETS_DIR, musica + ".mp3")
        dir_mapa = os.path.join(ASSETS_DIR, dificuldade + ".osu")

        # carrega a música e obtém sua duração
        pygame.mixer.music.load(dir_musica)
        music_length = pygame.mixer.Sound(dir_musica).get_length()

        # fonte usada durante o jogo
        font = pygame.font.SysFont("Consolas", 32)

        # posição x de cada lane e tecla correspondente
        lanes = [
            {"x": 768,  "y": 800, "key": pygame.K_d},
            {"x": 896,  "y": 800, "key": pygame.K_f},
            {"x": 1024, "y": 800, "key": pygame.K_j},
            {"x": 1152, "y": 800, "key": pygame.K_k},
        ]

        # dicionário que armazena o instante do último flash de cada lane
        lane_flash = {i: 0 for i in range(len(lanes))}
        # dicionário que armazena o instante do último miss em cada lane (flash vermelho)
        miss_flash = {i: 0 for i in range(len(lanes))}

        # inicializa contadores de jogo
        combo = 0
        max_combo = 0
        score = 0
        total_excellent = total_great = total_good = total_bad = total_miss = 0
        accuracy = 100.0
        feedback_text = None
        feedback_color = (255, 255, 255)
        feedback_timer = 0
        combo_color = (255, 255, 255)
        # escala atual do combo para animação de pulso
        combo_scale  = 1.0
        # instante em que o último pulso foi disparado
        combo_pulse_timer = 0

        # representa uma nota do mapa com tempo, lane e cor de snap
        class Note:
            def __init__(self, time, lane):
                self.time  = time            # tempo em ms em que a nota deve ser acertada
                self.lane  = lane            # índice da lane (0-3)
                self.hit   = False           # True quando acertada ou virou miss
                self.color = (93, 136, 150)  # cor de snap, definida no parse

        # tabela de cores por subdivisão rítmica — padrão Etterna/StepMania
        SNAP_COLORS = {
            1:  (255,  50,  50),   # 4th   — vermelho
            2:  ( 50, 100, 255),   # 8th   — azul
            3:  (180,   0, 255),   # 12th  — roxo
            4:  (255, 220,   0),   # 16th  — amarelo
            6:  (255, 100, 180),   # 24th  — rosa
            8:  (255, 140,   0),   # 32nd  — laranja
            12: (  0, 220, 220),   # 48th  — ciano
            16: (  0, 210,  80),   # 64th  — verde
        }
        SNAP_COLOR_DEFAULT = (200, 200, 200)  # 96th+ — branco/cinza

        def get_snap_color(note_time_ms, beat_length_ms, timing_offset_ms):
            # cada beat é dividido em 64 unidades (menor subdivisão usada)
            beat_length_64th = beat_length_ms / 64.0
            delta    = note_time_ms - timing_offset_ms
            # posição dentro do beat atual em unidades de 64th
            position = round(delta / beat_length_64th) % 64
            # percorre divisores do mais raro ao mais comum para achar o snap correto
            for divisor in sorted(SNAP_COLORS.keys()):
                unit = 64 // divisor
                if position % unit == 0:
                    return SNAP_COLORS[divisor]
            return SNAP_COLOR_DEFAULT

        # lê o arquivo .osu, extrai o BPM do TimingPoints e converte HitObjects em notas
        def parse_osu_file(path, num_lanes=4):
            notes            = []
            timing_offset_ms = 0.0    # offset do primeiro timing point em ms
            beat_length_ms   = 500.0  # duração de um beat em ms (padrão: 120 BPM)

            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # primeira passagem: lê o primeiro timing point uninherited para obter o BPM
            timing_section = False
            for line in lines:
                line = line.strip()
                if line == "[TimingPoints]":
                    timing_section = True
                    continue
                if timing_section:
                    if line == "" or line.startswith("["):
                        break
                    parts = line.split(",")
                    if len(parts) >= 2:
                        offset      = float(parts[0])
                        beat_len    = float(parts[1])
                        uninherited = int(parts[6]) if len(parts) > 6 else 1
                        # timing point uninherited (beat_length > 0) define o BPM real
                        if uninherited == 1 and beat_len > 0:
                            timing_offset_ms = offset
                            beat_length_ms   = beat_len
                            break

            # segunda passagem: lê os hit objects e calcula a cor de snap de cada nota
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
                        x    = int(parts[0])
                        time = int(parts[2])
                        # converte coordenada x (0-512) para índice de lane (0-3)
                        lane = int(x / (512 / num_lanes))
                        lane = max(0, min(lane, num_lanes - 1))
                        n        = Note(time, lane)
                        n.color  = get_snap_color(time, beat_length_ms, timing_offset_ms)
                        notes.append(n)
            return notes

        # carrega as notas com cores de snap calculadas a partir do .osu
        notes = parse_osu_file(dir_mapa, num_lanes=4)

        note_offset_ms = 120

        # garante pelo menos 1 nota para evitar divisão por zero
        total_notas = len(notes) if len(notes) > 0 else 1

        # pontuação máxima por nota de acordo com o julgamento
        excellent = 1000000 // total_notas
        great     = int(excellent * 0.5)
        good      = int(excellent * 0.25)
        bad       = int(excellent * 0.1)

        # tempo de viagem das notas do topo até a lane, em ms
        # quanto maior a velocidade, menor o appear_time (notas caem mais rápido)
        appear_time = max(1000 - (velocidade * 20), 200)
        travel_time = appear_time / 1000.0  # converte para segundos

        # posição y de onde as notas nascem (acima da tela) e onde devem ser acertadas
        spawn_y = -80
        hit_y   = lanes[0]["y"]

        # o countdown dura exatamente appear_time ms:
        # assim, quando current_time = 0 (música começa), a primeira nota que tem
        # spawn_time = 0 já está no topo e chega na lane no tempo exato.
        countdown_ms = appear_time

        # --- countdown inicial antes da música ---
        start_ticks = pygame.time.get_ticks()
        lane_flash = {i: 0 for i in range(len(lanes))}

        while pygame.time.get_ticks() - start_ticks < countdown_ms:
            screen.fill((0, 0, 0))

            # desenha as lanes; pisca de branco se flash ativo
            for i, lane in enumerate(lanes):
                fill_color = (255, 255, 255) if pygame.time.get_ticks() - lane_flash[i] < 150 else (48, 48, 48)
                pygame.draw.circle(screen, fill_color, (lane["x"], lane["y"]), 40)
                pygame.draw.circle(screen, (0, 0, 0), (lane["x"], lane["y"]), 40, 3)

            # referências de posição para HUD
            center_x    = screen.get_width() // 2
            center_y    = screen.get_height() // 2
            left_lane_x = lanes[0]["x"] - 100

            # exibe combo atual
            combo_surface = font.render(f"{combo}", True, combo_color)
            screen.blit(combo_surface, (center_x - combo_surface.get_width() // 2, center_y - 40))

            # exibe precisão atual
            accuracy_surface = font.render(f"{accuracy:.2f}%", True, (255, 255, 255))
            screen.blit(accuracy_surface, (1400, 200))

            # exibe feedback de julgamento se ainda estiver no tempo
            if feedback_text:
                if pygame.time.get_ticks() - feedback_timer < 500:
                    text_surface = font.render(feedback_text, True, feedback_color)
                    screen.blit(text_surface, (center_x - text_surface.get_width() // 2, center_y + 10))
                else:
                    feedback_text = None

            # exibe score atual
            score_surface = font.render(f"{score:,}".replace(",", "'"), True, (255, 255, 255))
            screen.blit(score_surface, (left_lane_x - 150, center_y))

            # barra de progresso zerada durante o countdown
            bar_width, bar_height = 600, 10
            bar_x, bar_y = 660, 900
            pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 150, 150), (bar_x, bar_y, 0, bar_height))

            # durante o countdown, exibe as notas que já deveriam estar descendo
            # current_time_countdown representa o tempo relativo ao início da música,
            # começando negativo (countdown_ms/1000 antes de zero) e subindo até 0
            elapsed = (pygame.time.get_ticks() - start_ticks) / 1000.0
            current_time_countdown = elapsed - (countdown_ms / 1000.0)

            for note in notes:
                note_time_sec = note.time / 1000.0
                spawn_time    = note_time_sec - travel_time
                # desenha a nota se ela já deveria estar descendo
                if spawn_time <= current_time_countdown <= note_time_sec + 0.200:
                    progress = (current_time_countdown - spawn_time) / travel_time
                    y = spawn_y + (hit_y - spawn_y) * progress
                    pygame.draw.circle(screen, note.color, (lanes[note.lane]["x"], int(y)), 40)

            pygame.display.flip()
            clock.tick(60)

            # permite flash nas lanes durante o countdown
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    for lane_index, lane in enumerate(lanes):
                        if event.key == lane["key"]:
                            lane_flash[lane_index] = pygame.time.get_ticks()

        # inicia a música exatamente após o countdown
        pygame.mixer.music.play()
        song_start_ticks  = pygame.time.get_ticks()
        paused_total_ms   = 0

        # reinicia variáveis de estado do jogo
        running           = True
        feedback_text     = None
        feedback_timer    = 0
        feedback_color    = (255, 255, 255)
        combo_color       = (255, 255, 255)
        combo             = 0
        max_combo         = 0
        score             = 0
        total_excellent   = total_great = total_good = total_bad = total_miss = 0
        lane_flash        = {i: 0 for i in range(len(lanes))}
        miss_flash        = {i: 0 for i in range(len(lanes))}
        combo_scale       = 1.0
        combo_pulse_timer = 0
        restart_requested = False

        # --- loop principal do jogo ---
        while running:
            screen.fill((0, 0, 0))

            # calcula o tempo atual da música em segundos, descontando pausas
            current_time = (pygame.time.get_ticks() - song_start_ticks - paused_total_ms) / 1000.0

            # desenha as lanes; pisca de branco se flash ativo
            for i, lane in enumerate(lanes):
                fill_color = (255, 255, 255) if pygame.time.get_ticks() - lane_flash[i] < 150 else (48, 48, 48)
                pygame.draw.circle(screen, fill_color, (lane["x"], lane["y"]), 40)
                pygame.draw.circle(screen, (0, 0, 0), (lane["x"], lane["y"]), 40, 3)

            # processa cada nota do mapa
            for note in notes:
                if note.hit:
                    continue

                # tempo em segundos em que a nota deve ser acertada
                note_time_sec = note.time / 1000.0
                # tempo em que a nota deve nascer no topo para chegar na lane no tempo certo
                spawn_time    = note_time_sec - travel_time

                # se passou 200ms após o tempo da nota sem ser acertada, conta como miss
                if current_time > note_time_sec + 0.200:
                    feedback_text  = "Miss!"
                    feedback_color = (139, 0, 0)
                    feedback_timer = pygame.time.get_ticks()
                    note.hit       = True
                    combo          = 0
                    total_miss    += 1
                    # flash vermelho na lane do miss
                    miss_flash[note.lane] = pygame.time.get_ticks()
                    continue

                # desenha a nota enquanto ela está descendo e nos 200ms de janela após a lane
                if spawn_time <= current_time <= note_time_sec + 0.200:
                    progress = (current_time - spawn_time) / travel_time
                    y = spawn_y + (hit_y - spawn_y) * progress
                    pygame.draw.circle(screen, note.color, (lanes[note.lane]["x"], int(y)), 40)

            # processa eventos de input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # tecla de reinício rápido
                    if event.key == pygame.K_QUOTE:
                        pygame.mixer.music.stop()
                        restart_requested = True
                        running = False
                        break

                    # abre menu de pausa
                    if event.key == pygame.K_ESCAPE:
                        pause_started = pygame.time.get_ticks()
                        acao = menu_pausa(screen, clock, font)

                        if acao == "sair":
                            pygame.mixer.music.stop()
                            return
                        elif acao == "reset":
                            pygame.mixer.music.stop()
                            restart_requested = True
                            running = False
                            break
                        elif acao == "continuar":
                            pygame.mixer.music.unpause()
                            # acumula o tempo pausado para não desincronizar current_time
                            paused_total_ms += pygame.time.get_ticks() - pause_started
                            continue

                    # verifica se a tecla pressionada corresponde a alguma lane
                    for lane_index, lane in enumerate(lanes):
                        if event.key == lane["key"]:
                            found_note = False

                            # busca a primeira nota não acertada dessa lane
                            for note in notes:
                                if note.lane == lane_index and not note.hit:
                                    # delta: positivo = nota ainda não chegou, negativo = já passou
                                    delta     = note.time / 1000.0 - current_time
                                    delta_abs = abs(delta * 1000)

                                    if -0.3 <= delta <= 0.250:
                                        found_note = True

                                        # classifica o julgamento pelo delta em ms
                                        if delta_abs < 40:
                                            feedback_text, feedback_color = "Excellent", (173, 216, 230)
                                            score += excellent
                                            combo += 1
                                            if combo > max_combo:
                                                max_combo = combo
                                            note.hit = True
                                            total_excellent += 1
                                            combo_pulse_timer = pygame.time.get_ticks()

                                        elif delta_abs < 75:
                                            feedback_text, feedback_color = "Great", (144, 238, 144)
                                            score += great
                                            combo += 1
                                            note.hit = True
                                            total_great += 1
                                            combo_pulse_timer = pygame.time.get_ticks()

                                        elif delta_abs < 120:
                                            feedback_text, feedback_color = "Good", (70, 130, 180)
                                            score += good
                                            combo += 1
                                            note.hit = True
                                            total_good += 1
                                            combo_pulse_timer = pygame.time.get_ticks()

                                        elif delta_abs < 200:
                                            feedback_text, feedback_color = "Bad", (138, 43, 226)
                                            score += bad
                                            combo += 1
                                            note.hit = True
                                            total_bad += 1
                                            combo_pulse_timer = pygame.time.get_ticks()

                                        else:
                                            # pressionou dentro da janela mas longe demais
                                            feedback_text, feedback_color = "Miss", (139, 0, 0)
                                            combo = 0
                                            note.hit = True
                                            total_miss += 1
                                            miss_flash[lane_index] = pygame.time.get_ticks()

                                        feedback_timer = pygame.time.get_ticks()
                                        lane_flash[lane_index] = pygame.time.get_ticks()
                                        break

                                    elif delta < -0.3:
                                        # nota já passou da janela, ignora o input
                                        found_note = True
                                        lane_flash[lane_index] = pygame.time.get_ticks()
                                        break

                            # flash na lane mesmo sem nota (input vazio)
                            if not found_note:
                                lane_flash[lane_index] = pygame.time.get_ticks()

            # referências de posição para o HUD
            center_x    = screen.get_width() // 2
            center_y    = screen.get_height() // 2
            left_lane_x = lanes[0]["x"] - 100

            # calcula escala do pulso do combo (dura 150ms, vai de 1.3 até 1.0)
            pulse_elapsed = pygame.time.get_ticks() - combo_pulse_timer
            if pulse_elapsed < 150:
                combo_scale = 1.3 - 0.3 * (pulse_elapsed / 150.0)
            else:
                combo_scale = 1.0

            # desenha o combo com escala de pulso
            base_combo_font  = pygame.font.SysFont("Consolas", 32)
            pulse_size       = int(32 * combo_scale)
            combo_font       = pygame.font.SysFont("Consolas", pulse_size)
            combo_surface    = combo_font.render(f"{combo}", True, combo_color)
            screen.blit(combo_surface, (center_x - combo_surface.get_width() // 2, center_y - 40))

            # flash vermelho semitransparente e redondo nas lanes com miss
            for i, lane in enumerate(lanes):
                miss_elapsed = pygame.time.get_ticks() - miss_flash[i]
                if miss_elapsed < 200:
                    alpha = int(180 * (1.0 - miss_elapsed / 200.0))
                    miss_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
                    pygame.draw.circle(miss_surface, (255, 0, 0, alpha), (40, 40), 40)
                    screen.blit(miss_surface, (lane["x"] - 40, lane["y"] - 40))

            # calcula e exibe precisão em tempo real
            total_hits = total_excellent + total_great + total_good + total_bad
            max_points = (total_hits + total_miss) * excellent
            accuracy   = (score / max_points * 100) if max_points > 0 else 100.0
            accuracy_surface = font.render(f"{accuracy:.2f}%", True, (255, 255, 255))
            screen.blit(accuracy_surface, (1400, 200))

            # atualiza a cor do combo conforme o desempenho acumulado
            if (total_hits + total_miss) >= len(notes) * 0.25:
                if total_great == 0 and total_good == 0 and total_bad == 0 and total_miss == 0:
                    combo_color = (173, 216, 230)   # azul claro: só excellents
                elif total_good == 0 and total_bad == 0 and total_miss == 0:
                    combo_color = (144, 238, 144)   # verde claro: pelo menos um great
                elif total_miss == 0:
                    combo_color = (200, 200, 0)     # amarelo: sem miss
                else:
                    combo_color = (255, 255, 255)   # branco: tem miss

            # exibe o feedback de julgamento por 500ms
            if feedback_text:
                if pygame.time.get_ticks() - feedback_timer < 500:
                    text_surface = font.render(feedback_text, True, feedback_color)
                    screen.blit(text_surface, (center_x - text_surface.get_width() // 2, center_y + 10))
                else:
                    feedback_text = None

            # exibe o score à esquerda
            score_surface = font.render(f"{score:,}".replace(",", "'"), True, (255, 255, 255))
            screen.blit(score_surface, (left_lane_x - 150, center_y))

            # barra de progresso da música
            progress = max(0, min(current_time / music_length, 1)) if music_length > 0 else 1
            bar_width, bar_height = 600, 10
            bar_x, bar_y = 660, 900
            pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 150, 150), (bar_x, bar_y, int(bar_width * progress), bar_height))

            pygame.display.flip()
            clock.tick(240)

            # detecta fim da música e vai para a tela de resultado
            if current_time >= music_length:
                pygame.time.delay(1000)

                acao = resultado(
                    screen, clock, font, score, accuracy,
                    total_excellent, total_great, total_good, total_bad, total_miss,
                    lambda: rodando(screen, clock, font, velocidade, musica, dificuldade, voltar_menu),
                    voltar_menu, max_combo, dificuldade, musica, nome)

                if acao == "sair":
                    pygame.quit()
                    return
                elif acao == "menu":
                    voltar_menu(screen, clock, font, 1.0, nome)
                    return
                elif acao == "replay":
                    pygame.mixer.music.stop()
                    restart_requested = True
                    running = False
                    break

        # se foi solicitado reinício, volta ao topo do while True
        if restart_requested:
            continue
        else:
            return