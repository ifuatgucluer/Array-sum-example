#!/usr/bin/env python3

"""

Yapay Zeka Destekli Akıllı Finansal Dolandırıcılık (Fraud) Tespit Sistemi

(AI-Powered Financial Fraud Detection & Automated Risk Scoring System)



Bu sistem; finansal işlem akışlarını, kullanıcı harcama alışkanlıklarını,

coğrafi konum anomalilerini ve işlem tutarlarını yapay zeka ile analiz ederek

potansiyel dolandırıcılık (fraud) girişimlerini anlık olarak tespit eder,

risk skoru atar ve Risk/Uyum ekibine otomatik e-posta bildirim raporu gönderir.

"""



import os

import logging

from typing import List, Dict, Any

from dataclasses import dataclass

from openai import OpenAI



# Loglama yapılandırması

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')



@dataclass

class FinancialTransaction:
  
    txn_id: str
  
    account_id: str
  
    amount: float
  
    currency: str
  
    merchant: str
  
    location: str
  
    device_fingerprint: str
  
    timestamp: str
  


class FraudAlertService:
  
    """Risk ve uyum ekibine acil dolandırıcılık uyarıları gönderen e-posta servis simülasyonu."""
  


    def __init__(self, risk_team_email: str = "fraud-ops@kurumsal-banka.com"):
      
        self.risk_team_email = risk_team_email
      


    def send_fraud_alert(self, subject: str, alert_report: str):
      
        """Dolandırıcılık alarmı ve blokaj raporunu simüle eder."""
      
        logging.info(f"[FRAUD UYARISI] Alıcı: {self.risk_team_email} | Konu: {subject}")
      
        logging.info(f"--- Detaylı Rapor ---\n{alert_report}\n----------------------")
      
        print(f"\n[ACİL RİSK BİLDİRİMİ]: '{subject}' konulu fraud alarmı {self.risk_team_email} adresine iletildi.\n")
      


class AIFraudDetector:
  
    def __init__(self, institution_name: str):
      
        self.institution_name = institution_name
      
        self.client = OpenAI()
      
        self.alert_service = FraudAlertService()
      


    def analyze_transaction(self, txn: FinancialTransaction) -> Dict[str, Any]:
      
        """Yapay zeka modelleri ile finansal işlemi analiz eder ve fraud riski skorlar."""
      
        logging.info(f"İşlem İnceleniyor -> ID: {txn.txn_id}, Hesap: {txn.account_id}, Tutar: {txn.amount} {txn.currency}")
      


        prompt = f"""
        
Sen "{self.institution_name}" kurumunun Kıdemli Finansal Güvenlik ve Dolandırıcılık (Fraud) Analistisin.

Aşağıdaki finansal işlemi şüpheli aktiviteler, anormallikler ve dolandırıcılık riskleri açısından analiz et:



İşlem ID: {txn.txn_id}

Hesap ID: {txn.account_id}

İşlem Tutarı: {txn.amount} {txn.currency}

İş Yeri / Üye İşyeri: {txn.merchant}

Konum: {txn.location}

Cihaz Parmak İzi (Device ID): {txn.device_fingerprint}

Zaman Damgası: {txn.timestamp}



Lütfen analizini şu formatta yap:

1. Risk Durumu (Risk Status): [Normal / Şüpheli / Yüksek Risk / Kritik Fraud]

2. Risk Skoru (Risk Score): [0 - 100 arası puan]

3. Tespit Edilen Anomali (Anomaly Type): [Yok / Coğrafi Uyumsuzluk / Tutar Anomalisi / Cihaz Değişikliği / Hesap Ele Geçirme (ATO)]

4. Alınması Gereken Aksiyon (Action Required): [İşleme İzin Ver / SMS Doğrulama (2FA) / İşlemi Bloke Et / Hesabı Geçici Askıya Al]

5. Detaylı Uyum ve Risk Raporu: Risk ekibi için gerekçeli açıklama ve aksiyon planı.

"""



        try:
        
            response = self.client.chat.completions.create(
            
                model="gpt-4o-mini",
                
                messages=[
                
                    {"role": "system", "content": "Sen bankacılık ve finans alanında uzmanlaşmış bir yapay zeka fraud dedektörüsün."},
                    
                    {"role": "user", "content": prompt}
                    
                ],
                
                temperature=0.2,
                
                max_tokens=850
                
            )
            
            analysis_result = response.choices[0].message.content
            

            
            # Yüksek veya Kritik riskli işlemlerde otomatik e-posta alarmı gönder ve blokesi simüle et
            
            if "yüksek risk" in analysis_result.lower() or "kritik fraud" in analysis_result.lower():
            
                subject = f"KRİTİK FRAUD TESPİT EDİLDİ - İşlem: {txn.txn_id} - Tutar: {txn.amount} {txn.currency}"
                
                self.alert_service.send_fraud_alert(subject, analysis_result)
                


            return {
            
                "txn_id": txn.txn_id,
                
                "status": "Analiz Tamamlandı",
                
                "fraud_report": analysis_result
                
            }
            
        except Exception as e:
        
            logging.error(f"Fraud AI Analiz Hatası: {str(e)}")
            
            return {"txn_id": txn.txn_id, "status": "Hata", "error": str(e)}
            


def main():

    print("=== Yapay Zeka Destekli Akıllı Finansal Dolandırıcılık (Fraud) Tespit Sistemi ===\n")
    

    
    # Fraud Dedektörü Tanımlama
    
    detector = AIFraudDetector(
    
        institution_name="Global Dijital Bankacılık A.Ş."
        
    )
    


    # Örnek Finansal İşlemler (Normal ve Fraud Senaryoları)
    
    sample_transactions = [
    
        FinancialTransaction(
        
            txn_id="TXN-7001",
            
            account_id="ACC-99281",
            
            amount=45000.00,
            
            currency="TRY",
            
            merchant="Lüks Saat ve Kuyumculuk",
            
            location="Bangkok, Tayland",
            
            device_fingerprint="Unknown_Device_XYZ999",
            
            timestamp="2026-08-19 03:15:00"
            
        ),
        
        FinancialTransaction(
        
            txn_id="TXN-7002",
            
            account_id="ACC-11024",
            
            amount=120.50,
            
            currency="TRY",
            
            merchant="Online Market Alışverişi",
            
            location="İstanbul, Türkiye",
            
            device_fingerprint="Trusted_iPhone_15_Pro",
            
            timestamp="2026-08-19 14:30:22"
            
        )
        
    ]
    


    # İşlemleri analiz etme
    
    for txn in sample_transactions:
    
        print(f"\n--- İşlem Analiz Ediliyor: {txn.txn_id} (Tutar: {txn.amount} {txn.currency}) ---")
        
        result = detector.analyze_transaction(txn)
        
        print(result["fraud_report"])
        
        print("-" * 65)
        


if __name__ == "__main__":

    main()
    























































































