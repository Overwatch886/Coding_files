// My name is Olawuyi Israel Mobolaji
// My Matric number is 250398
// I am in Computer Science Department
import java.util.Scanner;
public class assignment2{
	public static void main(String[] args){
		// Collecting user input for number of iterations to be done
		Scanner sc = new Scanner(System.in);
		System.out.println("Input the number of iteration to be done (the higer the iterations, the higher the accuracy of your Pi value");
		int series_count = sc.nextInt();

		double series = 0;
		// Pi here would be series(result of sums) of the iteration
		for (int n=1; n<=series_count; n++){
			// I noticed that the denominator changes following a specific sequence so I modeled it using the Arithmetic progression formula a+(n-1)d where a=1 and d=2
			double denom_sequence = 1+((n-1)*2);
			// Then I inputed it into the overall series(addition), math.pow is used to change the sign from + to - after every term and the numerator 4 is constant throughout the operation
			series = series + (Math.pow(-1, n-1)*(4/denom_sequence));
			double pi = series;

			System.out.println("The value of pi after " + n + " iterations is " + pi);
		}
	}
}