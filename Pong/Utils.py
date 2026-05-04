class Ball:
    def __init__(self, realX: float, realY: float, speed: float, sprite = 'O'):
        self.realX = realX
        self.realY = realY
        self.speed = speed
        self.sprite = sprite

    def roundedX(self):
        return round(self.realX)
    
    def roundedY(self):
        return round(self.realY)

class Paddle:
    def __init__(self, realY: float, height: int, sprite = '|'):
        self.realY = realY
        self.height = height
        self.sprite = sprite

    def roundedY(self):
        return round(self.realY)

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def zero(self):
        self.x = 0
        self.y = 0

    def one(self):
        self.x = 1
        self.y = 1

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"{self.x}, {self.y}"
    
    