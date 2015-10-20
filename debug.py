# -*- coding: utf-8 -*-

ROWS = 16
COLS = 32

class Matrix:
    
    def __init__(self, chains, parallel):
        self.chains = chains
        self.parallel = parallel

    def width(self):
        return COLS * self.chains

    def height(self):
        return ROWS * self.parallel

    def create_canvas(self):
        return Canvas(self.width(), self.height())

    def vsync(self, canvas):
        canvas.vsync()

class Canvas:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = [[' '] * width for _ in range(height)]

    def set_pixel(self, x, y, r, g, b):
        if r > 192 and g > 192 and b > 192:
            suffix = '\033[37m'
        elif r > 192 and g > 192:
            suffix = '\033[33m'
        elif g > 192 and b > 192:
            suffix = '\033[36m'
        elif r > 192 and b > 192:
            suffix = '\033[35m'
        elif r > 192:
            suffix = '\033[31m'
        elif g > 192:
            suffix = '\033[32m'
        elif b > 192:
            suffix = '\033[34m'
        else:
            suffix = '\033[30m'
        self.canvas[y][x] = '#' + suffix

    def vsync(self):
        print(chr(27) + '[2J')
        for y in range(self.height):
            print(''.join(self.canvas[y]))
