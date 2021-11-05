import java.util.ArrayList;
import java.util.HashMap;
import java.util.Stack;
import java.util.regex.Pattern;

public class LogicCalc {

    final private HashMap<String, Integer> precedence = new HashMap<String, Integer>() {{
        put("7", 4);
        put("^", 3);
        put("v", 2);
        put("=>", 1);
        put("<=>", 0);
    }};

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
                tokens.add(completeVar(logicChar, peekExpr)); 
            } else {
                throw new Exception();
            }
        }
        return tokens;
    }

    private boolean comparePrecedence(String token1, String token2) {
        return precedence.get(token1) < precedence.get(token2);
    }

    public ArrayList<String[]> rpn(ArrayList<String[]> tokens) {
        Stack<String[]> oprStack = new Stack<>();
        ArrayList<String[]> outList = new ArrayList<>();

        for(int i = 0; i < tokens.size(); i++) {
            if(tokens.get(i)[0].equals("Var")) {
                outList.add(tokens.get(i));
            } else if(tokens.get(i)[0].equals("Opr")) {
                while(!oprStack.isEmpty() && comparePrecedence(tokens.get(i)[1], oprStack.peek()[1])) {
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

    public void test(String expr1, String expr2) throws Exception {
        boolean result = checkEntailment(rpn(lex(expr1)), rpn(lex(expr2)));
        
        if (result) {
            System.out.println(expr1 + " |- " + expr2);
        } else {
            System.out.println(expr1 + " |/- " + expr2);
        }
    }

    public boolean checkEntailment(ArrayList<String[]> mask1, ArrayList<String[]> mask2) {
        ArrayList<String> varNames = new ArrayList<>();

        for (int i = 0; i < mask1.size(); i++) {
            if (mask1.get(i)[0].equals("Var") && !varNames.contains(mask1.get(i)[1])) {
                varNames.add(mask1.get(i)[1]);
            }
        }

        for (int i = 0; i < mask2.size(); i++) {
            if (mask2.get(i)[0].equals("Var") && !varNames.contains(mask2.get(i)[1])) {
                varNames.add(mask2.get(i)[1]);
            }
        }

        HashMap<String, Boolean[]> combinations = genCombinations(varNames);

        boolean[] result1 = calcTruthTable(mask1, combinations);
        boolean[] result2 = calcTruthTable(mask2, combinations);
        
        for(int i = 0; i < result1.length; i++) {
            if(result1[i] == true && result2[i] == false) {
                return false;
            }
        }

        return true;
    }

    public HashMap<String, Boolean[]> genCombinations(ArrayList<String> varNames) {
        Boolean[][] table = new Boolean[varNames.size()][(int) (Math.pow(2, varNames.size()))];
        HashMap<String, Boolean[]> combinations = new HashMap<>();

        for(int x = 1; x <= varNames.size(); x++) {
            boolean tableValue = false;

            for(int y = 0; y < Math.pow(2, varNames.size()); y++) {
                if(y % (Math.pow(2, varNames.size()) / Math.pow(2, x)) == 0) {
                    tableValue = !tableValue;
                }

                table[x - 1][y] = tableValue;
            }

            combinations.put(varNames.get(x - 1), table[x - 1]);
        }

        return combinations;
    }
    
    public boolean[] calcTruthTable(ArrayList<String[]> mask, HashMap<String, Boolean[]> combinations) {
        boolean[] resultTable = new boolean[(int) (Math.pow(2, combinations.size()))];

        for(int i = 0; i < resultTable.length; i++) {
            ArrayList<String[]> mutMask = new ArrayList<String[]>(mask);

            for(int j = 0; j < mutMask.size(); j++) {
                if(mutMask.get(j)[0].equals("Var")) {
                    mutMask.set(j, new String[] {"Var", String.valueOf(combinations.get(mutMask.get(j)[1])[i])});
                }
            }

            resultTable[i] = rpnCalc(mutMask);
        }

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
}
