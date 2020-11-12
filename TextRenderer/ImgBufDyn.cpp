#include <stdlib.h>
#include <iostream>
#include <string.h>

#include "ImgBufDyn.hpp"

//Image Buffer Dynamic Row

ImgBufDynRow::ImgBufDynRow(const unsigned int width) 
{
    m_Data = (unsigned char*)calloc(width * 4, sizeof(unsigned char));   
    if (m_Data == nullptr)
    {
        cout << "[RENDERER ERROR] Ran out of memory in image buffer" << endl;
        terminate();
    } 
    m_Width = width;
}

ImgBufDynRow::~ImgBufDynRow() 
{
    free(m_Data);
}

void ImgBufDynRow::Resize(const unsigned int newWidth) 
{
    unsigned char* temp;
    temp = (unsigned char *)realloc(m_Data, newWidth * 4);
    if (temp == nullptr)
    {
        cout << "[RENDERER ERROR] Ran out of memory in image buffer" << endl;
        terminate();
    }
    m_Data = temp;    
    memset(m_Data + (m_Width * 4), 0, (newWidth - m_Width) * 4);
    m_Width = newWidth;
}

unsigned char* ImgBufDynRow::Data() const
{
    return m_Data;    
}

unsigned int ImgBufDynRow::Width() const
{
    return m_Width;
}

//Image Buffer Dynamic

ImgBufDyn::ImgBufDyn(const unsigned int width, const unsigned int height) 
    : m_Width(width), m_Height(height), m_YMin(0), m_YMax(height - 1), r(0), g(0), b(0), a(0)
{
    for (int i = 0; i < height; i++)
        m_Rows[i] = new ImgBufDynRow(width);
}

ImgBufDyn::~ImgBufDyn() 
{
    for (auto i : m_Rows)
        delete i.second;
}

void ImgBufDyn::PlaceImage(unsigned char* data, const int width, const int height, const int x, const int y) 
{
    if (x + width > m_Width)
        ResizeX(x + width);
    if (y + height > m_YMax)
    {
        for (int i = m_YMax + 1; i < y + height; i++)
            AddY(i);
    }
    if (y < m_YMin)
    {
        for (int i = m_YMin - 1; i >= y; i--)
            AddY(i);
    }
    ImgBufDynRow* temprow;
    unsigned char temp;
    unsigned char* dataPos;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp = *(data + ((height - i - 1) * width) + j);
            if (temp)
            {
                temprow = m_Rows[y + i];
                dataPos = temprow->Data() + ((x + j) * 4);
                *dataPos = r;
                *(dataPos + 1) = g;
                *(dataPos + 2) = b;
                *(dataPos + 3) = temp * a / 255;
            }
        }
    }
}

void ImgBufDyn::ResizeX(const unsigned int width) 
{
    for (auto i : m_Rows)
        (i.second)->Resize(width);
    m_Width = width;
}

void ImgBufDyn::AddY(const int rowNum) 
{
    m_Rows[rowNum] = new ImgBufDynRow(m_Width);
    if (rowNum < m_YMin)
        m_YMin = rowNum;
    else if (rowNum > m_YMax)
        m_YMax = rowNum;
    m_Height++;    
}

void ImgBufDyn::SetRGBA(const unsigned int rgba) 
{
    r = rgba >> 24;
    g = rgba >> 16;
    b = rgba >> 8;
    a = rgba;
}

void ImgBufDyn::Clear() 
{
    m_Width = 0, m_Height = 0, m_YMax = -1, m_YMin = 0;
    r = 0, g = 0, b = 0, a = 0;
    for (auto i : m_Rows)
        delete i.second;
    m_Rows.clear();
}

unsigned int ImgBufDyn::Height() const
{
   return m_Height; 
}

unsigned int ImgBufDyn::Width() const
{
    return m_Width;
}

int ImgBufDyn::YMin() const
{
    return m_YMin;
}

int ImgBufDyn::YMax() const
{
    return m_YMax;
}

ImgBufDynRow* ImgBufDyn::Row(int rowNum)
{
    return m_Rows[rowNum];
}