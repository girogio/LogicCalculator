import java.util.ArrayList;
import java.util.Iterator;

public class PeekableStream {

    private Iterator<String> stream;
    private String currentElem;
    private boolean reachedEnd = false;

    public PeekableStream(String string) {
        ArrayList<String> characters = new ArrayList<String>();

        for(int i = 0; i < string.length(); i++) {
            characters.add(String.valueOf(string.charAt(i)));
        }

        this.stream = characters.iterator();
        try {nextElem(); } catch(Exception e) {e.printStackTrace(); }
    }

    public String nextElem() throws Exception {
        String ret = this.currentElem;

        if(this.stream.hasNext()) {
            this.currentElem = this.stream.next();
        } else if(!this.reachedEnd) {
            this.currentElem = null;
            this.reachedEnd = true;
        } else {
            throw new Exception();
        }

        return ret;
    }

    public String currentElem() {
        return this.currentElem;
    }
}