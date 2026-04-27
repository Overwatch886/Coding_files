// My name is Olawuyi Israel Mobolaji
// My Matric number is 250398
// I am in Computer Science Department
public class assignment4{
	public static void main(String[] args){
			int[] numbers = {4, 6, 10, 3, 9, 8, 1, 2, 7, 5};
			System.out.print("The unsorted array is ");
			for (int num:numbers){
				System.out.print(num+ " ");
			}

			int[] sorted_arr = bubbleSort(numbers);
			printArray(sorted_arr);
	}
	public static int[] bubbleSort(int[] numbers){
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
		return numbers;
	}
		
	public static void printArray(int[] sorted_arr){
		System.out.printf("%n  The sorted array is ");
		for (int num:sorted_arr){
			System.out.print(num+" ");
		}
	}
}
