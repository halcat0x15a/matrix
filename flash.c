#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include "led-matrix.h"
#include "gpio.h"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace rgb_matrix;

RGBMatrix *matrix = NULL;

void handler(int sig) {
    delete matrix;
    puts("exit");
    exit(0);
}

int main() {
    signal(SIGINT, handler);
    int chains = 1;
    int parallel = 1;
    int rows = 16;
    int cols = 32;
    int width = cols * chains;
    int height = rows * parallel;
    GPIO io;
    if (!io.Init()) return 1;
    matrix = new RGBMatrix(&io, rows, chains, parallel);
    matrix->set_luminance_correct(true);
    matrix->SetBrightness(80);
    matrix->SetPWMBits(11);
    FrameCanvas *canvas = matrix->CreateFrameCanvas();
    for (;;) {    
        cv::Mat image = cv::imread("sample.png");
        if (image.data) { 
            canvas->Clear();
            for (int i = 0; i < height; i++) {
                for (int j = 0; j < width; j++) {
                    cv::Vec3b vec = image.at<cv::Vec3b>(i, j);
                    canvas->SetPixel(j, i, vec[2], vec[1], vec[0]);
                }
            }
            matrix->SwapOnVSync(canvas);
        }
        usleep(1);
    }
    return 0;
}
