import pygame
import math
import random

from pygame import mixer
from playsound import playsound

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

#pygame.mixer.Sound("background.wav")
background = pygame.image.load("f1.jpg")

mixer.init()
mixer.music.load("background.wav")
mixer.music.play(-1)


pygame.display.set_caption("SpaceInvenders")
icon = pygame.image.load("iguana(1).png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("space-invaders.png")
player_x = 370
player_y = 480
player_x_change = 0

enemyImg = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("coronavirus.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

bulletImg = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_State = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

text_x = 10
text_y = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_Score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet(x, y):
    global bullet_State
    bullet_State = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5

            if event.key == pygame.K_RIGHT:
                player_x_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_State is "ready":
                    bullet_Sound = mixer.music.load("laser.wav")
                    mixer.music.play()
                    bullet_x = player_x
                    bullet(player_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_enemies):

        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

        collision = isCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            mixer.music.load("explosion.wav")
            mixer.music.play()
            bullet_y = 480
            bullet_State = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= 0:
        bullet_y = 480
        bullet_State = "ready"

    if bullet_State is "fire":
        bullet(player_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_Score(text_x, text_y)

    pygame.display.update()
