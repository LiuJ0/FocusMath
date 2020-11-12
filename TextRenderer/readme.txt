HOW TO USE RENDERER
import :
from bin.renderer import Renderer
instantiate object :
example = Renderer()
use renderer :
example.Render(input, color, size) <-- takes 3 parameters 
input is a string defining the input
color is the rgba color, it is recommended to put in hex as such : 0xFFFFFFFF (this would be rgba(255, 255, 255, 1.0) 0x00FF00FF would be rgba(0, 255, 0, 1.0))
size is a number representing the size of glyphs in pixels
example.Image(path) <-- takes 1 parameter
path is a string defining the path where the output png will be written/overwritten

Compile with cmake!
ensure pybind11 is properly installed
cmake -G"MSYS Makefiles" -B build_gcc
cmake --build build_gcc

cmake -G"MSYS Makefiles" -B build_py
cmake --build build_py