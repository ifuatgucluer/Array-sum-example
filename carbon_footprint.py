#!/usr/bin/env python3

"""

Karbon Ayak İzi Hesaplama Programı (Carbon Footprint Calculator)

Bu program, kullanıcının ulaşım, enerji tüketimi ve atık alışkanlıklarına göre

yıllık karbon ayak izini (ton CO2 eşdeğeri) hesaplar.

"""



def hesapla_ulasim(km_araba, km_ucak, toplu_tasima_saat):
  
    # Katsayılar (kg CO2e birim başına tahmini değerler)
  
    # Araba: ~0.12 kg CO2e / km
  
    # Uçak: ~0.25 kg CO2e / km
  
    # Toplu taşıma: ~0.05 kg CO2e / saat
  
    araba_emisyon = km_araba * 0.12 * 52 # Yıllık (haftalık girildiği varsayılabilir veya yıllık)
  
    ucak_emisyon = km_ucak * 0.25
  
    toplu_emisyon = toplu_tasima_saat * 0.05 * 52
  
    return (araba_emisyon + ucak_emisyon + toplu_emisyon) / 1000.0 # Ton cinsinden
  


def hesapla_enerji(elektrik_kwh, dogalgaz_m3):
  
    # Elektrik: ~0.4 kg CO2e / kWh
  
    # Doğalgaz: ~2.0 kg CO2e / m3
  
    elektrik_emisyon = elektrik_kwh * 0.4 * 12 # Yıllık
  
    dogalgaz_emisyon = dogalgaz_m3 * 2.0 * 12
  
    return (elektrik_emisyon + dogalgaz_emisyon) / 1000.0 # Ton cinsinden
  


def main():
  
    print("=== Karbon Ayak İzi Hesaplama Programına Hoş Geldiniz ===")
  
    try:
      
        # Örnek varsayılan hesaplama veya kullanıcı girdisi
      
        print("Örnek hesaplama çalıştırılıyor...")
      


        # Örnek değerler

        haftalik_araba_km = 100
      
        yillik_ucak_km = 2000
      
        haftalik_toplu_tasima_saat = 5
      
        aylik_elektrik_kwh = 250
      
        aylik_dogalgaz_m3 = 100
      


        ulasim_ton = hesapla_ulasim(haftalik_araba_km, yillik_ucak_km, haftalik_toplu_tasima_saat)
      
        enerji_ton = hesapla_enerji(aylik_elektrik_kwh, aylik_dogalgaz_m3)
      
        toplam_ton = ulasim_ton + enerji_ton
      


        print(f"Ulaşım Kaynaklı Karbon Ayak İzi: {ulasim_ton:.2f} ton CO2e")
      
        print(f"Enerji Kaynaklı Karbon Ayak İzi: {enerji_ton:.2f} ton CO2e")
      
        print(f"Toplam Yıllık Karbon Ayak İzi: {toplam_ton:.2f} ton CO2e")
      


    except Exception as e:
      
        print(f"Bir hata oluştu: {e}")
      


if __name__ == "__main__":
  
    main()
  



































