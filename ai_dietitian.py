#!/usr/bin/env python3

"""

Sistematize Edilmiş Yapay Zeka Diyetisyen (Systematized AI Dietitian)

Bu betik; kullanıcının yaş, cinsiyet, boy, kilo, aktivite düzeyi ve hedeflerini alarak

bazal metabolizma hızı (BMR) ve günlük kalori ihtiyacını (TDEE) matematiksel olarak hesaplar,

ardından OpenAI API kullanarak kişiselleştirilmiş 3 günlük örnek diyet ve beslenme programı üretir.

"""



import os

from openai import OpenAI



class AIDietitian:
  
    def __init__(self, age, gender, weight_kg, height_cm, activity_level, goal):
      
        self.age = age
      
        self.gender = gender.lower()
      
        self.weight = weight_kg
      
        self.height = height_cm
      
        self.activity_level = activity_level.lower()
      
        self.goal = goal.lower()
      


    def calculate_bmr(self):
      
        """Harris-Benedict denklemi kullanarak Bazal Metabolizma Hızı (BMR) hesaplar."""
      
        if self.gender == 'erkek':
          
            bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
          
        else:
          
            bmr = 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)
          
        return bmr
      


    def calculate_tdee(self):
      
        """Aktivite çarpanına göre Toplam Günlük Enerji Harcamasını (TDEE) hesaplar."""
      
        bmr = self.calculate_bmr()
      
        multipliers = {
          
            'sedanter': 1.2,
          
            'hafif': 1.375,
          
            'orta': 1.55,
          
            'aktif': 1.725,
          
            'cok_aktif': 1.9
          
        }
      
        mult = multipliers.get(self.activity_level, 1.2)
      
        tdee = bmr * mult
      


        # Hedefe göre kalori ayarlaması

        if 'kilo_verme' in self.goal:
          
            target_calories = tdee - 500  # Kalori açığı
          
        elif 'kilo_alma' in self.goal:
          
            target_calories = tdee + 500  # Kalori fazlası
          
        else:
          
            target_calories = tdee        # Kilo koruma
          


        return int(bmr), int(tdee), int(target_calories)
      


    def generate_diet_plan(self):
      
        """OpenAI API kullanarak kişiselleştirilmiş diyet planı oluşturur."""
      
        bmr, tdee, target_calories = self.calculate_tdee()
      


        prompt = f"""
        
        Sen profesyonel, klinik bir diyetisyensin. Aşağıdaki verilere sahip danışan için sistematik ve bilimsel bir beslenme programı hazırla:
        
        - Yaş: {self.age}
        
        - Cinsiyet: {self.gender}
        
        - Boy: {self.height} cm
        
        - Kilo: {self.weight} kg
        
        - Aktivite Düzeyi: {self.activity_level}
        
        - Hedef: {self.goal}
        
        - Hesaplanan BMR: {bmr} kcal
        
        - Hesaplanan Günlük Kalori Hedefi: {target_calories} kcal
        

        
        Lütfen şunları içeren Türkçe bir program hazırla:
        
        1. Günlük kalori ve makro besin (protein, karbonhidrat, yağ) dağılımı.
        
        2. 3 günlük örnek öğün planı (Kahvaltı, Ögle, Akşam, Ara Öğün).
        
        3. Danışana özel beslenme ve hidrasyon tavsiyeleri.
        
        """
      


        try:
          
            client = OpenAI()
          
            response = client.chat.completions.create(
              
                model="gpt-4o-mini",
              
                messages=[
                  
                    {"role": "system", "content": "Sen alanında uzman, bilimsel temelli çalışan kıdemli bir diyetisyensin."},
                  
                    {"role": "user", "content": prompt}
                  
                ],
              
                temperature=0.7,
              
                max_tokens=1000
              
              ]
              
            return response.choices[0].message.content
          
        except Exception as e:
          
            return f"Yapay zeka diyet planı oluşturulurken bir hata oluştu: {str(e)}"
          


def main():
  
    print("=== Sistematik Yapay Zeka Diyetisyen Sistemi ===")
  


    # Örnek Danışan Profili

    danisan = AIDietitian(
      
        age=28,
      
        gender="kadin",
      
        weight_kg=68,
      
        height_cm=165,
      
        activity_level="orta",
      
        goal="kilo_verme"
      
    )



    bmr, tdee, target = danisan.calculate_tdee()

    print(f"\\n[Hesaplanan Metabolik Veriler]")

    print(f"- Bazal Metabolizma (BMR): {bmr} kcal")

    print(f"- Günlük Kalori İhtiyacı (TDEE): {tdee} kcal")

    print(f"- Hedeflenen Günlük Kalori: {target} kcal\\n")



    print("Yapay Zeka Diyetisyen kişiselleştirilmiş programı hazırlıyor...\\n")

    plan = danisan.generate_diet_plan()



    print("--- Kişiselleştirilmiş Beslenme Planı ---")

    print(plan)

    print("---------------------------------------")



if __name__ == "__main__":
  
    main()
  














































































