import java.util.ArrayList;
import java.util.Stack;
import java.util.regex.Pattern;

public class LogicCalculator {

    /*
     * completeSub & completeBiSub are only for the desktop version since on 
     * a mobile phone we can make use of their unicode → and ↔
     */ 

    public String[] completeSub(PeekableStream expr) throws Exception {
        if(expr.nextElem().equals(">")) {
            return new String[] {"Opr", "->"};
        } else {
            throw new Exception();
        }
    }

    public String[] completeBiSub(PeekableStream expr) throws Exception {
        if(expr.nextElem().equals("-") && expr.nextElem().equals(">")) {
            return new String[] {"Opr", "<->"};
        } else {
            throw new Exception();
        }
    }

    public String[] completeVar(String logicChar, PeekableStream expr) throws Exception {
        String varName = logicChar;

        while(expr.currentElem() != null && !Pattern.matches("[ ()vu<^7\\-]", expr.currentElem())) {
            varName += expr.nextElem();
        }

        return new String[] {"Var", varName};
    }

    public ArrayList<String[]> lex(PeekableStream expr) throws Exception {
        ArrayList<String[]> tokens = new ArrayList<String[]>();

        while(expr.currentElem() != null) {
            String logicChar = expr.nextElem();
            System.out.println(logicChar);

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
            } else if(logicChar.equals("-")) {
                tokens.add(completeSub(expr));
            } else if(logicChar.equals("<")) {
                tokens.add(completeBiSub(expr));
            } else if(Pattern.matches("[a-zA-Z]", logicChar)) {
                tokens.add(completeVar(logicChar, expr));
            } else {
                throw new Exception();
            }
        }

        return tokens;
    }

    public ArrayList<String[]> rpn(ArrayList<String[]> tokens) {
        Stack<String[]> oprStack = new Stack<String[]>();
        Stack<String[]> outStack = new Stack<String[]>();

        for(int i = 0; i < tokens.size(); i++) {
            if(tokens.get(i)[0].equals("Var")) {
                outStack.push(tokens.get(i));
            } else if(tokens.get(i)[0].equals("Opr")) {
                while(!oprStack.isEmpty() && oprStack.peek()[1].equals("7")) {
                    outStack.push(oprStack.pop());
                }

                oprStack.push(tokens.get(i));
            } else if(tokens.get(i)[0].equals("(")) {
                oprStack.push(tokens.get(i));
            } else if(tokens.get(i)[0].equals(")")) {
                while(!oprStack.peek()[0].equals("(")) {
                    outStack.push(oprStack.pop());
                }

                oprStack.pop();
            }
        }

        while(!oprStack.isEmpty()) {
            outStack.push(oprStack.pop());
        }

        return new ArrayList<String[]>(outStack);
    }

    
}