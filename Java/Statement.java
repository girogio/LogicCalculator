import java.util.Random;

class Statement {

    private String[] operators = { "v", "^", "->", "<->" };
    private String[] variables = { "P", "Q", "R" };

    public String infixStatement = "";

    public Statement(int depth) {
        generateStatement(depth);
    }

    // 0: negation + 1 statement
    // 1: operator + 2 statements
    // 2: 1 variable = 1 letter
    public void generateStatement(int depth) {
        if (depth == 1) {
            infixStatement += randomVariable();
            return;
        } else {
            switch (new Random().nextInt(3)) { // ran 0-2
            case 0:

                infixStatement += "7(";
                generateStatement(depth - 1);
                infixStatement += ")";
                break;
            case 1:
                infixStatement += "(";
                generateStatement(depth - 1);
                infixStatement += randomOperator();
                generateStatement(depth - 1);
                infixStatement += ")";
                break;
            case 2:
                infixStatement += randomVariable();
                break;
            }
        }
    }

    // Generate random number from 0-3
    private String randomOperator() {
        return operators[new Random().nextInt(operators.length)];
    }

    // Generate random number from 0-2
    private String randomVariable() {
        return variables[new Random().nextInt(variables.length)];
    }

}
