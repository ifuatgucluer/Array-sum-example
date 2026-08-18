#!/usr/bin/env python3

"""

Gelişmiş Yapay Zeka Destekli Proje Yönetim ve Orkestrasyon Sistemi

(Advanced AI-Driven Project Management & Orchestration System)

Bu sistem; karmaşık projelerin iş yükünü analiz eder, görevleri önceliklendirir,

risk skorlaması yapar ve OpenAI API entegrasyonu ile stratejik yönlendirme raporu üretir.

"""



import os

import logging

from typing import List, Dict, Any

from dataclasses import dataclass

from openai import OpenAI



# Loglama yapılandırması

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



@dataclass

class Task:
  
    name: str
  
    complexity: int  # 1-10 arası
  
    priority: str    # Yüksek, Orta, Düşük
  
    assigned_to: str
  


class AIProjectOrchestrator:
  
    def __init__(self, project_name: str, tasks: List[Task]):
      
        self.project_name = project_name
      
        self.tasks = tasks
      
        self.client = OpenAI()
      


    def calculate_workload_score(self) -> float:
      
        """Projenin toplam karmaşıklık ve iş yükü skorunu hesaplar."""
      
        total_complexity = sum(task.complexity for task in self.tasks)
      
        return total_complexity / len(self.tasks) if self.tasks else 0.0
      


    def generate_ai_strategy_report(self) -> str:
      
        """Yapay zeka kullanarak proje için kapsamlı stratejik analiz raporu üretir."""
      
        avg_complexity = self.calculate_workload_score()
      


        task_summary = "\n".join([
          
            f"- {t.name} (Karmaşıklık: {t.complexity}/10, Öncelik: {t.priority}, Sorumlu: {t.assigned_to})"
          
            for t in self.tasks
          
        ])
      


        prompt = f"""
        
        Sen üst düzey bir Kıdemli Proje Yöneticisi ve Agile Koçusun. 
        
        "{self.project_name}" adlı proje için aşağıdaki görev dağılımı ve analiz verilerine dayanarak profesyonel bir yönetim raporu hazırla:
        

        
        Ortalama Karmaşıklık Skoru: {avg_complexity:.2f}/10
        

        
        Görev Listesi:
        
        {task_summary}
        

        
        Lütfen raporda şunlara yer ver:
        
        1. Projenin genel risk analizi ve darboğaz (bottleneck) tahminleri.
        
        2. Çevik (Agile/Scrum) metodolojiye göre sprint optimizasyon önerileri.
        
        3. Ekip verimliliğini artıracak stratejik tavsiyeler.
        
        """
        


        try:
        
            logging.info("OpenAI API üzerinden stratejik rapor talep ediliyor...")
            
            response = self.client.chat.completions.create(
            
                model="gpt-4o-mini",
                
                messages=[
                
                    {"role": "system", "content": "Sen uluslararası düzeyde deneyimli bir kurumsal proje yöneticisisin."},
                    
                    {"role": "user", "content": prompt}
                    
                ],
                
                temperature=0.7,
                
                max_tokens=1000
                
            ]
            
            return response.choices[0].message.content
            
        except Exception as e:
        
            logging.error(f"Rapor üretilirken hata oluştu: {str(e)}")
            
            return f"Hata: {str(e)}"
            


def main():

    print("=== Gelişmiş AI Proje Yönetim ve Orkestrasyon Sistemi ===")
    

    
    # Örnek Proje Görevleri
    
    sample_tasks = [
    
        Task(name="Mimari Tasarım ve Veritabanı Şeması", complexity=8, priority="Yüksek", assigned_to="Lead Architect"),
        
        Task(name="Backend API Geliştirme (FastAPI)", complexity=7, priority="Yüksek", assigned_to="Backend Team"),
        
        Task(name="Frontend Arayüz Geliştirme (React)", complexity=6, priority="Orta", assigned_to="Frontend Team"),
        
        Task(name="Yapay Zeka Entegrasyon Modülü", complexity=9, priority="Yüksek", assigned_to="AI Engineer"),
        
        Task(name="Sistem Testleri ve QA", complexity=5, priority="Orta", assigned_to="QA Team")
        
    ]
    

    
    orchestrator = AIProjectOrchestrator(
    
        project_name="Yeni Nesil AI Akıllı Asistan Platformu",
        
        tasks=sample_tasks
        
    )
    

    
    workload = orchestrator.calculate_workload_score()
    
    print(f"\\n[Proje Metrikleri]")
    
    print(f"- Toplam Görev Sayısı: {len(sample_tasks)}")
    
    print(f"- Ortalama Görev Karmaşıklığı: {workload:.2f} / 10\\n")
    

    
    print("Yapay Zeka Stratejik Raporu Hazırlanıyor...\\n")
    
    report = orchestrator.generate_ai_strategy_report()
    

    
    print("--- Yapay Zeka Proje Yönetim Raporu ---")
    
    print(report)
    
    print("---------------------------------------")
    


if __name__ == "__main__":

    main()
    














































































