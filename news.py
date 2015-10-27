# -*- coding: utf-8 -*-

from subprocess import call
import threading
import feedparser
#from matrix import Matrix
#from debug import Matrix
from image import Matrix
import time
from PIL import Image, ImageDraw, ImageFont

yahoo = 'http://rss.dailynews.yahoo.co.jp/fc/domestic/rss.xml'
niconico = 'http://news.nicovideo.jp/topiclist?rss=2.0'

fontsize = 80
font = ImageFont.truetype("ipag.ttf", fontsize)

def draw(matrix, text):
    text = unicode(text)
    image = Image.new("RGBA", (len(text) * fontsize, fontsize), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, (255, 255, 255), font=font)
    width = matrix.height() * len(text)
    resized = image.resize((width, matrix.height()), Image.ANTIALIAS)
    resized.save('sample.png', 'PNG')
    canvas = matrix.create_canvas()
    for n in range(width - matrix.width()):
        for y in range(matrix.height()):
            for x in range(matrix.width()):
                r, g, b, a = resized.getpixel((x + n, y))
                canvas.set_pixel(x, y, r, g, b)
        yield canvas

class News:

    def __init__(self, matrix, queue):
        self.matrix = matrix
        self.queue = queue

    def run(self):
        for news in [yahoo, niconico]:
            for entry in feedparser.parse(news)['entries']:
                text = entry.title
                #jtalk = threading.Thread(target=lambda: call(["./jsay_linux", text]))
                #jtalk.setDaemon(True)
                #jtalk.start()
                for canvas in draw(self.matrix, text):
                    while not self.queue.empty():
                        pressed, button = self.queue.get()
                        if pressed and button == '00':
                            return False
                    self.matrix.vsync(canvas)
                    time.sleep(0.1)
                time.sleep(1)
        return True

if __name__ == '__main__':
    matrix = Matrix(1, 1)
    for news in [yahoo, niconico]:
        entries = feedparser.parse(news)['entries']
        for entry in entries:
            text = entry.title
            #jtalk = threading.Thread(target=lambda: call(["./jsay_mac", text]))
            #jtalk.setDaemon(True)
            #jtalk.start()
            for canvas in draw(matrix, text):
                 matrix.vsync(canvas)
                 time.sleep(0.1)
            time.sleep(1)
