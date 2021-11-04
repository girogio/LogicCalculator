import java.util.Random;

class Statement {

    private String[] operators = { "v", "^", "->", "<->" };
    private String[] variables = { "P", "Q", "R" };

    public String statement = "";

    public Statement(int depth) {
        generateStatement(depth);
    }

    // 0: negation + 1 statement
    // 1: operator + 2 statements
    // 2: 1 variable = 1 letter
       public void generateStatement(int depth) {
        if (depth == 1) {
            statement += randomVariable();
            return;
        } else {
            switch (new Random().nextInt(3)) { //ran 0-2
            case 0:
                statement += "7";
                generateStatement(depth - 1);
                break;
            case 1:
                statement += randomOperator();
                generateStatement(depth - 1);
                generateStatement(depth - 1);
                break;
            case 2:
                statement += randomVariable();
                break;
            }
        }
    }
    //Generate random number from 0-3
    private String randomOperator() {
        return operators[new Random().nextInt(operators.length)];
    }
    //Generate random number from 0-2
    private String randomVariable() {
        return variables[new Random().nextInt(variables.length)];
    }

}
