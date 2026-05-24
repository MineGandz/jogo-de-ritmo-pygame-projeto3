import os
import json
import pygame

#funcao que guarda o resultado obtido na musica
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
            # Substitui apenas se o novo score for maior que o existente
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
import pygame, os, json

def leaderboard(screen, clock, font, musica, dificuldade, arquivo="leaderboard.json"):
    # Carregar dados
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    else:
        dados = []

    # Filtrar e ordenar
    dados_filtrados = [d for d in dados if d["musica"] == musica and d["dificuldade"] == dificuldade]
    dados_filtrados = sorted(dados_filtrados, key=lambda x: x["score"], reverse=True)[:10]

    showing = True
    while showing:
        screen.fill((30,30,30))

        # título fora da caixa (azul, mais baixo)
        titulo = font.render(f"Leaderboard - {musica} [{dificuldade}]", True, (0,128,255))
        screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 160))

        # painel central (aumentado e mais próximo do título)
        panel_width, panel_height = 1000, 600
        panel_x = screen.get_width()//2 - panel_width//2
        panel_y = screen.get_height()//2 - panel_height//2 + 40
        pygame.draw.rect(screen, (50,50,50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (200,0,0), (panel_x, panel_y, panel_width, panel_height), 4)

        # lista dos jogadores
        if dados_filtrados:
            for i, jogador in enumerate(dados_filtrados):
                if i == 0: cor = (255,215,0)   # ouro
                elif i == 1: cor = (192,192,192) # prata
                elif i == 2: cor = (205,127,50)  # bronze
                else: cor = (200,200,200)

                score_formatado = f"{jogador['score']:,}".replace(",", "'")
                texto = f"{i+1}º - {jogador['nome']} | Score: {score_formatado} | Acc: {jogador['accuracy']:.2f}% | Combo: {jogador['max_combo']}" 
                surf = font.render(texto, True, cor)
                screen.blit(surf, (panel_x + panel_width//2 - surf.get_width()//2, panel_y + 40 + i*40))
        else:
            vazio = font.render("Nenhum recorde ainda", True, (180,180,180))
            screen.blit(vazio, (panel_x + panel_width//2 - vazio.get_width()//2, panel_y + panel_height//2))

        # instrução
        instr_font = pygame.font.SysFont("Consolas", 24)
        sair_text = instr_font.render("ENTER para voltar", True, (180,180,180))
        screen.blit(sair_text, (screen.get_width()//2 - sair_text.get_width()//2, panel_y + panel_height - 40))

        pygame.display.flip()
        clock.tick(60)

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return "menu"

