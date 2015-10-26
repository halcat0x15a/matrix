# -*- coding: utf-8 -*-

import time
import threading
import feedparser
from subprocess import call
from image import Matrix
from news import News
from tetris import Tetris
import joystick

if __name__ == '__main__':
    matrix = Matrix(1, 1)
    (js, queue) = joystick.queue('/dev/input/js0')
    js.daemon = True
    app = News(matrix, queue)
    while True:
        if not app.run():
            if isinstance(app, News):
                app = Tetris(matrix, 0, queue)
            else:
                app = News(matrix)
        time.sleep(1 / 20)
