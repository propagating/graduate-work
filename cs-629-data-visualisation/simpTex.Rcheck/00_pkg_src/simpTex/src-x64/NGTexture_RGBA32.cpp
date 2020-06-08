
#define _CRT_SECURE_NO_WARNINGS

#include <iostream>
#include <math.h>
#include <time.h>

#include "NGTexture.h"
#include "Worley.h"

#ifndef STBI_INCLUDE_STB_IMAGE_H
#define STB_IMAGE_IMPLEMENTATION
#include "stb/stb_image.h"
#endif

#ifndef INCLUDE_STB_IMAGE_WRITE_H
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb/stb_image_write.h"
#endif

float Perlin_Noise2(float vec[2]);
float Simplex_Noise2(float x, float y);
int max(int a, int b);
int min(int a, int b);

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
    const int bufferIndex);

NGTexture2D_RGB32::NGTexture2D_RGB32(int iTextureID, int iWidth, int iHeight) : NGTexture(iTextureID)
{
    m_iWidth = iWidth;
    m_iHeight = iHeight;
    m_iChannels = 4;
    m_pData = new unsigned char[m_iWidth * m_iHeight * 4];

    int iPixel = 0;
    for (int y = 0; y < m_iHeight; y++)
    {
        for (int x = 0; x < m_iWidth; x++)
        {
            iPixel = (y * m_iWidth * 4) + (x * 4);

            m_pData[iPixel] = 255;
            m_pData[iPixel + 1] = 255;
            m_pData[iPixel + 2] = 255;
            m_pData[iPixel + 3] = 255;
        }
    }
}

NGTexture2D_RGB32::NGTexture2D_RGB32(int iTextureID, const char* szPNGFile) : NGTexture(iTextureID)
{
    m_iWidth = 0;
    m_iHeight = 0;
    m_iChannels = 0;
    m_pData = nullptr;

    unsigned char* pImage = stbi_load(szPNGFile, &m_iWidth, &m_iHeight, &m_iChannels, STBI_rgb_alpha);
    m_pData = pImage;
}

NGTexture2D_RGB32::~NGTexture2D_RGB32()
{
    if(m_pData != nullptr)
        delete m_pData;
}

void NGTexture2D_RGB32::Generate_SimplexNoise(float fNoiseResolution, float fNoiseIntensity)
{
    int iPixel = 0;
    float aUV[2];
    float fNoise;
    unsigned char iNoise;

    //  Sanity checks on noise resolution
    if (fNoiseResolution < 1.0f) fNoiseResolution = 1.0f;
    if (fNoiseResolution > 999.0f) fNoiseResolution = 999.0f;
    if (fNoiseIntensity < 0.0f) fNoiseIntensity = 0.0f;
    if (fNoiseIntensity > 1.0f) fNoiseIntensity = 1.0f;

    for (int y = 0; y < m_iHeight; y++)
    {
        for (int x = 0; x < m_iWidth; x++)
        {
            iPixel = (y * m_iWidth * 4) + (x * 4);

            fNoise = Simplex_Noise2(x * fNoiseResolution / (float)m_iWidth, y * fNoiseResolution / (float)m_iHeight);
            iNoise = (unsigned char)(255 * fNoise);

            m_pData[iPixel] = (m_pData[iPixel] * (1.0f - fNoiseIntensity)) + (iNoise * fNoiseIntensity);
            m_pData[iPixel + 1] = (m_pData[iPixel + 1] * (1.0f - fNoiseIntensity)) + (iNoise * fNoiseIntensity);
            m_pData[iPixel + 2] = (m_pData[iPixel + 2] * (1.0f - fNoiseIntensity)) + (iNoise * fNoiseIntensity);
            m_pData[iPixel + 3] = 255;
        }
    }
}

void NGTexture2D_RGB32::Generate_PerlinNoise(float fNoiseResolution, float fNoiseIntensity)
{
    int iPixel = 0;
    float aUV[2];
    float fNoise;
    unsigned char iNoise;

    //  Sanity checks on noise resolution
    if (fNoiseResolution < 1.0f) fNoiseResolution = 1.0f;
    if (fNoiseResolution > 999.0f) fNoiseResolution = 999.0f;
    if (fNoiseIntensity < 0.0f) fNoiseIntensity = 0.0f;
    if (fNoiseIntensity > 1.0f) fNoiseIntensity = 1.0f;

    for (int y = 0; y < m_iHeight; y++)
    {
        for (int x = 0; x < m_iWidth; x++)
        {
            iPixel = (y * m_iWidth * 4) + (x * 4);
            aUV[0] = (float)x * fNoiseResolution / (float)m_iWidth;
            aUV[1] = (float)y * fNoiseResolution / (float)m_iHeight;

            fNoise = Perlin_Noise2(aUV);
            iNoise = (unsigned char)(255 * fNoise);

            m_pData[iPixel] = (m_pData[iPixel] * (1.0f - fNoiseIntensity)) + (iNoise * fNoiseIntensity);
            m_pData[iPixel + 1] = (m_pData[iPixel + 1] * (1.0f - fNoiseIntensity)) + (iNoise * fNoiseIntensity);
            m_pData[iPixel + 2] = (m_pData[iPixel + 2] * (1.0f - fNoiseIntensity)) + (iNoise * fNoiseIntensity);
            m_pData[iPixel + 3] = 255;
        }
    }
}

void NGTexture2D_RGB32::Generate_IrregularStructuredNoise()
{

}

void NGTexture2D_RGB32::Generate_WorleyNoise(int iPoints, float fNoiseIntensity, const char* szColorFunc, const char* szDistanceFunc)
{
    int iPixel = 0;
    Color worleyColor;

    WorleyNoise* worley = new WorleyNoise(iPoints, m_iWidth, m_iHeight);
    worley->setColorFunction(szColorFunc);
    worley->setDistanceFunction(szDistanceFunc);

    for (int y = 0; y < m_iHeight; y++)
    {
        for (int x = 0; x < m_iWidth; x++)
        {
            iPixel = (y * m_iWidth * 4) + (x * 4);
            
            worleyColor = worley->GetNoise(x, y);

            m_pData[iPixel] = (m_pData[iPixel] * (1.0f - fNoiseIntensity)) + (worleyColor.r * fNoiseIntensity);
            m_pData[iPixel + 1] = (m_pData[iPixel + 1] * (1.0f - fNoiseIntensity)) + (worleyColor.g * fNoiseIntensity);
            m_pData[iPixel + 2] = (m_pData[iPixel + 2] * (1.0f - fNoiseIntensity)) + (worleyColor.b * fNoiseIntensity);
            m_pData[iPixel + 3] = 255;
        }
    }
}

void NGTexture2D_RGB32::Generate_ReactionDiffusion(int iIterations, int iSpawnPoints)
{


    float fCenterWeight = -1.0f;
    float fAdjacentWeight = 0.2f;
    float fDiagonalWeight = 0.051f;
    float fFeedRate = 0.055f;
    float fKillRate = 0.0625f;
    float fDiffusionRateA = 0.42f;
    float fDiffusionRateB = 0.125f;
    float fTimeStep = 1.0f;

    srand(time(NULL));
    
    int iBufferSize = m_iWidth * m_iHeight;
    float* pBufferA0 = new float[iBufferSize];
    float* pBufferB0 = new float[iBufferSize];
    float* pBufferA1 = new float[iBufferSize];
    float* pBufferB1 = new float[iBufferSize];

    for (int i = 0; i < iBufferSize; i++)
    {
        pBufferA0[i] = 1;
        pBufferB0[i] = 0;
        pBufferA1[i] = 1;
        pBufferB1[i] = 0;
    }

    int iSpawned = 0;
    while (iSpawned < iSpawnPoints)
    {
        int iSpawnLocationX = rand() % m_iWidth;
        int iSpawnLocationY = rand() % m_iHeight;
        int iSpawnLocation = (iSpawnLocationY * m_iWidth) + iSpawnLocationX;

        if (pBufferB0[iSpawnLocation] == 0)
        {
            pBufferB0[iSpawnLocation] = 1;
            pBufferB1[iSpawnLocation] = 1;
            iSpawned++;
        }
    }

    for (int n = 0; n < iIterations; n++)
    {
        std::cout << "Iteration " << n << " of " << iIterations << std::endl;
        for (int i = 0; i < iBufferSize; i++)
        {
            grayScott(i, pBufferA0, pBufferB0, pBufferA1, pBufferB1, m_iWidth, m_iHeight, fCenterWeight, fAdjacentWeight, fDiagonalWeight,
                fFeedRate, fKillRate, fDiffusionRateA, fDiffusionRateB, fTimeStep, n % 2);
        }
    }

    for (int i = 0; i < iBufferSize; i++)
    {
        int iVal = (int)((pBufferA0[i] - pBufferB0[i]) * 255);
        iVal = min(255, iVal);

        m_pData[(i * 4)] = (unsigned char)iVal;
        m_pData[(i * 4) + 1] = (unsigned char)iVal;
        m_pData[(i * 4) + 2] = (unsigned char)iVal;
        m_pData[(i * 4) + 3] = 255;
    }
}

bool NGTexture2D_RGB32::GetAs_RawData(void* aBuffer)
{
    if (m_pData == nullptr)
    {
        aBuffer = nullptr;
        return false;
    }
    else
    {
        aBuffer = (void*)m_pData;
        return true;
    }
}

bool NGTexture2D_RGB32::GetAs_PNGFile(const char* aFilePath)
{
    stbi_write_png(aFilePath, m_iWidth, m_iHeight, 4, m_pData, m_iWidth * 4);
    return false;
}

