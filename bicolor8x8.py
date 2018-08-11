from machine import I2C, Pin


RED = const(0)
GREEN = const(1)
YELLOW = const(2)


class BiColor8x8:
    """
    A driver for the AdaFruit 8x8 bi-color LED Matrix with the HT16K33 backpack.

    For example:

    display = BiColor8x8()

    # set the top-left pixel to red
    display[0, 0] = BiColor8x8.RED

    # turn off the top-left pixel
    display[0, 0] = None

    # draw a diagonal line in green
    for i in range(8):
        display[i, i] = BiColor8x8.GREEN

    # clear the display
    display.clear()
    """

    BAUDRATE = 400000

    def __init__(self, i2c=None, addr=0x70, brightness=15, reset=True):
        """
        Create a new matrix driver.

        :param i2c: an I2C object
        :param addr: the address of the backpack on the bus
        :param brightness: the initial brightness of the matrix
        :param reset: whether to clear the matrix
        """
        self.is_on = None
        self.addr = addr

        # Normally this would be a bytearray but this has to store u16 values
        self.buf = [0] * 8

        if i2c:
            self.i2c = i2c
        else:
            self.i2c = I2C(0, I2C.MASTER, baudrate=self.BAUDRATE)

        # Turn on the HT16K33 oscillator
        self._write(b'\x21')

        if reset:
            self.set_brightness(brightness)
            self.clear()
            self.on()

    def _write(self, data):
        self.i2c.writeto(self.addr, data)

    def on(self):
        """
        Turn on the matrix.
        """
        self.is_on = True
        self._write(bytes([0x81]))

    def off(self):
        """
        Turn off the matrix.
        """
        self.is_on = False
        self._write(b'\x80')

    def set_brightness(self, value):
        """
        Set the matrix brightness.

        :param value: a level between 0 and 15
        """
        self._write(bytes([0xE0 | value]))

    def clear(self):
        """
        Clear the buffer. This will only take effect after calling draw().
        """
        for i in range(8):
            self.buf[i] = 0

    def __setitem__(self, coord, color):
        """
        Set a pixel color in the buffer. This will only take effect after calling draw().
        """
        x, y = coord
        if color == GREEN:
            self.buf[y] |= 1 << x
            self.buf[y] &= ~(1 << (x + 8))
        elif color == RED:
            self.buf[y] |= 1 << (x + 8)
            self.buf[y] &= ~(1 << x)
        elif color == YELLOW:
            self.buf[y] |= (1 << (x + 8)) | (1 << x)
        elif color is None:
            self.buf[y] &= ~(1 << x) & ~(1 << (x + 8))
        else:
            raise ValueError("Invalid color")

    def draw(self):
        """
        Draw the buffer to the matrix.
        """
        data = bytearray(1)
        for b in self.buf:
            data.append(b & 0xff)
            data.append(b >> 8)
        self._write(data)
