import re
from PeekableStream import PeekableStream


# Truth Table

########################################################################################################################

# Function which generates a truth table depending on the number of variables
def create_table(num_vars):
    # This statement here is what is called a list comprehension in python
    table = [[0 for y in range(2 ** num_vars)] for x in range(num_vars)]

    # This nested for loop is used to fill the array with the required values
    for x in range(1, num_vars + 1):
        val = False

        for y in range(2 ** num_vars):
            if y % (2 ** num_vars / 2 ** x) == 0:
                val = not val

            table[x - 1][y] = val

    return table


# Function which prints a table
def print_table(table):
    for y in range(len(table[0])):
        for x in range(len(table)):
            print(str(table[x][y]) + " ", end='')

        print()


########################################################################################################################

# Lexer

########################################################################################################################

# This function is used to make sure that variables that are longer than one digit get classified as one variable
def complete_variable(logic_char, peekable_stream, allowed):
    ret = logic_char

    while peekable_stream.currentElem is not None and re.match(allowed, peekable_stream.currentElem):
        ret += peekable_stream.next_elem()

    return ret


# This function is used to make sure that the subjunctor is treated as one character in the rest of the program since it
# is made up of two characters
# If the next character is not the required character then it raises and exception
def complete_subjunctor(logic_char, peekable_stream):
    ret = logic_char

    if peekable_stream.next_elem() == ">":
        ret += ">"
    else:
        raise Exception("InvalidSymbol")

    return ret


# This function is used to make sure that the bi-subjunctor is treated as one character in the rest of the program since
# it is made up of three characters
# If the next character is not the required character then it raises and exception
def complete_bi_subjunctor(logic_char, peekable_stream):
    ret = logic_char

    if peekable_stream.next_elem() == "-":
        ret += "-"
    else:
        raise Exception("InvalidSymbol")

    if peekable_stream.next_elem() == ">":
        ret += ">"
    else:
        raise Exception("InvalidSymbol")

    return ret


# This function takes in a string and moves through that string ignoring spaces and classifying characters then it
# returns an iterable of tokens
def lex(logic_expression):
    logic_peekable_stream = PeekableStream(list(logic_expression))

    while logic_peekable_stream.currentElem is not None:
        logic_char = logic_peekable_stream.next_elem()

        if logic_char in " ":
            pass
        elif logic_char in "¬":
            yield "negator", logic_char  # negator ==> (not A)
        elif logic_char in "^":
            yield "conjunctor", logic_char  # conjunctor ==> A and B
        elif logic_char in "v":
            yield "adjunctor", logic_char  # adjunctor ==> A or B
        elif logic_char in "u":
            yield "disjunctor", logic_char  # disjunctor ==> (A and (not B)) or ((not B) and A)
        elif logic_char in "->":
            yield "subjunctor", complete_subjunctor(logic_char, logic_peekable_stream)  # subjunctor ==> (not A) or B
        elif logic_char in "<->":
            yield ("bi-subjunctor", complete_bi_subjunctor(logic_char,
                                                           logic_peekable_stream))
            # bi-subjunctor ==> (A and B) or ((not A) and (not B))
        elif logic_char in "()":
            yield logic_char, logic_char
        elif re.match("[a-zA-Z]", logic_char):
            yield "variable", complete_variable(logic_char, logic_peekable_stream, "[1-9a-zA-Z]")
        elif re.match("[1-9]", logic_char):
            raise Exception("InvalidVariable")
        else:
            raise Exception("UnrecognisedSymbol")  # If symbols not specified above are found it will raise an exception


# This function converts that iterable tokens into a list
# then the list is checked to make sure that unnecessary variable names are not used for example if the symbols 1, 2 and
# 13 are used
# then the function will raise an exception because instead of 13, 3 should be used
def lex_list(logic_expression):
    return list(lex(logic_expression))


########################################################################################################################

# Parser

########################################################################################################################

# Thanks to Giorgio for inspiring me to come up with this specific algorithm
# The complete_argument method is very important as it groups tokens into one argument token as most of the operators
# are binary and the negator is unary
# Because of the above an operator can operate on another logic expression for example (1 ^ 2) v 3
# Know the grouping happens using recursion. Basically, the algorithm follows the principle that the last bracket is the
# first one to be closed
# Generally, this would be done using a stack however we are not just checking for balanced brackets

def complete_argument(token, peekable_stream):
    ret = ("argument", [token])

    # The != ')' added bracket matching
    while peekable_stream.currentElem is not None and peekable_stream.currentElem[0] != ")":
        if peekable_stream.currentElem[0] == "(":
            ret[1].append(complete_argument(peekable_stream.next_elem(), peekable_stream))
        elif peekable_stream.currentElem[0] == "negator":
            ret[1].append(complete_negator(peekable_stream.next_elem(), peekable_stream))
        else:
            ret[1].append(peekable_stream.next_elem())

    try:
        ret[1].append(peekable_stream.next_elem())
    except Exception:
        raise Exception("Unmatched '('")

    return ret


# The complete_negator function follows the same principle, ¬1 should be treated as an argument for the other operators
# and it itself can take a variable or an argument

def complete_negator(token, peekable_stream):
    ret = ("argument", [token])

    if peekable_stream.currentElem[0] == "variable":  # In the case that it takes a variable
        ret[1].append(peekable_stream.next_elem())
    elif peekable_stream.currentElem[0] == "(":  # In the case that it takes an argument
        ret[1].append(complete_argument(peekable_stream.next_elem(), peekable_stream))
    else:
        raise Exception("InvalidSucceedingToken")

    return ret


# This function is used to create a tree structure using lists 

def parse(peekable_token_table):
    while peekable_token_table.currentElem is not None:
        logic_token = peekable_token_table.next_elem()

        # If a token ( or negator is found the below methods are called
        if logic_token[0] == "(":
            yield complete_argument(logic_token, peekable_token_table)
        elif logic_token[0] == "negator":
            yield complete_negator(logic_token, peekable_token_table)
        else:
            yield logic_token


# This function converts the iterable created by the parse function into a list
def parse_list(token_table):
    return list(parse(PeekableStream(token_table)))


########################################################################################################################

# Evaluator

########################################################################################################################

# This is a list of all the valid combinations. This list is consulted to make sure that the input is valid
combinations = [
    "argument",
    "negatorargument",
    "argumentconjunctorargument",
    "argumentadjunctorargument",
    "argumentdisjunctorargument",
    "argumentsubjunctorargument",
    "argumentbi-subjunctorargument",
    "variable",
    "negatorvariable",
    "variableconjunctorvariable",
    "variableadjunctorvariable",
    "variabledisjunctorvariable",
    "variablesubjunctorvariable",
    "variablebi-subjunctorvariable",
    "variableconjunctorargument",
    "variableadjunctorargument",
    "variabledisjunctorargument",
    "variablesubjunctorargument",
    "variablebi-subjunctorargument",
    "argumentconjunctorvariable",
    "argumentadjunctorvariable",
    "argumentdisjunctorvariable",
    "argumentsubjunctorvariable",
    "argumentbi-subjunctorvariable",
]


# This function is used to check if the syntax of the input is valid
def check_syntax(parsed_list):
    parsed_peekable_stream = PeekableStream(parsed_list)

    combination = ""

    # This code segment generates a combination string according to the input
    # If an argument is found the method is called on that argument and that argument is checked separately
    # Otherwise if what you are dealing with is not an argument it just adds the token name to the combination string 
    while parsed_peekable_stream.currentElem is not None:
        if parsed_peekable_stream.currentElem[0] in "()":
            parsed_peekable_stream.next_elem()
        elif parsed_peekable_stream.currentElem[0] == "argument":
            combination += "argument"
            check_syntax((parsed_peekable_stream.next_elem())[1])
        else:
            combination += (parsed_peekable_stream.next_elem())[0]

    # This is the section which makes sure that one of the combinations is met if that is not the case it raises an
    # exception
    combination_incorrect = True

    for properCombination in combinations:
        if properCombination == combination:
            combination_incorrect = False

    if combination_incorrect:
        raise Exception("SyntaxError")

    return parsed_list


# This is probably by far the most complicated method, this is because its job is to convert the disjunctor (u),
# subjunctor (->) and bi-subjunctor (<->) into nots (¬) ands (^)
# and ors (v) [Using a complete system of junctors]

def converter(checked_list):
    checked_peekable_stream = PeekableStream(checked_list)

    ret = []

    while checked_peekable_stream.currentElem is not None:
        if checked_peekable_stream.currentElem[0] in "()":
            ret.append(checked_peekable_stream.next_elem())

        # The logic found in this elif statement is basically the same thing as the logic found in the elif statement
        # for when a variable is found
        elif checked_peekable_stream.currentElem[0] == "argument":
            # The argument is kept in temporary vairable
            temp = ("argument", converter(checked_peekable_stream.next_elem()[1]))

            # In this if else if ladder we consider the junctor u, -> and <->
            # If any of these junctors are found they are converted
            # However to do this the second variable is also required
            if checked_peekable_stream.currentElem is not None and checked_peekable_stream.currentElem[0] == "subjunctor":
                ret.append(("argument", [("negator", "¬"), temp]))
                checked_peekable_stream.next_elem()
                ret.append(("adjunctor", "v"))

                # This is used to check what the next element is and handle both possibilities
                # In the case where an argument is found the function converter is called again on the argument
                if checked_peekable_stream.currentElem[0] == "variable":
                    ret.append(checked_peekable_stream.next_elem())
                elif checked_peekable_stream.currentElem[0] == "argument":
                    ret.append(("argument", converter(checked_peekable_stream.next_elem()[1])))

            elif checked_peekable_stream.currentElem is not None and checked_peekable_stream.currentElem[0] == "bi-subjunctor":
                temp2 = ("argument",
                         [("argument", [("(", "("), ("argument", [("negator", "¬"), temp]), ("adjunctor", "v")]),
                          ("conjunctor", "^"), ("argument", [("(", "("), temp, ("adjunctor", "v")])])
                checked_peekable_stream.next_elem()

                # Again it checks what the next element is and handles both possibilities
                # the instructions are a bit more complicated because they are placing the element in the correct
                # position in the temp2 variable
                if checked_peekable_stream.currentElem[0] == "variable":
                    temp3 = checked_peekable_stream.next_elem()
                    temp2[1][0][1].append(temp3)
                    temp2[1][0][1].append((")", ")"))

                    temp2[1][2][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][2][1].append((")", ")"))
                elif checked_peekable_stream.currentElem[0] == "argument":
                    temp3 = ("argument", converter(checked_peekable_stream.next_elem()[1]))
                    temp2[1][0][1].append(temp3)
                    temp2[1][0][1].append((")", ")"))

                    temp2[1][2][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][2][1].append((")", ")"))

                ret.append(temp2)

            # This does the same thing as the bi-subjunctor but for the disjunctor
            elif checked_peekable_stream.currentElem is not None and checked_peekable_stream.currentElem[0] == "disjunctor":
                temp2 = ("argument",
                         [("argument", [("(", "("), temp, ("conjunctor", "^")]), ("adjunctor", "v"),
                          ("argument", [("(", "("), ("argument", [("negator", "¬"), temp]), ("conjunctor", "^")])])
                checked_peekable_stream.next_elem()

                if checked_peekable_stream.currentElem[0] == "variable":
                    temp3 = checked_peekable_stream.next_elem()
                    temp2[1][0][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][0][1].append((")", ")"))

                    temp2[1][2][1].append(temp3)
                    temp2[1][2][1].append((")", ")"))
                elif checked_peekable_stream.currentElem[0] == "argument":
                    temp3 = ("argument", converter(checked_peekable_stream.next_elem()[1]))
                    temp2[1][0][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][0][1].append((")", ")"))

                    temp2[1][2][1].append(temp3)
                    temp2[1][2][1].append((")", ")"))

                ret.append(temp2)

            else:
                ret.append(temp)

        elif checked_peekable_stream.currentElem[0] == "variable":
            temp = checked_peekable_stream.next_elem()

            if checked_peekable_stream.currentElem is not None and checked_peekable_stream.currentElem[0] == "subjunctor":
                ret.append(("argument", [("negator", "¬"), temp]))
                checked_peekable_stream.next_elem()
                ret.append(("adjunctor", "v"))

                if checked_peekable_stream.currentElem[0] == "variable":
                    ret.append(checked_peekable_stream.next_elem())
                elif checked_peekable_stream.currentElem[0] == "argument":
                    ret.append(("argument", converter(checked_peekable_stream.next_elem()[1])))

            elif checked_peekable_stream.currentElem is not None and checked_peekable_stream.currentElem[
                0] == "bi-subjunctor":
                temp2 = ("argument",
                         [("argument", [("(", "("), ("argument", [("negator", "¬"), temp]), ("adjunctor", "v")]),
                          ("conjunctor", "^"), ("argument", [("(", "("), temp, ("adjunctor", "v")])])
                checked_peekable_stream.next_elem()

                if checked_peekable_stream.currentElem[0] == "variable":
                    temp3 = checked_peekable_stream.next_elem()
                    temp2[1][0][1].append(temp3)
                    temp2[1][0][1].append((")", ")"))

                    temp2[1][2][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][2][1].append((")", ")"))
                elif checked_peekable_stream.currentElem[0] == "argument":
                    temp3 = ("argument", converter(checked_peekable_stream.next_elem()[1]))
                    temp2[1][0][1].append(temp3)
                    temp2[1][0][1].append((")", ")"))

                    temp2[1][2][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][2][1].append((")", ")"))

                ret.append(temp2)

            elif checked_peekable_stream.currentElem is not None and checked_peekable_stream.currentElem[0] == "disjunctor":
                temp2 = ("argument",
                         [("argument", [("(", "("), temp, ("conjunctor", "^")]), ("adjunctor", "v"),
                          ("argument", [("(", "("), ("argument", [("negator", "¬"), temp]), ("conjunctor", "^")])])
                checked_peekable_stream.next_elem()

                if checked_peekable_stream.currentElem[0] == "variable":
                    temp3 = checked_peekable_stream.next_elem()
                    temp2[1][0][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][0][1].append((")", ")"))

                    temp2[1][2][1].append(temp3)
                    temp2[1][2][1].append((")", ")"))
                elif checked_peekable_stream.currentElem[0] == "argument":
                    temp3 = ("argument", converter(checked_peekable_stream.next_elem()[1]))
                    temp2[1][0][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][0][1].append((")", ")"))

                    temp2[1][2][1].append(temp3)
                    temp2[1][2][1].append((")", ")"))

                ret.append(temp2)

            else:
                ret.append(temp)

        else:
            ret.append(checked_peekable_stream.next_elem())

    return ret


# This function basically generates python code which can be executed using the eval function

def gen_eval_string(conv_list):
    conv_peekable_stream = PeekableStream(conv_list)

    ret = ""

    while conv_peekable_stream.currentElem is not None:
        if conv_peekable_stream.currentElem[0] == "argument":
            ret += gen_eval_string(conv_peekable_stream.next_elem()[1])
        elif conv_peekable_stream.currentElem[0] == "variable":
            ret += conv_peekable_stream.next_elem()[1]
        elif conv_peekable_stream.currentElem[0] == "negator":
            ret += "not "
            conv_peekable_stream.next_elem()
        elif conv_peekable_stream.currentElem[0] == "adjunctor":
            ret += " or "
            conv_peekable_stream.next_elem()
        elif conv_peekable_stream.currentElem[0] == "conjunctor":
            ret += " and "
            conv_peekable_stream.next_elem()
        elif conv_peekable_stream.currentElem[0] in "()":
            ret += conv_peekable_stream.next_elem()[1]

    return ret


# This function basically is used to create one big function and return the python executable string along with the
# number of variables and the variables

def eval_logic_expression(logic_expression):
    token_list = lex_list(logic_expression)

    variable_count = 0
    variables = []

    for token in token_list:
        if token[0] == "variable" and token[1] not in "".join(variables):
            variable_count += 1
            variables.append(token[1])

    yield variable_count
    yield variables
    yield gen_eval_string(converter(check_syntax(parse_list(token_list))))


########################################################################################################################

# Main Loop

########################################################################################################################

# This is the main loop

while True:
    temp = list(eval_logic_expression(input("Input logic expression: ")))

    variableCount = temp[0]
    variables = temp[1]
    maskString = temp[2]

    print("\n" + maskString + "\n")

    # Generates Appropriate Table
    table = create_table(variableCount)

    print("Truth Table\n")

    print(variables)
    print_table(table)

    print("\nEvaluated Expression\n")

    # For loop which through all the possibilities and calculates the result of each possibility
    for y in range(len(table[0])):
        for x in range(len(table)):
            exec(str(variables[x]) + '=' + str(table[x][y]))

        print(eval(maskString, locals()))

    print()
