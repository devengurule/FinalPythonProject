import curses
import time
import random
from Utils import Ball, Vector2, Paddle

def ResetBall():
    currentBallPos.x = ballPosi.x
    currentBallPos.y = ballPosi.y
    ball.realX = ballPosi.x
    ball.realY = ballPosi.y

    direction.zero()

    while(direction.x == 0):
        direction.x = random.randint(-3, 3)

    while(direction.y == direction.x or direction.y == -direction.x or direction.y == 0):
        direction.y = random.randint(-3, 3)

def CheckPaddleWallCollision():
    # Paddle 1

    if currentPaddlePos.x + paddleVertDirection.x >= h - paddle1.height or currentPaddlePos.x + paddleVertDirection.x<= 0:
        # hitting/exiting bottom or top of screen
        paddleVertDirection.x = 0

    # Paddle 2
    if currentPaddlePos.y + paddleVertDirection.y >= h - paddle1.height or currentPaddlePos.y + paddleVertDirection.y <= 0:
        # hitting/exiting bottom or top of screen
        paddleVertDirection.y = 0

def CheckForInputs(screen):
    global running

    keys = []

    while True:
        key = screen.getch()
        if key == -1:
            break
        keys.append(key)

    if 10 in keys or 13 in keys:
        running = False
        return running 

    # Paddle 1
    if ord(up_1) in keys:
        paddleVertDirection.x = -1

    elif ord(down_1) in keys:
        paddleVertDirection.x = 1

    else:paddleVertDirection.x = 0

    # Paddle 2
    if up_2 in keys:
        paddleVertDirection.y = -1

    elif down_2 in keys:
        paddleVertDirection.y = 1

    else:paddleVertDirection.y = 0

    CheckPaddleWallCollision()

    return running
    
def CalculatePaddlePositions():
    paddle1Velocity = paddleVertDirection.x * paddleSpeed * timeStep
    paddle2Velocity = paddleVertDirection.y * paddleSpeed * timeStep

    paddle1.realY += paddle1Velocity
    paddle2.realY += paddle2Velocity

    currentPaddlePos.x = paddle1.roundedY()
    currentPaddlePos.y = paddle2.roundedY()

def DrawPaddles(win: curses.window):
    # Paddle 1
    for i in range(paddle1.height):
        win.addstr(currentPaddlePos.x + i, paddle1Posi.x, paddle1.sprite)
    # Paddle 2
    for i in range(paddle2.height):
        win.addstr(currentPaddlePos.y + i, paddle2Posi.x, paddle2.sprite)

def CalculateBallPos():
    velocity = direction * ball.speed * timeStep

    ball.realX += velocity.x
    ball.realY += velocity.y

    currentBallPos.x = ball.roundedX()
    currentBallPos.y = ball.roundedY()

def CheckWallCollision():
    # Collision check with paddle 1
    if currentBallPos.x == paddle1Posi.x:
        if currentBallPos.y == currentPaddlePos.x or currentBallPos.y - currentPaddlePos.x <= paddle1.height and currentBallPos.y - currentPaddlePos.x > 0:
            direction.x *= -1


    # Collision check with paddle 2
    if currentBallPos.x + 1 == paddle2Posi.x:
        if currentBallPos.y == currentPaddlePos.y or currentBallPos.y - currentPaddlePos.y <= paddle2.height and currentBallPos.y - currentPaddlePos.y > 0:
            direction.x *= -1


    if currentBallPos.x + len(ball.sprite) - 1 >= w - 1:
        ResetBall()
        points.x += 1
    elif currentBallPos.x <= 0:
        ResetBall()
        points.y += 1

    elif currentBallPos.y >= h - 1 or currentBallPos.y <= 0:
        # hitting/exiting bottom or top of screen
        direction.y *= -1

        # recalculate position with new direction
        CalculateBallPos()

def DrawBall(win: curses.window):
    win.addstr(currentBallPos.y, currentBallPos.x, ball.sprite)

def DrawPoints(win: curses.window):
    win.addstr(2, 35, f'Player 1) {points.x}   Player 2) {points.y}')

def FixedUpdate(win: curses.window):
    CalculatePaddlePositions()
    DrawPaddles(win)
    
    CalculateBallPos()
    CheckWallCollision()
    DrawBall(win)

    DrawPoints(win)

    time.sleep(timeStep)

def SetUp():
    curses.curs_set(0)  # hide cursor

    y, x = 0, 0

    win = curses.newwin(h, w, y, x)
    win.border()

    return win

def RefreshScreen(win: curses.window):
    win.refresh()

def main(screen):
    global running
    running = True

    screen.keypad(True)
    screen.nodelay(True)

    while(running):
        win = SetUp() 

        running = CheckForInputs(screen)

        FixedUpdate(win)

        RefreshScreen(win)

paddleSpeed = 50

#Player 1 Keybinds
up_1, down_1 = 'w', 's'
#Player 2 Keybinds
up_2, down_2 = curses.KEY_UP, curses.KEY_DOWN

timeStep = 1 / 60

# screen height & width
h, w = 30, 100

# inital ball position
ballPosi = Vector2(50, 15)

paddle1Posi = Vector2(10, 2)
paddle2Posi = Vector2(90, 2)

currentBallPos = Vector2()
currentPaddlePos = Vector2(0, 0)

# x = p1, y = p2
points = Vector2()

# ball object
ball = Ball(ballPosi.x, ballPosi.y, 10, '()')

# paddle objects
paddle1 = Paddle(paddle1Posi.y, 5)
paddle2 = Paddle(paddle2Posi.y, 5)

paddleVertDirection = Vector2(0, 0)

# inital ball direction
direction = Vector2(0, 0)

direction.x = random.randint(-3, 3)
while(direction.x == 0):
    direction.x = random.randint(-3, 3)
direction.y = random.randint(-3, 3)
while(direction.y == direction.x or direction.y == -direction.x):
    direction.y = random.randint(-3, 3)

curses.wrapper(main)