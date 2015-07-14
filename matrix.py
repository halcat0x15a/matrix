from rgbmatrix import RGBMatrix

rows = 16
cols = 32
chains = 1
parallel = 1
width = cols * chains
height = rows * parallel
size = (height, width)

matrix = RGBMatrix(rows, chains, parallel)

