import sys
import cv2

rows = 16
cols = 32
chains = 1
parallel = 3
width = cols * chains
height = rows * parallel
size = (height, width)
xs = range(width)
ys = range(height)

input = sys.argv[1]
output = sys.argv[2]
cap = cv2.VideoCapture(input)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter(output, 0, 20.0, size)

try:
    while(cap.isOpened()):
        ret, frame = cap.read()
        print(cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC))
        if ret:
            frame = cv2.resize(frame, size)
            out.write(frame)
        else:
            break
finally:
    cap.release()
    out.release()
