import pygame as pg


class Paddle:
    def __init__(self, screen, x, y, speed=5):
        self.borders = screen
        self.width = 180
        self.height = 10
        self.speed = speed
        self.command = 0
        self.alive = True
        self.body = pg.Rect((x - self.width / 2), (y - self.height),
                            self.width, self.height)

    def movement(self, command):
        self.command = command

    # Update position based on speed
    def update(self):
        self.body.x += (self.speed * self.command)
        if self.body.left < 0:
            self.body.left = 0
        elif self.body.right > self.borders[0]:
            self.body.right = self.borders[0]

    def draw(self, screen):
        pg.draw.rect(screen, pg.Color('red'), self.body)
