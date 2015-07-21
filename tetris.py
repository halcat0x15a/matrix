import pygame
from pygame.locals import *
import random
import threading
import matrix

BLACK = (0, 0, 0)

WIDTH = 16
HEIGHT = 32

class Block:

        def __init__(self, shape, color, x, y):
                self.shape = shape
		self.color = color
                self.x = x
                self.y = y

        def points(self):
                return ((self.x + x, self.y + y) for x, y in self.shape)

        def check(self, display):
                return any(y >= HEIGHT or x >= WIDTH or x < 0 or y >= 0 and display[y][x] != BLACK for x, y in self.points())

        def move(self, x, y):
                return Block(self.shape, self.color, self.x + x, self.y + y)

        def turn(self, r):
                shape = tuple((-y * r, x * r) for x, y in self.shape)
                return Block(shape, self.color, self.x, self.y)

        def fix(self, display):
                display = [list(line) for line in display]
                for x, y in self.points():
                        if y >= 0 and x >= 0 and y < HEIGHT and x < WIDTH:
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

def newblock(x, y):
	n = random.randint(0, len(SHAPES) - 1)
        shape = SHAPES[n]
	color = COLORS[n]
        return Block(shape, color, x, y)

def show(display):
	canvas = matrix.matrix.CreateFrameCanvas()
	for x, line in enumerate(display):
		for y, pixel in enumerate(line):
			for i in range(matrix.height / WIDTH):
				for j in range(matrix.width / HEIGHT):
					if pixel != BLACK:
 						r, g, b = pixel
						canvas.SetPixel(x * matrix.height / WIDTH + i, y * matrix.width / HEIGHT + j, r, g, b)
	matrix.matrix.SwapOnVSync(canvas)

def main():
        pygame.init()
        current = None
        display = ((BLACK,) * WIDTH,) * HEIGHT
        clock = pygame.time.Clock()
        counter = 0
        while True:
		clock.tick(30)
                if current == None:
                        current = newblock(WIDTH / 2, 0)
                        if current.check(display):
                                break
                keys = pygame.key.get_pressed()
                if keys[K_LEFT]:
                    current = current.move(-1, 0)
                if keys[K_RIGHT]:
                    current = current.move(1, 0)
                if counter < 10:
                        counter += 1
                else:
                        if current.move(0, 1).check(display):
                                display = current.fix(display)
                                current = None
                                show(display)
                        else:
                                current = current.move(0, 1)
                                show(current.fix(display))
                        counter = 0

if __name__ == '__main__':
        main()

