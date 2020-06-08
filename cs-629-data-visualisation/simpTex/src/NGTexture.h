#pragma once
class NGTexture
{
private:

    int m_iTextureID;

public:

    NGTexture(int iTextureID) { m_iTextureID = iTextureID; }
    ~NGTexture() {}

    int Get_ID() { return m_iTextureID; }

    virtual void Generate_SimplexNoise(float fNoiseResolution, float fNoiseIntensity) = 0;
    virtual void Generate_PerlinNoise(float fNoiseResolution, float fNoiseIntensity) = 0;
    virtual void Generate_IrregularStructuredNoise() = 0;
    virtual void Generate_WorleyNoise(int iPoints, float fNoiseIntensity, const char* szColorFunc, const char* szDistanceFunc) = 0;
    virtual void Generate_ReactionDiffusion(int iIterations, int iSpawnPoints) = 0;

    virtual bool GetAs_RawData(void* aBuffer) = 0;
    virtual bool GetAs_PNGFile(const char* aFilePath) = 0;
};

class NGTexture2D_RGB32 : public NGTexture
{
private:

    int m_iWidth;
    int m_iHeight;
    int m_iChannels;
    unsigned char* m_pData;

public:

    NGTexture2D_RGB32(int iTextureID, int iWidth, int iHeight);
    NGTexture2D_RGB32(int iTextureID, const char* szPNGFile);
    ~NGTexture2D_RGB32();

    virtual void Generate_SimplexNoise(float fNoiseResolution, float fNoiseIntensity);
    virtual void Generate_PerlinNoise(float fNoiseResolution, float fNoiseIntensity);
    virtual void Generate_IrregularStructuredNoise();
    virtual void Generate_WorleyNoise(int iPoints, float fNoiseIntensity, const char* szColorFunc, const char* szDistanceFunc);
    virtual void Generate_ReactionDiffusion(int iIterations, int iSpawnPoints);

    virtual bool GetAs_RawData(void* aBuffer);
    virtual bool GetAs_PNGFile(const char* aFilePath);
};


