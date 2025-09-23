import pygame, sys, random

# ФУНКЦІЇ !

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,665))
    screen.blit(floor_surface,(floor_x_pos + 432,665))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 768:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 665:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (210,30))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255,255,255))
        score_rect = score_surface.get_rect(center = (210,30))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High score: {int(high_score)}", True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (210,620))
        screen.blit(high_score_surface, high_score_rect)

def check_score(pipes):
    global score
    for pipe in pipes:
        if 95 < pipe.centerx < 105:
            score += 0.5

# ІНІЦІАЛІЗАЦІЯ !

pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',30)

# ЗМІННІ ГРИ !

gravity = 0.35
bird_movement = 0
game_active = True
score = 0
high_score = 0

# РЕЖИМИ ГРИ (ДЕНЬ / НІЧ)

game_mode = "day"
mode_selected = False   # меню на початку
menu_done = False       # після вибору більше не показуємо меню

# Фони
bg_day = pygame.image.load("assets/background-day.png").convert()
bg_day = pygame.transform.scale(bg_day,(432,768))

bg_night = pygame.image.load("assets/background-night.png").convert()
bg_night = pygame.transform.scale(bg_night,(432,768))

# Підлога
floor_surface = pygame.image.load("assets/base.png").convert_alpha()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# Пташки для дня
bird_day_downflap = pygame.image.load("assets/bluebird-downflap.png").convert_alpha()
bird_day_downflap = pygame.transform.scale(bird_day_downflap,(48,36))
bird_day_midflap = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
bird_day_midflap = pygame.transform.scale(bird_day_midflap,(48,36))
bird_day_upflap = pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
bird_day_upflap = pygame.transform.scale(bird_day_upflap,(48,36))
bird_day_frames = [bird_day_downflap, bird_day_midflap, bird_day_upflap]

# Пташки для ночі
bird_night_downflap = pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()
bird_night_downflap = pygame.transform.scale(bird_night_downflap,(48,36))
bird_night_midflap = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
bird_night_midflap = pygame.transform.scale(bird_night_midflap,(48,36))
bird_night_upflap = pygame.image.load("assets/yellowbird-upflap.png").convert_alpha()
bird_night_upflap = pygame.transform.scale(bird_night_upflap,(48,36))
bird_night_frames = [bird_night_downflap, bird_night_midflap, bird_night_upflap]

# Початково пусті (заповняться після вибору)
bird_frames = bird_day_frames
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,384))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

# ТРУБИ

pipe_surface = pygame.image.load("assets/pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [200,300,400,500]

# GAME OVER
game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface,(300,450))
game_over_rect = game_over_surface.get_rect(center = (216,330))

# ГОЛОВНИЙ ЦИКЛ

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Якщо режим ще не вибрали і меню ще активне
        if not mode_selected and not menu_done:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = "day"
                    bird_frames = bird_day_frames
                    bg_surface = bg_day
                    mode_selected = True
                    menu_done = True   # меню більше не показуємо
                if event.key == pygame.K_2:
                    game_mode = "night"
                    bird_frames = bird_night_frames
                    bg_surface = bg_night
                    mode_selected = True
                    menu_done = True   # меню більше не показуємо

        else:  # Режим вибраний → звичайна гра
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 10
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100,384)
                    bird_movement = 0
                    score = 0

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())

            if event.type == BIRDFLAP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                bird_surface, bird_rect = bird_animation()

    # Малювання
    if not mode_selected and not menu_done:
        screen.fill((0,0,0))
        text1 = game_font.render("DAY mode(1)", True, (255,255,255))
        text2 = game_font.render("NIGHT mode(2)", True, (255,255,255))
        screen.blit(text1, (40,300))
        screen.blit(text2, (40,400))

    else:
        screen.blit(bg_surface,(0,0))

        if game_active:
            bird_movement += gravity
            rotated_bird = rotate_bird(bird_surface)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird,bird_rect)
            game_active = check_collision(pipe_list)

            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            check_score(pipe_list)
            score_display("main_game")
        else:
            screen.blit(game_over_surface,game_over_rect)
            if score > high_score:
                high_score = score
            score_display("game_over")

        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -432:
            floor_x_pos = 0

    pygame.display.update()
    clock.tick(60)