#!/usr/bin/env python3
"""
Yapay Zeka Destekli Akıllı Şehir ve Trafik Optimizasyon Sistemi
(AI-Powered Smart City & Traffic Optimization System)

Geleceğin akıllı şehirlerinde gerçek zamanlı sensör verilerini, hava koşullarını ve
yoğunluk haritalarını yapay zeka ile analiz ederek trafik ışığı sürelerini optimize eden,
kaza veya yoğunluk anında acil durum ekiplerine otomatik uyarı gönderen sistem.
"""

import os
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
from openai import OpenAI

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

@dataclass
class IntersectionData:
    intersection_id: str
    location_name: str
    vehicle_count_per_minute: int
    average_speed_kmh: float
    weather_condition: str
    emergency_vehicle_detected: bool

class SmartCityNotificationService:
    """Trafik yoğunluğu, kazalar veya acil durumları ilgili belediye birimlerine bildiren servis."""
    def __init__(self, municipal_team_email: str = "traffic.control@akillisehir.gov.tr"):
        self.municipal_team_email = municipal_team_email

    def send_alert(self, subject: str, report_content: str):
        logging.info(f"[EMAIL SIMULATION] To: {self.municipal_team_email}")
        logging.info(f"Subject: {subject}")
        logging.info(f"Body:\n{report_content}")
        print(f"-> E-posta başarıyla gönderildi: {self.municipal_team_email} | Konu: {subject}")

class SmartCityTrafficOrchestrator:
    def __init__(self):
        self.client = OpenAI()
        self.notifier = SmartCityNotificationService()

    def optimize_traffic_flow(self, data: IntersectionData) -> str:
        """OpenAI API kullanarak kavşak için anlık sinyal optimizasyonu ve strateji raporu üretir."""
        prompt = f"""
        Sen yapay zeka tabanlı bir Akıllı Şehir ve Ulaşım Mühendisisin. Aşağıdaki kavşak verilerine göre anlık trafik optimizasyon stratejisi ve sinyalizasyon süresi önerisi hazırla:
        
        Kavşak ID: {data.intersection_id}
        Konum: {data.location_name}
        Dakika Başına Araç Sayısı: {data.vehicle_count_per_minute}
        Ortalama Hız: {data.average_speed_kmh} km/s
        Hava Koşulları: {data.weather_condition}
        Acil Durum Aracı Tespit Edildi mi?: {'EVET' * data.emergency_vehicle_detected or 'HAYIR'}
        
        Lütfen Türkçe olarak şunları içeren profesyonel bir rapor sun:
        1. Mevcut Trafik Durum Analizi ve Yoğunluk Skoru
        2. Trafik Işığı / Sinyalizasyon Optimizasyon Önerisi (Yeşil ışık süreleri vb.)
        3. Acil Durum / Kaza Müdahale Planı (Varsa)
        """;

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Sen kıdemli bir Akıllı Şehir ve Ulaşım Sistemleri Mimarısın."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            report = response.choices[0].message.content
            
            # E-posta bildirimi gönder
            self.notifier.send_alert(
                f"Akıllı Şehir Trafik Optimizasyon Raporu - {data.location_name}",
                report
            )
            return report
        except Exception as e:
            logging.error(f"Yapay zeka analiz hatası: {e}")
            return f"Analiz gerçekleştirilemedi. Hata: {str(e)}"

if __name__ == "__main__":
    print("--- Yapay Zeka Akıllı Şehir ve Trafik Optimizasyon Sistemi Başlatılıyor ---")
    
    sample_intersection = IntersectionData(
        intersection_id="IST-MEC-04",
        location_name="Mecidiyeköy Meydanı Ana Arter",
        vehicle_count_per_minute=145,
        average_speed_kmh=18.5,
        weather_condition="Yağmurlu",
        emergency_vehicle_detected=True
    )
    
    orchestrator = SmartCityTrafficOrchestrator()
    result_report = orchestrator.optimize_traffic_flow(sample_intersection)
    print("\n--- Oluşturulan Akıllı Trafik Raporu ---\n")
    print(result_report)
