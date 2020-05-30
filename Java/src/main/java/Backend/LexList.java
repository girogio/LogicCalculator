package Backend;

import java.util.ArrayList;
import java.util.regex.Pattern;

public class LexList {

	private String completeSubjunctor(String logicChar, PeekableStream peekableStream) {
		var ret = logicChar;

		if (peekableStream.nextElem() == '>') {
			ret += ">";
		}

		// raise Exception("GrammarError")

		return ret;
	}

	private String completeBiSubjunctor(String logicChar, PeekableStream peekableStream) {
		var ret = logicChar;

		if (peekableStream.nextElem() == '-')
			ret += "-";

		if (peekableStream.nextElem() == '>')
			ret += ">";

		return ret;
	}

	// Start leXer

	public ArrayList<Token> lexList(String logicExpression) {

		PeekableStream logicPeekableStream = new PeekableStream(logicExpression);
		int number = 1;
		ArrayList<Token> lex1 = new ArrayList<Token>();
		while (logicPeekableStream.currentElem != '\u0000') {

			String logicChar = String.valueOf(logicPeekableStream.nextElem());
			System.out.print(logicChar + " ");

			if (Pattern.matches("[1-9]", logicChar)) {
				lex1.add(new Token("variable", logicChar));
			} else if (logicChar.contains("¬")) {
				lex1.add(new Token("negator", logicChar)); // negator ==> (not A)
			} else if (logicChar.contains("^")) {
				lex1.add(new Token("conjunctor", logicChar)); // conjunctor ==> A and B
			} else if (logicChar.contains("v")) {
				lex1.add(new Token("adjunctor", logicChar)); // adjunctor ==> A or B
			} else if (logicChar.contains("u")) {
				lex1.add(new Token("disjunctor", logicChar)); // disjunctor ==> (A and (not B)) or ((not B) and A)
			} else if (logicChar.contains("-")) {
				lex1.add(new Token("subjunctor", completeSubjunctor(logicChar, logicPeekableStream)));
			} else if (logicChar.contains("<")) {
				lex1.add(new Token("bi-subjunctor", completeBiSubjunctor(logicChar,
						logicPeekableStream))); /* bi-subjunctor ==> (A and B) or ((not A) and (not B)) */
			} else if (logicChar.contains("(")) {
				lex1.add(new Token(logicChar, ""));
			} else if (logicChar.contains(")")) {
				lex1.add(new Token(logicChar, ""));
			}

		}
		for (int i = 0; i < lex1.size(); i++) {
			if (lex1.get(i).type == "variable") {
				if (Integer.parseInt(lex1.get(i).token) >= number + 1) {
					return null;
				} else {
					number++;
				}
			}
		}
		return lex1;

	}
}
