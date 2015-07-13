import pygame
import random
import threading

class Block:

        def __init__(self, shape, x, y):
                self.shape = shape
                self.x = x
                self.y = y

        def points(self):
                return ((self.x + x, self.y + y) for x, y in self.shape)

        def check(self, display):
                height = len(display)
                width = len(display[0])
                return any(y >= height or x >= width or x < 0 or y >= 0 and display[y][x] for x, y in self.points())

        def move(self, x, y):
                return Block(self.shape, self.x + x, self.y + y)

        def turn(self, r):
                shape = tuple((-y * r, x * r) for x, y in self.shape)
                return Block(shape, self.x, self.y)

        def fix(self, display):
                height = len(display)
                width = len(display[0])
                display = [list(line) for line in display]
                for x, y in self.points():
                        if y >= 0 and x >= 0 and y < height and x < width:
                                display[y][x] = True
                return display

I = ((0, -1), (0, 0), (0, 1), (0, 2))
T = ((0, -1), (0, 0), (1, 0), (-1, 0))
Z = ((0, -1), (0, 0), (1, 0), (1, -1))
S = ((0, -1), (0, 0), (-1, 0), (1, -1))
O = ((0, -1), (0, 0), (1, 0), (-1, -1))
L = ((0, -1), (0, 0), (0, 1), (-1, 1))
J = ((0, -1), (0, 0), (0, 1), (1, 1))

SHAPES = (I, T, Z, S, O, L, J)

def newblock(x, y):
        shape = SHAPES[random.randint(0, len(SHAPES) - 1)]
        return Block(shape, x, y)

def show(display):
        print(chr(27) + "[2J")
        for line in display:
                print("".join('*' if dot else ' ' for dot in line))

def main():
        width = 8
        height = 16
        current = None
        display = ((False,) * width,) * height
        clock = pygame.time.Clock()
        counter = 0
        while True:
		clock.tick(30)
                if current == None:
                        current = newblock(width / 2, 0)
                        if current.check(display):
                                break
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
