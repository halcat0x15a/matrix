# -*- coding: utf-8 -*-

import sys
from subprocess import call
import feedparser
import pygame
from pygame.locals import *
from matrix import *

yahoo = 'http://rss.dailynews.yahoo.co.jp/fc/domestic/rss.xml'

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
    for entry in feedparser.parse(yahoo)['entries']:
        text = entry.title
        draw(text)
        call(["./jsay", text])
