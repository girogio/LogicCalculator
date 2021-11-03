import java.util.Random;

public class Operand {
    String value;
    Operand left;
    Operand right;
    static final String[] operators = { "->", "v", "^", "<->" };
    static private final String[] variables = { "P", "Q", "R" };

    public Operand(String value) {
        this.value = value;
        right = null;
        left = null;
    }

    public Operand addOperatorLayer(Operand current, String operator) {

        if (current == null) {
            return new Operand(randomOperator());
        }

        current.left = addOperatorLayer(current.right, randomOperator());
        current.right = addOperatorLayer(current.right, randomOperator());

        return current;
    }

    public Operand addVarLayer(Operand current) {
        if (current.left != null || current.right != null) {
            addVarLayer(current.left);
            addVarLayer(current.right);
        } else {
            current.left = new Operand(randomVariable());
            current.right = new Operand(randomVariable());
        }

        return current;
    }

    public void traverseInOrder(Operand node) {
        if (node != null) {
            traverseInOrder(node.left);
            System.out.print(" " + node.value);
            traverseInOrder(node.right);
        }
    }

    static String randomOperator() {
        return operators[new Random().nextInt(operators.length)];
    }

    static String randomVariable() {
        return variables[new Random().nextInt(variables.length)];
    }
}