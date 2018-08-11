import time

from bicolor8x8 import BiColor8x8, RED, GREEN, YELLOW


matrix = BiColor8x8()

while True:
    for color in (RED, GREEN, YELLOW):
        for x in range(8):
            for y in range(8):
                matrix[x, y] = color

        matrix.draw()
        time.sleep(1)
