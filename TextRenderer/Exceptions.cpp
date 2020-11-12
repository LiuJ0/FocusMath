#include "Exceptions.hpp"

const char* ftGetError(FT_Error err)
{
    
    #undef FTERRORS_H_
    #define FT_ERRORDEF( e, v, s )  case e: return s;
    #define FT_ERROR_START_LIST     switch (err) {
    #define FT_ERROR_END_LIST       }
    #include FT_ERRORS_H
    return "Unknown error";
}

const char* literalEscape(char input)
{
    switch (input)
    {
            case '\a':
                return "\\a";
                break;
            case '\b':
                return "\\b";
                break;
            case '\f':
                return "\\f";
                break;
            case '\n':
                return "\\n";
                break;
            case '\r':
                return "\\r";
                break;
            case '\t':
                return "\\t";
                break;
            case '\v':
                return "\\v";
                break;
            case ' ':
                return " ";
                break;
            case '*':
                return "*";
                break;
            case '/':
                return "/";
                break;
            default:
                return "unrecognized character";
    }
}