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
time = 10
xtarget = randint(500, 900)
ytarget = 640
angley= 430
null = 69
# trig
angle = math.pi / 6
Vtot = 1300
powerx = 120 + Vtot/10
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
drag1 = False
drag2 = False
# game stuff
score = 0
lives = 5

class slider(object):
    def __init__(self, xbox1, ybox1, xline1, yline1, xline2, yline2):
        self.xbox1 = xbox1
        self.ybox1 = ybox1
        self.xline1 = xline1
        self.yline1 = yline1
        self.xline2 = xline2
        self.yline2 = yline2
    def draw(self, win):
        pygame.draw.line(win, (0, 0, 0), (self.xline1, self.yline1), (self.xline2, self.yline2), 4)
        pygame.draw.rect(win, (0, 0, 0), (self.xbox1, self.ybox1, 20, 20))

angleslider = slider(53, int(angley), 63, 190, 63, 550)
powerslider = slider(powerx, 690, 120, 700, 490, 700)

# debug space so that it can't run when game hasnt started
# function list

def go():
    font = pygame.font.SysFont("monospace", 60, True)
    titleText = font.render("Projectile Game", 1, (0, 0, 0))
    font = pygame.font.SysFont("comicsans", 40, True)
    howTo1 = font.render("Press Backspace --- Clear and Start Game", 1, (0, 0, 0))
    howTo2 = font.render("Press Up/Down ------ Adjust Launch Angle", 1, (0, 0, 0))
    howTo3 = font.render("Press Right/Left ----- Adjust Launch Power", 1, (0,0,0))
    howTo4 = font.render("Press Space Bar ----------- Launch The Ball", 1, (0, 0, 0))
    howTo5 = font.render("Press Escape Key ----------------- Quit Game", 1, (0, 0, 0))

    font = pygame.font.SysFont("palatinolinotype", 40, True)
    goalText = font.render("Objective: launch the ball to hit the target", 1, (0, 0, 0))

    win.blit(titleText, (250, 120))
    win.blit(howTo1, (200, 330))
    win.blit(howTo2, (200, 370))
    win.blit(howTo3, (200, 410))
    win.blit(howTo4, (200, 450))
    win.blit(howTo5, (200, 490))
    win.blit(goalText, (140, 240))
    pygame.display.update()


def redraw():
    font = pygame.font.SysFont("comicsans", 40, True)
    win.blit(bg, (0, 0))
    if not launch:
        pygame.draw.line(win, (0, 0, 0), (x, y), (int((x + powerx/6 * math.cos(angle))), int(y - powerx/6 * math.sin(angle))), 4)
        angleText = font.render("Angle: " + str(round(math.degrees(angle))) + "°", 1, (0, 0, 0))  # Arguments are: text, anti-aliasing, color
        scoreText = font.render("Score: " + str(score), 1, (0, 0, 0))
        livesText = font.render("Lives: " + str(lives), 1, (0, 0, 0))
        powerText = font.render("Power: " + str(Vtot), 1, (0,0,0))
        win.blit(angleText, (60, 60))
        win.blit(powerText, (60, 100))
        win.blit(livesText, (850, 60))
        win.blit(scoreText, (850, 100))

    font = pygame.font.SysFont("leelawadeeui", 60, True)
    miss = font.render("You Missed :(", 1, (0, 0, 0))
    slingImg = pygame.image.load('slingshot.png')

    if lives == 0:
        font = pygame.font.SysFont("palatinolinotype", 100, True)
        gameOver = font.render("Game Over", 1, (0, 0, 0))
        font = pygame.font.SysFont("ebrima", 50, True)
        finalScore = font.render("Your Score is " + str(score), 1, (0, 0, 0))
        font = pygame.font.SysFont("leelawadeeui", 40, True)
        playAgain = font.render("Play Again?", 1, (0, 0, 0))
        miss = font.render("", 1, (0, 0, 0))

        pygame.draw.rect(win, (255, 255, 255), (370, 400, 250, 60))
        win.blit(gameOver, (240, 200))
        win.blit(finalScore, (320, 300))
        win.blit(playAgain, (380, 400))

    if missed:
        win.blit(miss, (320, 300))

    if hit:
        font = pygame.font.SysFont("leelawadeeui", 100, True)
        miss = font.render("You Hit It!", 1, (0, 0, 0))
        win.blit(miss, (240, 200))

    if lives != 0:
        pygame.draw.line(win, (0,0,0), (120, 700), (480, 700), 4)
        pygame.draw.rect(win, (0,0,0), (powerx, 690, 20, 20))
        pygame.draw.line(win, (0, 0, 0), (63, 190), (63, 550), 4)
        pygame.draw.rect(win, (0, 0, 0), (53, int(angley), 20, 20))

    win.blit(slingImg, (30, 620))
    pygame.draw.circle(win, (0, 0, 255), (x, y), 15)
    win.blit(target, (xtarget, ytarget))

    angleslider = slider(53, int(angley), 63, 190, 63, 550)
    powerslider = slider(powerx, 690, 120, 700, 490, 700)
    angleslider.draw(win)
    powerslider.draw(win)
    pygame.display.update()

#main loop
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

    # reset
    if keys[pygame.K_BACKSPACE]:
        if hit:
            xtarget = randint(500, 900)
        launch = False
        fall = True
        Vy = -Vtot * math.sin(angle)
        x = 63
        y = 630
        missed = False
        start = False
        hit = False
        lock = True

    if fall and launch:
        x += int(Vx * t)
        y += int(Vy * t)
        Vy = Vy + g
        redraw()

        # hit
        if (((x+15) >= xtarget) and (x-15) <= (xtarget + 115)) and ((y >= ytarget) and (y <= (ytarget + 26)) ):
            hit = True
            score += 1
            fall = False
        # miss
        elif y >= 670:
            fall = False
            redraw()
            missed = True
            lives -= 1

    if keys[pygame.K_UP]:
        angle += math.pi / 180
        if angle > math.pi / 2:
            angle = math.pi / 2
        angley = 550 - 4*(math.degrees(angle))
        redraw()
        start = False

    if keys[pygame.K_DOWN]:
        angle -= math.pi / 180
        if angle < 0:
            angle = 0
        angley = 550 - 4 * (math.degrees(angle))
        redraw()
        start = False
    if keys[pygame.K_LEFT]:
        Vtot -= 50
        powerx = 120 + Vtot / 10
        if Vtot < 0:
            Vtot = 0
    if keys[pygame.K_RIGHT]:
        Vtot += 50
        powerx = 120 + Vtot / 10
        if Vtot > 3600:
            Vtot = 3600
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pos() >= (53, angley) and pygame.mouse.get_pos() <= (73, angley + 20):
            drag1 = True
        if pygame.mouse.get_pos() >= (powerx, 690) and pygame.mouse.get_pos() <= (powerx+20, 710):
            drag2 = True
    if event.type == pygame.MOUSEBUTTONUP:
        drag1 = False
        drag2 = False
    if drag1:
        (null,angley) = pygame.mouse.get_pos()
        if angley <= 190:
            angley = 190
        if angley >= 550:
            angley = 550
        angle = (math.radians(550 - angley) / 4)
    if drag2:
        (powerx,null) = pygame.mouse.get_pos()
        if powerx < 120:
            powerx = 120
        if powerx > 480:
            powerx = 480
        Vtot = 10 * (powerx - 120)
    if keys[pygame.K_ESCAPE]:
        run = False
    if lives == 0:
        end = True

    if start:
        go()
        win.blit(bg, (0, 0))

    if not start:
        redraw()

    if lives == 0:
        if event.type == pygame.MOUSEBUTTONDOWN:
            (apple,pie) = pygame.mouse.get_pos()
            if  apple>= 370 and apple <= 620 and pie >= 400 and pie <= 460:
                # Variable list
                x = 63
                y = 630
                time = 10
                xtarget = randint(500, 900)
                ytarget = 640
                angley = 430
                null = 69
                # trig
                angle = math.pi / 6
                Vtot = 1300
                powerx = 120 + Vtot / 10
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
                drag1 = False
                drag2 = False
                # game stuff
                score = 0
                lives = 5

pygame.quit()