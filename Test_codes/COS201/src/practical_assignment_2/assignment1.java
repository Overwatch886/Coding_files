// My name is Olawuyi Israel Mobolaji
// My Matric number is 250398
// I am in Computer Science Department
public class assignment1{
	public static void main(String[] args){
		for (double x = -1.0; x<=3.01; x+=0.1){
			// I made the condition for x to be less than or equal to 3.01 because of floating point precison where the computer approximates repeating floating point binary numbers(like 0.00110111) leading to minor decimal additions to the number. This would make the code have something like -3.0001 meaning it ignores 3 inclusive condition
			double y = (x*x) - (3*x) +2;
			System.out.printf("Y(x) is %.2f", y);
			System.out.printf(" when x is %.2f%n", x);
		}
	}
}