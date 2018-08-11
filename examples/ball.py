from time import sleep
import machine
import sys

from bicolor8x8 import BiColor8x8, RED, GREEN, YELLOW


class BouncingBall:
    def __init__(self):
        self._colors = (RED, GREEN, YELLOW)
        self._color_idx = 0

    def rand_int(self, min, max):
        return int(min + (max - min) * (machine.rng() / (2 << 24)))

    def inc_color(self):
        self._color_idx = (self._color_idx + 1) % len(self._colors)

    @property
    def color(self):
        return self._colors[self._color_idx]

    def loop(self):
        matrix = BiColor8x8()

        screen_min, screen_max = 0, 7
        x = self.rand_int(screen_min + 1, screen_max - 1)
        y = self.rand_int(screen_min + 1, screen_max - 1)
        dx = 1
        dy = 1

        while True:
            # Clear the last position
            matrix[x, y] = None

            is_deflected = False

            # Deflect horziontally
            if x >= screen_max or x <= screen_min:
                dx = -dx
                is_deflected = True

            # Deflect vertically
            if y >= screen_max or y <= screen_min:
                dy = -dy
                is_deflected = True

            if is_deflected:
                self.inc_color()

            x += dx
            y += dy

            if x < screen_min:
                x = screen_min
            elif x > screen_max:
                x = screen_max

            if y < screen_min:
                y = screen_min
            elif y > screen_max:
                y = screen_max

            # Draw the new position
            matrix[x, y] = self.color
            matrix.draw()
            sleep(0.1)


ball = BouncingBall()
ball.loop()
