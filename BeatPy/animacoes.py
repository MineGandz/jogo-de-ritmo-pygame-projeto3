# transicoes.py
import pygame
def fade_out(screen, clock, speed=25, color=(0,0,0)):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(color)  # preto
    for alpha in range(0, 255, speed):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0,0))
        pygame.display.flip()
        clock.tick(60)

def fade_in(screen, clock, speed=25, color=(0,0,0), final_color=(0,0,0)):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(color)  # preto
    for alpha in range(255, -1, -speed):
        # redesenha o fundo cinza antes de aplicar o fade
        screen.fill(final_color)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0,0))
        pygame.display.flip()
        clock.tick(60)
