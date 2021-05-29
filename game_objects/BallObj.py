import pygame as pg


class Ball:
    def __init__(self, screen, x, y, speed_x=4, speed_y=4, size=12):
        self.borders = screen
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.size = 12
        self.body = pg.Rect((x - self.size / 2), y - self.size - 2, self.size,
                            self.size)

    def bouncing(self, paddle):
        # code to limit bottom =  or self.body.bottom >= self.borders[1]
        if self.body.top <= 0:
            self.speed_y *= -1
        if self.body.left <= 0 or self.body.right >= self.borders[0]:
            self.speed_x *= -1
        if self.body.bottom == paddle.body.top and (
                self.body.right >= paddle.body.left and self.body.left <= paddle.body.right):
            self.speed_y *= -1
        if self.body.top >= paddle.body.bottom:
            paddle.alive = False

    # Update position based on speed
    def update(self, paddle):
        self.bouncing(paddle)
        self.body.x += self.speed_x
        self.body.y += self.speed_y

    def draw(self, screen):
        pg.draw.ellipse(screen, pg.Color('white'), [self.body.x, self.body.y, self.size, self.size])
