import sys
import cv2
from rgbmatrix import RGBMatrix

rows = 16
cols = 32
chains = 1
parallel = 3
width = cols * chains
height = rows * parallel

matrix = RGBMatrix(rows, chains, parallel)

filename = sys.argv[1]

cap = cv2.VideoCapture(filename)

xs = range(width)
ys = range(height)

try:
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (height, width))
            for x in xs:
                col = frame[x]
                for y in ys:
                    b, g, r = col[y]
                    matrix.SetPixel(x, y, r, g, b)
finally:
    cap.release()
    matrix.Clear()
