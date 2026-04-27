// My name is Olawuyi Israel Mobolaji
// My Matric number is 250398
// I am in Computer Science Department
public class assignment3{
	// Setting the constant values
	static final double I0 = 2.0 * Math.pow(10, -6);
	static final double q = 1.602 * Math.pow(10, -19);
	static final double k = 1.38 * Math.pow(10, -23);
	public static void main(String[] args){
		// ID = diode current (Amperes)
		// VD = diode voltage (Volts)
		// I0 = 2.0 × 10−6 A
		// q = 1.602 × 10−19 C
		// k = 1.38 × 10−23 J/K
		// T = temperature (Kelvin)
		double ID;
		double VD;
		// Putting all the temperature(in F) values we are testing with in an array
		int temps_in_f[] = {75, 100, 125};
		// Using each temperature in F one after the other
		for (int temp_in_f:temps_in_f){
			System.out.println("These are the diode current values when F is "+ temp_in_f + "°F");
			double temp_in_c = (5.0/9) * (temp_in_f-32);
			double T = temp_in_c+273.15; // This is the temperature value in kelvin		
			for (VD= -1.0; VD<=0.7; VD+=0.1){
				ID = I0*(Math.pow((Math.E), (q*VD)/(k*T)) -1); //This is the formula
				System.out.printf("When Diode Voltage is %.2f", VD );
				System.out.printf(" V and temperature is %.2f", T );
				System.out.println(" K, We have a Diode Current of "+ ID + " A");
			}
		}
	}
}
		