import java.util.Scanner;
public class Main {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        String sentence = sc.nextLine();
        String [] words = sentence.split(" ");
        for (String word:words){
            if (word=="Water")
            System.out.println("True");
        }
    }
}
