#include <cmath>

#include "NGTexture_RGBA32.h"

#ifndef STBI_INCLUDE_STB_IMAGE_H
#define STB_IMAGE_IMPLEMENTATION
#include "stb/stb_image.h"
#endif

#ifndef INCLUDE_STB_IMAGE_WRITE_H
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb/stb_image_write.h"
#endif

float generate_perlin_two_dim(float vec[2]);
float generate_simplex_two_dim(float x, float y);

NGTexture2D_RGB32::NGTexture2D_RGB32(int iTextureID, int iWidth, int iHeight)
{
    m_iTextureID = iTextureID;
    m_iWidth = iWidth;
    m_iHeight = iHeight;
    m_iChannels = 4;
    m_pData = new unsigned char[m_iWidth * m_iHeight * 4];

    auto iPixel = 0;
    for (auto y = 0; y < m_iHeight; y++)
    {
        for (auto x = 0; x < m_iWidth; x++)
        {
            iPixel = (y * m_iWidth * 4) + (x * 4);

            m_pData[iPixel] = 255;
            m_pData[iPixel + 1] = 255;
            m_pData[iPixel + 2] = 255;
            m_pData[iPixel + 3] = 255;
        }
    }
}

NGTexture2D_RGB32::NGTexture2D_RGB32(int iTextureID, const char* szPNGFile)
{
    m_iTextureID = iTextureID;
    m_iWidth = 0;
    m_iHeight = 0;
    m_iChannels = 0;
    m_pData = nullptr;

    auto pImage = stbi_load(szPNGFile, &m_iWidth, &m_iHeight, &m_iChannels, STBI_rgb_alpha);
    m_pData = pImage;
}

NGTexture2D_RGB32::~NGTexture2D_RGB32()
{
    if(m_pData != nullptr)
        delete m_pData;
}

void NGTexture2D_RGB32::Generate_SimplexNoise(float fNoiseResolution, float fNoiseIntensity)
{
	auto iPixel = 0;
    float aUV[2];
    float fNoise;
    unsigned char iNoise;

    //  Sanity checks on noise resolution
    if (fNoiseResolution < 1.0f) fNoiseResolution = 1.0f;
    if (fNoiseResolution > 999.0f) fNoiseResolution = 999.0f;
    if (fNoiseIntensity < 0.0f) fNoiseIntensity = 0.0f;
    if (fNoiseIntensity > 1.0f) fNoiseIntensity = 1.0f;

    for (auto y = 0; y < m_iHeight; y++)
    {
        for (auto x = 0; x < m_iWidth; x++)
        {
            iPixel = (y * m_iWidth * 4) + (x * 4);

            fNoise = generate_simplex_two_dim(x * fNoiseResolution / (float)m_iWidth, y * fNoiseResolution / (float)m_iHeight);
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
	auto iPixel = 0;
    float aUV[2];
    float fNoise;
    unsigned char iNoise;

    //  Sanity checks on noise resolution
    if (fNoiseResolution < 1.0f) fNoiseResolution = 1.0f;
    if (fNoiseResolution > 999.0f) fNoiseResolution = 999.0f;
    if (fNoiseIntensity < 0.0f) fNoiseIntensity = 0.0f;
    if (fNoiseIntensity > 1.0f) fNoiseIntensity = 1.0f;

    for (auto y = 0; y < m_iHeight; y++) 
    {
        for (auto x = 0; x < m_iWidth; x++)
        {
            iPixel = (y * m_iWidth * 4) + (x * 4);
            aUV[0] = (float)x * fNoiseResolution / (float)m_iWidth;
            aUV[1] = (float)y * fNoiseResolution / (float)m_iHeight;

            fNoise = generate_perlin_two_dim(aUV);
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

void NGTexture2D_RGB32::Generate_WorleyNoise()
{

}

void NGTexture2D_RGB32::Generate_AnisotropicDiffusion()
{

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

