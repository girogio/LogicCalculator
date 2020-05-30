package Main;

import java.util.ArrayList;
import java.util.Scanner;

import Backend.LexList;
import Backend.Token;

public class App {
	LexList LexList = new LexList();
	static Scanner s = new Scanner(System.in);

	public static void main(String args[]) {
		LexList LexList = new LexList();
		ArrayList<Token> f = new ArrayList<Token>();
		f = LexList.lexList(s.nextLine());
		for (int i = 0; i < f.size(); i++) {
			System.out.print(f.get(i).type + ": " + f.get(i).token + ", ");
		}
	}

}
