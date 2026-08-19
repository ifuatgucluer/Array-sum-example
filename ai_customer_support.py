#!/usr/bin/env python3

"""

Yapay Zeka Destekli Akıllı Müşteri Destek ve Duygu Analizi Sistemi

(AI-Powered Smart Customer Support & Sentiment Analysis System)



Bu sistem; gelen müşteri taleplerini yapay zeka ile analiz eder (duygu analizi,

önceliklendirme ve otomatik yanıt önerisi) ve kurumsal e-posta bildirim modülü

aracılığıyla ilgili operasyon birimlerine rapor iletir.

"""



import os

import logging

from typing import List, Dict, Any

from dataclasses import dataclass

from openai import OpenAI



# Loglama yapılandırması

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')



@dataclass

class CustomerTicket:
  
    ticket_id: str
  
    customer_name: str
  
    customer_email: str
  
    subject: str
  
    message: str
  
    category: str = "Genel"
  


class EmailNotificationService:
  
    """İşlem sonuçlarını ve yapay zeka raporlarını ilgili adreslere bildiren servis simülasyonu."""
  


    def __init__(self, smtp_server: str = "smtp.kurumsal.com", sender_email: str = "system@kurumsal.com"):
      
        self.smtp_server = smtp_server
      
        self.sender_email = sender_email
      


    def send_notification(self, recipient_email: str, subject: str, report_body: str):
      
        """Gerçek SMTP entegrasyonu için altyapı sunan e-posta gönderim simülasyonu."""
      
        logging.info(f"[E-POSTA GÖNDERİMİ] Alıcı: {recipient_email} | Konu: {subject}")
      
        logging.info(f"--- E-Posta İçeriği ---\n{report_body}\n------------------------")
      
        # Gerçek ortamda smtplib kütüphanesi ile TLS üzerinden gönderim yapılır.

        print(f"\n[SİSTEM BİLDİRİMİ]: '{subject}' konulu rapor {recipient_email} adresine başarıyla e-posta olarak iletildi.\n")
      


class AICustomerSupportOrchestrator:
  
    def __init__(self, company_name: str, notification_recipient: str):
      
        self.company_name = company_name
      
        self.client = OpenAI()
      
        self.notifier = EmailNotificationService()
      
        self.recipient = notification_recipient
      


    def analyze_and_respond(self, ticket: CustomerTicket) -> Dict[str, Any]:
      
        """Yapay zeka modelleri ile müşteri talebini analiz eder ve yanıt üretir."""
      
        logging.info(f"Destek Talebi İnceleniyor -> ID: {ticket.ticket_id}, Müşteri: {ticket.customer_name}")
      


        prompt = f"""
        
Sen "{self.company_name}" şirketinin profesyonel Müşteri İlişkileri ve Destek Yöneticisisin.

Aşağıdaki müşteri talebini analiz et:



Müşteri Adı: {ticket.customer_name}

Konu: {ticket.subject}

Mesaj: {ticket.message}



Lütfen şu 3 unsuru içeren JSON formatına benzer yapılandırılmış bir yanıt hazırla:

1. Duygu Analizi (Sentiment): [Olumlu / Nötr / Olumsuz / Öfkeli]

2. Öncelik Derecesi: [Düşük / Orta / Yüksek / Kritik]

3. Profesyonel Yanıt Taslağı: Müşteriye gönderilecek nazik, çözüm odaklı kurumsal Türkçe yanıt.

"""



        try:
        
            response = self.client.chat.completions.create(
            
                model="gpt-4o-mini",
                
                messages=[
                
                    {"role": "system", "content": "Sen müşteri memnuniyeti odaklı uzman bir destek asistanısın."},
                    
                    {"role": "user", "content": prompt}
                    
                ],
                
                temperature=0.7,
                
                max_tokens=800
                
            )
            
            ai_analysis = response.choices[0].message.content
            

            
            # E-posta bildirim modülünü tetikle
            
            subject = f"Destek Talebi Analizi ve Yanıt Önerisi - [{ticket.ticket_id}]"
            
            body = f"Sayın Yetkili,\n\n{ticket.customer_name} ({ticket.customer_email}) tarafından gelen talep işlenmiştir.\n\n{ai_analysis}"
            
            self.notifier.send_notification(self.recipient, subject, body)
            


            return {
            
                "ticket_id": ticket.ticket_id,
                
                "status": "Başarılı",
                
                "ai_analysis": ai_analysis
                
            }
            
        except Exception as e:
        
            logging.error(f"AI Analiz Hatası: {str(e)}")
            
            return {"ticket_id": ticket.ticket_id, "status": "Hata", "error": str(e)}
            


def main():

    print("=== Yapay Zeka Destekli Akıllı Müşteri Destek ve E-Posta Bildirim Sistemi ==-\n")
    

    
    # Orkestratör ve Bildirim Alıcısı Tanımlama
    
    support_system = AICustomerSupportOrchestrator(
    
        company_name="Global Teknoloji Çözümleri A.Ş.",
        
        notification_recipient="operasyon@kurumsal.com"
        
    )
    


    # Örnek Müşteri Destek Talepleri
    
    sample_tickets = [
    
        CustomerTicket(
        
            ticket_id="TICK-501",
            
            customer_name="Ahmet Yılmaz",
            
            customer_email="ahmet.yilmaz@ornek.com",
            
            subject="Fatura ve Lisans Yenileme Sorunu",
            
            message="Merhaba, son yaptığım ödemeye rağmen yıllık lisansım aktifleşmedi. Acil desteğinizi rica ederim işlerim aksıyor.",
            
            category="Finans/Lisans"
            
        ),
        
        CustomerTicket(
        
            ticket_id="TICK-502",
            
            customer_name="Zeynep Demir",
            
            customer_email="zeynep.demir@ornek.com",
            
            subject="API Entegrasyon Hatası",
            
            message="Sisteminizdeki yeni v2 API uç noktalarına bağlanırken 401 Unauthorized hatası alıyorum. Dokümantasyondaki örnekler güncel mi?",
            
            category="Teknik Destek"
            
        )
        
    ]
    


    # Talepleri işleme sokma ve otomatik e-posta bildirimlerini tetikleme
    
    for ticket in sample_tickets:
    
        print(f"\n--- Talep İşleniyor: {ticket.ticket_id} ---")
        
        result = support_system.analyze_and_respond(ticket)
        
        print(result["ai_analysis"])
        
        print("-" * 60)
        


if __name__ == "__main__":

    main()
    




















































































