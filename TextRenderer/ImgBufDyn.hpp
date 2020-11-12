#pragma once

#include <unordered_map>

using namespace std;

class ImgBufDynRow {
private:
    unsigned char* m_Data;
    unsigned int m_Width;
public:
    ImgBufDynRow(const unsigned int width);
    ~ImgBufDynRow();
    void Resize(const unsigned int width);
    unsigned char* Data() const;
    unsigned int Width() const;
};

class ImgBufDyn {
private:
    unordered_map<int, ImgBufDynRow*> m_Rows;
    int m_Width, m_Height, m_YMin, m_YMax;
    unsigned char r, g, b, a;
public:
    ImgBufDyn(const unsigned int width, const unsigned int height);
    ~ImgBufDyn();
    void PlaceImage(unsigned char* data, const int width, const int height, const int x, const int y);
    void ResizeX(const unsigned int width);
    void AddY(const int rowNum);
    void SetRGBA(const unsigned int rgba);
    void Clear();
    unsigned int Height() const;
    unsigned int Width() const;
    int YMin() const;
    int YMax() const;
    ImgBufDynRow* Row(int rowNum);
};