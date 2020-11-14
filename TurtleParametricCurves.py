import turtle
import time
from statistics import mean
from math import *


# TODO: Faster without compromising quality (as much)
# TODO: Rainbow animation (https://clarle.github.io/yui3/yui/docs/color/rgb-slider.html)
# TODO: Be able to input your own curve


class ParametricCurve:
    PEN_SPEED = 10  # Speed sacrifices quality :(

    def __init__(self, xeq, yeq, t_min, t_max, mag):
        self.t_min = t_min
        self.t_max = t_max

        self.t = t_min  # Default
        t = self.t

        self.xeq = xeq
        self.yeq = yeq

        self.x = eval(self.xeq)
        self.y = eval(self.yeq)
        self.mag = mag
        self.mag_x = self.mag * self.x
        self.mag_y = self.mag * self.y

    def update_coords(self, t_input):
        t = t_input

        self.x = eval(self.xeq)  # Do I need to update this way
        self.y = eval(self.yeq)
        self.mag_x = self.mag * self.x
        self.mag_y = self.mag * self.y

    def go_to_start(self):
        t = self.t_min

        pen.up()
        pen.goto(self.mag_x, self.mag_y)
        pen.down()

    @staticmethod
    def increment_color(turtle):
        """
        :param turtle: turtle from Turtle
        :param pencolor: pencolor (r,g,b) tuple as per Python turtle documentation
        :return: new pen color tuple
        """
        # TODO: Account for non-rgb colors (e.g. "blue")
        COLOR_SPEED = 0.2  # Value from 0 to 0.2

        current_color = turtle.pencolor()
        sign = 1 if mean(current_color) < 0.8 else -1
        increment = tuple(sign * COLOR_SPEED for _ in range(3))
        new_pencolor = tuple(p + q for p, q in zip(current_color, increment))  # Element-wise incrementing color
        turtle.pencolor(new_pencolor)

    def plot_curve(self):
        self.go_to_start()

        while True:
            self.update_coords(self.t)

            if self.t >= self.t_max:
                break

            pen.goto(self.mag_x, self.mag_y)
            self.t += ParametricCurve.PEN_SPEED / 100
            self.increment_color(pen)


# Default parametric curves
heart = ParametricCurve("16 * sin(t) ** 3", "13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)", -pi, pi, 18)
lisajous_curve = ParametricCurve("4*sin(12/13*t)", "3*sin(t)", 0, 16 * pi, 75)
butterfly = ParametricCurve("sin(t)*(e**cos(t)-2*cos(4*t)-(sin(t/12)**5))",
                            "cos(t)*(e**cos(t)-2*cos(4*t)-(sin(t/12)**5))", 0, 2*pi, 50)

default_curves = [heart, lisajous_curve, butterfly]

# Turtle Graphics setup
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Turtle Graphics")
wn.setup(700, 700)

pen = turtle.Turtle()
pen.color(0.1, 0.5, 0.6)
pen.shape("turtle")
pen.width(10)

time.sleep(1)


def main():
    for curve in default_curves:
        curve.plot_curve()
        if curve == default_curves[-1]:
            input("Press enter to quit: ")
        else:
            input("Press enter to move on to the next curve: ")
        pen.clear()


if __name__ == "__main__":
    main()
