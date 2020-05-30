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
    ret = ["argument", [token]]

    while peekableStream.currentElem is not None and peekableStream.currentElem[0] != ")":
        if peekableStream.currentElem[0] == "(":
            ret[1].append(completeArgument(
                peekableStream.nextElem(), peekableStream))
        else:
            ret[1].append(peekableStream.nextElem())

    if token[0] != "negator":
        ret[1].append(peekableStream.nextElem())

    return ret


def completeNegator(token, peekableStream):
    ret = ["argument", [token]]

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
    "variableconjunctorarguenment",
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


def checkSyntax(parseList):
    parsePeekableStream = PeekableStream(parseList)

    combination = ""

    while parsePeekableStream.currentElem is not None:
        if parsePeekableStream.currentElem[0] in "()":
            parsePeekableStream.nextElem()
        elif parsePeekableStream.currentElem[0] == "argument":
            combination += "argument"
            checkSyntax((parsePeekableStream.nextElem())[1])
        else:
            combination += (parsePeekableStream.nextElem())[0]

        #print(combination)

    combinationIncorrect = True

    for properCombination in combinations:
        #print("For " + properCombination)
        if properCombination == combination:
            combinationIncorrect = False

    if combinationIncorrect:
        raise Exception("SyntaxError")

    return parseList


def breakNegator(peekableStream):
    if peekableStream.nextElem()[0] == "variable":
        peekableStream.prevElem()
        return peekableStream.nextElem()[1]
    elif peekableStream.nextElem()[0] == "argument":
        peekableStream.prevElem()
        return converter(peekableStream.nextElem())


evalString = ""

def converter(parseList):
    global evalString
    parsePeekableStream = PeekableStream(parseList)

    while parsePeekableStream.currentElem is not None:
        if parsePeekableStream.currentElem[0] == "argument":
            converter(parsePeekableStream.nextElem()[1])
        elif parsePeekableStream.currentElem[0] == "adjunctor":
            evalString += " or "
            parsePeekableStream.nextElem()
        elif parsePeekableStream.currentElem[0] == "conjunctor":
            evalString += " and "
            parsePeekableStream.nextElem()
        elif parsePeekableStream.currentElem[0] == "disjunctor":
            pass
        elif parsePeekableStream.currentElem[0] == "subjunctor":
            pass
        elif parsePeekableStream.currentElem[0] == "bi-subjunctor":
            pass
        elif parsePeekableStream.currentElem[0] == "negator":
            evalString += "( not" + converter(parsePeekableStream.nextElem()[1]) + ")"
        elif parsePeekableStream.currentElem[0] == "variable":
            evalString += parsePeekableStream.nextElem()[1]
        elif parsePeekableStream.currentElem[0] == "(":
            evalString += parsePeekableStream.nextElem()[1]
        elif parsePeekableStream.currentElem[0] == ")":
            evalString += parsePeekableStream.nextElem()[1]

        print("Stuck")

while True:
    evalString = ""
    #print(parseList(lexList(input("Enter a logic expression: "))))
    print(checkSyntax(parseList(lexList(input("Enter a logic expression: ")))))
    converter(checkSyntax(parseList(lexList(input("Enter a logic expression: ")))))
    print(evalString)
