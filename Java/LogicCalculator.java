import java.util.ArrayList;
import java.util.HashMap;
import java.util.Stack;
import java.util.regex.Pattern;

public class LogicCalculator {

    private int varCount = 0;
    private ArrayList<String> varNames = new ArrayList<>();
    private HashMap<String, boolean[]> pointers = new HashMap<>();
    private int BUFFER_SIZE = 0;
    private ArrayList<boolean[]> resultBuffer = new ArrayList<>(); 
    private ArrayList<String> exprBuffer = new ArrayList<>();

    public LogicCalculator(int BUFFER_SIZE) {
        this.BUFFER_SIZE = BUFFER_SIZE;
    }

    public String[] completeSub(PeekableStream expr) throws Exception {
        if(expr.nextElem().equals(">")) {
            return new String[] {"Opr", "=>"};
        } else {
            throw new Exception();
        }
    }

    public String[] completeBiSub(PeekableStream expr) throws Exception {
        if(expr.nextElem().equals("=") && expr.nextElem().equals(">")) {
            return new String[] {"Opr", "<=>"};
        } else {
            throw new Exception();
        }
    }

    public String[] completeVar(String logicChar, PeekableStream expr) throws Exception {
        String varName = logicChar;

        //[ ()vu<^7\\-]
        while(expr.currentElem() != null && !Pattern.matches("[ ()vu<^7=]", expr.currentElem())) {
            varName += expr.nextElem();
        }

        return new String[] {"Var", varName};
    }

    public ArrayList<String[]> lex(String expr) throws Exception {
        PeekableStream peekExpr = new PeekableStream(expr);
        ArrayList<String[]> tokens = new ArrayList<>();

        while(peekExpr.currentElem() != null) {
            String logicChar = peekExpr.nextElem();

            if(logicChar.equals(" ")) {
                // Nothing
            } else if(logicChar.equals("7")) {
                tokens.add(new String[] {"Opr", "7"});
            } else if(logicChar.equals("v")) {
                tokens.add(new String[] {"Opr", "v"});
            } else if(logicChar.equals("^")) {
                tokens.add(new String[] {"Opr", "^"});
            } else if(logicChar.equals("u")) {
                tokens.add(new String[] {"Opr", "u"});
            } else if(logicChar.equals("(")) {
                tokens.add(new String[] {"(", "("});
            } else if(logicChar.equals(")")) {
                tokens.add(new String[] {")", ")"});
            } else if(logicChar.equals("=")) {
                tokens.add(completeSub(peekExpr));
            } else if(logicChar.equals("<")) {
                tokens.add(completeBiSub(peekExpr));
            } else if(Pattern.matches("[a-zA-Z]", logicChar)) {
                String[] varToken = completeVar(logicChar, peekExpr); 
                tokens.add(varToken);

                if(!this.varNames.contains(varToken[1])) {
                    this.varNames.add(varToken[1]);
                    this.varCount++;
                }

            } else {
                throw new Exception();
            }
        }

        if(this.exprBuffer.size() < this.BUFFER_SIZE) {
            this.exprBuffer.add(0, expr);
        } else if(this.exprBuffer.size() == this.BUFFER_SIZE) {
            this.exprBuffer.remove(this.BUFFER_SIZE - 1);
            this.exprBuffer.add(0, expr);
        }

        return tokens;
    }

    public ArrayList<String[]> shuntingYard(ArrayList<String[]> tokens) {
        Stack<String[]> oprStack = new Stack<>();
        ArrayList<String[]> outList = new ArrayList<>();

        for(int i = 0; i < tokens.size(); i++) {
            if(tokens.get(i)[0].equals("Var")) {
                outList.add(tokens.get(i));
            } else if(tokens.get(i)[0].equals("Opr")) {
                while(!oprStack.isEmpty() && oprStack.peek()[1].equals("7")) {
                    outList.add(oprStack.pop());
                }

                oprStack.push(tokens.get(i));
            } else if(tokens.get(i)[0].equals("(")) {
                oprStack.push(tokens.get(i));
            } else if(tokens.get(i)[0].equals(")")) {
                while(!oprStack.peek()[0].equals("(")) {
                    outList.add(oprStack.pop());
                }

                oprStack.pop();
            }
        }

        while(!oprStack.isEmpty()) {
            outList.add(oprStack.pop());
        }

        return outList;
    }

    public boolean[][] genTable() {
        boolean[][] table = new boolean[this.varCount][(int) (Math.pow(2, this.varCount))];
        
        for(int x = 1; x <= this.varCount; x++) {
            boolean tableValue = false;

            for(int y = 0; y < Math.pow(2, this.varCount); y++) {
                if(y % (Math.pow(2, this.varCount) / Math.pow(2, x)) == 0) {
                    tableValue = !tableValue;
                }

                table[x - 1][y] = tableValue;
            }

            this.pointers.put(this.varNames.get(x - 1), table[x - 1]);
        }

        return table;
    }

    public boolean[] calcTruthTable(ArrayList<String[]> mask) {
        boolean[] resultTable = new boolean[(int) (Math.pow(2, this.varCount))];

        for(int i = 0; i < resultTable.length; i++) {
            ArrayList<String[]> mutMask = new ArrayList<>(mask);

            for(int j = 0; j < mutMask.size(); j++) {
                if(mutMask.get(j)[0].equals("Var")) {
                    mutMask.set(j, new String[] {"Var", String.valueOf(this.pointers.get(mutMask.get(j)[1])[i])});
                }
            }

            resultTable[i] = rpnCalc(mutMask);
        }

        if(this.resultBuffer.size() < this.BUFFER_SIZE) {
            this.resultBuffer.add(0, resultTable);
        } else if(this.resultBuffer.size() == this.BUFFER_SIZE) {
            this.resultBuffer.remove(this.BUFFER_SIZE - 1);
            this.resultBuffer.add(0, resultTable);
        }

        resetCalc();

        return resultTable;
    }

    public boolean rpnCalc(ArrayList<String[]> expr) {
        while(expr.size() > 1) {
            int i = 0;

            while(!expr.get(i)[0].equals("Opr") && expr.size() > 1) {
                i++;
            }

            if(expr.get(i)[1].equals("v")) {
                boolean result = Boolean.parseBoolean(expr.get(i - 2)[1]) | Boolean.parseBoolean(expr.get(i - 1)[1]);
                expr.add(i + 1, new String[] {"Var", String.valueOf(result)});
                expr.remove(i);
                expr.remove(i - 1);
                expr.remove(i - 2);
            } else if(expr.get(i)[1].equals("^")) {
                boolean result = Boolean.parseBoolean(expr.get(i - 2)[1]) & Boolean.parseBoolean(expr.get(i - 1)[1]);
                expr.add(i + 1, new String[] {"Var", String.valueOf(result)});
                expr.remove(i);
                expr.remove(i - 1);
                expr.remove(i - 2);
            } else if(expr.get(i)[1].equals("u")) {
                boolean result = Boolean.parseBoolean(expr.get(i - 2)[1]) ^ Boolean.parseBoolean(expr.get(i - 1)[1]);
                expr.add(i + 1, new String[] {"Var", String.valueOf(result)});
                expr.remove(i);
                expr.remove(i - 1);
                expr.remove(i - 2);
            } else if(expr.get(i)[1].equals("<=>")) {
                boolean result = !(Boolean.parseBoolean(expr.get(i - 2)[1]) ^ Boolean.parseBoolean(expr.get(i - 1)[1]));
                expr.add(i + 1, new String[] {"Var", String.valueOf(result)});
                expr.remove(i);
                expr.remove(i - 1);
                expr.remove(i - 2);
            } else if(expr.get(i)[1].equals("=>")) {
                boolean result = !Boolean.parseBoolean(expr.get(i - 2)[1]) | Boolean.parseBoolean(expr.get(i - 1)[1]);
                expr.add(i + 1, new String[] {"Var", String.valueOf(result)});
                expr.remove(i);
                expr.remove(i - 1);
                expr.remove(i - 2);
            } else if(expr.get(i)[1].equals("7")) {
                boolean result = !(Boolean.parseBoolean(expr.get(i - 1)[1]));
                expr.add(i + 1, new String[] {"Var", String.valueOf(result)});
                expr.remove(i);
                expr.remove(i - 1);
            }
        }

        return Boolean.parseBoolean(expr.get(0)[1]);
    }

    public boolean checkImplication(int firstExpr, int secondExpr) {
        boolean[] resultFirst = resultBuffer.get(firstExpr);
        boolean[] resultSecond = resultBuffer.get(secondExpr);

        int lengthFirst = resultBuffer.get(firstExpr).length;
        int lengthSecond = resultBuffer.get(secondExpr).length;

        int lengthMax = (lengthFirst > lengthSecond) ? lengthFirst : lengthSecond;

        for (int i = 0; i < lengthMax; i++) {
            if (resultFirst[i % lengthFirst] == true && resultSecond[i % lengthSecond] == false) {

                System.out.println(exprBuffer.get(firstExpr) + " |/- " + exprBuffer.get(secondExpr) + "\n");
                return false;
            }
        }

        System.out.println(exprBuffer.get(firstExpr) + " |- " + exprBuffer.get(secondExpr) + "\n");

        return true;
    }

    public void printBuffer() {
        for(int i = 0; i < this.resultBuffer.size(); i++) {
            System.out.print((i + 1) + ". " + this.exprBuffer.get(i) + "\n");

            // for(int j = 0; j < this.resultBuffer.get(i).length; j++) {
            //     System.out.print(this.resultBuffer.get(i)[j] + " ");
            // }

            // System.out.println();
        }
    }

    public int bufferSize() {
        return resultBuffer.size();
    }

    public void resetCalc() {
        this.varCount = 0;
        this.varNames.clear();
        this.pointers.clear();
    }

    public void clrBuffer() {
        this.resultBuffer.clear();
        this.exprBuffer.clear();
    }
}