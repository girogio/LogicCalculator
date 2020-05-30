package Backend;

import java.util.ArrayList;
import java.util.List;

public class Parser {

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

	public ArrayList<LexList> parse(String tokenTable) {

		PeekableStream peekableTokenTable = new PeekableStream(tokenTable);
		ArrayList<LexList>  parsed = new ArrayList<LexList>();
		while (peekableTokenTable.getCurrentElem() != '\u0000') {

			String logicToken = String.valueOf(peekableTokenTable.nextElem());
			System.out.print(logicToken + " ");

			/*if (true) {
				parsed.add(new LexList("variable", logicToken ))
			} else if (logicToken.contains("¬")) {
				parsed.add(new String[] { "negator", logicToken }); // negator ==> (not A)
			} else if (logicToken.contains("^")) {
				parsed.add(new String[] { "conjunctor", logicToken }); // conjunctor ==> A and B
			} else if (logicToken.contains("v")) {
				parsed.add(new String[] { "adjunctor", logicToken }); // adjunctor ==> A or B
			} else if (logicToken.contains("u")) {
				parsed.add(new String[] { "disjunctor", logicToken }); // disjunctor ==> (A and (not B)) or ((not B) and
			} else if (logicToken.contains("-")) {
				parsed.add(new String[] { "subjunctor",  }); // subjunctor
			} else if (logicToken.contains("<")) {
				parsed.add(new String[] { "bi-subjunctor", (logicToken,
						peekableTokenTable) }); // bi-subjunctor ==> (A and B) or ((not A) and (not B)) 
			} else if (logicToken.contains("(")) {
				parsed.add(new String[] { logicToken, "" });
			} else if (logicToken.contains(")")) {
				parsed.add(new String[] { logicToken, "" });
			}*/

		}
		return parsed;

	}

}
