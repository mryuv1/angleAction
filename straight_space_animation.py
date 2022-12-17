import pygame
import pandas as pd
import numpy as np
import re

colors = {'BLACK': (0, 0, 0),
          'GRAY': (127, 127, 127),
          'WHITE': (255, 255, 255),
          'YELLOW': (255, 255, 0),
          'CYAN': (0, 255, 255),
          'MAGENTA': (255, 0, 255),
          'RED': (255, 0, 0),
          'GREEN': (0, 255, 0)
          }

h_initial_conditions = {
    'current_q1': 300,
    'current_q2': 400,
    'res': (1000, 1000)
}


class twoD_Harmonic_separable_Heniltonian:
    def __init__(self, **kwargs):
        self.m1 = kwargs.setdefault('m1', 1)
        self.m2 = kwargs.setdefault('m2', 1)
        self.w1 = kwargs.setdefault('w1', 1)
        self.w2 = kwargs.setdefault('w2', 1)
        self.current_q1 = kwargs.setdefault('current_q1', 0)
        self.current_p1 = kwargs.setdefault('current_p1', 0)
        self.current_q2 = kwargs.setdefault('current_q2', 0)
        self.current_p2 = kwargs.setdefault('current_p2', 0)
        self.previous_q1 = kwargs.setdefault('previous_q1', self.current_q1)
        self.previous_p1 = kwargs.setdefault('previous_p1', self.current_p1)
        self.previous_q2 = kwargs.setdefault('previous_q2', self.current_q2)
        self.previous_p2 = kwargs.setdefault('previous_p2', self.current_p2)
        self.res = kwargs.setdefault('res', (0, 0))
        self.radius = kwargs.setdefault('radius', 5)
        self.center = kwargs.setdefault('center', (0, 0))
        self.dt = kwargs.setdefault('dt', 0.01)
        # print((self.current_q1, self.current_p1, self.current_q2, self.current_p2))

    def step(self):
        self.previous_q1 = self.current_q1
        self.previous_p1 = self.current_p1
        self.previous_q2 = self.current_q2
        self.previous_p2 = self.current_p2

        self.current_q1 = self.previous_q1 + self.dt * (self.previous_p1 // self.m1)
        self.current_p1 = self.previous_p1 - self.dt * (self.w1 ** 2) * self.current_q1
        self.current_q2 = self.previous_q2 + self.dt * (self.previous_p2 // self.m2)
        self.current_p2 = self.previous_p2 - self.dt * (self.w2 ** 2) * self.current_q2

        # print((self.current_q1, self.current_p1, self.current_q2, self.current_p2))

        self.center = (self.current_q1 + self.res[0] // 2, -self.current_q2 + self.res[1] // 2)


class Step:
    def __init__(self, **kwargs):
        """
        The cordinats are NOT in the pyGame board
        :param kwargs:
        """
        self.x_right = kwargs.setdefault('x_right', -200)
        self.y_up = kwargs.setdefault('y_up', -200)
        self.x_left = kwargs.setdefault('x_left', -500)
        self.y_down = kwargs.setdefault('y_down', -500)
        self.flag = 1
        self.epsilon = kwargs.setdefault('epsilon', 5)

    def convert_to_rect_params(self, width, height):
        left = self.x_left + width // 2
        top = -self.y_up + height // 2
        width = self.x_right - self.x_left
        height = self.y_up - self.y_down

        return left, top, width, height

    def return_rule(self, q1, q2, p1, p2):
        if (q1 < self.x_right) and (q1 > (self.x_right - self.epsilon)):
            if q2 < self.y_up:
                self.flag = 0
                return -p1, p2

        if (q2 < self.y_up) and (q2 > (self.y_up - self.epsilon)):
            if q1 < self.x_right:
                self.flag = 0
                return p1, -p2

        if (q1 > self.x_right) and (q2 > self.y_up):
            self.flag = 1

        return p1, p2


class Trimmed_step:
    def __init__(self, **kwargs):
        """
        The cordinats are NOT in the pyGame board
        :param kwargs:
        """
        self.x_right = kwargs.setdefault('x_right', -200)
        self.y_up = kwargs.setdefault('y_up', -200)
        self.x_left = kwargs.setdefault('x_left', -500)
        self.y_down = kwargs.setdefault('y_down', -500)
        self.x_trim = kwargs.setdefault('x_trim', -300)
        self.y_trim = kwargs.setdefault('y_trim', -400)
        self.epsilon = kwargs.setdefault('epsilon', 5)
        self.flag = 1

        if self.x_right != self.x_trim:
            self.slope = (self.y_trim - self.y_up) / (self.x_right - self.x_trim)
        else:
            self.slope = np.inf

    def convert_to_polygon_params(self, width, height):
        top_left = (self.x_left + width // 2, -self.y_up + height // 2)
        trim_up_left = (self.x_trim + width // 2, -self.y_up + height // 2)
        trim_down_right = (self.x_right + width // 2, -self.y_trim + height // 2)
        bottom_right = (self.x_right + width // 2, -self.y_down + height // 2)
        corner = (self.x_left + width // 2, -self.y_down + height // 2)

        return [top_left, trim_up_left, trim_down_right, bottom_right, corner]

    def calculated_returned_momentum(self, p1, p2):
        """
        calculate the return values of the momentum, by the formula of:
        |p1_return| = |cos(2*theta)      sin(2*theta)    | |p1|
        |p2_return| = |sin(2 * theta)    -cos(2 * theta) | |p2|
        :param p1:
        :param p2:
        :return: p1_return, p2_return
        """
        theta = np.arctan(self.slope)
        p1_return = p1*np.cos(2*theta) + p2*np.sin(2*theta)
        p2_return = p1*np.sin(2 * theta) - p2*np.cos(2 * theta)
        return p1_return, p2_return

    def return_rule(self, q1, q2, p1, p2):

        if (q1 < self.x_right) and (q1 > (self.x_right - self.epsilon)):
            if q2 < self.y_trim and self.flag:
                self.flag = 0
                return -p1, p2

        if (q2 < self.y_up) and (q2 > (self.y_up - self.epsilon)):
            if q1 < self.x_trim and self.flag:
                self.flag = 0
                return p1, -p2

        if (q1 < self.x_right) and (q2 < self.y_up):
            line_val = (q1 - self.x_trim) * self.slope
            if ((q2 - self.y_up) < line_val) and self.flag:
                self.flag = 0
                print("now flag is" + str(self.flag))
                p1_return, p2_return = self.calculated_returned_momentum(p1, p2)
                return p1_return, p2_return

        if (q1 > self.x_right) and (q2 > self.y_up):
            self.flag = 1

        return p1, p2


def dynamics(screen, hamiltonian, obstacle=None):
    hamiltonian.step()
    if obstacle:
        hamiltonian.current_p1, hamiltonian.current_p2 = obstacle.return_rule(hamiltonian.current_q1,
                                                                              hamiltonian.current_q2,
                                                                              hamiltonian.current_p1,
                                                                              hamiltonian.current_p2)
    pygame.draw.circle(screen, colors['WHITE'],
                       center=hamiltonian.center,
                       radius=hamiltonian.radius)


def main():
    # initializing the constructor
    pygame.init()
    pygame.font.init()
    # screen resolution
    res = h_initial_conditions['res']

    # opens up a window
    screen = pygame.display.set_mode(res)
    
    width, height = screen.get_width(), screen.get_height()

    # Screen Update Speed (FPS)
    clock = pygame.time.Clock()

    h = twoD_Harmonic_separable_Heniltonian(**h_initial_conditions)
    step1 = Step()
    trimmed_step = Trimmed_step()

    while True:
        # fills the screen with a color
        screen.fill(colors['BLACK'])

        # show axis
        pygame.draw.line(screen, colors['YELLOW'], (0, height//2), (width, height//2))  # X-axis
        pygame.draw.line(screen,colors['YELLOW'], (width//2, 0), (width//2, height)) # Y-axis
        pygame.draw.line(screen, colors['YELLOW'], (0, 0), (width, height))  # X=-Y-axis
        pygame.draw.line(screen, colors['YELLOW'], (width, 0), (0, height))  # X=Y-axis
        # NO OBSTACLE:
        # dynamics(screen=screen, hamiltonian=h)

        # RECT OBSTACLE:
        # pygame.draw.rect(screen, colors['RED'], step1.convert_to_rect_params(width, height))
        # dynamics(screen=screen, hamiltonian=h, obstacle=step1)

        # RECT-TRIMMED OBSTACLE:
        pygame.draw.polygon(screen, colors['CYAN'], trimmed_step.convert_to_polygon_params(width, height))
        dynamics(screen=screen, hamiltonian=h, obstacle=trimmed_step)

        pygame.display.update()

        # Setting FPS
        clock.tick(50)


if __name__ == '__main__':
    main()
