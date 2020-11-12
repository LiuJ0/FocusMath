#include <sstream>

#include "EquationParts.hpp"
#include "parsers.hpp"
#include "Exceptions.hpp"

Group::Group(string input) {

    for (int i = 0; i < 6; i++)
        m_Iterator.push_back(0);

    int i = 0;
    m_Organization = "default";
    while (i < input.length())
    {
        if (input[i] == '+' || input[i] == '-')
        {
            Operation temp({input[i], false});
            m_Operations.push_back(temp);
            m_Order.push_back(4);
            i++;
        }

        if (input[i] == '=')
        {
            Escape temp({"=", false, "0"});
            m_Escapes.push_back(temp);
            m_Order.push_back(5);
            i++;
            continue;
        }

        auto potentialTerm = findTermParser(input, i);
        auto termParsed = termParser(potentialTerm.group);

        if (termParsed.isTerm) {
            Group temp(potentialTerm.group, "term");
            m_Groups.push_back(temp);
            m_Order.push_back(1);
        } else {
            if (termParsed.type == "constant") {
                Constant temp({stoi(potentialTerm.group)});
                m_Constants.push_back(temp);
                m_Order.push_back(2);
            } else if (termParsed.type == "variable") {
                Variable temp({potentialTerm.group[0]});
                m_Variables.push_back(temp);
                m_Order.push_back(3);
            } else if (termParsed.type == "parenthesis") {
                auto removeParenthesis = groupParser(potentialTerm.group, 0);
                Group temp(removeParenthesis.group);
                temp.SetOrganization("parenthesis");
                m_Groups.push_back(temp);
                m_Order.push_back(1);
            } else if (termParsed.type == "symbol") {
                auto symbolParsed = escapeParser(potentialTerm.group, 0);
                Escape temp({symbolParsed.group, symbolParsed.useSuppValue, symbolParsed.suppValue});
                m_Escapes.push_back(temp);
                m_Order.push_back(5);
            }
        }
        i = potentialTerm.pos;

        if (potentialTerm.reachedStringEnd)
            break;
    }
}

Group::Group(string input, string organization) {
    
    for (int i = 0; i < 6; i++)
        m_Iterator.push_back(0);

    if (organization == "term")
    {
        m_Organization = "term";
        int i = 0;
        while (i < input.length())
        {
            stringstream termPart;
            //bool addMultOp = true;
            if (isNumber(input[i])) {
                for (int j = i; j <= input.length(); j++)
                {
                    if (isNumber(input[j]))
                        termPart << input[j];
                    else {
                        i = j;
                        break;
                    }
                }
                Constant temp({stoi(termPart.str())});
                m_Constants.push_back(temp);
                m_Order.push_back(2);
            } else if (isLowerLetter(input[i])) {
                Variable temp({input[i]});
                m_Variables.push_back(temp);
                m_Order.push_back(3);
                i++;
            } else if (input[i] == '(' || input[i] == '{') {
                auto groupParsed = groupParser(input, i);
                Group temp(groupParsed.group);
                if (input[i] == '(')
                    temp.SetOrganization("parenthesis");
                else 
                    temp.SetOrganization("operation group");
                m_Groups.push_back(temp);
                m_Order.push_back(1);
                i = groupParsed.pos;
            } else if (input[i] == '\\') {
                auto escapeParsed = escapeParser(input, i);
                Escape temp({escapeParsed.group, escapeParsed.useSuppValue, escapeParsed.suppValue});
                m_Escapes.push_back(temp);
                m_Order.push_back(5);
                i = escapeParsed.pos;
                if (escapeParsed.reachedStringEnd)
                    break;
            } else if (input[i] == '^') {
                Operation temp({'^', true});
                m_Operations.push_back(temp);
                m_Order.push_back(4);
                i++;
            } else if (input[i] == '_') {
                Operation temp({'_', true});
                m_Operations.push_back(temp);
                m_Order.push_back(4);
                i++;
            } else {
                TERMINATE(cout << "[PARSER ERROR] ( Character is unrecognized/unsupported : \"" << literalEscape(input[i]) << "\" )" << endl;)
            }
            /*
            if (!(input[i] == '^' || input[i] == '_' || input[i - 1] == '^' || input[i - 1] == '_') && i < input.length() - 1) {
                Operation temp({'*', false});
                m_Operations.push_back(temp);
                m_Order.push_back(4);
            }
            */
        }
    }
}

Group::~Group() { }

EqPart Group::RetrieveNext() {
    
    void* output;
    string type;

    switch (m_Order[m_Iterator[0]++])
    {
    case 1:
        output = &m_Groups[m_Iterator[1]++];
        type = "group";
        break;
    case 2:
        output = &m_Constants[m_Iterator[2]++];
        type = "constant";
        break;
    case 3:
        output = &m_Variables[m_Iterator[3]++];
        type = "variable";
        break;
    case 4:
        output = &m_Operations[m_Iterator[4]++];
        type = "operation";
        break;
    case 5:
        output = &m_Escapes[m_Iterator[5]++];
        type = "escape";
        break;
    default:
        break;
    }

    return {output, type};
}