package Backend;

import java.util.ArrayList;

public class PeekableStream {
	private String stream;
	private int pos = -1;
	private ArrayList<Integer> posStack = new ArrayList<Integer>();
	public char currentElem;

	public PeekableStream(String stream) {
		this.stream = stream;
		this.currentElem = this.stream.toCharArray()[0];
	}

	public char nextElem() {

		if (this.pos < this.stream.length()) {
			this.pos++;
		}
		try {
			return this.stream.toCharArray()[this.pos];
		} catch (ArrayIndexOutOfBoundsException e) {
			this.currentElem = '\u0000';
			return '\u0000';
		}
	}

	public char getCurrentElem() {
		if (this.pos < this.stream.length()) {
			return this.stream.toCharArray()[this.pos];
		}

		return '\u0000';
	}

	public void pushPos() {
		this.posStack.add(this.pos);
	}

	public void popPos() {
		this.currentElem = this.stream.toCharArray()[posStack.size() - 1];
		this.posStack.remove(posStack.size() - 1);
	}
}
