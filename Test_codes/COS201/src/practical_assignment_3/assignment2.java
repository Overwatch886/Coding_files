import java.util.Scanner;
// My name is Olawuyi Israel Mobolaji
// My Matric number is 250398
// I am in Computer Science Department
public class assignment2{
	public static void main(String[] args){
		Scanner sc = new Scanner(System.in);
		System.out.print("Enter the operation you want to perform (+, -, *, /) : ");
		String operation = sc.nextLine();
		System.out.print("Enter the first number: ");
		int n1 = sc.nextInt();
		System.out.print("Enter the second number: ");
		int n2 = sc.nextInt();
		switch (operation){
		case "+": System.out.println("The result is "+ add(n1,n2)); break;
		case "-": System.out.println("The result is "+ subtract(n1,n2)); break;
		case "*": System.out.println("The result is "+ multiply(n1,n2)); break; 
		case "/": System.out.println("The result is "+ divide(n1,n2)); break;
		default: System.out.println("Invalid Operation!");
		}
	}
	public static int add(int n1, int n2){
		int result = n1+n2;
		return result;
	}
	public static int subtract(int n1, int n2){
		int result = n1-n2;
		return result;
	}
	public static int multiply(int n1, int n2){
		int result = n1*n2;
		return result;
	}
	public static double divide(double n1, double n2){
		double result = n1/n2;
		if (n2==0){
			System.out.println("Error, you can't divide by zero");
			result = Double.NaN;
		}
		
		return result;
	}

}