// My name is Olawuyi Israel Mobolaji
// My Matric number is 250398
// I am in Computer Science Department
public class assignment3{
	public static void main(String[] args){
		int[] numbers = {5, 7, 2, 1, 8, 9, 3, 10, 6, 4};
		System.out.print("The unsorted array is ");
		for (int num:numbers){
			System.out.print(num+ " ");
		}

		int size = numbers.length;
		for (int i=0; i<=size-1; i++){
			for (int j=0; j<=size-i-2; j++){
				if (numbers[j] > numbers[j+1]){
					// Swapping the positons
					int holder = numbers[j];
					numbers[j] = numbers[j+1];
					numbers[j+1] = holder;
				}
			}
		}
		System.out.printf("%n  The sorted array is ");
		for (int num:numbers){
			System.out.print(num+" ");
		}
	}
}
				