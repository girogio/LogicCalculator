import java.util.ArrayList;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String logicExpression = sc.nextLine();
        PeekableStream expression = new PeekableStream(logicExpression);

        LogicCalculator lc = new LogicCalculator();
        ArrayList<String[]> tokens = new ArrayList<String[]>();

        try {
            tokens = lc.lex(expression);    
        } catch(Exception e) {
            e.printStackTrace();
        }

        // for(int i = 0; i < tokens.size(); i++) {
        //     System.out.println(tokens.get(i)[0] + ", " + tokens.get(i)[1]);
        // }

        ArrayList<String[]> rpn = lc.rpn(tokens);
        // System.out.println();

        for(int i = 0; i < rpn.size(); i++) {
            System.out.print(rpn.get(i)[0] + ", " + rpn.get(i)[1] + " ");
        }

        boolean[][] table = lc.genTable();
        boolean[] table2 = lc.calcTruthTable(rpn);

        System.out.println();

        for(int i = 0; i < table[0].length; i++) {
            for(int j = 0; j < table.length; j++) {
                System.out.print(table[j][i] + ", ");
            }

            System.out.println();
        }

        System.out.println();

        for(int i = 0; i < table2.length; i++) {
            System.out.println(table2[i]);
        }
    }
}