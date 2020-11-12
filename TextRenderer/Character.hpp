#pragma once

#include <ft2build.h>
#include FT_FREETYPE_H

class CharacterTex {
private:
    unsigned char* m_LocalBuffer;
public:
    CharacterTex();
    ~CharacterTex();
    void LoadChar(const char input, FT_Face font, const int size);
    void LoadChar(const unsigned int input, FT_Face font, const int size);
    int m_Width, m_Height, m_Advance, m_BearingX, m_BearingY;
    unsigned char* Buffer() const;
};