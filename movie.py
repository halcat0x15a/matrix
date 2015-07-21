import sys
import cv2
import pygame
from rgbmatrix import RGBMatrix

rows = 16
cols = 32
chains = 3
parallel = 3
width = cols * chains
height = rows * parallel
size = (width, height)

matrix = RGBMatrix(rows, chains, parallel)
matrix.brightness = 20
videoname = sys.argv[1]
musicname = sys.argv[2]
pygame.mixer.init()
cap = cv2.VideoCapture(videoname)
pygame.mixer.music.load(musicname)
pygame.mixer.music.play()

try:
    canvas = matrix.CreateFrameCanvas()
    while cap.isOpened():
        ret, frame = cap.read()
        pos = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        if pos > pygame.mixer.music.get_pos():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        if ret:
            frame = cv2.resize(frame, size)
            for y, row in enumerate(frame):
                for x, col in enumerate(row):
                    b, g, r = col
                    canvas.SetPixel(x, y, r, g, b)
            canvas = matrix.SwapOnVSync(canvas)
finally:
    cap.release()
    matrix.Clear()
