public class Assignment3{
	public static void main(String[] args){
		//Changing all letters to lower case
		String name = "Olawuyi Israel Mobolaji".toLowerCase();
		int count = 0;
		for (int i = 0; i < name.length(); i++){
			char ch = name.charAt(i);
			//checking if any lowercase vowel is found at current index in the string
			if (ch=='a'||ch=='e'||ch=='i'||ch=='o'||ch=='u'){
 				count++;
			}
		}
		System.out.println("Count: "+ count);
	}
}