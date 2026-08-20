#!/usr/bin/env python3

"""

Yapay Zeka Destekli Akıllı İnsan Kaynakları ve Yetenek Analiz Sistemi

(AI-Powered Smart HR & Talent Analytics System)



Bu sistem; aday özgeçmişlerini (CV) ve yetkinliklerini pozisyon gereksinimlerine göre

yapay zeka ile analiz eder, uyumluluk skoru (Match Score) atar, mülakat soru önerileri

oluşturur ve İK / İşe Alım ekibine otomatik e-posta bildirim raporu gönderir.

"""



import os

import logging

from typing import List, Dict, Any

from dataclasses import dataclass

from openai import OpenAI



# Loglama yapılandırması

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')



@dataclass

class CandidateProfile:
  
    candidate_id: str
  
    full_name: str
  
    email: str
  
    applied_position: str
  
    experience_years: int
  
    skills: List[str]
  
    resume_summary: str
  


class HRNotificationService:
  
    """İK ve işe alım ekibine değerlendirme raporları gönderen e-posta servis simülasyonu."""
  


    def __init__(self, hr_email: str = "recruitment@kurumsal.com"):
      
        self.hr_email = hr_email
      


    def send_evaluation_report(self, subject: str, report_body: str):
      
        """Aday değerlendirme ve mülakat davet raporunu simüle eder."""
      
        logging.info(f"[İK BİLDİRİMİ] Alıcı: {self.hr_email} | Konu: {subject}")
      
        logging.info(f"--- Değerlendirme Raporu ---\n{report_body}\n---------------------------")
      
        print(f"\n[SİSTEM BİLDİRİMİ]: '{subject}' konulu aday raporu {self.hr_email} adresine iletildi.\n")
      


class AIHRTalentAnalyzer:
  
    def __init__(self, company_name: str):
      
        self.company_name = company_name
      
        self.client = OpenAI()
      
        self.notifier = HRNotificationService()
      


    def analyze_candidate(self, candidate: CandidateProfile, job_description: str) -> Dict[str, Any]:
      
        """Yapay zeka modelleri ile aday profilini pozisyon gereksinimlerine göre analiz eder."""
      
        logging.info(f"Aday İnceleniyor -> ID: {candidate.candidate_id}, Ad: {candidate.full_name}, Pozisyon: {candidate.applied_position}")
      


        prompt = f"""
        
Sen "{self.company_name}" şirketinin Kıdemli İnsan Kaynakları ve Yetenek Kazanımı Yöneticisisin.

Aşağıdaki aday profilini ve iş tanımını (Job Description) detaylı bir şekilde karşılaştırarak analiz et:



--- İŞ TANIMI ---

{job_description}



--- ADAY PROFİLİ ---

Aday ID: {candidate.candidate_id}

Ad Soyad: {candidate.full_name}

Başvurduğu Pozisyon: {candidate.applied_position}

Deneyim Süresi: {candidate.experience_years} yıl

Yetenekler: {', '.join(candidate.skills)}

Özgeçmiş Özeti: {candidate.resume_summary}



Lütfen analizini şu formatta yap:

1. Uyumluluk Durumu (Match Status): [Güçlü Eşleşme / Alternatif / Uygun Değil]

2. Uyumluluk Skoru (Match Score): [0 - 100 arası puan]

3. Güçlü Yönler (Strengths): Adayın pozisyona en büyük katkı sağlayacak teknik ve sosyal yetkinlikleri.

4. Gelişime Açık Alanlar / Eksiklikler (Gaps): Pozisyon gereksinimlerine göre eksik görülen noktalar.

5. Teknik Mülakat Soru Önerileri: Adayın mülakatında sorulması gereken 2 kritik teknik soru.

6. İK Değerlendirme Raporu: İşe alım ekibi için nihai karar önerisi ve aksiyon planı.

"""



        try:
        
            response = self.client.chat.completions.create(
            
                model="gpt-4o-mini",
                
                messages=[
                
                    {"role": "system", "content": "Sen kurumsal işe alım ve yetenek yönetimi konusunda uzmanlaşmış bir yapay zeka İK analistisin."},
                    
                    {"role": "user", "content": prompt}
                    
                ],
                
                temperature=0.3,
                
                max_tokens=850
                
            )
            
            analysis_result = response.choices[0].message.content
            

            
            # Güçlü eşleşmelerde otomatik İK bilgilendirme raporu gönder
            
            if "güçlü eşleşme" in analysis_result.lower() or "85" in analysis_result or "90" in analysis_result:
            
                subject = f"YÜKSEK UYUMLU ADAY TESPİT EDİLDİ - {candidate.full_name} ({candidate.applied_position})"
                
                self.notifier.send_evaluation_report(subject, analysis_result)
                


            return {
            
                "candidate_id": candidate.candidate_id,
                
                "status": "Analiz Tamamlandı",
                
                "hr_report": analysis_result
                
            }
            
        except Exception as e:
        
            logging.error(f"İK AI Analiz Hatası: {str(e)}")
            
            return {"candidate_id": candidate.candidate_id, "status": "Hata", "error": str(e)}
            


def main():

    print("=== Yapay Zeka Destekli Akıllı İnsan Kaynakları ve Yetenek Analiz Sistemi ===\n")
    

    
    # İK Analizörü Tanımlama
    
    analyzer = AIHRTalentAnalyzer(
    
        company_name="Global Teknoloji ve Yazılım A.Ş."
        
    )
    


    # Örnek İş Tanımı
    
    job_desc = "En az 5 yıl Python ve FastAPI deneyimi olan, bulut mimarileri (AWS/GCP) konusunda bilgili, mikroservis mimarilerinde görev yapmış Kıdemli Yazılım Mühendisi aranmaktadır."
    


    # Örnek Aday Profilleri
    
    sample_candidates = [
    
        CandidateProfile(
        
            candidate_id="CAND-501",
            
            full_name="Ahmet Yılmaz",
            
            email="ahmet.yilmaz@example.com",
            
            applied_position="Kıdemli Yazılım Mühendisi",
            
            experience_years=7,
            
            skills=["Python", "FastAPI", "Docker", "AWS", "Kubernetes", "PostgreSQL"],
            
            resume_summary="7 yıldır kurumsal projelerde backend geliştirme yapmaktadır. Mikroservisler ve bulut bilişim alanında uzmandır."
            
        ),
        
        CandidateProfile(
        
            candidate_id="CAND-502",
            
            full_name="Ayşe Demir",
            
            email="ayse.demir@example.com",
            
            applied_position="Kıdemli Yazılım Mühendisi",
            
            experience_years=2,
            
            skills=["JavaScript", "React", "Node.js", "HTML/CSS"],
            
            resume_summary="2 yıldır frontend odaklı projelerde çalışan, web teknolojilerine ilgi duyan yazılımcı."
            
        )
        
    ]
    


    # Adayları analiz etme
    
    for candidate in sample_candidates:
    
        print(f"\n--- Aday Analiz Ediliyor: {candidate.full_name} ({candidate.a
















































































