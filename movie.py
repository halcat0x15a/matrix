import sys
import cv2
import pygame
from rgbmatrix import RGBMatrix

rows = 16
cols = 32
chains = 1
parallel = 3
width = cols * chains
height = rows * parallel
size = (height, width)
xs = range(width)
ys = range(height)

matrix = RGBMatrix(rows, chains, parallel)
matrix.brightness = 20
videoname = sys.argv[1]
musicname = sys.argv[2]
pygame.mixer.init()
cap = cv2.VideoCapture(videoname)
pygame.mixer.music.load(musicname)
pygame.mixer.music.play()

try:
    buf = [[(0, 0, 0) for y in ys] for x in xs]
    while(cap.isOpened()):
        ret, frame = cap.read()
        pos = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        if pos > pygame.mixer.music.get_pos():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        if ret:
            #frame = cv2.resize(frame, size)
            for x in xs:
                cols = frame[x]
                buf_cols = buf[x]
                for y in ys:
                    b, g, r = cols[y]
                    buf_b, buf_g, buf_r = buf_cols[y]
                    if b != buf_b or g != buf_g or r != buf_r:
                        matrix.SetPixel(x, y, r, g, b)
            buf = frame
finally:
    cap.release()
    matrix.Clear()
