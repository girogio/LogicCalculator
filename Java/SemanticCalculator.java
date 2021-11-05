import java.util.ArrayList;

public class SemanticCalculator {

    Statement s1;
    Statement s2;
    int depth;
    int bufferSize;

    public SemanticCalculator(int depth) {
        this.depth = depth;
        s1 = new Statement(depth);
        s2 = new Statement(depth);
    }

    public boolean[] truthValue(String statement) {
        LogicCalculator lc = new LogicCalculator(10);
        ArrayList<String[]> tokens = new ArrayList<String[]>();

        try {
            tokens = lc.lex(statement);
        } catch (Exception e) {
            e.printStackTrace();
        }

        ArrayList<String[]> rpn = lc.shuntingYard(tokens);

        lc.genTable();
        return lc.calcTruthTable(rpn);
    }

    public boolean checkImplication(boolean[] firstExpr, boolean[] secondExpr) {

        int lengthFirst = firstExpr.length;
        int lengthSecond = secondExpr.length;

        int lengthMax = (lengthFirst > lengthSecond) ? lengthFirst : lengthSecond;

        for (int i = 0; i < lengthMax; i++) {
            if (firstExpr[i % lengthFirst] == true && secondExpr[i % lengthSecond] == false) {
                return false;
            }
        }
        return true;
    }

    void regenerateStatements() {
        s1 = new Statement(depth);
        s2 = new Statement(depth);
    }

    void outputEquivalence() {
        while (!checkImplication(truthValue(s1.infixStatement), truthValue(s2.infixStatement)))
            regenerateStatements();

        for (boolean b : truthValue(s1.infixStatement)) {
            System.out.println(b);
        }

        System.out.println();
        for (boolean b : truthValue(s2.infixStatement)) {
            System.out.println(b);
        }
        System.out.println(s1.infixStatement + "  |-    " + s2.infixStatement);
    }

}
