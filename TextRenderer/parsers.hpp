#pragma once

#include <sstream>
#include <string>
#include <iostream>

#include "Exceptions.hpp"

using namespace std;

bool isNumber(char input) {
    return (input <= 57 && input >= 48) ? true : false;
}

bool isLowerLetter(char input) {
    return (input <= 122 && input >= 97) ? true : false;
}

struct parsedLayout {
    string group;
    int pos;
    bool reachedStringEnd;
};

struct escapeParsedLayout {
    string group;
    int pos;
    bool reachedStringEnd;
    bool useSuppValue;
    string suppValue;
};

struct termParsedLayout {
    bool isTerm;
    string type;
};

parsedLayout findTermParser(string input, int pos) {
    int newPos = pos;
    stringstream output;
    bool reachedStringEnd = false;
    for (int i = pos, ignore = 0; i < input.length(); i++)
    {
        if ((input[i] != '+' && input[i] != '-' && input[i] != '=') || ignore != 0)
            output << input[i];
        else if (ignore == 0) {
            newPos = i;
            break;
        }

        if (input[i] == '{' || input[i] == '(')
            ignore++;
        if (input[i] == '}' || input[i] == ')')
            ignore--;
    }

    if (newPos == pos)
        reachedStringEnd = true;

    return {output.str(), newPos, reachedStringEnd};
}

escapeParsedLayout escapeParser(string input, int pos) {
    int newPos = pos;
    bool useSuppValue = false;
    stringstream suppValue("0");
    bool reachedStringEnd = false;
    stringstream escapeCode;
    for (int i = pos + 1, ignore = 0; i < input.length(); i++)
    {
        if (isLowerLetter(input[i]))
            escapeCode << input[i];
        else if (input[i] == '[')
        {
            useSuppValue = true;
            for (int j = i + 1; j < input.length(); j++)
            {
                if (input[j] != ']')
                    suppValue << input[j];
                else {
                    newPos = j + 1;
                    break;
                }
            }
            break;
        } else {
            newPos = i;
            break;
        }   
    }

    if (newPos == pos)
        reachedStringEnd = true;

    return {escapeCode.str(), newPos, reachedStringEnd, useSuppValue, suppValue.str()};
}

parsedLayout groupParser(string input, int pos) {
    stringstream group;
    int newPos = pos;
    bool reachedStringEnd = false;

    char ig1 = input[pos], ig2;
    if (ig1 == '(')
        ig2 = ')';
    else if (ig1 == '{')
        ig2 = '}';
    else if (ig1 == '|')
        ig2 = '|';

    for (int i = pos+1, ignore = 0; i < input.length(); i++)
    {
        if (input[i] == ig2 && ignore == 0) 
        {
            newPos = ++i;
            break;
        } else if (input[i] == ig1)
            ignore++;
        else if (input[i] == ig2)
            ignore--;

        group << input[i];
    }

    if (newPos == pos)
        reachedStringEnd = true;

    return {group.str(), newPos, reachedStringEnd};
}

termParsedLayout termParser(string input) {
    bool isTerm = false;
    string type = "term";

    if (isNumber(input[0]))
    {
        for (int i = 0; i < input.length(); i++)
        {
            if (!isNumber(input[i]))
            {
                isTerm = true;
                break;
            }
        }

        if (!isTerm)
            type = "constant";
    } else if (isLowerLetter(input[0]))
    {
        if (input.length() == 1)
            type = "variable";
        else 
            isTerm = true;
    } else if (input[0] == '(')
    {
        int x = input.find_first_of(')', 0);

        if (x == input.length() - 1)
            type = "parenthesis";
        else
            isTerm = true;
    } else if (input[0] == '\\')
    {
        for (int i = 1; i < input.length() - 1; i++)
        {
            if (!isLowerLetter(input[i]))
            {
                isTerm = true;
                break;
            }
        }

        if (!isTerm)
            type = "symbol";
    } else if (type == "term" && isTerm == false)
    {
        TERMINATE(cout << "[PARSER ERROR] ( Character is unrecognized/unsupported : \"" << literalEscape(input[0]) << "\" )" << endl;)
    }

    return {isTerm, type};
}