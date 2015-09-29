from rgbmatrix import RGBMatrix

rows = 16
cols = 32
chains = 3
parallel = 3
width = cols * chains
height = rows * parallel
size = (width, height)

matrix = RGBMatrix(rows, chains, parallel)
