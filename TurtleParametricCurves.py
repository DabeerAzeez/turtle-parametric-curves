import turtle
import time
from math import *

# TODO: Faster without compromising quality (as much)
# TODO: Be able to input your own curve
# TODO: Optional parameters for plotcurve()
# TODO: Multithreading to draw multiple curves at once
# TODO: Start at any arbitrary color

# Turtle Graphics setup
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Turtle Graphics")
wn.setup(700, 700)

turtle = turtle.Turtle()
turtle.shape("turtle")
turtle.width(10)
time.sleep(1)


class ParametricCurve:
    STEP_SIZE = 1 / 100  # Step size for pen; larger step size is faster but lower quality :(

    def __init__(self, xeq, yeq, t_min, t_max, mag):
        self.t_min = t_min
        self.t_max = t_max

        self.t = t_min  # Default
        t = self.t

        self.xeq = xeq  # Evaluate (initial) x and y coordinates
        self.yeq = yeq
        self.x = eval(self.xeq)
        self.y = eval(self.yeq)
        self.mag = mag
        self.mag_x = self.mag * self.x
        self.mag_y = self.mag * self.y

        self.stage = 1  # For color changing

    def update_coords(self, t_input):
        """
        Re-evaluates (x,y) coordinates for a new t value
        :param t_input: new t-value to re-evaluate the coordinates at
        """
        t = t_input

        self.x = eval(self.xeq)  # Do I need to update this way
        self.y = eval(self.yeq)
        self.mag_x = self.mag * self.x
        self.mag_y = self.mag * self.y

    def go_to_start(self):
        """
        Lifts pen, drops it at the start of the parametric curve, and resets color
        """
        t = self.t_min

        turtle.up()
        turtle.goto(self.mag_x, self.mag_y)
        turtle.color(1, 0, 0)  # reset color to red (beginning of rainbow)
        turtle.down()

    def increment_color(self, input_turtle):
        """
        Increments turtle pen color in a rainbow pattern
        :param input_turtle: turtle object from turtle library
        """
        # TODO: Account for non-rgb colors (e.g. "blue")

        STEPS = (self.t_max - self.t_min) / ParametricCurve.STEP_SIZE
        NUM_STAGES = 6  # Rainbow pattern has 6 stages
        COLOR_SPEED = NUM_STAGES / STEPS  # Lower values indicate smoother color transitions; suggested values 0-0.5

        current_color = input_turtle.pencolor()

        if current_color == (1, 0, 0):
            self.stage = 1
        elif current_color == (1, 1, 0):
            self.stage = 2
        elif current_color == (0, 1, 0):
            self.stage = 3
        elif current_color == (0, 1, 1):
            self.stage = 4
        elif current_color == (0, 0, 1):
            self.stage = 5
        elif current_color == (1, 0, 1):
            self.stage = 6

        # determine appropriate increment depending on progress through the rainbow
        increment = (0, 0, 0)  # default

        if self.stage == 1:
            increment = (0, COLOR_SPEED, 0)  # Add green
        elif self.stage == 2:
            increment = (-COLOR_SPEED, 0, 0)  # Remove red
        elif self.stage == 3:
            increment = (0, 0, COLOR_SPEED)  # Add blue
        elif self.stage == 4:
            increment = (0, -COLOR_SPEED, 0)  # Remove green
        elif self.stage == 5:
            increment = (COLOR_SPEED, 0, 0)  # Add red
        elif self.stage == 6:
            increment = (0, 0, -COLOR_SPEED)  # Remove blue

        # Calculate new pen color
        new_pencolor = tuple(p + q for p, q in zip(current_color, increment))  # Add increment to old pen color tuple
        new_pencolor = tuple(1 if color > 1 else color for color in new_pencolor)  # Check for extraneous color values
        new_pencolor = tuple(0 if color < 0 else color for color in new_pencolor)
        input_turtle.pencolor(new_pencolor)

    def plot_curve(self):
        """
        Plots the parametric curve, moving the pen incrementally throughout the curve and changing the pen color
        """
        self.go_to_start()

        while True:
            self.update_coords(self.t)

            if self.t >= self.t_max:
                break

            turtle.goto(self.mag_x, self.mag_y)
            self.t += ParametricCurve.STEP_SIZE
            self.increment_color(turtle)


# Default parametric curves—things I've gathered from the internet; NOT my own creations
heart = ParametricCurve("16 * sin(t) ** 3", "13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)", -pi, pi, 18)
lisajous_curve = ParametricCurve("4*sin(12/13*t)", "3*sin(t)", 0, 16 * pi, 75)
butterfly = ParametricCurve("sin(t)*(e**cos(t)-2*cos(4*t)-(sin(t/12)**5))",
                            "cos(t)*(e**cos(t)-2*cos(4*t)-(sin(t/12)**5))", 0, 2 * pi, 50)
mystery = ParametricCurve("cos(t)-cos(80*t)*sin(t)", "2*sin(t)-sin(80*t)", 0, 2 * pi, 75)

default_curves = [mystery, heart, lisajous_curve, butterfly]


def main():
    for curve in default_curves:
        curve.plot_curve()
        if curve == default_curves[-1]:  # If you've reached the last curve
            input("Press enter to quit: ")
        else:
            input("Press enter to move on to the next curve: ")
        turtle.clear()


if __name__ == "__main__":
    main()
