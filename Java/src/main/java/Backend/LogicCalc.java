package Backend;

import java.util.ArrayList;
import java.util.regex.Pattern;

public class LogicCalc {

	static String completeSubjunctor(String logicChar, PeekableStream peekableStream) {
		var ret = logicChar;

		if (peekableStream.nextElem() == '>') {
			ret += ">";
		}

		// raise Exception("GrammarError")

		return ret;
	}

	static String completeBiSubjunctor(String logicChar, PeekableStream peekableStream) {
		String ret = logicChar;

		if (peekableStream.nextElem() == '-')
			ret += "-";

		if (peekableStream.nextElem() == '>')
			ret += ">";

		return ret;
	}

	/*
	 * 
	 * 
	 * LeXer
	 * 
	 * 
	 */
	public static ArrayList<String[]> lex(String logicExpression) {

		PeekableStream logicPeekableStream = new PeekableStream(logicExpression);
		ArrayList<String[]> lex1 = new ArrayList<String[]>();
		while (logicPeekableStream.currentElem != '\u0000') {

			String logicChar = String.valueOf(logicPeekableStream.nextElem());
			System.out.print(logicChar + " ");

			if (Pattern.matches("[1-9]", logicChar)) {
				lex1.add(new String[] { "variable", logicChar });
			} else if (logicChar.contains("¬")) {
				lex1.add(new String[] { "negator", logicChar }); // negator ==> (not A)
			} else if (logicChar.contains("^")) {
				lex1.add(new String[] { "conjunctor", logicChar }); // negator ==> (not A)
			} else if (logicChar.contains("v")) {
				lex1.add(new String[] { "adjunctor", logicChar }); // negator ==> (not A)
			} else if (logicChar.contains("u")) {
				lex1.add(new String[] { "disjunctor", logicChar }); // negator ==> (not A)
			} else if (logicChar.contains("->")) {
				lex1.add(new String[] { "subjunctor", completeSubjunctor(logicChar, logicPeekableStream) }); // ==>
			} else if (logicChar.contains("<->")) {
				lex1.add(new String[] { "bi-subjunctor", completeBiSubjunctor(logicChar,
						logicPeekableStream) }); /* bi-subjunctor ==> (A and B) or ((not A) and (not B)) */
			} else if (logicChar.contains("(")) {
				lex1.add(new String[] { logicChar, "" });
			} else if (logicChar.contains(")")) {
				lex1.add(new String[] { logicChar, "" });
			}

		}
		return lex1;

	}

	public ArrayList<String[]> lexList(String logicExpression) {

		ArrayList<String[]> lexList = lex(logicExpression);

		int number = 1;

		// # Validation for number ie 1, 2, 3 accepted 1, 2, 4 not accepted

		// for token in lexList:
		for (int i = 0; i < lexList.size(); i++) {
			if (lexList.get(i)[0] == "variable") {
				if (Integer.parseInt(lexList.get(i)[1]) >= number + 1) {
					return null;
				} else {
					number++;
				}
			}
		}
		// if token[0] == "variable":
		// if int(token[1]) >= (number + 1):

		// raise Exception("SyntaxError")
		// else:
		// number += 1

		return lexList; // Array of Array of Strings
	}

	/* 
	 * 
	 * 
	 * End LeXer
	 * 
	 * 
	 * 
	 */
}
