#pragma once

#include <vector>
#include <string>

using namespace std;

struct EqPart {
    void* stored;
    string type;
};

struct TrigRatio {
    string type;
    bool inverse;
};

struct Root {
    int nvalue;
};

struct Escape {
    string escapeCode;
    bool useSuppValue;
    string suppValue;
};

struct Operation {
    char type;
    bool isRendererOp;
};

struct Constant {
    int value;
};

struct Variable {
    char symbol;
};

class Group {
private:
    vector<Group> m_Groups;
    vector<Constant> m_Constants;
    vector<Variable> m_Variables;
    vector<Operation> m_Operations;
    vector<Escape> m_Escapes;
    vector<int> m_Order;
    vector<int> m_Iterator;
    string m_Organization;
public: 
    Group(const string input);
    Group(const string input, const string organization);
    inline void SetOrganization(const string input) { m_Organization = input; }
    inline string Organization() const { return m_Organization; }   
    EqPart RetrieveNext(); 
    inline int OrderSize() const { return m_Order.size();}
    ~Group();
};