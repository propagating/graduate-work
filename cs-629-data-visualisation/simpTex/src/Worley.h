
#define WIDTH  1680
#define HEIGHT 1050

#include <functional>
#include <string>
#include <vector>

struct Color
{
    unsigned char r, g, b, a;
    Color() { r = 0; g = 0; b = 0; a = 0; }
    Color(unsigned char _r, unsigned char _g, unsigned char _b, unsigned char _a){ r = _r; g = _g; b = _b; a = _a; }
};

struct Vector2i
{
    int x, y;
    Vector2i() { x = 0; y = 0; }
    Vector2i(int _x, int _y) { x = _x; y = _y; }
};

typedef std::function<int(int, int, int, int)> DistanceFunc;
typedef std::function<Color(int)> ColorFunc;

class WorleyNoise 
{
private:

    int numberOfPoints;

    DistanceFunc distanceFunc;
    ColorFunc    colorFunc;
    std::vector<Vector2i> points;

public:

    WorleyNoise(int iPoints, int iWidth, int iHeight);

    void setColorFunction(const std::string& colorFunction);
    void setDistanceFunction(const std::string& distanceFunction);
    
    Color GetNoise(int x, int y);
};
