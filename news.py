# -*- coding: utf-8 -*-

import sys
from subprocess import call
import threading
import feedparser
import pygame
from pygame.locals import *
#from matrix import Matrix
from debug import Matrix
import time

yahoo = 'http://rss.dailynews.yahoo.co.jp/fc/domestic/rss.xml'
niconico = 'http://news.nicovideo.jp/topiclist?rss=2.0'

pygame.init()
 
font = pygame.font.Font("ipag.ttf", 80)

def draw(matrix, text):
    text = unicode(text)
    image = font.render(text, True, (0, 0, 0))
    width = matrix.height() * len(text)
    resized = pygame.transform.scale(image, (width, matrix.height()))
    pixel = pygame.PixelArray(resized)
    for n in range(width - matrix.width()):
        canvas = matrix.create_canvas()
        for y in range(matrix.height()):
            for x in range(matrix.width()):
                value = pixel[x + n][y]
                if value > 0:
                    color = pygame.Color(value)
                    canvas.set_pixel(x, y, color[1], color[2], color[3])
        yield canvas

if __name__ == '__main__':
    matrix = Matrix(1, 1)
    while True:
        for news in [yahoo, niconico]:
            for entry in feedparser.parse(news)['entries']:
                text = entry.title
                jtalk = threading.Thread(target=lambda: call(["./jsay_mac", text]))
                jtalk.setDaemon(True)
                jtalk.start()
                for canvas in draw(matrix, text):
                    matrix.vsync(canvas)
                    time.sleep(0.05)
                time.sleep(1)
