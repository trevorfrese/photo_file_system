import java.util.Arrays;

import main.Embed;
import main.Extract;

/*
 * Created on May 18, 2011
 */

/**
 * This is just for having only one class for both, Embed and Extract
 * 
 * @author cgaffga
 */
public class Main {

    /**
     * @param args
     */
    public static void main(final String[] args) {

        if (args.length < 1 || args[0].equals("-h") || args[0].equals("--help")) {
            System.out
                    .println("f5 Usage:  f5 [e|x|-h] [-options] files...\n -e for Embed mode\n -x for eXtract mode\n -h for help");
            System.out.println("\nHelp for embedding:\n");
            Embed.main(new String[0]);
            System.out.println("\n\n----------------------------------\nHelp for extracting:\n\n");
            Extract.main(new String[0]);
            System.out.println("\n\n----------------------------------\nExamples:");
            System.out.println("f5 e -e msg.txt -p mypasswd -q 70 in.jpg out.jpg");
            System.out.println("f5 x -p mypasswd -e out.txt in.jpg");
            System.out.println();
        } else if (args[0].equals("e")) {
            Embed.main(Arrays.copyOfRange(args, 1, args.length));
        } else if (args[0].equals("x")) {
            Extract.main(Arrays.copyOfRange(args, 1, args.length));
        }

    }
}
