"""
Calls From Wolfram|Alpha Step by Step API.
Writes into a file known as solutions.txt
"""

from datetime import datetime

import_time = datetime.now()
"""
import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations,implicit_multiplication_application
from sympy.printing import pretty
from sympy import init_printing
from sympy import pretty_print as pp, latex
from sympy import Eq, solve, Symbol
import wolframalpha
import os
import configparser
import time
"""
print(f"[StepPyStep] Import time: {datetime.now() - import_time}")


# Set of tools used to process TeX inputs.
class create_zip(object):
    def __init__(self):
        pass

    def create_directory(self, root_directory):
        start = datetime.now()
        # imports
        import os
        import configparser
        import time
        # get config data
        config = configparser.ConfigParser()
        config['HISTORY'] = {'count': '1',
                             'recent': '1-1-1',
                             }
        config['THEME'] = {
            'theme': 'default'
        }
        config.read("MathSolverApp/settings.ini")
        print(config.sections())
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
        config['HISTORY']['RECENT_DATE'] = str(time.strftime("%I-%M-%S %p, %b %d, %Y"))
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
        try:
            self.fpath = config['HISTORY']['RECENT_DATE']
            os.makedirs(os.path.join(root_directory, "Solutions", self.fpath))
            print(os.path.join(root_directory, "Solutions", self.fpath))
        except FileExistsError:
            pass
        with open(os.path.join(root_directory, "Solutions", self.fpath, "solution.txt"), "w+", encoding='utf-8'):
            pass
        print(f"[StepPyStep][create_zip][create_directory] runtime: {datetime.now() - start}")
        return self.fpath


class parse_tex(object):
    # Appends, starting from s till it runs into d
    def start_appending(self, s, d, i):
        temp = ""
        count = 1
        while (True):
            if (s[i] == "{"):
                count += 1
            if (s[i] == "}"):
                if (count == 1):
                    break
                else:
                    count -= 1
            temp += s[i]
            i += 1
        return temp

    # splits LaTeX arrays by {...}
    def split_array(self, tex):
        texl = []
        temp = ""
        flag = False
        i = 0
        while i < len(tex):
            if (tex[i] == "{"):
                temp = self.start_appending(tex, "}", i + 1)
                texl.append(temp)
                i += len(temp)
            else:
                i += 1
        del texl[0]
        del texl[0]
        del texl[len(texl) - 1]
        return texl

    # Determines the characters in a string, returns a list containing the variable(s)
    def determine_chars(self, tex):
        ch = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']
        found = []
        for k in tex:
            if (k in ch) and (k not in found):
                found.append(k)
        if found == []:
            return None
        return found

    def replaceBackSlash(self, tex):
        temp = tex
        if "\\frac" in tex:
            texList = self.split_array(tex)
            temp = texList[0] + "/" + texList[1]
        # greek letters
        temp = temp.replace("\pi", "pi")
        temp = temp.replace("\alpha", "alpha")
        temp = temp.replace("\mu", "mu")
        temp = temp.replace("\theta", "theta")

        # trig Functions
        temp = temp.replace("\sin", "sin")
        temp = temp.replace("\cos", "cos")
        temp = temp.replace("\tan", "tan")
        temp = temp.replace("\csc", "csc")
        temp = temp.replace("\sec", "sec")
        temp = temp.replace("\cot", "cot")
        temp = temp.replace("\sqrt", "sqrt")

        return temp

    # Converts 'a = b' equation into Eq(a,b), since sympy does not use '=' or '=='.
    def parse_equals(self, tex):
        try:
            return tex.split('=')
        except Exception:
            return tex

    def detectFrac(self, tex):
        if "\\frac" in tex:
            texList = self.split_array(tex)
            return texList[0] + "/" + texList[1]
        else:
            return tex

    def pretty_config(self, tex):
        start = datetime.now()
        import sympy
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        from sympy import init_printing
        from sympy.printing import pretty
        from sympy import Eq, Symbol
        # definition of the transformation used in parse_expr
        transformations = transformations = (standard_transformations + (implicit_multiplication_application,))
        # ^ is considered the bitwise-XOR in programming, as such, ** is adopted in python.
        tex = str(tex).replace("^", "**")
        # Sympy does not handle equations well ,so we need to split them
        if ("=" in tex):
            rhs, lhs = tex.split('=')
            try:
                rhs = parse_expr(rhs, transformations=transformations)
                lhs = parse_expr(lhs, transformations=transformations)
            except SyntaxError as e:
                print(e)
                print(f"[StepPyStep][parse_tex][pretty_config] runtime: {datetime.now() - start}")
                return tex
            # Actual pretty print of sympy
            # using more common unicode that looks bette
            rhs = pretty(rhs, use_unicode=True)

            rhs = rhs.replace("╲╱", "√")
            rhs = rhs.replace("sqrt", "√")

            lhs = pretty(lhs, use_unicode=True)

            lhs = lhs.replace("╲╱", "√")
            lhs = lhs.replace("sqrt", "√")

            tex = rhs + "=" + lhs + "\n"

            print(f"[StepPyStep][parse_tex][pretty_config] runtime: {datetime.now() - start}")

            return tex
        # Without equations the procedure is very simple
        else:

            sympy_expr = parse_expr(tex, transformations=transformations)

            print(f"[StepPyStep][parse_tex][pretty_config] runtime: {datetime.now() - start}")
            pretty_expr = pretty(sympy_expr)
            pretty_expr = pretty_expr.replace("╲╱", "√").replace("sqrt", "√")
            return pretty_expr


class solve_equation(object):
    def wolfram_alpha(self, call, image=False):
        image = False
        start = datetime.now()
        # imports
        import sympy
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        import wolframalpha
        import os
        import configparser
        import time
        from sympy import Eq, solve, Symbol

        # Calls from the wolfram|alpha api for step-by-step calculations.

        client = wolframalpha.Client('EVHR3T-ULQ98AEG66')
        self.res = client.query(call)
        # Checks if there was an error calling the client

        try:
            print(self.res.pods)
        except AttributeError:
            return "Our software ran into an issue. Sorry!"
        solution_list = []
        # Is it an image?
        if image is False:
            # Parse through the many outputs of wolfram|alpha
            for pod in self.res.pods:
                for sub in pod.subpods:
                    # Find the right one
                    if sub['@title'] == "Possible intermediate steps":
                        if parse_tex().determine_chars(call) is None:
                            print("no symbols found")
                            solution = str(sub.plaintext).split(':')
                            for step in solution:
                                solution_list.append(step)
                            print(f"solution_list: {solution_list}")
                            return solution_list
                        s = str(sub.plaintext).split('\n')
                        print(f"array s is {s}")
                        for i in range(len(s)):
                            if ":" not in s[i]:
                                # is there an '=' in it? If so, it must be math
                                # Are there multiple solutions?
                                if 'or' in s[i]:
                                    # Deal with multiple solutions
                                    mult_solution = s[i].split('or')
                                    for x in range(len(mult_solution)):
                                        # f.write(mult_solution[x] + " ")
                                        solution_list.append(mult_solution[x])
                                    # f.write('\n')
                                # There is only one solution
                                else:
                                    # render
                                    # f.write(s[i] + '\n')
                                    solution_list.append(s[i])
                                    print(s[i])
                            # The line is simply an explaination, as such, we do not need to render it
                            else:
                                if '=' in s[i]:
                                    # f.write(s[i] + '\n')
                                    solution_list.append(f"{s[i]}")
                                    print(s[i] + '\n')
                                elif "Answer" not in s[i]:
                                    # f.write(s[i] + '\n')
                                    solution_list.append(f"text: {s[i]}")
                                    print(s[i] + '\n')
        # Image was passed - simple procedure
        else:
            print('image passed')
            for pod in self.res.pods:
                for sub in pod.subpods:
                    # Get the right pod
                    temp = sub['img']['@src']
        print(f"[StepPyStep][solve_equation][wolfram_alpha] runtime: {datetime.now() - start}")
        print(f"Solution list is: {solution_list}")

        return solution_list

    # Used with check_equation().check_eq()

    def get_answer(self, tex):
        start = datetime.now()
        # imports
        import sympy
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        import wolframalpha
        import os
        import configparser
        import time
        from sympy import Eq, solve, Symbol
        # Deal with '='
        lhs, rhs = parse_tex().parse_equals(tex)
        transformations = (standard_transformations +
                           (implicit_multiplication_application,))
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)

        Equ = Eq(lhs, rhs)
        # Solve
        Equ = Eq(lhs, rhs)
        a = solve(Equ)
        print(f"[StepPyStep][solve_equation][get_answer] runtime: {datetime.now() - start}")
        return a


class check_equation(object):
    # str -> check_eq -> bool
    # int ----^
    def check_eq(self, eq, answer, precision, step, writepath):
        start = datetime.now()
        # imports
        import sympy
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        import wolframalpha
        import os
        import configparser
        import time
        from sympy import Eq, solve, Symbol

        transformations = (standard_transformations +
                           (implicit_multiplication_application,))
        # Parsing into sympy expr
        lhs, rhs = parse_tex().parse_equals(eq)
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        # Are there multiple solutions?
        if (isinstance(answer, list)):
            for solutions in answer:
                # Rounding, since the Newton-Rapson techinque fails to return precise integers, only very close approximations.
                lhs = lhs.subs(Symbol('x'), solutions)
                lhs = round(lhs, precision)
                rhs = rhs.subs(Symbol('x'), solutions)
                rhs = round(rhs, precision)
                with open(os.path.join(writepath, "solution.tmp"), "a") as f:
                    # It's correct
                    if (lhs == rhs):
                        # Write into solution.tmp
                        f.write(f"[STEP{step}]\n")
                        f.write(f"step = {eq}\n")
                        f.write(f"solution = Correct\n")
                        print(f"[StepPyStep][Check_equation][check_eq] runtime: {datetime.now() - start}")
                        return eq
            # It's wrong, because it did not return yet
            with open(os.path.join(writepath, "solution.tmp"), "a") as f:
                # Formattting
                f.write(f"[STEP{step}]\n")
                f.write(f"step = {eq}\n")
                print(f"[StepPyStep][Check_equation][check_eq] runtime: {datetime.now() - start}")
                output = f"{eq}" + "(False)"
                return output

        else:
            lhs = lhs.subs(Symbol('x'), answer)
            rhs = rhs.subs(Symbol('x'), answer)
            with open(os.path.join(writepath, "solution.tmp"), "a") as f:
                if lhs == rhs:
                    f.write(eq + "\t + True")
                    print(f"[StepPyStep][Check_equation][check_eq] runtime: {datetime.now() - start}")
                    return eq
                else:
                    f.write(eq + "\t + False")
                    print(f"[StepPyStep][Check_equation][check_eq] runtime: {datetime.now() - start}")
                    output = f"{eq}"
                    return output + "(False)"

