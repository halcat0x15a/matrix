from rgbmatrix import RGBMatrix

ROWS = 16
COLS = 32

class Matrix:
    
    def __init__(self, chains, parallel):
        self.chains = chains
        self.parallel = parallel
        self.matrix = RGBMatrix(ROWS, chains, parallel)

    def width(self):
        return COLS * self.chains

    def height(self):
        return ROWS * self.parallel

    def create_canvas(self):
        return Canvas(self.matrix.CreateFrameCanvas())

    def vsync(self, canvas):
        self.matrix.SwapOnVSync(canvas.canvas)

class Canvas:

    def __init__(self, canvas):
        self.canvas = canvas

    def set_pixel(self, x, y, r, g, b):
        self.canvas.SetPixel(x, y, r, g, b)
