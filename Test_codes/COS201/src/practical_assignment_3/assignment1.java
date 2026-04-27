// My name is Olawuyi Israel Mobolaji
// My Matric number is 250398
// I am in Computer Science Department
import java.util.Scanner;
public class assignment1{
	public static void main(String[] args){
		Scanner sc = new Scanner(System.in);
		System.out.print("Enter the number you want to calculate factorial for: "); 
		// Inputting numbers too larger would create an integer overflow because the result would be too large for the int container
		int n = sc.nextInt(); // n here represents the number whose factorial we want to get
		int _factorial = factorial(n);
		System.out.println("The factorial of "+ n + " is " +_factorial);
		}
	public static int factorial(int n){
		if (n==1 || n==0){
			return 1;
		}
		else{
			return n * factorial(n-1);
		}
	}
}