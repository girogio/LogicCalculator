import re
from PeekableStream import PeekableStream

# Truth Table

##################################################################################################################################

# Function which generates a truth table depending on the number of variables
def createTable(numVars):
    # This statement here is what is called a list comprehension in python
    table = [[0 for y in range(2**numVars)] for x in range(numVars)]

    # This nested for loop is used to fill the array with the required values
    for x in range(1, numVars + 1):
        val = False

        for y in range(2**numVars):
            if y % (2**numVars / 2**x) == 0:
                val = not val

            table[x - 1][y] = val

    return table

# Function which prints a table
def printTable(table):
    for y in range(len(table[0])):
        for x in range(len(table)):
            print(str(table[x][y]) + " ", end='')

        print()


##################################################################################################################################

# Lexer

##################################################################################################################################

# This function is used to make sure that variables that are longer than one digit get classified as one variable
def completeVariable(logicChar, peekableStream, allowed):
    ret = logicChar

    while peekableStream.currentElem is not None and re.match(allowed, peekableStream.currentElem):
        ret += peekableStream.nextElem()

    return ret

# This function is used to make sure that the subjunctor is treated as one character in the rest of the program since it is made up of two characters
# If the next character is not the required character then it raises and exception
def completeSubjunctor(logicChar, peekableStream):
    ret = logicChar

    if peekableStream.nextElem() == ">":
        ret += ">"
    else:
        raise Exception("InvalidSymbol")

    return ret

# This function is used to make sure that the bi-subjunctor is treated as one character in the rest of the program since it is made up of three characters
# If the next character is not the required character then it raises and exception
def completeBiSubjunctor(logicChar, peekableStream):
    ret = logicChar

    if peekableStream.nextElem() == "-":
        ret += "-"
    else:
        raise Exception("InvalidSymbol")

    if peekableStream.nextElem() == ">":
        ret += ">"
    else:
        raise Exception("InvalidSymbol")

    return ret


# This function takes in a string and moves through that string ignoring spaces and classifying characters then it returns an iterable of tokens
def lex(logicExpression):
    logicPeekableStream = PeekableStream(list(logicExpression))

    while logicPeekableStream.currentElem is not None:
        logicChar = logicPeekableStream.nextElem()

        if logicChar in " ":
            pass
        elif logicChar in "¬":
            yield ("negator", logicChar)  # negator ==> (not A)
        elif logicChar in "^":
            yield ("conjunctor", logicChar)  # conjunctor ==> A and B
        elif logicChar in "v":
            yield ("adjunctor", logicChar)  # adjunctor ==> A or B
        elif logicChar in "u":
            yield ("disjunctor", logicChar) # disjunctor ==> (A and (not B)) or ((not B) and A)
        elif logicChar in "->":
            yield ("subjunctor", completeSubjunctor(logicChar, logicPeekableStream)) # subjunctor ==> (not A) or B
        elif logicChar in "<->":
            yield ("bi-subjunctor", completeBiSubjunctor(logicChar, logicPeekableStream)) # bi-subjunctor ==> (A and B) or ((not A) and (not B))
        elif logicChar in "()":
            yield (logicChar, logicChar)
        elif re.match("[a-zA-Z]", logicChar):
            yield ("variable", completeVariable(logicChar, logicPeekableStream, "[1-9a-zA-Z]"))
        elif re.match("[1-9]", logicChar):
            raise Exception("InvalidVairable")
        else:
            raise Exception("UnrecognisedSymbol") # If symbols not specified above are found it will raise an exception



# This function converts that iterable tokens into a list
# then the list is checked to make sure that unnecessary variable names are not used for example if the symbols 1, 2 and 13 are used
# then the function will raise an exception because instead of 13, 3 should be used
def lexList(logicExpression):
    return list(lex(logicExpression))


##################################################################################################################################

# Parser

##################################################################################################################################

# Thanks to Giorgio for inspiring me to come up with this specific algorithm
# The completeArgument method is very important as it groups tokens into one argument token as most of the operators are binary and the negator is unary
# Because of the above an operator can operate on another logic expression for example (1 ^ 2) v 3
# Know the grouping happens using recursion. Basically, the algorithm follows the principle that the last bracket is the first one to be closed
# Generally, this would be done using a stack however we are not just checking for balanced brackets

def completeArgument(token, peekableStream):
    ret = ("argument", [token])

    # The != ')' added bracket matching
    while peekableStream.currentElem is not None and peekableStream.currentElem[0] != ")":
        if peekableStream.currentElem[0] == "(":
            ret[1].append(completeArgument(peekableStream.nextElem(), peekableStream))
        elif peekableStream.currentElem[0] == "negator":
            ret[1].append(completeNegator(peekableStream.nextElem(), peekableStream))
        else:
            ret[1].append(peekableStream.nextElem())

    try:
        ret[1].append(peekableStream.nextElem())
    except Exception:
        raise Exception("Unmatched '('")

    return ret

# The completeNegator function follows the same principle, ¬1 should be treated as an argument for the other operators and it itself can take a variable or an argument

def completeNegator(token, peekableStream):
    ret = ("argument", [token])

    if peekableStream.currentElem[0] == "variable": # In the case that it takes a variable
        ret[1].append(peekableStream.nextElem())
    elif peekableStream.currentElem[0] == "(": # In the case that it takes an argument
        ret[1].append(completeArgument(peekableStream.nextElem(), peekableStream))
    else:
        raise Exception("InvalidSucceedingToken")

    return ret


# This function is used to create a tree structure using lists 

def parse(peekableTokenTable):
    while peekableTokenTable.currentElem is not None:
        logicToken = peekableTokenTable.nextElem()

        # If a token ( or negator is found the below methods are called
        if logicToken[0] == "(":
            yield (completeArgument(logicToken, peekableTokenTable))
        elif logicToken[0] == "negator":
            yield (completeNegator(logicToken, peekableTokenTable))
        else:
            yield logicToken

# This function converts the iteratble created by the parse function into a list
def parseList(tokenTable):
    return list(parse(PeekableStream(tokenTable)))


##################################################################################################################################

# Evaluator

##################################################################################################################################

#This is a list of all the valid combinations. This list is consulted to make sure that the input is valid
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
def checkSyntax(parsedList):
    parsedPeekableStream = PeekableStream(parsedList)

    combination = ""

    # This code segment generates a combination string according to the input
    # If an argument is found the method is called on that argument and that argument is checked sperately
    # Otherwise if what you are dealing with is not an argument it just adds the token name to the combination string 
    while parsedPeekableStream.currentElem is not None:
        if parsedPeekableStream.currentElem[0] in "()":
            parsedPeekableStream.nextElem()
        elif parsedPeekableStream.currentElem[0] == "argument":
            combination += "argument"
            checkSyntax((parsedPeekableStream.nextElem())[1])
        else:
            combination += (parsedPeekableStream.nextElem())[0]

    # This is the section which makes sure that one of the combinations is met if that is not the case it raises an exception
    combinationIncorrect = True

    for properCombination in combinations:
        if properCombination == combination:
            combinationIncorrect = False

    if combinationIncorrect:
        raise Exception("SyntaxError")

    return parsedList


# This is probably by far the most complicated method, this is because its job is to convert the disjunctor (u), subjunctor (->) and bi-subjunctor (<->) into nots (¬) ands (^) 
# and ors (v) [Using a complete system of junctors]

def converter(checkedList):
    checkedPeekableStream = PeekableStream(checkedList)

    ret = []

    while checkedPeekableStream.currentElem is not None:
        if checkedPeekableStream.currentElem[0] in "()":
            ret.append(checkedPeekableStream.nextElem())
        
        # The logic found in this elif statement is basicall the same thing as the logic found in the elif statment for when a variable is found
        elif checkedPeekableStream.currentElem[0] == "argument":
            # The argument is kept in temporary vairable
            temp = ("argument", converter(checkedPeekableStream.nextElem()[1]))

            # In this if else if ladder we consider the junctor u, -> and <->
            # If any of these junctors are found they are converted
            # However to do this the second variable is also required
            if checkedPeekableStream.currentElem is not None and checkedPeekableStream.currentElem[0] == "subjunctor":
                ret.append(("argument", [("negator", "¬"), temp]))
                checkedPeekableStream.nextElem()
                ret.append(("adjunctor", "v"))

                # This is used to check what the next element is and handle both possibilies
                # In the case where an argument is found the function converter is called again on the argument
                if checkedPeekableStream.currentElem[0] == "variable":
                    ret.append(checkedPeekableStream.nextElem())
                elif checkedPeekableStream.currentElem[0] == "argument":
                    ret.append(("argument", converter(checkedPeekableStream.nextElem()[1])))

            elif checkedPeekableStream.currentElem is not None and checkedPeekableStream.currentElem[0] == "bi-subjunctor":
                temp2 = ("argument", [("argument", [("(", "("), ("argument", [("negator", "¬"), temp]), ("adjunctor", "v")]), ("conjunctor", "^"), ("argument", [("(", "("), temp, ("adjunctor", "v")])])
                checkedPeekableStream.nextElem()

                # Again it checks what the next element is and handles both possibilities
                # the instructions are a bit more complicated because they are placing the element in the correct position in te temp2 variable
                if checkedPeekableStream.currentElem[0] == "variable":
                    temp3 = checkedPeekableStream.nextElem()
                    temp2[1][0][1].append(temp3)
                    temp2[1][0][1].append((")", ")"))
                    
                    temp2[1][2][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][2][1].append((")", ")"))
                elif checkedPeekableStream.currentElem[0] == "argument":
                    temp3 = ("argument", converter(checkedPeekableStream.nextElem()[1]))
                    temp2[1][0][1].append(temp3)
                    temp2[1][0][1].append((")", ")"))
                    
                    temp2[1][2][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][2][1].append((")", ")"))

                ret.append(temp2)

            # This does the same thing as the bi-subjunctor but for the disjunctor
            elif checkedPeekableStream.currentElem is not None and checkedPeekableStream.currentElem[0] == "disjunctor":
                temp2 = ("argument", [("argument", [("(", "("), temp, ("conjunctor", "^")]), ("adjunctor", "v"), ("argument", [("(", "("), ("argument", [("negator", "¬"), temp]), ("conjunctor", "^")])])
                checkedPeekableStream.nextElem()

                if checkedPeekableStream.currentElem[0] == "variable":
                    temp3 = checkedPeekableStream.nextElem()
                    temp2[1][0][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][0][1].append((")", ")"))
                    
                    temp2[1][2][1].append(temp3)
                    temp2[1][2][1].append((")", ")"))
                elif checkedPeekableStream.currentElem[0] == "argument":
                    temp3 = ("argument", converter(checkedPeekableStream.nextElem()[1]))
                    temp2[1][0][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][0][1].append((")", ")"))
                    
                    temp2[1][2][1].append(temp3)
                    temp2[1][2][1].append((")", ")"))

                ret.append(temp2)
            
            else:
                ret.append(temp)

        elif checkedPeekableStream.currentElem[0] == "variable":
            temp = checkedPeekableStream.nextElem()

            if checkedPeekableStream.currentElem is not None and checkedPeekableStream.currentElem[0] == "subjunctor":
                ret.append(("argument", [("negator", "¬"), temp]))
                checkedPeekableStream.nextElem()
                ret.append(("adjunctor", "v"))

                if checkedPeekableStream.currentElem[0] == "variable":
                    ret.append(checkedPeekableStream.nextElem())
                elif checkedPeekableStream.currentElem[0] == "argument":
                    ret.append(("argument", converter(checkedPeekableStream.nextElem()[1])))

            elif checkedPeekableStream.currentElem is not None and checkedPeekableStream.currentElem[0] == "bi-subjunctor":
                temp2 = ("argument", [("argument", [("(", "("), ("argument", [("negator", "¬"), temp]), ("adjunctor", "v")]), ("conjunctor", "^"), ("argument", [("(", "("), temp, ("adjunctor", "v")])])
                checkedPeekableStream.nextElem()

                if checkedPeekableStream.currentElem[0] == "variable":
                    temp3 = checkedPeekableStream.nextElem()
                    temp2[1][0][1].append(temp3)
                    temp2[1][0][1].append((")", ")"))
                    
                    temp2[1][2][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][2][1].append((")", ")"))
                elif checkedPeekableStream.currentElem[0] == "argument":
                    temp3 = ("argument", converter(checkedPeekableStream.nextElem()[1]))
                    temp2[1][0][1].append(temp3)
                    temp2[1][0][1].append((")", ")"))
                    
                    temp2[1][2][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][2][1].append((")", ")"))

                ret.append(temp2)

            elif checkedPeekableStream.currentElem is not None and checkedPeekableStream.currentElem[0] == "disjunctor":
                temp2 = ("argument", [("argument", [("(", "("), temp, ("conjunctor", "^")]), ("adjunctor", "v"), ("argument", [("(", "("), ("argument", [("negator", "¬"), temp]), ("conjunctor", "^")])])
                checkedPeekableStream.nextElem()

                if checkedPeekableStream.currentElem[0] == "variable":
                    temp3 = checkedPeekableStream.nextElem()
                    temp2[1][0][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][0][1].append((")", ")"))
                    
                    temp2[1][2][1].append(temp3)
                    temp2[1][2][1].append((")", ")"))
                elif checkedPeekableStream.currentElem[0] == "argument":
                    temp3 = ("argument", converter(checkedPeekableStream.nextElem()[1]))
                    temp2[1][0][1].append(("argument", [("negator", "¬"), temp3]))
                    temp2[1][0][1].append((")", ")"))
                    
                    temp2[1][2][1].append(temp3)
                    temp2[1][2][1].append((")", ")"))

                ret.append(temp2)
            
            else:
                ret.append(temp)
                
        else:
            ret.append(checkedPeekableStream.nextElem())

    return ret


# This function basically generates python code which can be executed using the eval function

def genEvalString(convList):
    convPeekableStream = PeekableStream(convList)

    ret = ""

    while convPeekableStream.currentElem is not None:
        if convPeekableStream.currentElem[0] == "argument":
            ret += genEvalString(convPeekableStream.nextElem()[1])
        elif convPeekableStream.currentElem[0] == "variable":
            ret += convPeekableStream.nextElem()[1]
        elif convPeekableStream.currentElem[0] == "negator":
            ret += "not "
            convPeekableStream.nextElem()
        elif convPeekableStream.currentElem[0] == "adjunctor":
            ret += " or "
            convPeekableStream.nextElem()
        elif convPeekableStream.currentElem[0] == "conjunctor":
            ret += " and "
            convPeekableStream.nextElem()
        elif convPeekableStream.currentElem[0] in "()":
            ret += convPeekableStream.nextElem()[1]

    return ret

# This function basically is used to create one big function and return the python executable string along with the number of variables and the variables

def evalLogicExpression(logicExpression):
    tokenList = lexList(logicExpression)

    variableCount = 0
    variables = []

    for token in tokenList:
        if token[0] == "variable" and token[1] not in "".join(variables):
            variableCount += 1
            variables.append(token[1])

    yield variableCount
    yield variables
    yield genEvalString(converter(checkSyntax(parseList(tokenList))))

##################################################################################################################################

# Main Loop

##################################################################################################################################

# This is the main loop

while True:
    temp = list(evalLogicExpression(input("Input logic expression: ")))

    variableCount = temp[0]
    variables = temp[1]
    maskString = temp[2]
    
    print("\n" + maskString + "\n")
    
    # Generates Appropriate Table
    table = createTable(variableCount)
    
    print("Truth Table\n")

    print(variables)
    printTable(table)

    print("\nEvaluated Expression\n")
    
    # For loop which through all the possibilities and calulates the result of each possibility
    for y in range(len(table[0])):
        for x in range(len(table)):
            exec(str(variables[x]) + '=' + str(table[x][y]))

        print(eval(maskString, locals()))

    print()