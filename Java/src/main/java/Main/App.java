package Main;

import java.util.ArrayList;
import java.util.Scanner;

import Backend.LogicCalc;

public class App {
	static LogicCalc LogicCalc = new LogicCalc();
	static Scanner s = new Scanner(System.in);

	public static void main(String args[]) {
		String a = s.nextLine();
		ArrayList<String[]> f = new ArrayList<String[]>();
		f = LogicCalc.lexList(a);
		for (int i = 0; i < f.size(); i++) {
			for (int j = 0; j < f.get(i).length; j++) {
				System.out.print(f.get(i)[j] + " ");

			}
		}
	}

}
