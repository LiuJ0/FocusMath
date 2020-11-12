#include <iostream>

#include "imgdyntopng.hpp"
#include "Renderer.hpp"
#include "Character.hpp"
#include "Exceptions.hpp"

using namespace std;

Renderer::Renderer(const string regularPath, const string italicsPath)
    : m_PenPosX(0), m_PenPosY(0), m_PenPosYMax(0), m_PenPosYMin(0), m_FontSize(0)
{
    //Initializes Freetype
    FT_Error test;
    if (test = FT_Init_FreeType(&ft)) {
        TERMINATE(cout << "[FREETYPE ERROR] ( " << ftGetError(test) << " in Library Init ): " << __FILE__ << ":" << __LINE__ << endl;) }

    if (test = FT_New_Face(ft, regularPath.c_str(), 0, &regular)) {
        TERMINATE(cout << "[FREETYPE ERROR] ( " << ftGetError(test) << " in Regular Font Face Init ): " << __FILE__ << ":" << __LINE__ << endl;) }
    
    if (test = FT_New_Face(ft, italicsPath.c_str(), 0, &italics)) {
        TERMINATE(cout << "[FREETYPE ERROR] ( " << ftGetError(test) << " in Italics Font Face Init ): " << __FILE__ << ":" << __LINE__ << endl;) }

    m_Bufferdyn = new ImgBufDyn(0, 0);
}

Renderer::~Renderer()
{
    //Clears Freetype resources
    FT_Done_Face(regular);
    FT_Done_Face(italics);
    FT_Done_FreeType(ft);
    //Removes buffer
    delete m_Bufferdyn;
}

void Renderer::Draw(const char input, const unsigned int fontSize, const bool italicized)
{
    if (input == 32)
    {
        m_PenPosX += m_FontSize / 4;
        return;
    }
    CharacterTex temp;
    if (italicized)
        temp.LoadChar(input, italics, fontSize);
    else
        temp.LoadChar(input, regular, fontSize);
    int xOrig = m_PenPosX + temp.m_BearingX;
    if (xOrig < 0)
        xOrig = 0;
    int yOrig = m_PenPosY - (temp.m_Height - temp.m_BearingY);
    m_Bufferdyn->PlaceImage(temp.Buffer(), temp.m_Width, temp.m_Height, xOrig, yOrig);

    m_PenPosX = xOrig + temp.m_Width;
    if (temp.m_BearingY + m_PenPosY > m_PenPosYMax)
        m_PenPosYMax = temp.m_BearingY + m_PenPosY;
    if (m_PenPosY - (temp.m_Height - temp.m_BearingY) < m_PenPosYMin) 
        m_PenPosYMin = m_PenPosY - (temp.m_Height - temp.m_BearingY);
}

void Renderer::Draw(const unsigned int input, const unsigned int fontSize)
{
    CharacterTex temp;
    temp.LoadChar(input, regular, fontSize);
    int xOrig = m_PenPosX + temp.m_BearingX;
    if (xOrig < 0)
        xOrig = 0;
    int yOrig = m_PenPosY - (temp.m_Height - temp.m_BearingY);
    m_Bufferdyn->PlaceImage(temp.Buffer(), temp.m_Width, temp.m_Height, xOrig, yOrig);

    m_PenPosX = xOrig + temp.m_Width;
    if (temp.m_BearingY + m_PenPosY > m_PenPosYMax)
        m_PenPosYMax = temp.m_BearingY + m_PenPosY;
    if (m_PenPosY - (temp.m_Height - temp.m_BearingY) < m_PenPosYMin) 
        m_PenPosYMin = m_PenPosY - (temp.m_Height - temp.m_BearingY);
}

void Renderer::Draw(const Constant input, const unsigned int fontSize)
{
    string inputString = to_string(input.value);

    for (int i = 0; i < inputString.size(); i++)
        Draw(inputString[i], fontSize, false);
}

void Renderer::Draw(const Variable input, const unsigned int fontSize)
{
    Draw(input.symbol, fontSize, true);
}

void Renderer::Draw(const Operation input, const unsigned int fontSize)
{
    Draw(input.type, fontSize, false);
}

void Renderer::Draw(const Escape input, const unsigned int fontSize)
{
    if (input.escapeCode == "sqrt") {
        Draw(0x221A, fontSize);
    } else if (input.escapeCode == "(") {
        Draw(0x0028, fontSize);
    } else if (input.escapeCode == ")") {
        Draw(0x0029, fontSize);
    } else if (input.escapeCode == "pi") {
        Draw(0x03C0, fontSize);
    } else if (input.escapeCode == "=") {
        Draw(0x003D, fontSize);
    } else if (input.escapeCode == "sin" || input.escapeCode == "cos" || input.escapeCode == "tan" || input.escapeCode == "log") {
        for (int i = 0; i < input.escapeCode.length(); i++)
            Draw(input.escapeCode[i], fontSize, false);
    } else if (input.escapeCode == "text") {
        for (int i = 0; i < input.suppValue.length(); i++)
            Draw(input.suppValue[i], fontSize, false);
    } else {
        TERMINATE(cout << "[RENDERER ERROR] ( Parsed escape code does not exist : " << input.escapeCode << " ): " << __FILE__ << ":" << __LINE__ << endl;)  
    }  
}

void Renderer::Draw(Group input, const unsigned int fontSize)
{
    int renderFlag = 0;
    int vsize = fontSize;
    for (int i = 0; i < input.OrderSize(); i++)
    {
        auto temp = input.RetrieveNext();
        if (temp.type == "constant")
            Draw(*(Constant *)(temp.stored), vsize);
        else if (temp.type == "variable")
            Draw(*(Variable *)(temp.stored), vsize);
        else if (temp.type == "operation") {
            Operation test = *(Operation *)(temp.stored);
            if (test.isRendererOp) {
                if (test.type == '^')
                {
                    m_PenPosY += 0.5 * vsize;
                    vsize *= 0.62;
                    renderFlag = 1;
                    continue;
                } else if (test.type == '_')
                {
                    m_PenPosY -= 0.16 * vsize;
                    vsize *= 0.62;
                    renderFlag = 2;
                    continue;
                }
            } else {
                Draw(test, vsize);
            }
        } else if (temp.type == "escape")
            Draw(*(Escape *)(temp.stored), vsize);
        else if (temp.type == "group")
        {
            Group test = *(Group *)(temp.stored);
            if (test.Organization() != "parenthesis")
                Draw(test, vsize);
            else {
                Escape leftPar = {"(", false, "0"}, rightPar = {")", false, "0"};
                Draw(leftPar, vsize);
                Draw(test, vsize);
                Draw(rightPar, vsize);
            }
        }
        switch (renderFlag) {
            case 0:
                break;
            case 1:
                vsize = fontSize;
                m_PenPosY -= 0.5 * vsize;
                renderFlag = 0;
                break;
            case 2:
                vsize = fontSize;
                m_PenPosY += 0.16 * vsize;
                renderFlag = 0;
                break;
        }
    }
}

void Renderer::Render(string input, unsigned int rgba, int size)
{
    m_Bufferdyn->SetRGBA(rgba);
    m_FontSize = size;
    Group InputGroup(input);
    Draw(InputGroup, size);
}

void Renderer::Image(string filepath)
{
    GeneratePNG(m_Bufferdyn, filepath.c_str());
}

void Renderer::Clear()
{
    m_PenPosX = 0;
    m_PenPosY = 0;
    m_PenPosYMax = 0;
    m_PenPosYMin = 0;
    m_Bufferdyn->Clear();
}

#ifdef PYBIND
#include <pybind11/pybind11.h>
namespace py = pybind11;

PYBIND11_MODULE(renderer, r) {
    py::class_<Renderer>(r, "Renderer")
        .def(py::init<string, string>())
        .def("Render", &Renderer::Render)
        .def("Image", &Renderer::Image)
        .def("Clear", &Renderer::Clear)
        ;
}
#endif