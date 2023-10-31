import pygame as pg
import colours
from random import randint


def gravity(g=9.8):
    return g * 0.16 * 0.16 / 2


class GameObject:
    """Virtual class, describing virtual game object"""
    def __init__(self, surf, x, y, colour=None):
        self.x = x
        self.y = y
        self.surf = surf
        if not colour:
            colour = colours.rand_colour


class Ball(GameObject):
    """Class, which creates a ball object and draws it on given surface"""
    def __init__(self, surf, x=0, y=0, colour=None, width=0):
        """
        Constructor method.
        :param surf: surface, where ball should be drawn
        :param x: x coordinate of left side of ball
        :param y: y coordinate of left side of ball
        :param colour: colour of ball (default None, if nothing given to constructor, colour is random)
        :param width: width of ball
        """
        super().__init__(surf, x, y, colour)
        self.x = x
        self.y = y
        self.width = width
        self.height = self.width
        if not colour:
            colour = colours.rand_colour
        self.colour = colour
        self.is_falling = True
        self.y_acceleration = 0
        self.x_acceleration = 0

    def draw(self):
        """Method, drawing ball with given parameters"""
        pg.draw.ellipse(self.surf, self.colour, (self.x, self.y, self.width, self.height))


class Racket(GameObject):
    def __init__(self, surf, x, y, colour=None, width=20, height=8):
        """
        Constructor method.
        :param surf: surface, where racket should be drawn
        :param x: x coordinate of left side of racket
        :param y: y coordinate of left side of racket
        :param colour: colour of racket (default None, if nothing given to constructor, colour is random)
        :param width: width of racket
        :param height: height of racket
        """
        super().__init__(surf, x, y, colour)
        if not colour:
            colour = colours.rand_colour
        self.surf = surf
        self.colour = colour
        self.width = width
        self.height = height
        self.x = x - self.width / 2
        self.y = y - self.height / 2

    def draw(self):
        """Method, drawing a racket with given parameters"""
        pg.draw.line(self.surf, self.colour, (self.x, self.y), (self.x + self.width, self.y), self.height)


class GameWindow:
    """Class, which creates window with given parameters, creates game objects, tracking their interaction"""
    def __init__(self, resolution=(1600, 900), fps=60):
        self.resolution = resolution
        self.fps = fps
        self.balls = []
        self.window = pg.display.set_mode(resolution)
        self.racket = Racket(self.window, resolution[0]//2, resolution[1], width=resolution[0]//15)

    def game_round(self):
        """
        Creates new ball
        :return: None
        """

        self.balls.append(Ball(self.window, x=randint(0, self.resolution[0]), y=randint(0, self.resolution[1]), width=randint(20, 100)))

    def show(self):
        """Shows window in a screen, tracking game objects interaction for given window"""
        timer = pg.time.Clock()
        is_running = True
        while is_running:
            timer.tick(self.fps)
            self.window.fill(colours.white)
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    is_running = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                    self.game_round()
            is_pressed = pg.key.get_pressed()
            if is_pressed[pg.K_LEFT]:
                if self.racket.x > 0:
                    self.racket.x -= self.racket.height
            elif is_pressed[pg.K_RIGHT]:
                if self.racket.x < self.window.get_width() - self.racket.width:
                    self.racket.x += self.racket.height
            for ball in self.balls:
                if is_pressed[pg.K_LEFT] and ball.y > self.window.get_height() - ball.height - self.racket.height and ball.x > self.racket.x - ball.width / 2 and ball.x < self.racket.x + self.racket.width:
                    ball.x_acceleration -= 1
                if is_pressed[pg.K_RIGHT] and ball.y > self.window.get_height() - ball.height - self.racket.height and ball.x > self.racket.x - ball.width / 2 and ball.x < self.racket.x + self.racket.width:
                    ball.x_acceleration += 1
                if ball.is_falling:
                    ball.y_acceleration += gravity()
                    ball.y += ball.y_acceleration
                    if ball.y > self.racket.y - ball.height:
                        if ball.is_falling and ball.y < self.window.get_height() and ball.x > self.racket.x - ball.width * 0.7 and ball.x < self.racket.x + self.racket.width - ball.width * 0.3:
                            ball.is_falling = False
                if not ball.is_falling:
                    ball.y -= ball.y_acceleration
                    ball.y_acceleration -= gravity()
                    if not ball.is_falling and ball.y_acceleration < 0:
                        ball.is_falling = True

                if ball.x > self.window.get_width() - ball.width or ball.x < 0 and ball.y < self.window.get_height():
                    ball.x_acceleration *= -1
                    ball.x += ball.x_acceleration

                ball.x += ball.x_acceleration
                ball.draw()

            self.racket.draw()
            pg.display.flip()


def main():

    win1 = GameWindow()
    win1.show()


main()
