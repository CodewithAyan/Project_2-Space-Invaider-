import pygame
import random
import math
import time
from pygame.locals import *
from pygame import mixer

# for mixer and font we have to use pygame.init()
pygame.init()

# Setting Window
win = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

# Setting Window's Caption
pygame.display.set_caption("Space Invaider")

# Setting Icon
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# INTRO
INTRO = pygame.image.load('universe.jpg')

# Setting baackground
back = pygame.image.load("background.png")

# background music
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

game_over_sound = mixer.Sound('game_over.wav')

# Setting player image and position

player_image = pygame.image.load("player.png")
playerX = 480
playerY = 480

X_change = 0

# Setting enemy image and position
Enemy_image = []
enemyX = []
enemyY = []
X_change_enemy = []
Y_change_enemy = []
num_of_enemy = 8

for i in range(num_of_enemy):
    Enemy_image.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))

    X_change_enemy.append(4)
    Y_change_enemy.append(40)

# Setting bullet image and position
bullet_image = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
X_change_bullet = 0
Y_change_bullet = 20

# Ready - can't see the bullet
# Fire - the bullet is currently moving
bullet_state = "ready"

# Score
score = 0
font = pygame.font.Font('Hello Avocado.ttf', 32)
textX = 10
textY = 10

# game over
game_font = pygame.font.Font('Hello Avocado.ttf', 64)


def Score_show(x, y):
    score_s = font.render("Score : " + str(score), True, (255, 255, 255))
    win.blit(score_s, (x, y))


def game_over():
    game_s = game_font.render("GAME OVER", True, (255, 255, 255))
    win.blit(game_s, (200, 250))
    pygame.mixer.music.pause()
    # game_over_sound.play()
    # time.sleep(3)
    # game_over_sound.stop()



def player(x, y):
    # blit is used for showing image in the window
    win.blit(player_image, (x, y))


def enemy(x, y, i):
    # blit is used for showing image in the window
    win.blit(Enemy_image[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    win.blit(bullet_image, (x + 16, y + 10))


def isCollison(enemy_X, enemy_Y, bullet_X, bullet_Y):
    dist = math.sqrt((math.pow((bullet_X - enemy_X), 2)) + (math.pow((bullet_Y - enemy_Y), 2)))

    if dist < 27: 
        return True
    return False

#pygame.display.flip()


running = True
while running:
    # Setting window color
    win.fill((0, 0, 0))

    # background
    win.blit(back, (0, 0))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            pass
            if event.key == K_ESCAPE:
                running = False

            # Changing coordinate of the space ship
            if event.key == pygame.K_LEFT:
                X_change = -15

            if event.key == pygame.K_RIGHT:
                X_change = 15

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    sound = mixer.Sound("laser.wav")
                    sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                X_change = 0

        elif event.type == QUIT:
            running = False

    # Player part
    playerX = playerX + X_change
    if playerX <= 0:
        playerX = 0

    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemy):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemy):
                new_var = 2000
                enemyY[j] = new_var
            game_over()
            break

            # Enemy part
        enemyX[i] += X_change_enemy[i]
        # Restricting it from going outside of the window
        if enemyX[i] <= 0:
            X_change_enemy[i] = 7
            enemyY[i] += Y_change_enemy[i]

        elif enemyX[i] >= 736:  # we need to substract the size of the enemy pic from the length(800-64) = 736
            X_change_enemy[i] = -7
            enemyY[i] += Y_change_enemy[i]

        # Collision Happening
        collison = isCollison(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            Sound_explosion = mixer.Sound("explosion.wav")
            Sound_explosion.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print((score))
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

        # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= Y_change_bullet

    player(playerX, playerY)
    Score_show(textX, textY)
    pygame.display.flip()