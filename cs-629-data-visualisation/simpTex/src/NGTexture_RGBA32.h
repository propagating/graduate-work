class NGTexture2D_RGB32
{
private:
    int m_iTextureID{};
    int m_iWidth;
    int m_iHeight;
    int m_iChannels;
    unsigned char* m_pData;

public:

    NGTexture2D_RGB32(int iTextureID, int iWidth, int iHeight);
    NGTexture2D_RGB32(int iTextureID, const char* szPNGFile);
    int Get_ID() { return m_iTextureID; }
    ~NGTexture2D_RGB32();

    virtual void Generate_SimplexNoise(float fNoiseResolution, float fNoiseIntensity);
    virtual void Generate_PerlinNoise(float fNoiseResolution, float fNoiseIntensity);
    virtual void Generate_IrregularStructuredNoise();
    virtual void Generate_WorleyNoise();
    virtual void Generate_AnisotropicDiffusion();

    virtual bool GetAs_RawData(void* aBuffer);
    virtual bool GetAs_PNGFile(const char* aFilePath);
};

