import java.util.ArrayList;
import java.util.HashMap;
import java.util.Stack;
import java.util.regex.Pattern;

public class LogicCalculator {

    /*
     * completeSub & completeBiSub are only for the desktop version since on a
     * mobile phone we can make use of their unicode → and ↔
     */

    private int varCount = 0;
    private ArrayList<String[]> varNames = new ArrayList<>();
    private HashMap<String, boolean[]> pointers = new HashMap<>();

    public String[] completeSub(PeekableStream expr) throws Exception {
        if (expr.nextElem().equals(">")) {
            return new String[] { "Opr", "->" };
        } else {
            throw new Exception();
        }
    }

    public String[] completeBiSub(PeekableStream expr) throws Exception {
        if (expr.nextElem().equals("-") && expr.nextElem().equals(">")) {
            return new String[] { "Opr", "<->" };
        } else {
            throw new Exception();
        }
    }

    public String[] completeVar(String logicChar, PeekableStream expr) throws Exception {
        String varName = logicChar;

        while (expr.currentElem() != null && !Pattern.matches("[ ()vu<^7\\-]", expr.currentElem())) {
            varName += expr.nextElem();
        }

        return new String[] { "Var", varName };
    }

    public ArrayList<String[]> lex(PeekableStream expr) throws Exception {
        ArrayList<String[]> tokens = new ArrayList<>();

        while (expr.currentElem() != null) {
            String logicChar = expr.nextElem();
            // System.out.println(logicChar);

            if (logicChar.equals(" ")) {
                // Nothing
            } else if (logicChar.equals("7")) {
                tokens.add(new String[] { "Opr", "7" });
            } else if (logicChar.equals("v")) {
                tokens.add(new String[] { "Opr", "v" });
            } else if (logicChar.equals("^")) {
                tokens.add(new String[] { "Opr", "^" });
            } else if (logicChar.equals("u")) {
                tokens.add(new String[] { "Opr", "u" });
            } else if (logicChar.equals("(")) {
                tokens.add(new String[] { "(", "(" });
            } else if (logicChar.equals(")")) {
                tokens.add(new String[] { ")", ")" });
            } else if (logicChar.equals("-")) {
                tokens.add(completeSub(expr));
            } else if (logicChar.equals("<")) {
                tokens.add(completeBiSub(expr));
            } else if (Pattern.matches("[a-zA-Z]", logicChar)) {
                String[] varName = completeVar(logicChar, expr);
                tokens.add(varName);

                boolean duplicate = false;

                for (int i = 0; i < this.varNames.size(); i++) {
                    if (this.varNames.get(i)[1].equals(varName[1])) {
                        duplicate = true;
                        break;
                    }
                }

                if (!duplicate) {
                    this.varNames.add(varName);
                    this.varCount++;
                }

            } else {
                throw new Exception();
            }
        }

        return tokens;
    }

    public ArrayList<String[]> rpn(ArrayList<String[]> tokens) {
        Stack<String[]> oprStack = new Stack<>();
        Stack<String[]> outStack = new Stack<>();

        for (int i = 0; i < tokens.size(); i++) {
            if (tokens.get(i)[0].equals("Var")) {
                outStack.push(tokens.get(i));
            } else if (tokens.get(i)[0].equals("Opr")) {
                while (!oprStack.isEmpty() && oprStack.peek()[1].equals("7")) {
                    outStack.push(oprStack.pop());
                }

                oprStack.push(tokens.get(i));
            } else if (tokens.get(i)[0].equals("(")) {
                oprStack.push(tokens.get(i));
            } else if (tokens.get(i)[0].equals(")")) {
                while (!oprStack.peek()[0].equals("(")) {
                    outStack.push(oprStack.pop());
                }

                oprStack.pop();
            }
        }

        while (!oprStack.isEmpty()) {
            outStack.push(oprStack.pop());
        }

        return new ArrayList<String[]>(outStack);
    }

    public boolean[][] genTable() {
        boolean[][] table = new boolean[this.varCount][(int) (Math.pow(2, this.varCount))];

        for (int x = 1; x <= this.varCount; x++) {
            boolean tableValue = false;

            for (int y = 0; y < Math.pow(2, this.varCount); y++) {
                if (y % (Math.pow(2, this.varCount) / Math.pow(2, x)) == 0) {
                    tableValue = !tableValue;
                }

                table[x - 1][y] = tableValue;
            }

            this.pointers.put(this.varNames.get(x - 1)[1], table[x - 1]);
        }

        return table;
    }

    public boolean[] calcTruthTable(ArrayList<String[]> mask) {
        boolean[] resultTable = new boolean[(int) (Math.pow(2, this.varCount))];

        for (int i = 0; i < resultTable.length; i++) {
            ArrayList<String[]> mutMask = new ArrayList<>(mask);

            for (int j = 0; j < mutMask.size(); j++) {
                if (mutMask.get(j)[0].equals("Var")) {
                    mutMask.set(j, new String[] { "Var", String.valueOf(this.pointers.get(mutMask.get(j)[1])[i]) });
                }

                // System.out.println("{" + mutMask.get(j)[0] + ", " + mutMask.get(j)[1] + "}
                // ");
            }

            resultTable[i] = rpnCalc(mutMask);

            System.out.println();
        }

        return resultTable;
    }

    public boolean rpnCalc(ArrayList<String[]> expr) {
        while (expr.size() > 1) {
            int i = 0;

            while (!expr.get(i)[0].equals("Opr") && expr.size() > 1) {
                i++;
            }

            if (expr.get(i)[1].equals("v")) {
                boolean result = Boolean.parseBoolean(expr.get(i - 2)[1]) | Boolean.parseBoolean(expr.get(i - 1)[1]);
                expr.add(i + 1, new String[] { "Var", String.valueOf(result) });
                expr.remove(i);
                expr.remove(i - 1);
                expr.remove(i - 2);
            } else if (expr.get(i)[1].equals("^")) {
                boolean result = Boolean.parseBoolean(expr.get(i - 2)[1]) & Boolean.parseBoolean(expr.get(i - 1)[1]);
                expr.add(i + 1, new String[] { "Var", String.valueOf(result) });
                expr.remove(i);
                expr.remove(i - 1);
                expr.remove(i - 2);
            } else if (expr.get(i)[1].equals("u")) {
                boolean result = Boolean.parseBoolean(expr.get(i - 2)[1]) ^ Boolean.parseBoolean(expr.get(i - 1)[1]);
                expr.add(i + 1, new String[] { "Var", String.valueOf(result) });
                expr.remove(i);
                expr.remove(i - 1);
                expr.remove(i - 2);
            } else if (expr.get(i)[1].equals("<->")) {
                boolean result = !(Boolean.parseBoolean(expr.get(i - 2)[1]) ^ Boolean.parseBoolean(expr.get(i - 1)[1]));
                expr.add(i + 1, new String[] { "Var", String.valueOf(result) });
                expr.remove(i);
                expr.remove(i - 1);
                expr.remove(i - 2);
            } else if (expr.get(i)[1].equals("->")) {
                boolean result = !Boolean.parseBoolean(expr.get(i - 2)[1]) | Boolean.parseBoolean(expr.get(i - 1)[1]);
                expr.add(i + 1, new String[] { "Var", String.valueOf(result) });
                expr.remove(i);
                expr.remove(i - 1);
                expr.remove(i - 2);
            } else if (expr.get(i)[1].equals("7")) {
                boolean result = !(Boolean.parseBoolean(expr.get(i - 1)[1]));
                expr.add(i + 1, new String[] { "Var", String.valueOf(result) });
                expr.remove(i);
                expr.remove(i - 1);
            }
        }

        return Boolean.parseBoolean(expr.get(0)[1]);
    }

    public void resetCalc() {
        this.varCount = 0;
        this.varNames.clear();
        this.pointers.clear();
    }
}