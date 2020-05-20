

void grayScott(
    int i,
    float* A0,
    float* B0,
    float* A1,
    float* B1,
    const int w,
    const int h,
    const float centerWeight,
    const float adjacentWeight,
    const float diagonalWeight,
    const float feedRate,
    const float killRate,
    const float diffusionRateA,
    const float diffusionRateB,
    const float timestep,
    const int bufferIndex)
{
    // compute x and y coordinates of pixel
    const int x = i % w;
    const int y = i / w;

    // compute u and v coordinates of pixel in range [0, 1]
    const float u = (float)x / (w - 1);
    const float v = 1 - (float)y / (h - 1);

    // compute kill and feed rates for this pixel
    const float k = killRate + (u - 0.5) * 0;
    const float f = feedRate + (v - 0.5) * 0;

    // find neighboring pixels, wrapping around edges
    const int xp = x == 0 ? w - 1 : x - 1;
    const int xn = x == w - 1 ? 0 : x + 1;
    const int yp = y == 0 ? h - 1 : y - 1;
    const int yn = y == h - 1 ? 0 : y + 1;

    // figure out which buffers to use (kinda like double buffering)
    float* A = bufferIndex == 0 ? A0 : A1;
    float* B = bufferIndex == 0 ? B0 : B1;
    float* newA = bufferIndex == 0 ? A1 : A0;
    float* newB = bufferIndex == 0 ? B1 : B0;

    // get the values for A and B at this pixel
    const float a = A[i];
    const float b = B[i];

    // compute A diffusion
    float dda = 0;
    dda += a * centerWeight;
    dda += A[yp * w + xp] * diagonalWeight;
    dda += A[yp * w + xn] * diagonalWeight;
    dda += A[yn * w + xp] * diagonalWeight;
    dda += A[yn * w + xn] * diagonalWeight;
    dda += A[yp * w + x] * adjacentWeight;
    dda += A[yn * w + x] * adjacentWeight;
    dda += A[y * w + xp] * adjacentWeight;
    dda += A[y * w + xn] * adjacentWeight;

    // compute B diffusion
    float ddb = 0;
    ddb += b * centerWeight;
    ddb += B[yp * w + xp] * diagonalWeight;
    ddb += B[yp * w + xn] * diagonalWeight;
    ddb += B[yn * w + xp] * diagonalWeight;
    ddb += B[yn * w + xn] * diagonalWeight;
    ddb += B[yp * w + x] * adjacentWeight;
    ddb += B[yn * w + x] * adjacentWeight;
    ddb += B[y * w + xp] * adjacentWeight;
    ddb += B[y * w + xn] * adjacentWeight;

    // apply reaction diffusion formula
    float mag = a * b * b;
    const float da = (diffusionRateA * dda) - mag + (f * (1 - a));
    const float db = (diffusionRateB * ddb) + mag - ((f + k) * b);

    // write new A and B values for this pixel
    newA[i] = a + da * timestep;
    newB[i] = b + db * timestep;
}
