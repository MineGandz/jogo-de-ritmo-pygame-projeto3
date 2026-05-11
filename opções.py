import pygame
import sys

def preferencias(screen, clock, font, velocidade):
    pref_options = ["Velocidade +", "Velocidade -", "Voltar"]
    pref_index = 0
    running_pref = True

    while running_pref:
        screen.fill((20,20,20))
        title_surface = font.render("Preferências", True, (255,255,0))
        screen.blit(title_surface, (screen.get_width()//2 - title_surface.get_width()//2, 150))

        # mostrar opções
        for i, option in enumerate(pref_options):
            color = (255,255,255)
            if i == pref_index:
                color = (0,255,0)
            text_surface = font.render(option, True, color)
            screen.blit(text_surface, (screen.get_width()//2 - text_surface.get_width()//2, 300 + i*80))

        # mostrar valores atuais
        status_surface = font.render(f"Velocidade: {velocidade}", True, (0,200,200))
        screen.blit(status_surface, (screen.get_width()//2 - status_surface.get_width()//2, 700))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pref_index = (pref_index - 1) % len(pref_options)
                elif event.key == pygame.K_DOWN:
                    pref_index = (pref_index + 1) % len(pref_options)
                elif event.key == pygame.K_RETURN:
                    chosen = pref_options[pref_index]
                    if chosen == "Velocidade +":
                        velocidade += 1
                    elif chosen == "Velocidade -":
                        if velocidade > 1:
                            velocidade -= 1
                    elif chosen == "Voltar":
                        running_pref = False

        clock.tick(60)
    return velocidade 

    