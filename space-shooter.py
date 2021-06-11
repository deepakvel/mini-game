import pygame
import os
from pygame.constants import K_RCTRL, K_SPACE

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CENTER = pygame.Rect(WIDTH//2-1, 0, 2, HEIGHT)
FPS = 60
SPEED = 5
BULLET_SPEED = 10
MAX_BULLETS = 2
SHIP_WIDTH, SHIP_HEIGHT = 50, 50

WIN_ICON = pygame.image.load(os.path.join('res', 'win_icon.png'))
ALLY_IMAGE = pygame.image.load(os.path.join('res', 'ally.png'))
ALLY = pygame.transform.scale(ALLY_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
ENEMY_IMAGE = pygame.image.load(os.path.join('res', 'enemy.png'))
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('res', 'space.png')), (WIDTH, HEIGHT))

ALLY_HIT = pygame.USEREVENT+1
ENEMY_HIT = pygame.USEREVENT+2

HEALTH_TEXT = pygame.font.Font(os.path.join('res', 'seguihis.ttf'), 30)
WINNER_TEXT = pygame.font.Font(os.path.join('res', 'seguihis.ttf'), 60)

FIRE_SOUND = pygame.mixer.Sound(os.path.join('res', 'fire.mp3'))
HIT_SOUND = pygame.mixer.Sound(os.path.join('res', 'hit.mp3'))

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
pygame.display.set_icon(WIN_ICON)


def draw(ally, enemy, ally_bullets, enemy_bullets, ally_health, enemy_health):
    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, WHITE, CENTER)

    ally_text = HEALTH_TEXT.render("Health: "+str(ally_health), 1, WHITE)
    enemy_text = HEALTH_TEXT.render("Health: "+str(enemy_health), 1, WHITE)

    WINDOW.blit(ally_text, (10, 10))
    WINDOW.blit(enemy_text, (WIDTH-ally_text.get_width()-20, 10))

    WINDOW.blit(ALLY, (ally.x, ally.y))
    WINDOW.blit(ENEMY, (enemy.x, enemy.y))
    for bullet in ally_bullets:
        pygame.draw.rect(WINDOW, WHITE, bullet)
    for bullet in enemy_bullets:
        pygame.draw.rect(WINDOW, WHITE, bullet)
    pygame.display.update()


def ally_movement(key_press, ally):
    if key_press[pygame.K_a] and ally.x-SPEED > 0:  # left
        ally.x -= SPEED
    if key_press[pygame.K_d] and ally.x+ally.width+SPEED < CENTER.x:  # right
        ally.x += SPEED
    if key_press[pygame.K_w] and ally.y-SPEED > 0:  # up
        ally.y -= SPEED
    if key_press[pygame.K_s] and ally.y+ally.height+SPEED < HEIGHT:  # down
        ally.y += SPEED


def enemy_movement(key_press, enemy):
    if key_press[pygame.K_LEFT] and enemy.x-SPEED > CENTER.x+CENTER.width:  # left
        enemy.x -= SPEED
    if key_press[pygame.K_RIGHT] and enemy.x+enemy.width+SPEED < WIDTH:  # right
        enemy.x += SPEED
    if key_press[pygame.K_UP] and enemy.y-SPEED > 0:  # up
        enemy.y -= SPEED
    if key_press[pygame.K_DOWN] and enemy.y+enemy.height+SPEED < HEIGHT:  # down
        enemy.y += SPEED


def handle_bullets(ally, ally_bullets, enemy, enemy_bullets):
    for bullet in ally_bullets:
        bullet.x += BULLET_SPEED
        if enemy.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
            ally_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            ally_bullets.remove(bullet)
    for bullet in enemy_bullets:
        bullet.x -= BULLET_SPEED
        if ally.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ALLY_HIT))
            enemy_bullets.remove(bullet)
        elif bullet.x < 0:
            enemy_bullets.remove(bullet)


def draw_winner(text):
    win_text = WINNER_TEXT.render(text, 1, WHITE)
    WINDOW.blit(win_text, (WIDTH//2-win_text.get_width() //
                2, HEIGHT*3/4))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    ally = pygame.Rect(50, 175, SHIP_WIDTH, SHIP_HEIGHT)
    enemy = pygame.Rect(500, 175, SHIP_WIDTH, SHIP_HEIGHT)
    ally_bullets = []
    enemy_bullets = []
    clock = pygame.time.Clock()
    ally_health = 10
    enemy_health = 10
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE and len(ally_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        ally.x+ally.width, ally.y+ally.height//2, 8, 4)
                    ally_bullets.append(bullet)
                    FIRE_SOUND.play()
                if event.key == K_RCTRL and len(enemy_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        enemy.x, enemy.y+enemy.height//2, 8, 4)
                    enemy_bullets.append(bullet)
                    FIRE_SOUND.play()
            if event.type == ALLY_HIT:
                ally_health -= 1
                HIT_SOUND.play()
            if event.type == ENEMY_HIT:
                enemy_health -= 1
                HIT_SOUND.play()
        winner_msg = ""
        if ally_health <= 0:
            winner_msg = "Player 2 Wins!"
        if enemy_health <= 0:
            winner_msg = "Player 1 Wins!"
        if winner_msg != '':
            draw_winner(winner_msg)
            break

        key_press = pygame.key.get_pressed()
        ally_movement(key_press, ally)
        enemy_movement(key_press, enemy)
        draw(ally, enemy, ally_bullets, enemy_bullets, ally_health, enemy_health)
        handle_bullets(ally, ally_bullets, enemy, enemy_bullets)
    main()


if __name__ == "__main__":
    main()
