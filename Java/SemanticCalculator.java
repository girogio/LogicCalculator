import java.util.ArrayList;

public class SemanticCalculator {

    Statement s1;
    Statement s2;
    int depth = 0;

    public SemanticCalculator(int depth) {
        this.depth = depth;
        s1 = new Statement(depth);
        s2 = new Statement(depth);
    }

    boolean areSemanticallyEquivalent() {

        if (truthValue(s1.infixStatement).length != truthValue(s2.infixStatement).length) {
            return false;
        } else {
            for (int i = 0; i < truthValue(s1.infixStatement).length; i++) {
                if (truthValue(s1.infixStatement)[i] && !truthValue(s2.infixStatement)[i]) {
                    return false;
                } else if (i == truthValue(s1.infixStatement).length - 1) {
                    System.out.println(s1.infixStatement + " |- " + s2.infixStatement);
                    return true;
                }
            }
        }
        return false;
    }

    boolean[] truthValue(String statement) {
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

    void regenerateStatements() {
        s1 = new Statement(depth);
        s2 = new Statement(depth);
    }

    void outputEquivalence() {
        while (!areSemanticallyEquivalent())
            regenerateStatements();
    }

}
