import pygame
import functools
import random
import multiprocessing
import matrix
import joystick

BLACK = (0, 0, 0)
WIDTH_VERTICAL = 16
HEIGHT_VERTICAL = 24
WIDTH_HORIZONTAL = 16
HEIGHT_HORIZONTAL = 32
LEVEL = 10

class Block:

        def __init__(self, shape, color, width, height, x, y):
                self.shape = shape
                self.color = color
		self.width = width
		self.height = height
                self.x = x
                self.y = y

        def points(self):
                return ((self.x + x, self.y + y) for x, y in self.shape)

        def check(self, display):
                return any(y >= self.height or x >= self.width or x < 0 or y >= 0 and display[y][x] != BLACK for x, y in self.points())

        def move(self, x, y):
                return Block(self.shape, self.color, self.width, self.height, self.x + x, self.y + y)

        def turn(self, r):
                shape = tuple((-y * r, x * r) for x, y in self.shape)
                return Block(shape, self.color, self.width, self.height, self.x, self.y)

        def fix(self, display):
                display = [list(line) for line in display]
                for x, y in self.points():
                        if y >= 0 and x >= 0 and y < self.height and x < self.width:
                                display[y][x] = self.color
                return display

I = ((0, -1), (0, 0), (0, 1), (0, 2))
T = ((0, -1), (0, 0), (1, 0), (-1, 0))
Z = ((0, -1), (0, 0), (1, 0), (-1, -1))
S = ((0, -1), (0, 0), (-1, 0), (1, -1))
O = ((0, -1), (0, 0), (1, 0), (1, -1))
L = ((0, -1), (0, 0), (0, 1), (-1, 1))
J = ((0, -1), (0, 0), (0, 1), (1, 1))

SHAPES = (I, T, Z, S, O, L, J)
COLORS = ((255, 0, 0), (0, 255, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 127, 0), (0, 0, 255))

def newblock(width, height, x, y):
        n = random.randint(0, len(SHAPES) - 1)
        shape = SHAPES[n]
        color = COLORS[n]
        return Block(shape, color, width, height, x, y)

def show_horizontal(canvas, display, width, height):
        for x, line in enumerate(display):
                for y, pixel in enumerate(line):
                        for i in range(matrix.height / width):
                                for j in range(matrix.width / height):
                                        if pixel != BLACK:
                                                r, g, b = pixel
                                                canvas.SetPixel(x * matrix.height / width + i, y * matrix.width / height + j, r, g, b)
        return canvas

def show_vertical(pos, canvas, display, width, height):
        for y, line in enumerate(display):
                for x, pixel in enumerate(line):
                        for i in range(matrix.cols / width):
                                for j in range(matrix.height / height):
                                        if pixel != BLACK:
                                                r, g, b = pixel
                                                canvas.SetPixel(x * matrix.cols / width + i + matrix.cols * pos, y * matrix.height / height + j, r, g, b)
	return canvas

def clear(display, width, height):
        bottom = tuple(line for line in display if not all(pixel != BLACK for pixel in line))
        n = height - len(bottom)
        top = ((BLACK,) * width,) * n
        return (top + bottom, n)

class Tetris:

	def __init__(self, pos, queue):
		self.pos = pos
		self.queue = queue
		self.current = None
		self.width = WIDTH_VERTICAL if pos else WIDTH_HORIZONTAL
		self.height = HEIGHT_VERTICAL if pos else HEIGHT_HORIZONTAL
        	self.display = ((BLACK,) * self.width,) * self.height
		self.score = 0
        	self.counter = 0
       		self.buttons = {'05':False,'07':False,'06':False,'0D':False,'0E':False}

	def run(self):
		playing = True
		if not self.current:
                        self.current = newblock(self.width, self.height, self.width / 2, 0)
                        if self.current.check(self.display):
                                playing = False
                while not self.queue.empty():
                        (pressed, button) = self.queue.get()
                        self.buttons[button] = pressed
                if self.buttons['07' if pos else '05'] and not self.current.move(-1, 0).check(self.display):
                        self.current = self.current.move(-1, 0)
                if self.buttons['05' if pos else '07'] and not self.current.move(1, 0).check(self.display):
                        self.current = self.current.move(1, 0)
                if self.buttons['06'] and not self.current.move(0, 1).check(display):
                        self.current = self.current.move(0, 1)
                if self.buttons['0D'] and not self.current.turn(1).check(display):
                        self.current = self.current.turn(1)
                if self.buttons['0E'] and not self.current.turn(-1).check(display):
                        self.current = self.current.turn(-1)
                if self.counter < LEVEL - self.score / 4:
                        self.counter += 1
                else:
                        if self.current.move(0, 1).check(self.display):
                                (self.display, n) = clear(self.current.fix(self.display), self.width, self.height)
                                self.score += n
                                self.current = None
                        else:
                                self.current = self.current.move(0, 1)
                        self.counter = 0
		return playing

	def show(self, canvas):
		show = functools.partial(show_vertical, self.pos - 1) if self.pos else show_horizontal
		return show(canvas, self.current.fix(self.display) if self.current else self.display, self.width, self.height)

if __name__ == '__main__':
	(js0, queue0) = joystick.queue('/dev/input/js0')
	js0.daemon = True
      	a = Tetris(1, queue0)
	(js1, queue1) = joystick.queue('/dev/input/js1')
	b = Tetris(3, queue1)
	js0.start()
	js1.start()
        canvas = matrix.matrix.CreateFrameCanvas()
        clock = pygame.time.Clock()
	while True:
                clock.tick(10)
		a.run()
		b.run()
		canvas.Clear()
		canvas = a.show(canvas)
		canvas = b.show(canavs)
		canvas = matrix.matrix.SwapOnVSync(canvas)

