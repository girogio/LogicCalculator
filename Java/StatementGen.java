
public class StatementGen {

    public static void main(String args[]) {
        Statement s = new Statement(3);
        System.out.println("Prefix notation: " + s.prefixStatement);
    }

}

/*
 * // Creating the Frame JFrame frame = new JFrame("Chat Frame");
 * frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); frame.setSize(400,
 * 400);
 * 
 * // Creating the MenuBar and adding components JMenuBar mb = new JMenuBar();
 * JMenu m1 = new JMenu("File"); JMenu m2 = new JMenu("Help"); mb.add(m1);
 * mb.add(m2); JMenuItem m11 = new JMenuItem("Open"); JMenuItem m22 = new
 * JMenuItem("Save as"); m1.add(m11); m1.add(m22);
 * 
 * // Creating the panel at bottom and adding components JPanel panel = new
 * JPanel(); // the panel is not visible in output JCheckBox orcheck = new
 * JCheckBox("v"); JCheckBox andcheck = new JCheckBox("^"); JCheckBox implcheck
 * = new JCheckBox("->"); JCheckBox biimplcheck = new JCheckBox("<->");
 * panel.add(orcheck); panel.add(andcheck); panel.add(implcheck);
 * panel.add(biimplcheck);
 * 
 * // Text Area at the Center JTextArea ta = new JTextArea();
 * 
 * // Adding Components to the frame.
 * frame.getContentPane().add(BorderLayout.SOUTH, panel);
 * frame.getContentPane().add(BorderLayout.NORTH, mb);
 * frame.getContentPane().add(BorderLayout.CENTER, ta); frame.setVisible(true);
 */
