import pygame
import math
from random import randint

pygame.init()
win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("First Game")
screenWidth = 1024
screenheight = 768
pygame.display.set_mode((screenWidth, screenheight), flags=0, depth=0, display=0)
bg = pygame.image.load("background.jpg")
target = pygame.image.load("target.png")
# Variable list
x = 63
y = 630
time = 50
xtarget = 500
ytarget = 640
# trig
angle = math.pi / 6
Vtot = 1300
Vx = Vtot * math.cos(angle)
Vy = -Vtot * math.sin(angle)
# motion stuff
g = 98
t = time / 1000
# boolean stuff
run = True
fall = True
launch = False
start = True
missed = False
hit = False
lock = True
end = False
# game stuff
score = 0
lives = 5

# debug space so that it can't run when game hasnt started
# function list

def go():
    font = pygame.font.SysFont("monospace", 60, True)
    titleText = font.render("Projectile Game", 1, (0, 0, 0))  # Arguments are: text, anti-aliasing, color
    font = pygame.font.SysFont("comicsans", 40, True)
    howto1 = font.render("Press Backspace to start game", 1, (0, 0, 0))
    howto2 = font.render("Use Up/Down arrow keys to adjust launch angle", 1, (0, 0, 0))
    howto3 = font.render("Press Space Bar to launch", 1, (0, 0, 0))
    howto4 = font.render("Press Esc to quit", 1, (0, 0, 0))
    font = pygame.font.SysFont("ebrima", 40, True)
    goalText = font.render("Objective: launch the ball to hit the target", 1, (0, 0, 0))

    win.blit(titleText, (250, 170))
    win.blit(howto1, (290, 250))
    win.blit(howto2, (150, 300))
    win.blit(howto3, (315, 350))
    win.blit(howto4, (320, 400))
    win.blit(goalText, (140, 450))
    pygame.display.update()


def redraw():
    font = pygame.font.SysFont("comicsans", 40, True)
    win.blit(bg, (0, 0))
    if not launch:
        pygame.draw.line(win, (0, 0, 0), (x, y), (int((x + 60 * math.cos(angle))), int(y - 60 * math.sin(angle))), 4)
    angleText = font.render("Angle: " + str(round(math.degrees(angle))) + "°", 1,
                            (0, 0, 0))  # Arguments are: text, anti-aliasing, color
    scoreText = font.render("Score: " + str(score), 1, (0, 0, 0))
    livesText = font.render("Lives: " + str(lives), 1, (0, 0, 0))
    slingImg = pygame.image.load('slingshot.png')
    miss = font.render("You Missed :(", 1, (0, 0, 0))
    if lives == 0:
        font = pygame.font.SysFont("leelawadeeui", 100, True)
        gameover = font.render("Game Over", 1, (0, 0, 0))
        win.blit(gameover, (240, 200))
        font = pygame.font.SysFont("ebrima", 50, True)
        finalscore = font.render("Your Score is " + str(score), 1, (0, 0, 0))
        win.blit(finalscore, (270, 320))
        miss = font.render(" ", 1, (0, 0, 0))
    if missed:
        font = pygame.font.SysFont("leelawadeeui", 100, True)
        win.blit(miss, (220, 200))

    if hit:
        font = pygame.font.SysFont("leelawadeeui", 100, True)
        miss = font.render("You Hit It!", 1, (0, 0, 0))
        win.blit(miss, (240, 200))

    win.blit(slingImg, (30, 620))
    pygame.draw.circle(win, (0, 0, 255), (x, y), 15)
    win.blit(angleText, (40, 30))
    win.blit(scoreText, (40, 70))
    win.blit(livesText, (40, 110))
    win.blit(target, (xtarget, ytarget))
    pygame.display.update()


while run:
    pygame.time.delay(time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    # launch
    if keys[pygame.K_SPACE] and start == False and lock and end == False:
        launch = True
        lock = False
        Vx = Vtot * math.cos(angle)
        Vy = -Vtot * math.sin(angle)
    # movement x independent from y
    if keys[pygame.K_LEFT]:
        xtarget -= 5

    if keys[pygame.K_RIGHT]:
        xtarget += 5

    if fall and launch:
        x += int(Vx * t)
        y += int(Vy * t)
        Vy = Vy + g
        redraw()

        # hit
        if ((x >= xtarget) and x <= (xtarget + 115)) and ((y >= ytarget) and (y <= (ytarget + 26)) ):
            hit = True
            score += 1
            fall = False
        # miss
        elif y >= 670:
            fall = False
            redraw()
            missed = True
            lives -= 1


    # reset
    if keys[pygame.K_BACKSPACE]:
        launch = False
        fall = True
        Vy = -Vtot * math.sin(angle)
        x = 63
        y = 630
        missed = False
        start = False
        hit = False
        lock = True

    if keys[pygame.K_UP]:
        angle += math.pi / 180
        if angle > math.pi / 2:
            angle = math.pi / 2
        print(math.degrees(angle))

        redraw()
        start = False

    if keys[pygame.K_DOWN]:
        angle -= math.pi / 180
        if angle < 0:
            angle = 0
        print(math.degrees(angle))

        redraw()
        start = False

    if keys[pygame.K_ESCAPE]:
        run = False
    if lives == 0:
        end = True

    if start:
        go()
        win.blit(bg, (0, 0))

    if not start:
        redraw()

pygame.quit()