#pragma once

#include <ft2build.h>
#include FT_FREETYPE_H

#define TERMINATE(x) x terminate();

const char* ftGetError(FT_Error);
const char* literalEscape(char);