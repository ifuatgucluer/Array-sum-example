public class ArraySum {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5};
        int total = 0;
        for (int n : numbers) total += n;
        System.out.println(total);
    }
}