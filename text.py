# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
from matrix import *

pygame.init()
 
font = pygame.font.Font("ipag.ttf", 80)

def draw(text):
    text = font.render(unicode(text), True, (0, 0, 0))
    resized = pygame.transform.scale(text, (matrix.width, matrix.height))
    pixel = pygame.PixelArray(resized)
    canvas = matrix.CreateFrameCanvas()
    for x, row in enumerate(pixel):
        for y, value in enumerate(row):
            color = pygame.Color(value)
            canvas.SetPixel(x, y, color.r, color.g, color.b)
    return matrix.SwapOnVSync(canvas)

while True:
    draw(sys.stdin.readline().decode('utf-8')[:-1])
