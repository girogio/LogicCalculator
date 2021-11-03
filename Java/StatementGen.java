public class StatementGen{

    public static void main(String args[]){
        Operand o = new Operand("v");
        o.addOperatorLayer(o, "");
        o.addVarLayer(o);
        o.traverseInOrder(o);
    }
}
