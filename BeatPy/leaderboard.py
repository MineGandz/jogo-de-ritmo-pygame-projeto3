import os
import json
import pygame

# -------------------------------
# Função para salvar resultado
# -------------------------------
def salvar_resultado(nome, musica, dificuldade, score, accuracy, max_combo, arquivo="leaderboard.json"):
    """
    Salva o resultado do jogador no arquivo JSON.
    - Se não existir o arquivo, cria um novo.
    - Se já existir entrada para (nome, musica, dificuldade), substitui apenas se o novo score for maior.
    - Caso contrário, adiciona uma nova entrada.
    """

    # Carrega leaderboard existente
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    else:
        dados = []

    # Procura se já existe entrada para esse jogador nessa música/dificuldade
    encontrado = False
    for entry in dados:
        if entry["nome"] == nome and entry["musica"] == musica and entry["dificuldade"] == dificuldade:
            encontrado = True
            # Substitui apenas se o novo score for maior
            if score > entry["score"]:
                entry["score"] = score
                entry["accuracy"] = accuracy
                entry["max_combo"] = max_combo
            break

    # Se não encontrou, adiciona nova entrada
    if not encontrado:
        dados.append({
            "nome": nome,
            "musica": musica,
            "dificuldade": dificuldade,
            "score": score,
            "accuracy": accuracy,
            "max_combo": max_combo
        })

    # Salva de volta no arquivo
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)


# -------------------------------
# Função para exibir leaderboard
# -------------------------------
def leaderboard(screen, clock, font, musica, dificuldade, arquivo="leaderboard.json"):
    """
    Exibe o Top 10 jogadores para uma música e dificuldade específica.
    - Lê os dados do arquivo JSON.
    - Filtra apenas os resultados da música/dificuldade escolhida.
    - Ordena por score decrescente.
    - Mostra em um painel central na tela.
    """

    # Carrega dados
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    else:
        dados = []

    # Filtra por música e dificuldade
    dados_filtrados = [d for d in dados if d["musica"] == musica and d["dificuldade"] == dificuldade]

    # Ordena por score decrescente e pega Top 10
    dados_filtrados = sorted(dados_filtrados, key=lambda x: x["score"], reverse=True)[:10]

    showing = True
    while showing:
        screen.fill((30,30,30))

        # painel central
        panel_width, panel_height = 800, 600
        panel_x = screen.get_width()//2 - panel_width//2
        panel_y = screen.get_height()//2 - panel_height//2
        pygame.draw.rect(screen, (50,50,50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (200,0,0), (panel_x, panel_y, panel_width, panel_height), 4)

        # título
        titulo = font.render(f"Leaderboard - {musica} [{dificuldade}]", True, (255,255,255))
        screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, panel_y + 40))

        # lista dos jogadores
        for i, jogador in enumerate(dados_filtrados):
            texto = f"{i+1}. {jogador['nome']} - Score: {jogador['score']} - Acc: {jogador['accuracy']:.2f}% - Combo: {jogador['max_combo']}"
            surf = font.render(texto, True, (200,200,200))
            screen.blit(surf, (panel_x + 40, panel_y + 100 + i*40))

        # instrução para voltar
        instr_font = pygame.font.SysFont("Consolas", 24)
        sair_text = instr_font.render("ENTER para voltar", True, (180,180,180))
        screen.blit(sair_text, (panel_x + panel_width - sair_text.get_width() - 20,
                                panel_y + panel_height - 40))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    return "menu"
