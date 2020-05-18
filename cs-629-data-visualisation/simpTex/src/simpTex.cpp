#include <Rcpp.h>
// [[Rcpp::plugins(cpp14)]] 

#define WIN32_LEAN_AND_MEAN
#include <cstdio>
#include <cstring>
#include <Rcpp.h>
#include "NoiseGenerator.h"
#include "NGTexture_RGBA32.h"

using namespace Rcpp;
#define MAX_TEXTURES    1000
char* g_sLibraryName;
int g_iTextures = 0;
NGTexture2D_RGB32* g_aTextures[MAX_TEXTURES];

NGTexture2D_RGB32* GetTexture(int iTextureID)
{
    for (auto i = 0; i < MAX_TEXTURES; i++){
        if (g_aTextures[i] && g_aTextures[i]->Get_ID() == iTextureID)
        {
            return g_aTextures[i];
            }
    }
        return nullptr;
}


/*
 * Supported format string are RGBA32
 * Returns texture ID for newly created texture
 */

// [[Rcpp::export]]
int CreateTexture2D(const char* szFormat, int iWidth, int iHeight)
{
    if (g_iTextures >= MAX_TEXTURES - 1)
        return 0;
    
    if (strcmp(szFormat, "RGBA32") == 0)
    {
        g_iTextures++;
        g_aTextures[g_iTextures] = new NGTexture2D_RGB32(g_iTextures, iWidth, iHeight);
        return g_iTextures;
    }
    
    return 0;
}

/*
 * Load an exising PNG file from disk. Format, width and height will depend on PNG file
 * Returns texture ID of the texture loaded from disk
 */

// [[Rcpp::export]]
int CreateTextureOnImage2D(const char* szFormat, const char* szPNGFile)
{
    if (g_iTextures >= MAX_TEXTURES - 1)
        return 0;
    
    if (strcmp(szFormat, "RGBA32") == 0)
    {
        g_iTextures++;
        g_aTextures[g_iTextures] = new NGTexture2D_RGB32(g_iTextures, szPNGFile);
        
        //  If PNG was loaded properly, only then return the texture ID
        void* pPixelBuffer = nullptr;
        if(g_aTextures[g_iTextures]->GetAs_RawData(pPixelBuffer) == true)
            return g_iTextures;
    }
    
    return 0;
}

/*
 * Saves pointer to raw texture data in pBuffer. Raw data must be interpetted according to format, width and height of texture
 * Returns whether function was successful or not
 */
bool GetRawData(int iTextureID, void* pBuffer)
{
    auto pTexture = GetTexture(iTextureID);
    if (pTexture == nullptr)
        return false;
    
    return pTexture->GetAs_RawData(pBuffer);
}

/*
 * Saves the texture as a PNG image
 * Returns whether function was successful or not
 */

// [[Rcpp::export]]
bool SaveTextureToFile(int iTextureID, const char* szFile)
{
    auto pTexture = GetTexture(iTextureID);
    if (pTexture == nullptr)
        return false;
    
    return pTexture->GetAs_PNGFile(szFile);
}

/*
 * Functions for generating various types of noises.
 * Textures can be empty or have loaded/generated data in them. The noise functions will add the noise on top
 of the exising pixels. Hence same texture can be passed multiple times to multiple functions.
 * Returns whether the noise was successfully added to the texture or not
 */

// [[Rcpp::export]]
bool Generate_SimplexNoise(int iTextureID, float fNoiseResolution, float fNoiseIntensity)
{
    auto pTexture = GetTexture(iTextureID);
    if (pTexture == nullptr)
        return false;
    
    pTexture->Generate_SimplexNoise(fNoiseResolution, fNoiseIntensity);
    return true;
}


// [[Rcpp::export]]
bool Generate_PerlinNoise(int iTextureID, float fNoiseResolution, float fNoiseIntensity)
{
    auto pTexture = GetTexture(iTextureID);
    if (pTexture == nullptr)
        return false;
    
    pTexture->Generate_PerlinNoise(fNoiseResolution, fNoiseIntensity);
    return true;
}

bool Generate_IrregularStructuredNoise(int iTextureID)
{
    return false;
}

bool Generate_WorleyNoise(int iTextureID)
{
    return false;
}

bool Generate_AnisotropicDiffusion(int iTextureID)
{
    return false;
}


