#!/usr/bin/env python3

"""

Yapay Zeka Destekli Akıllı Siber Güvenlik ve Tehdit Tespit Sistemi

(AI-Powered Cyber Threat Detection & Automated Incident Response System)



Bu sistem; sunucu loglarını ve ağ trafik verilerini yapay zeka ile analiz ederek

olasılık bazlı siber saldırı girişimlerini (Brute Force, SQLi, DDoS, Anomali) tespit eder,

tehdit seviyesi (Risk Score) atar ve SOC (Security Operations Center) ekibine

otomatik e-posta bildirim raporu gönderir.

"""



import os

import logging

from typing import List, Dict, Any

from dataclasses import dataclass

from openai import OpenAI



# Loglama yapılandırması

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')



@dataclass

class SecurityLog:
  
    log_id: str
  
    source_ip: str
  
    endpoint: str
  
    payload: str
  
    timestamp: str
  
    user_agent: str = "Unknown"
  


class SecurityIncidentResponseService:
  
    """Siber güvenlik olaylarını SOC ve Sistem Yöneticilerine bildiren e-posta servis simülasyonu."""
  


    def __init__(self, soc_email: str = "soc-team@kurumsal.com"):
      
        self.soc_email = soc_email
      


    def send_incident_alert(self, subject: str, incident_report: str):
      
        """Güvenlik alarmı ve olay müdahale raporunu simüle eder."""
      
        logging.info(f"[GÜVENLİK ALARMI] Alıcı: {self.soc_email} | Konu: {subject}")
      
        logging.info(f"--- Olay Raporu ---\n{incident_report}\n--------------------")
      
        print(f"\n[ACİL SİSTEM BİLDİRİMİ]: '{subject}' konulu güvenlik alarmı {self.soc_email} adresine iletildi.\n")
      


class AICyberThreatDetector:
  
    def __init__(self, organization_name: str):
      
        self.organization_name = organization_name
      
        self.client = OpenAI()
      
        self.incident_service = SecurityIncidentResponseService()
      


    def analyze_log(self, log: SecurityLog) -> Dict[str, Any]:
      
        """Yapay zeka modelleri ile log kaydını analiz eder ve tehdit tespiti yapar."""
      
        logging.info(f"Log İnceleniyor -> ID: {log.log_id}, Kaynak IP: {log.source_ip}")
      


        prompt = f"""
        
Sen "{self.organization_name}" şirketinin Baş Siber Güvenlik Uzmanı ve SOC Analistisin.

Aşağıdaki şüpheli ağ/sunucu logunu derinlemesine analiz et:



Log ID: {log.log_id}

Kaynak IP: {log.source_ip}

Hedef Endpoint: {log.endpoint}

İçerik/Payload: {log.payload}

Zaman damgası: {log.timestamp}

User-Agent: {log.user_agent}



Lütfen analizini şu formatta yap:

1. Tehdit Tipi (Threat Type): [Normal Trafik / Brute Force / SQL Injection / XSS / DDoS / Şüpheli Anomali]

2. Risk Skoru (Risk Score): [0 - 100 arası puan]

3. Kritiklik Seviyesi (Severity): [Düşük / Orta / Yüksek / Kritik]

4. Alınması Gereken Aksiyon (Mitigation): [IP Engelleme / WAF Kuralı / Hesap Kilitleme / İzleme]

5. Teknik Olay Raporu: SOC ekibi için detaylı açıklama ve aksiyon planı.

"""



        try:
        
            response = self.client.chat.completions.create(
            
                model="gpt-4o-mini",
                
                messages=[
                
                    {"role": "system", "content": "Sen kıdemli bir yapay zeka siber güvenlik ve tehdit avcısısın."},
                    
                    {"role": "user", "content": prompt}
                    
                ],
                
                temperature=0.3,
                
                max_tokens=850
                
            )
            
            analysis_result = response.choices[0].message.content
            

            
            # Kritik veya Yüksek tehditlerde otomatik e-posta alarmı gönder
            
            if "kritik" in analysis_result.lower() or "yüksek" in analysis_result.lower():
            
                subject = f"KRİTİK GÜVENLİK TEHDİDİ TESPİT EDİLDİ - [{log.log_id}] - IP: {log.source_ip}"
                
                self.incident_service.send_incident_alert(subject, analysis_result)
                


            return {
            
                "log_id": log.log_id,
                
                "status": "Analiz Tamamlandı",
                
                "analysis_report": analysis_result
                
            }
            
        except Exception as e:
        
            logging.error(f"Siber Güvenlik AI Analiz Hatası: {str(e)}")
            
            return {"log_id": log.log_id, "status": "Hata", "error": str(e)}
            


def main():

    print("=== Yapay Zeka Destekli Akıllı Siber Güvenlik ve Tehdit Tespit Sistemi ===\n")
    

    
    # Güvenlik Dedektörü Tanımlama
    
    detector = AICyberThreatDetector(
    
        organization_name="Global Finans ve Teknoloji A.Ş."
        
    )
    


    # Örnek Şüpheli Log Kayıtları
    
    sample_logs = [
    
        SecurityLog(
        
            log_id="LOG-9001",
            
            source_ip="185.220.101.5",
            
            endpoint="/api/v1/auth/login",
            
            payload="admin' OR '1'='1 -- (SQL Injection denemesi)",
            
            timestamp="2026-08-19 21:00:15",
            
            user_agent="sqlmap/1.6.7-stable"
            
        ),
        
        SecurityLog(
        
            log_id="LOG-9002",
            
            source_ip="45.154.255.88",
            
            endpoint="/admin/dashboard",
            
            payload="POST /admin/login - Arka arkaya 150 başarısız şifre denemesi",
            
            timestamp="2026-08-19 21:05:42",
            
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            
        )
        
    ]
    


    # Logları işleme sokma ve tehdit tespiti
    
    for log in sample_logs:
    
        print(f"\n--- Log Analiz Ediliyor: {log.log_id} (IP: {log.source_ip}) ---")
        
        result = detector.analyze_log(log)
        
        print(result["analysis_report"])
        
        print("-" * 65)
        


if __name__ == "__main__":

    main()
    

















































































