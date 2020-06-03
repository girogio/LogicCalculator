import re
from PeekableStream import PeekableStream

# Truth Table

##################################################################################################################################


def createTable(numVars):  # method araylist<list>
    table = [[0 for y in range(2**numVars)] for x in range(numVars)]

    for x in range(1, numVars + 1):
        val = False

        for y in range(2**numVars):
            if y % (2**numVars / 2**x) == 0:
                val = not val

            table[x - 1][y] = val

    return table


def printTable(table):  # func to print table
    for y in range(len(table[0])):
        for x in range(len(table)):
            print(str(table[x][y]) + " ", end='')

        print()


##################################################################################################################################

# Lexer

##################################################################################################################################


def completeNumber(logicChar, peekableStream, allowed):
    ret = logicChar

    while peekableStream.currentElem is not None and re.match(allowed, peekableStream.currentElem):
        ret += peekableStream.nextElem()

    return ret


def completeSubjunctor(logicChar, peekableStream):
    ret = logicChar

    if peekableStream.nextElem() == ">":
        ret += ">"
    else:
        raise Exception("GrammarError")

    return ret


def completeBiSubjunctor(logicChar, peekableStream):
    ret = logicChar

    if peekableStream.nextElem() == "-":
        ret += "-"
    else:
        raise Exception("GrammarError")

    if peekableStream.nextElem() == ">":
        ret += ">"
    else:
        raise Exception("GrammarError")

    return ret


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
            # disjunctor ==> (A and (not B)) or ((not B) and A)
            yield ("disjunctor", logicChar)
        elif logicChar in "->":
            # subjunctor ==> (not A) or B
            yield ("subjunctor", completeSubjunctor(logicChar, logicPeekableStream))
        elif logicChar in "<->":
            # bi-subjunctor ==> (A and B) or ((not A) and (not B))
            yield ("bi-subjunctor", completeBiSubjunctor(logicChar, logicPeekableStream))
        elif logicChar in "()":
            yield (logicChar, logicChar)
        elif re.match("[1-9]", logicChar):
            yield ("variable", completeNumber(logicChar, logicPeekableStream, "[1-9]"))
        else:
            raise Exception("GrammarError")


def lexList(logicExpression):
    lexList = list(lex(logicExpression))

    number = 1

    for token in lexList:

        if token[0] == "variable":
            if int(token[1]) >= (number + 1):
                raise Exception("SyntaxError")
            else:
                number += 1


    return lexList


##################################################################################################################################

# Parser

##################################################################################################################################

# Thanks to Giorgio for inspiring me to come up with this specific algorithm


def completeArgument(token, peekableStream):
    ret = ("argument", [token])

    while peekableStream.currentElem is not None and peekableStream.currentElem[0] != ")":
        if peekableStream.currentElem[0] == "(":
            ret[1].append(completeArgument(peekableStream.nextElem(), peekableStream))
        elif peekableStream.currentElem[0] == "negator":
            ret[1].append(completeNegator(peekableStream.nextElem(), peekableStream))
        else:
            ret[1].append(peekableStream.nextElem())


    ret[1].append(peekableStream.nextElem())

    return ret


def completeNegator(token, peekableStream):
    ret = ("argument", [token])

    if peekableStream.currentElem[0] == "variable":
        ret[1].append(peekableStream.nextElem())
    elif peekableStream.currentElem[0] == "(":
        ret[1].append(completeArgument(peekableStream.nextElem(), peekableStream))
    else:
        raise Exception("SyntaxError")

    return ret


def parse(peekableTokenTable):
    while peekableTokenTable.currentElem is not None:
        logicToken = peekableTokenTable.nextElem()

        if logicToken[0] == "(":
            yield (completeArgument(logicToken, peekableTokenTable))
        elif logicToken[0] == "negator":
            yield (completeNegator(logicToken, peekableTokenTable))
        elif logicToken[0] == "variable":
            yield logicToken
        elif logicToken[0] == "conjunctor":
            yield logicToken
        elif logicToken[0] == "adjunctor":
            yield logicToken
        elif logicToken[0] == "disjunctor":
            yield logicToken
        elif logicToken[0] == "subjunctor":
            yield logicToken
        elif logicToken[0] == "bi-subjunctor":
            yield logicToken
        else:
            raise Exception("SyntaxError")


def parseList(tokenTable):
    parseList = list(parse(PeekableStream(tokenTable)))
    return parseList


##################################################################################################################################

# Evaluator

##################################################################################################################################


combinations = [
    "argument",
    "negatorargument",
    "argumentconjunctorarguenment",
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


def checkSyntax(parsedList):
    parsedPeekableStream = PeekableStream(parsedList)

    combination = ""

    while parsedPeekableStream.currentElem is not None:
        if parsedPeekableStream.currentElem[0] in "()":
            parsedPeekableStream.nextElem()
        elif parsedPeekableStream.currentElem[0] == "argument":
            combination += "argument"
            checkSyntax((parsedPeekableStream.nextElem())[1])
        else:
            combination += (parsedPeekableStream.nextElem())[0]

    combinationIncorrect = True

    for properCombination in combinations:
        if properCombination == combination:
            combinationIncorrect = False

    if combinationIncorrect:
        raise Exception("SyntaxError")

    return parsedList


def converter(checkedList):
    checkedPeekableStream = PeekableStream(checkedList)

    ret = []

    while checkedPeekableStream.currentElem is not None:
        if checkedPeekableStream.currentElem[0] in "()":
            ret.append(checkedPeekableStream.nextElem())
        elif checkedPeekableStream.currentElem[0] == "argument":
            temp = ("argument", converter(checkedPeekableStream.nextElem()[1]))

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


def evalLogicExpression(logicExpression):
    return genEvalString(converter(checkSyntax(parseList(lexList(logicExpression)))))

##################################################################################################################################

# Main Loop

##################################################################################################################################


def replaceVariables(string, variable, replacer):
    string = list(string)

    for i in range(len(string)):
        if string[i] == variable:
            string[i] = replacer

    return "".join(string)

while True:
    maskString = evalLogicExpression(input("Input logic expression: "))

    variableCount = 0
    
    print("\n" + maskString + "\n")
    
    for c in list(maskString):
        if re.match("[1-9]", c):
            if int(c) > variableCount:
                variableCount = int(c)
    
    table = createTable(variableCount)
    
    print("Truth Table\n")

    printTable(table)

    print("\nEvaluated Expression\n")
    
    for y in range(len(table[0])):
        tempString = maskString
        tempString = list(tempString)
    
        for x in range(len(table)):
            tempString = replaceVariables(tempString, str(x + 1), str(table[x][y]))
    
        print(eval(tempString))

    print()