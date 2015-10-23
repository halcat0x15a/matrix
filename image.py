# -*- coding: utf-8 -*-

from PIL import Image

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
        self.canvas = Image.new("RGB", (width, height))

    def set_pixel(self, x, y, r, g, b):
        self.canvas.load()[x, y] = (r, g, b)

    def vsync(self):
        self.canvas.save('sample.png')
