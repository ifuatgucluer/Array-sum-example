#!/usr/bin/env python3
"""
Yapay Zeka Destekli Kişiselleştirilmiş Küresel Eğitim ve Yetenek Yolu Mimarı
(AI-Powered Personalized Global Education & Skill Path Architect)

Geleceğin eğitim teknolojilerini simüle eden bu sistem; bireylerin mevcut yetenek setini,
öğrenme hızını ve kariyer hedeflerini küresel iş piyasası trendleriyle yapay zeka kullanarak
eşleştirir, kişiselleştirilmiş bir öğrenme yol haritası çizer ve ilerleme raporlarını
otomatik olarak mentorlara / kullanıcılara e-posta ile bildirir.
"""

import os
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
from openai import OpenAI

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

@dataclass
class LearnerProfile:
    learner_id: str
    full_name: str
    email: str
    current_skills: List[str]
    target_role: str
    preferred_learning_style: str
    weekly_hours_available: int

class EducationNotificationService:
    """Eğitim yol haritası ve kilometre taşı raporlarını ilgili kişilere ileten servis."""
    def __init__(self, mentor_email: str = "career.mentor@global-education.ai"):
        self.mentor_email = mentor_email

    def send_alert(self, subject: str, report_content: str):
        logging.info(f"[EMAIL SIMULATION] To: {self.mentor_email}")
        logging.info(f"Subject: {subject}")
        logging.info(f"Body:\n{report_content}")
        print(f"-> E-posta başarıyla gönderildi: {self.mentor_email} | Konu: {subject}")

class EducationPathArchitect:
    def __init__(self):
        self.client = OpenAI()
        self.notifier = EducationNotificationService()

    def generate_learning_path(self, profile: LearnerProfile) -> str:
        """OpenAI API kullanarak bireye özel kariyer ve eğitim yol haritası oluşturur."""
        prompt = f"""
        Sen kıdemli bir Küresel Kariyer Mimarı ve Eğitim Teknolojileri Uzmanısın. Aşağıdaki öğrenci profiline göre kapsamlı ve kişiselleştirilmiş bir eğitim ve yetenek gelişim yol haritası hazırla:
        
        Öğrenci ID: {profile.learner_id}
        Ad Soyad: {profile.full_name}
        Mevcut Yetenekler: {', '.join(profile.current_skills)}
        Hedef Pozisyon: {profile.target_role}
        Tercih Edilen Öğrenme Stili: {profile.preferred_learning_style}
        Haftalık Ayrılan Süre: {profile.weekly_hours_available} saat
        
        Lütfen Türkçe olarak şunları içeren profesyonel bir yol haritası raporu sun:
        1. Mevcut Yetenek Analizi ve Yetenek Açığı (Skill Gap) Değerlendirmesi
        2. Adım Adım Modüler Eğitim Yol Haritası (Aylar bazında konular ve projeler)
        3. Önerilen Kaynaklar, Sertifikalar ve Pratik Uygulama Tavsiyeleri
        """;

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Sen kıdemli bir Küresel Kariyer Mimarı ve AI Eğitim Danışmanısın."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            report = response.choices[0].message.content
            
            # E-posta bildirimi gönder
            self.notifier.send_alert(
                f"Kişiselleştirilmiş Eğitim Yol Haritası - {profile.full_name}",
                report
            )
            return report
        except Exception as e:
            logging.error(f"Yapay zeka analiz hatası: {e}")
            return f"Analiz gerçekleştirilemedi. Hata: {str(e)}"

if __name__ == "__main__":
    print("--- Yapay Zeka Küresel Eğitim ve Yetenek Yolu Mimarı Başlatılıyor ---")
    
    sample_learner = LearnerProfile(
        learner_id="LRN-9982",
        full_name="İbrahim Fuat Güçlüer",
        email="ifuatgucluer@example.com",
        current_skills=["Python", "Temel Veri Analizi", "Problem Çözme"],
        target_role="Yapay Zeka ve Makine Öğrenmesi Mühendisi",
        preferred_learning_style="Proje Tabanlı ve Uygulamalı",
        weekly_hours_available=15
    )
    
    architect = EducationPathArchitect()
    result_report = architect.generate_learning_path(sample_learner)
    print("\n--- Oluşturulan Eğitim Yol Haritası Raporu ---\n")
    print(result_report)
