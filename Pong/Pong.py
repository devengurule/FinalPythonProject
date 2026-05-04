import curses
import time
from Utils import Ball, Vector2

def TryQuit(screen: curses.window):
    key = screen.getch()

    if key in (10, 13):
        return True
    else: return False

def CalculateBallPos():
    velocity = direction * ball.speed * timeStep

    ball.realX += velocity.x
    ball.realY += velocity.y

    currentBallPos.x = ball.roundedX()
    currentBallPos.y = ball.roundedY()

def CheckWallCollision():
    if currentBallPos.x + len(ball.sprite) - 1 >= w - 1 or currentBallPos.x <= 0:
        # hitting/exiting right or left side of screen
        direction.x *= -1

        CalculateBallPos()

    elif currentBallPos.y >= h - 1 or currentBallPos.y <= 0:
        # hitting/exiting bottom or top of screen
        direction.y *= -1

        CalculateBallPos()

def DrawBall(win: curses.window):
    win.addstr(currentBallPos.y, currentBallPos.x, ball.sprite)

def MainFixedUpdate(win: curses.window, screen: curses.window):
    CalculateBallPos()
    CheckWallCollision()
    DrawBall(win)

def SetUp():
    curses.curs_set(0)  # hide cursor

    y, x = 0, 0

    win = curses.newwin(h, w, y, x)
    win.border()

    return win

def RefreshScreen(win: curses.window):
    win.refresh()
    time.sleep(timeStep)

def main(screen):
    running = True
    screen.keypad(True)
    screen.nodelay(True)

    while(running):
        win = SetUp()

        MainFixedUpdate(win, screen)
        
        running = not TryQuit(screen)

        RefreshScreen(win)

timeStep = 1 / 60

# screen height & width
h, w = 30, 100

# inital ball position
ballPos = Vector2(15,15)

currentBallPos = Vector2()

# ball object
ball = Ball(ballPos.x, ballPos.y, 10, '()')

# inital ball direction
direction = Vector2(3,1)

curses.wrapper(main)