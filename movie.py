import sys
import cv2
import pygame
from debug import Matrix
#from matrix import Matrix

if __name__ == '__main__':
    videoname = sys.argv[1]
    musicname = sys.argv[2]
    cap = cv2.VideoCapture(videoname)
    pygame.mixer.init()
    #pygame.mixer.music.load(musicname)
    #pygame.mixer.music.play()
    matrix = Matrix(3, 3)
    size = (matrix.width(), matrix.height())
    while cap.isOpened():
        ret, frame = cap.read()
        pos = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        if pos > pygame.mixer.music.get_pos():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        canvas = matrix.create_canvas()
        if ret:
            frame = cv2.resize(frame, size)
            for y, row in enumerate(frame):
                for x, col in enumerate(row):
                    b, g, r = col
                    canvas.set_pixel(x, y, r, g, b)
            matrix.vsync(canvas)
