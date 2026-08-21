#!/usr/bin/env python3

"""

Yapay Zeka Destekli Kişiselleştirilmiş Gelecek Sağlık Tahmin ve Önleyici Tıp Sistemi

(AI-Powered Personalized Future Health Prediction & Preventive Medicine System)



Geleceğin sağlık teknolojilerini simüle eden bu sistem; bireylerin genetik eğilimlerini,

yaşam tarzı verilerini, beslenme ve uyku alışkanlıklarını yapay zeka ile analiz ederek

gelecekteki olası sağlık risklerini önceden öngörür, koruyucu tıp önerileri sunar

ve kritik risk durumlarında sağlık birimlerine / kullanıcılara otomatik e-posta raporu gönderir.

"""



import os

import logging

from typing import List, Dict, Any

from dataclasses import dataclass

from openai import OpenAI



# Loglama yapılandırması

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')



@dataclass

class HealthProfile:
  
    patient_id: str
  
    full_name: str
  
    email: str
  
    age: int
  
    genetic_risk_factors: List[str]
  
    lifestyle_habits: Dict[str, Any]
  
    biometrics: Dict[str, float]
  


class HealthNotificationService:
  
    """Sağlık uyarıları ve koruyucu tıp raporlarını ilgili birimlere ileten e-posta servis simülasyonu."""
  


    def __init__(self, medical_team_email: str = "preventive.medicine@saglik-ai.com"):
      
        self.medical_team_email = medical_team_email
      


    def send_health_alert(self, subject: str, report_body: str, recipient_email: str):
      
        """Sağlık analiz raporunu ve acil uyarıları simüle eder."""
      
        logging.info(f"[SAĞLIK BİLDİRİMİ] Alıcı: {recipient_email} | Konu: {subject}")
      
        logging.info(f"--- Koruyucu Sağlık Raporu ---\n{report_body}\n------------------------------")
      
        print(f"\n[SİSTEM UYARISI]: '{subject}' konulu gelecek sağlık raporu {recipient_email} adresine iletildi.\n")
      


class AIFutureHealthPredictor:
  
    def __init__(self, system_name: str):
      
        self.system_name = system_name
      
        self.client = OpenAI()
      
        self.notifier = HealthNotificationService()
      


    def predict_health_trajectory(self, profile: HealthProfile) -> Dict[str, Any]:
      
        """Yapay zeka modelleri ile bireyin gelecekteki sağlık risklerini ve önleyici tıp yol haritasını çıkarır."""
      
        logging.info(f"Sağlık Analizi Çalıştırılıyor -> Hasta ID: {profile.patient_id}, İsim: {profile.full_name}")
      


        prompt = f"""
        
Sen "{self.system_name}" platformunun Kıdemli Yapay Zeka Tıbbi Veri Analisti ve Önleyici Tıp Uzmanısın.

Geleceğin sağlık teknolojilerini kullanarak, aşağıdaki bireyin biyometrik verilerini, genetik risklerini ve yaşam tarzını analiz et:



--- HASTA PROFİLİ ---

ID: {profile.patient_id}

Ad Soyad: {profile.full_name}

Yaş: {profile.age}

Genetik Risk Faktörleri: {', '.join(profile.genetic_risk_factors)}

Yaşam Tarzı Alışkanlıkları: {profile.lifestyle_habits}

Biyometrik Veriler: {profile.biometrics}



Lütfen analizinizi şu formatta detaylı olarak yap:

1. Gelecek Sağlık Risk Skoru (Future Risk Score): [0 - 100 arası genel risk puanı]

2. Olası Sağlık Tehditleri (5 Yıllık Projeksiyon): Önümüzdeki dönemde karşılaşabileceği kronik veya metabolik riskler.

3. Önleyici Tıp ve Yaşam Tarzı Stratejisi: Riskleri sıfırlamak veya minimize etmek için yapılması gerekenler (Beslenme, Egzersiz, Uyku).

4. Öngörücü Biyobelirteç Takibi (Predictive Biomarkers): Düzenli olarak takip edilmesi gereken kritik kan ve laboratuvar değerleri.

5. Klinik Aksiyon Planı: Sağlık ekibi ve birey için acil alınması gereken önlemler.

"""



        try:
        
            response = self.client.chat.completions.create(
            
                model="gpt-4o-mini",
                
                messages=[
                
                    {"role": "system", "content": "Sen geleceğin önleyici tıp ve yapay zeka destekli sağlık analitiği sistemisin."},
                    
                    {"role": "user", "content": prompt}
                    
                ],
                
                temperature=0.3,
                
                max_tokens=900
                
            )
            
            analysis_result = response.choices[0].message.content
            

            
            # Yüksek risk tespit edildiğinde otomatik e-posta bildirimi gönder
            
            if "yüksek risk" in analysis_result.lower() or "dikkat" in analysis_result.lower() or "70" in analysis_result:
            
                subject = f"GELECEK SAĞLIK UYARISI & ÖNLEYİCİ RAPOR - {profile.full_name}"
                
                self.notifier.send_health_alert(subject, analysis_result, profile.email)
                


            return {
            
                "patient_id": profile.patient_id,
                
                "status": "Gelecek Sağlık Analizi Tamamlandı",
                
                "health_report": analysis_result
                
            }
            
        except Exception as e:
        
            logging.error(f"AI Sağlık Analiz Hatası: {str(e)}")
            
            return {"patient_id": profile.patient_id, "status": "Hata", "error": str(e)}
            


def main():

    print("=== Yapay Zeka Destekli Kişiselleştirilmiş Gelecek Sağlık Tahmin ve Önleyici Tıp Sistemi ===\n")
    

    
    predictor = AIFutureHealthPredictor(
    
        system_name="OmniHealth AI 2030"
        
    )
    


    # Örnek Hasta Profili (Gelecek Vizyonu)
    
    sample_patient = HealthProfile(
    
        patient_id="PAT-9090",
        
        full_name="Canan Öztürk",
        
        email="canan.ozturk@example.com",
        
        age=42,
        
        genetic_risk_factors=["Tip 2 Diyabet Eğilimi", "Kardiyovasküler Hassasiyet"],
        
        lifestyle_habits={
        
            "daily_sitting_hours": 9,
            
            "sleep_hours_average": 5.5,
            
            "diet_type": "Yüksek Karbonhidrat / Fast-Food",
            
            "exercise_frequency": "Haftada 0 gün"
            
        },
        
        biometrics={
        
            "fasting_glucose": 108.5,
            
            "cholesterol_ldl": 152.0,
            
            "blood_pressure_systolic": 135.0,
            
            "bmi": 28.4
            
        }
        
    )
    


    print(f"\n--- Gelecek Sağlık Simülasyonu Çalıştırılıyor: {sample_patient.full_name} ---")
    
    result = predictor.predict_health_trajectory(sample_patient)
    
    print(result["health_report"])
    
    print("-" * 65)
    


if __name__ == "__main__":

    main()
    
















































































