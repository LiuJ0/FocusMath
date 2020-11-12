#pragma once

#include <iostream>
#include <chrono>

#include "Renderer.hpp"

using namespace std;
int implementation()
{
    int size = 256;
    unsigned int color = 0xFFFFFFFF;
    /*
    cout << "Enter string to render : " << endl;
    string input;
    getline(cin, input);
    */
    auto start = chrono::steady_clock::now();
    Renderer Renderer("resources/fonts/STIX2Math.otf", "resources/fonts/STIX2Text-Italic.otf");
    Renderer.Render("\\text[speed]", color, size);
    Renderer.Image("resources/images/output.png");
    Renderer.Clear();
    Renderer.Render("\\text[speed]", 0x0000FFFF, 256);
    Renderer.Image("resources/images/output2,png");
    auto end = chrono::steady_clock::now();
    cout << "Elapsed time in microseconds : " << chrono::duration_cast<chrono::microseconds>(end - start).count() << " µs" << endl;
    
    return 0;
}