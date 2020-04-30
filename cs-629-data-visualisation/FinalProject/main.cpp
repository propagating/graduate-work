#include <cstdlib>

#define noiseWidth 128
#define noiseHeight 128

double noise[noiseHeight][noiseWidth]; //the noise array

void generateNoise();

int main(int argc, char *argv[])
{
    screen(noiseWidth, noiseHeight, 0, "Random Noise");
    generateNoise();

    ColorRGB color;

    for(int y = 0; y < h; y++)
        for(int x = 0; x < w; x++)
        {
            color.r = color.g = color.b = Uint8(256 * noise[x][y]);
            pset(x, y, color);
        }

    redraw();
    sleep();
    return 0;
}

void generateNoise()
{
    for (int y = 0; y < noiseHeight; y++)
        for (int x = 0; x < noiseWidth; x++)
        {
            noise[y][x] = (rand() % 32768) / 32768.0;
        }
}