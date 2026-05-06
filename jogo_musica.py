import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.play()

font = pygame.font.SysFont("Arial", 32)

lanes = [
    {"x": 250, "y": 500, "key": pygame.K_x},
    {"x": 350, "y": 500, "key": pygame.K_c},
    {"x": 450, "y": 500, "key": pygame.K_n},
    {"x": 550, "y": 500, "key": pygame.K_m},
]

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

notes = parse_osu_file("mapa.osu", num_lanes=4)

running = True
feedback_text = None
feedback_timer = 0

while running:
    screen.fill((0,0,0))
    current_time = pygame.mixer.music.get_pos()

    # desenhar lanes
    for lane in lanes:
        pygame.draw.rect(screen, (50,50,50), (lane["x"]-25, lane["y"]-25, 50, 50), 2)

    # desenhar notas
    appear_time = 500  # notas caem em 0,5s
    for note in notes:
        if note.hit:
            continue
        dt = note.time - current_time
        if dt >= -200:
            progress = 1 - (dt / appear_time)
            if 0 <= progress <= 1:
                y = -50 + progress * (lanes[note.lane]["y"] + 50)
                pygame.draw.circle(screen, (0,0,255), (lanes[note.lane]["x"], int(y)), 20)

    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            for lane in lanes:
                if event.key == lane["key"]:
                    for note in notes:
                        if note.lane == lanes.index(lane) and not note.hit:
                            if abs(note.time - current_time) < 80:
                                feedback_text = "Hit!"
                                feedback_timer = pygame.time.get_ticks()
                                note.hit = True
                            else:
                                feedback_text = "Miss!"
                                feedback_timer = pygame.time.get_ticks()

    # desenhar feedback
    if feedback_text:
        # exibe por 500ms
        if pygame.time.get_ticks() - feedback_timer < 500:
            text_surface = font.render(feedback_text, True, (255,255,255))
            screen.blit(text_surface, (350, 100))
        else:
            feedback_text = None  # limpa depois de 500ms

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
