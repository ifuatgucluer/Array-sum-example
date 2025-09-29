public class Return {

    public static void guncelle() {
        System.out.println("Guncellendi");
    }

    public static int topla() {
        return 5;
    }

    public static String sehirVer() {
        return "Ankara";
    }

    public static double kareAl(double x) {
        return x * x;
    }

    public static boolean pozitifMi(int sayi) {
        return sayi > 0;
    }

    public static void main(String[] args) {
        guncelle();
        System.out.println("Toplam: " + topla());
        System.out.println("Şehir: " + sehirVer());
        System.out.println("Karesi: " + kareAl(3));
        System.out.println("Pozitif mi: " + pozitifMi(-2));
    }
}
