#pragma once

#define WIN32_LEAN_AND_MEAN

char* NoiseGenerator_GetLibraryName();

/*
* Supported format string are RGBA_32
* Returns texture ID for newly created texture
*/
int CreateTexture2D(const char* szFormat, int iWidth, int iHeight);

/*
* Load an exising PNG file from disk. Format, width and height will depend on PNG file
* Returns texture ID of the texture loaded from disk
*/
int CreateTextureOnImage2D(const char* szFormat, const char* szPNGFile);

/*
* Saves pointer to raw texture data in pBuffer. Raw data must be interpetted according to format, width and height of texture
* Returns whether function was successful or not
*/
bool GetRawData(int iTextureID, void* pBuffer);

/*
* Saves the texture as a PNG image
* Returns whether function was successful or not
*/
bool SaveTextureToFile(int iTextureID, const char* szFile);

/*
* Functions for generating various types of noises.
* Textures can be empty or have loaded/generated data in them. The noise functions will add the noise on top
  of the exising pixels. Hence same texture can be passed multiple times to multiple functions.
* Returns whether the noise was successfully added to the texture or not
*/
bool Generate_SimplexNoise(int iTextureID, float fNoiseResolution, float fNoiseIntensity);
bool Generate_PerlinNoise(int iTextureID, float fNoiseResolution, float fNoiseIntensity);
bool Generate_IrregularStructuredNoise(int iTextureID);
bool Generate_WorleyNoise(int iTextureID);
bool Generate_AnisotropicDiffusion(int iTextureID);