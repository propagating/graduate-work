
#include "Worley.h"
#include <cmath>
#include <stdlib.h> 
#include <time.h>

int max(int a, int b)
{
    if (a >= b) return a; else return b;
}

int min(int a, int b)
{
    if (a < b) return a; else return b;
}

int euclideanDistance(int x1, int y1, int x2, int y2) 
{
    int xDiff = x1 - x2;
    int yDiff = y1 - y2;
    return sqrt((xDiff * xDiff) + (yDiff * yDiff));
}

int manhattanDistance(int x1, int y1, int x2, int y2) 
{
    int xDiff = abs(x1 - x2);
    int yDiff = abs(y1 - y2);
    return xDiff + yDiff;
}

int chebyshevDistance(int x1, int y1, int x2, int y2) 
{
    return std::fmax(abs(x1 - x2), abs(y1 - y2));
}

int orth(int x1, int y1, int x2, int y2, DistanceFunc f) 
{
    int xDiff = abs(x1 - x2);
    int yDiff = abs(y1 - y2);

    if (yDiff > xDiff)
        return (0.41 * xDiff) + (0.941246 * yDiff);
    else
        return f(x1, y1, x2, y2);
}

int orthEuclideanDistance(int x1, int y1, int x2, int y2) { return orth(x1, y1, x2, y2, euclideanDistance); }
int orthManhattanDistance(int x1, int y1, int x2, int y2) { return orth(x1, y1, x2, y2, manhattanDistance); }
int orthChebyshevDistance(int x1, int y1, int x2, int y2) { return orth(x1, y1, x2, y2, chebyshevDistance); }

Color linearColor(int value) { return Color(value, value, value, 255);}
Color xorColor(int value) { return Color(value ^ 64, value ^ 32, value ^ 16, 255); }
Color modColor(int value) { return Color(value % 70, value % 8, value % 255, 255); }
Color andColor(int value) { return Color(value & 3, value & 80, value & 150, 255); }
Color tanColor(int value) { return Color(tan(value * 3.00) * 10.0, tan(value * 3.00) * 100.0, tan(value * 4.07) * 10.0, 255); }

Color sinColor(int value) 
{
    int gammaAdj = 40.0;
    float redPart = 20.5;
    float greenPart = 5.9;
    float bluePart = 3.9;

    return Color((sin(value * redPart) * 10.0) - gammaAdj, (sin(value * greenPart) * 10.0) + gammaAdj, (sin(value * bluePart) * 10.0) - gammaAdj, 255);
}

Color mintyColor(int distance) 
{
    int value = distance * 2;
    Color oct1 = sinColor(value);
    Color oct2 = modColor(value * 3);
    Color oct3 = xorColor(value);

    Color fin = Color((oct1.r + oct2.r + oct3.r) / 3, (oct1.g + oct2.g + oct3.g) / 3, +(oct1.b + oct2.b + oct3.b) / 3, 255);
    fin = Color(max(0, 255 - fin.r), max(0, 255 - fin.g), max(0, 255 - fin.b), 255);
    return fin;
}

WorleyNoise::WorleyNoise(int iPoints, int iWidth, int iHeight)
{
    srand(time(NULL));

    colorFunc = linearColor;
    distanceFunc = euclideanDistance;
    numberOfPoints = iPoints;

    Vector2i point;
    points.clear();
    points.reserve(iPoints);

    for (int i = 0; i < iPoints; i++)
    {
        point.x = rand() % iWidth;
        point.y = rand() % iHeight;
        points.push_back(point);
    }
}


void WorleyNoise::setColorFunction(const std::string& colorFunction) 
{
    if(!colorFunction.compare("Linear")) colorFunc = linearColor;
    if (!colorFunction.compare("Xor")) colorFunc = xorColor;
    if (!colorFunction.compare("Mod")) colorFunc = modColor;
    if (!colorFunction.compare("And")) colorFunc = andColor;
    if (!colorFunction.compare("Tan")) colorFunc = tanColor;
    if (!colorFunction.compare("Sin")) colorFunc = sinColor;
    if (!colorFunction.compare("Minty")) colorFunc = mintyColor;
}

void WorleyNoise::setDistanceFunction(const std::string& distanceFunction)
{
    if (!distanceFunction.compare("Euclidean")) distanceFunc = euclideanDistance;
    if (!distanceFunction.compare("Manhattan")) distanceFunc = manhattanDistance;
    if (!distanceFunction.compare("Chebyshev")) distanceFunc = chebyshevDistance;
    if (!distanceFunction.compare("OrthoEuclidean")) distanceFunc = orthEuclideanDistance;
    if (!distanceFunction.compare("OrthoManhattan")) distanceFunc = orthManhattanDistance;
    if (!distanceFunction.compare("OrthoChebyshev")) distanceFunc = orthChebyshevDistance;
}

Color WorleyNoise::GetNoise(int x, int y)
{
    int closestDist = 255;

    for (int i = 0; i < points.size(); i++)
    {
        int xDiff = x - points[i].x;
        int yDiff = y - points[i].y;

        bool inRange = (xDiff * xDiff) + (yDiff * yDiff) < (255 * 255);

        if (inRange)
        {
            int dist = distanceFunc(x, y, points[i].x, points[i].y);
            if (dist < closestDist)
                closestDist = dist;
        }
    }

    return colorFunc(closestDist);
}


