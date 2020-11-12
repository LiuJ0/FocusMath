#pragma once

#include <ft2build.h>
#include FT_FREETYPE_H

#include <string>

#include "EquationParts.hpp"
#include "ImgBufDyn.hpp"

using namespace std;

class Renderer {
private:
    int m_PenPosX;
    int m_PenPosY;
    int m_PenPosYMax;
    int m_PenPosYMin;
    int m_FontSize;
    FT_Library ft;
    FT_Face regular;
    FT_Face italics;
    ImgBufDyn* m_Bufferdyn;
public:
    Renderer(const string regularFontPath, const string italicsFontPath);
    ~Renderer();
    void Draw(const char input, const unsigned int fontSize, const bool italicized);
    void Draw(const unsigned int input, const unsigned int fontSize);
    void Draw(const Constant input, const unsigned int fontSize);
    void Draw(const Variable input, const unsigned int fontSize);
    void Draw(const Operation input, const unsigned int fontSize);
    void Draw(const Escape input, const unsigned int fontSize);
    void Draw(Group input, const unsigned int fontSize);
    void Render(string, unsigned int, int);
    void Image(string);
    void Clear();
};
