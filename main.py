import pygame
import os
import random as rnd
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shrek destroyer")
BG_MUSIC_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'music.mp3'))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER_WIDTH = 10
BORDER = pygame.Rect(WIDTH // 2 - BORDER_WIDTH // 2, 0, BORDER_WIDTH, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
WELCOME_HEADER_FONT = pygame.font.SysFont('comicsans', 80)
END_GAME_FONT = pygame.font.SysFont('comicsans', 60)
INSTRUCTIONS_FONT = pygame.font.SysFont('comicsans', 30)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BULLET_WIDTH, BULLET_HEIGHT = 10, 5

WINNING_SCORE = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
TIMER_EVENT = pygame.USEREVENT + 3

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_score, yellow_score):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    red_score_text = HEALTH_FONT.render(str(red_score), 1, WHITE)
    yellow_score_text = HEALTH_FONT.render(str(yellow_score), 1, WHITE)
    WIN.blit(red_score_text, (WIDTH / 2 + BORDER_WIDTH + 5, 10))
    WIN.blit(yellow_score_text, (WIDTH / 2 - BORDER_WIDTH - 5 - yellow_score_text.get_width(), 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)   

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 15: # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10: # DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH + 15: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10: # DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

def draw_countdown_to_reset(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, clock, red_score, yellow_score):
    timer_counter = 5
    pygame.time.set_timer(TIMER_EVENT, 1000)

    while timer_counter >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == TIMER_EVENT:
                draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_score, yellow_score)
                text = 'Game resets in ' + str(timer_counter)
                draw_text = WINNER_FONT.render(text, 1, WHITE)
                WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))

                pygame.display.update()

                timer_counter -= 1
    
    pygame.time.set_timer(TIMER_EVENT, 0)

def welcome(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, clock, red_score, yellow_score):        
    text_1a = 'Welcome to Shrek Destroyer'
    draw_text_1a = WELCOME_HEADER_FONT.render(text_1a, 1, WHITE)

    text_1b = f'First to {WINNING_SCORE} wins'
    draw_text_1b = WELCOME_HEADER_FONT.render(text_1b, 1, WHITE)

    text_yellow_controls = '"WASD" to move. "T" to shoot'
    draw_text_yellow_controls = INSTRUCTIONS_FONT.render(text_yellow_controls, 1, WHITE)

    text_red_controls = 'Arrows to move. "/" to shoot'
    draw_text_red_controls = INSTRUCTIONS_FONT.render(text_red_controls, 1, WHITE)

    timer_counter = 10
    pygame.time.set_timer(TIMER_EVENT, 1000)

    while timer_counter >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == TIMER_EVENT:
                draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_score, yellow_score)

                WIN.blit(draw_text_1a, (WIDTH // 2 - draw_text_1a.get_width() // 2, 50))
                WIN.blit(draw_text_1b, (WIDTH // 2 - draw_text_1b.get_width() // 2, 50 + draw_text_1a.get_height() + 20))
                WIN.blit(draw_text_yellow_controls, (100, HEIGHT // 2))
                WIN.blit(draw_text_red_controls, (WIDTH - draw_text_red_controls.get_width() - 100, HEIGHT // 2))

                text_2 = 'First game starts in ' + str(timer_counter)
                draw_text_2 = WINNER_FONT.render(text_2, 1, WHITE)
                WIN.blit(draw_text_2, (WIDTH // 2 - draw_text_2.get_width() // 2, HEIGHT - 100))

                pygame.display.update()

                timer_counter -= 1

    pygame.time.set_timer(TIMER_EVENT, 0)

MOUSE_OPTIONS = [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL]

def disable_mouse_input():
    pygame.mouse.set_visible(False)
    for mouse_option in MOUSE_OPTIONS:
        pygame.event.set_blocked(mouse_option)

def enable_mouse_input():
    pygame.mouse.set_visible(True)
    for mouse_option in MOUSE_OPTIONS:
        pygame.event.set_allowed(mouse_option)

def end_game(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, clock, red_score, yellow_score):
    winner_text = 'Red' if red_score == WINNING_SCORE else 'Yellow'
    text = 'Game has ended. ' + winner_text + ' has won!'
    draw_text = END_GAME_FONT.render(text, 1, WHITE)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_score, yellow_score)
        WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
        pygame.display.update()


def play(is_first_game, clock, red_score, yellow_score):
    red_start_x, red_start_y = rnd.randint(WIDTH - 200, WIDTH - SPACESHIP_WIDTH), rnd.randint(0, HEIGHT - SPACESHIP_HEIGHT)
    yellow_start_x, yellow_start_y = rnd.randint(0, 200), rnd.randint(0, HEIGHT - SPACESHIP_HEIGHT)
    red = pygame.Rect(red_start_x, red_start_y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(yellow_start_x, yellow_start_y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    if is_first_game == True:
        disable_mouse_input()
        welcome(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, clock, red_score, yellow_score)
        enable_mouse_input()
        is_first_game = False

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - BULLET_HEIGHT//2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_SLASH and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - BULLET_HEIGHT//2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_score, yellow_score)

        winner_text = ""
        if red_health <= 0:
            yellow_score += 1
            winner_text = "Yellow wins!"
        if yellow_health <= 0:
            red_score += 1
            winner_text = "Red wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

    if red_score == WINNING_SCORE or yellow_score == WINNING_SCORE:
        end_game(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, clock, red_score, yellow_score)
    else:
        # disable_mouse_input()
        draw_countdown_to_reset(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, clock, red_score, yellow_score)
        # enable_mouse_input()
        play(is_first_game, clock, red_score, yellow_score) # Play again

def main():
    clock = pygame.time.Clock()
    # clock.tick(FPS)

    BG_MUSIC_SOUND.set_volume(0.3)
    BG_MUSIC_SOUND.play(loops=-1)

    red_score = 0
    yellow_score = 0

    is_first_game = True
    play(is_first_game, clock, red_score, yellow_score)

if __name__ == "__main__":
    main()