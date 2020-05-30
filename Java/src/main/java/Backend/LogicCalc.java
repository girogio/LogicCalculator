package Backend;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

public class LogicCalc {

	String completeSubjunctor(String logicChar, PeekableStream peekableStream) {
		var ret = logicChar;

		if (peekableStream.nextElem() == '>') {
			ret += ">";
		}

		// raise Exception("GrammarError")

		return ret;
	}

	String completeBiSubjunctor(String logicChar, PeekableStream peekableStream) {
		String ret = logicChar;

		if (peekableStream.nextElem() == '-')
			ret += "-";

		if (peekableStream.nextElem() == '>')
			ret += ">";

		return ret;
	}

	// Start leXer

	public ArrayList<String[]> lex(String logicExpression) {

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
				lex1.add(new String[] { "conjunctor", logicChar }); // conjunctor ==> A and B
			} else if (logicChar.contains("v")) {
				lex1.add(new String[] { "adjunctor", logicChar }); // adjunctor ==> A or B
			} else if (logicChar.contains("u")) {
				lex1.add(new String[] { "disjunctor", logicChar }); // disjunctor ==> (A and (not B)) or ((not B) and A)
			} else if (logicChar.contains("-")) {
				lex1.add(new String[] { "subjunctor", completeSubjunctor(logicChar, logicPeekableStream) }); // subjunctor
																												// ==>
																												// (not
																												// A) or
																												// B
			} else if (logicChar.contains("<")) {
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

	// End leXer

	// Start parSer
	public List<String> completeArgument(String token, PeekableStream peekableStream) {
		List<String> tokens = new ArrayList<String>();
		while (peekableStream.currentElem != '\u0000' && peekableStream.getCurrentElem() != ')') {
			if (peekableStream.getCurrentElem() == ')') {
				tokens.add(completeArgument(String.valueOf(peekableStream.nextElem()), peekableStream).get(1));

			} else {
				tokens.add(String.valueOf(peekableStream.nextElem()));
			}

		}

		return tokens;

	}
}
