#include <iostream>

#include "Character.hpp"
#include "Exceptions.hpp"

using namespace std;

CharacterTex::CharacterTex()
    : m_LocalBuffer(nullptr), m_Width(0), m_Height(0), m_BearingX(0), m_BearingY(0)
{
}

CharacterTex::~CharacterTex()
{
}

void CharacterTex::LoadChar(const char input, FT_Face font, const int size)
{
    FT_Set_Pixel_Sizes(font, 0, size);
    if (FT_Error temp = FT_Load_Char(font, input, FT_LOAD_RENDER)) {
        TERMINATE(cout << "[FREETYPE ERROR] ( " << ftGetError(temp) << " in loading glyph : " << input << " ): " << __FILE__ << ":" << __LINE__ << endl;) }
    m_LocalBuffer = font->glyph->bitmap.buffer;
    m_Width = font->glyph->bitmap.width;
    m_Height = font->glyph->bitmap.rows;
    m_BearingX = font->glyph->bitmap_left;
    m_BearingY = font->glyph->bitmap_top;
    m_Advance = font->glyph->advance.x;
}

void CharacterTex::LoadChar(const unsigned int input, FT_Face font, const int size)
{
    FT_Set_Pixel_Sizes(font, 0, size);
    FT_Select_Charmap(font, FT_ENCODING_UNICODE);
    FT_UInt charIndex = FT_Get_Char_Index(font, input);
    if (FT_Error temp = FT_Load_Glyph(font, charIndex, FT_LOAD_RENDER)) {
        TERMINATE(cout << "[FREETYPE ERROR] ( " << ftGetError(temp) << " in loading glyph : " << hex << input << dec << " ): " << __FILE__ << ":" << __LINE__ << endl;) }
    m_LocalBuffer = font->glyph->bitmap.buffer;
    m_Width = font->glyph->bitmap.width;
    m_Height = font->glyph->bitmap.rows;
    m_BearingX = font->glyph->bitmap_left;
    m_BearingY = font->glyph->bitmap_top;
    m_Advance = font->glyph->advance.x;
}

unsigned char* CharacterTex::Buffer() const
{
    return m_LocalBuffer;
}