import java.util.ArrayList;
import java.util.InputMismatchException;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        System.out.println("\n");

        boolean debug = false;

        if (args.length >= 1 && args[0].equals("debug")) {
            debug = true;
        }

        Scanner sc = new Scanner(System.in);
        LogicCalculator lc = new LogicCalculator(10);

        while (true) {
            System.out.print("1. Calculate Truth Table\n2. Help\n3. Check Implication\n4. Exit\n<< ");
            int option = 0;

            try {
                option = sc.nextInt();
                System.out.println();
                sc.nextLine();

                if (option == 2) {
                    System.out.println("v - adjunctor");
                    System.out.println("^ - conjunctor");
                    System.out.println("u - disjunctor");
                    System.out.println("-> - subjunctor");
                    System.out.println("<-> - bi-subjunctor");
                    System.out.println("7 - negator\n");
                }

                if (option == 4) {
                    System.out.println("Thanks!");
                    break;
                }

                if (option < 1 || option > 4 /* 5 */) {
                    System.out.println("Invalid");
                    continue;
                }

            } catch (InputMismatchException e) {
                sc.next();
                e.printStackTrace();
            }

            if (option == 1) {
                System.out.print("Input logic expression: ");
                String logicExpression = sc.nextLine();

                // if(logicExpression.equals("stop")) {
                // System.out.println("Thank You!");
                // break;
                // }

                ArrayList<String[]> tokens = new ArrayList<String[]>();

                try {
                    tokens = lc.lex(logicExpression);
                } catch (Exception e) {
                    e.printStackTrace();
                }

                if (debug == true) {
                    System.out.println("Tokens: \n");

                    for (int i = 0; i < tokens.size(); i++) {
                        System.out.print("{" + tokens.get(i)[0] + ", " + tokens.get(i)[1] + "} ");
                    }

                    System.out.println("\n");
                }

                ArrayList<String[]> rpn = lc.shuntingYard(tokens);

                if (debug == true) {
                    System.out.println("RPN Expression: \n");

                    for (int i = 0; i < rpn.size(); i++) {
                        System.out.print(rpn.get(i)[0] + ", " + rpn.get(i)[1] + " ");
                    }

                    System.out.println("\n");
                }

                boolean[][] table = lc.genTable();
                boolean[] resultTable = lc.calcTruthTable(rpn);

                System.out.println("\nCombinations of Junctions:\n");

                for (int i = 0; i < table[0].length; i++) {
                    for (int j = 0; j < table.length; j++) {
                        System.out.print(table[j][i] + ", ");
                    }

                    System.out.println();
                }

                System.out.println("\nResult:\n");

                for (int i = 0; i < resultTable.length; i++) {
                    System.out.println(resultTable[i]);
                }

                System.out.println("\nBuffer:\n");

                lc.printBuffer();

                System.out.println();

            } else if (option == 3) {
                lc.printBuffer();

                /*
                 * TODO: Implement a try-catch block for better error handling
                 */

                int firstExpr;
                int secondExpr;

                try {
                    System.out.print("Enter first expresssion: ");
                    firstExpr = sc.nextInt();

                    System.out.print("Enter second expression: ");
                    secondExpr = sc.nextInt();

                    if ((firstExpr < 1 || firstExpr > lc.bufferSize()) || (secondExpr < 1 || secondExpr > lc.bufferSize())) {
                        System.out.println("Input must between 1  and " + lc.bufferSize() + " (inclusive).");
                        continue;
                    }

                    System.out.println();
                    lc.checkImplication(firstExpr - 1, secondExpr - 1);
                
                } catch(InputMismatchException e) {
                    e.printStackTrace();
                }
            }

        }

        sc.close();
    }
}
