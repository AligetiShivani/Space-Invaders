import pygame
from pygame import mixer
import random
import math

# Initalising the pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1000, 700))

# Title
pygame.display.set_caption("Space Invaders")

# Icon
gameIcon = pygame.image.load('./images/spaceship.png')
pygame.display.set_icon(gameIcon)

# BackgroundColor
screen.fill((0, 0, 0))
# Background Img
backgroundImg = pygame.image.load('./images/background.png')
# Background Music
mixer.music.load('./sounds/background.wav')
mixer.music.play(-1)

# Spaceship positioning
spaceshipImg = pygame.image.load('./images/saaas.png')
spaceshipPosX = 468
spaceshipPosY = 570
spaceshipChangeX = 0

# Enemy positioning
numOfEnemies = 6
enemyImg = []
enemyPosX = []
enemyPosY = []
enemyChangeX = []
enemyChangeY = []

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load('./images/ghost.png'))
    enemyPosX.append(random.randint(0, 1000 - 64))
    enemyPosY.append(random.randint(50, 200))
    enemyChangeX.append(1)
    enemyChangeY.append(40)

# Bullet positioning
bulletImg = pygame.image.load('./images/bullet.png')
bulletPosX = 0
bulletPosY = 570
bulletChangeX = 0
bulletChangeY = 3
bulletState = "ready"

# SCORE
score = 0
scoreFont = pygame.font.Font('freesansbold.ttf', 32)
scorePosX = 10
scorePosY = 10

# GAME OVER
gameOverFont = pygame.font.Font('freesansbold.ttf', 64)

def scoreBoard(X,Y):
    scoreVal= scoreFont.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(scoreVal, (X,Y))

def spaceship(X, Y):
    screen.blit(spaceshipImg, (X, Y))


def enemy(X, Y, i):
    screen.blit(enemyImg[i], (X, Y))


def fireBullet(X, Y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (X + 9, Y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False

def GameOverText():
    gameOver = gameOverFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameOver, (320, 300))



# Game Loop
isGameRunning = True
while isGameRunning:
    # BackgroundColor
    screen.fill((0, 1, 0))
    # Background image
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            isGameRunning = False

        # if keystroke is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceshipChangeX = -1
            if event.key == pygame.K_RIGHT:
                spaceshipChangeX = 1
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletSound = mixer.Sound('./sounds/bullet.wav')
                    bulletSound.play()
                    bulletPosX = spaceshipPosX
                    fireBullet(bulletPosX, spaceshipPosY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceshipChangeX = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    spaceshipPosX += spaceshipChangeX
    if spaceshipPosX <= 0:
        spaceshipPosX = 0
    elif spaceshipPosX >= (1000 - 64):
        spaceshipPosX = (1000 - 64)

    # Enemy movements
    for i in range(numOfEnemies):

        # GAME OVER
        if enemyPosY[i] >= 515:
            for j in range(numOfEnemies):
                enemyPosY[j] = 3000
            GameOverText()
            break

        enemyPosX[i] += enemyChangeX[i]
        if enemyPosX[i] <= 0:
            enemyChangeX[i] = 1
            enemyPosY[i] += enemyChangeY[i]
        elif enemyPosX[i] >= (1000 - 64):
            enemyChangeX[i] = -1
            enemyPosY[i] += enemyChangeY[i]

        # Collision
        collision = isCollision(enemyPosX[i], enemyPosY[i], bulletPosX, bulletPosY)
        if collision:
            collisionSound = mixer.Sound('./sounds/collision.wav')
            collisionSound.play()
            bulletPosY = 570
            bulletState = "ready"
            score += 1
            enemyPosX[i] = random.randint(0, 1000 - 64)
            enemyPosY[i] = random.randint(50, 200)

        enemy(enemyPosX[i], enemyPosY[i], i)

    # Bullet movement
    if bulletPosY <= 0:
        bulletPosY = 570
        bulletState = "ready"
    if bulletState == "fire":
        fireBullet(bulletPosX, bulletPosY)
        bulletPosY -= bulletChangeY

    spaceship(spaceshipPosX, spaceshipPosY)
    scoreBoard(scorePosX, scorePosY)
    pygame.display.update()
