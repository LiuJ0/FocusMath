cmake_minimum_required(VERSION 3.0)

set(CMAKE_BUILD_TYPE Release)

project(renderer)

set(CMAKE_CXX_FLAGS "-O3")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../bin)

find_package(pybind11 REQUIRED)

link_directories(resources/libs)
include_directories(resources/include)

pybind11_add_module(
    renderer
    MODULE
    Renderer.cpp
    Character.cpp
    EquationParts.cpp
    Exceptions.cpp
    ImgBufDyn.cpp
)

set_property(
    TARGET renderer
    APPEND PROPERTY
        CXX_STANDARD 11
)

set_property(
    SOURCE Renderer.cpp
    APPEND PROPERTY
        COMPILE_DEFINITIONS PYBIND
)

target_link_libraries(
    renderer
    PRIVATE
    freetype
)

target_link_libraries(
    renderer
    PRIVATE
    z
)