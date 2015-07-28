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
	canvas.Clear()
        for x, line in enumerate(display):
                for y, pixel in enumerate(line):
                        for i in range(matrix.height / width):
                                for j in range(matrix.width / height):
                                        if pixel != BLACK:
                                                r, g, b = pixel
                                                canvas.SetPixel(x * matrix.height / width + i, y * matrix.width / height + j, r, g, b)
        return matrix.matrix.SwapOnVSync(canvas)

def show_vertical(pos, canvas, display, width, height):
	canvas.Clear()
        for y, line in enumerate(display):
                for x, pixel in enumerate(line):
                        for i in range(matrix.cols / width):
                                for j in range(matrix.height / height):
                                        if pixel != BLACK:
                                                r, g, b = pixel
                                                canvas.SetPixel(x * matrix.cols / width + i + matrix.cols * pos, y * matrix.height / height + j, r, g, b)
        return matrix.matrix.SwapOnVSync(canvas)

def clear(display, width, height):
        bottom = tuple(line for line in display if not all(pixel != BLACK for pixel in line))
        n = height - len(bottom)
        top = ((BLACK,) * width,) * n
        return (top + bottom, n)

def main(pos, queue):
        current = None
	width = WIDTH_VERTICAL if pos else WIDTH_HORIZONTAL
	height = HEIGHT_VERTICAL if pos else HEIGHT_HORIZONTAL
        display = ((BLACK,) * width,) * height
        clock = pygame.time.Clock()
        score = 0
        counter = 0
        buttons = {'05':False,'07':False,'06':False,'0D':False,'0E':False}
        canvas = matrix.matrix.CreateFrameCanvas()
        while True:
                clock.tick(10)
                if not current:
                        current = newblock(width, height, width / 2, 0)
                        if current.check(display):
                                break
                while not queue.empty():
                        (pressed, button) = queue.get()
                        buttons[button] = pressed
                if buttons['07' if pos else '05'] and not current.move(-1, 0).check(display):
                        current = current.move(-1, 0)
                elif buttons['05' if pos else '07'] and not current.move(1, 0).check(display):
                        current = current.move(1, 0)
                elif buttons['06'] and not current.move(0, 1).check(display):
                        current = current.move(0, 1)
                elif buttons['0D'] and not current.turn(1).check(display):
                        current = current.turn(1)
                elif buttons['0E'] and not current.turn(-1).check(display):
                        current = current.turn(-1)
                if counter < LEVEL - score / 4:
                        counter += 1
                else:
                        if current.move(0, 1).check(display):
                                (display, n) = clear(current.fix(display), width, height)
                                score += n
                                current = None
                        else:
                                current = current.move(0, 1)
                        counter = 0
		show = functools.partial(show_vertical, pos - 1) if pos else show_horizontal
		canvas = show(canvas, current.fix(display) if current else display, width, height)

if __name__ == '__main__':
	(js0, queue0) = joystick.queue('/dev/input/js0')
	js0.daemon = True
      	a = multiprocessing.Process(target=main, args=(1, queue0))
	a.daemon = True
	(js1, queue1) = joystick.queue('/dev/input/js1')
	b = multiprocessing.Process(target=main, args=(3, queue1))
	b.daemon = True
	js0.start()
	js1.start()
	a.start()
	b.start()
	while a.is_alive() and b.is_alive():
		pass

