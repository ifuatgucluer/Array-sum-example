#!/usr/bin/env python3

"""

Yapay Zeka Destekli Akıllı Envanter ve Stok Tahmin Sistemi

(AI-Powered Smart Inventory & Stock Prediction System)



Bu sistem; depo envanterini yönetir, kritik stok seviyelerini analiz eder,

tüketim oranlarına göre yeniden sipariş (reorder) noktalarını hesaplar

ve OpenAI API entegrasyonu ile stratejik tedarik zinciri raporu üretir.

"""



import os

import logging

from typing import List, Dict, Any

from dataclasses import dataclass

from openai import OpenAI



# Loglama yapılandırması

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



@dataclass

class InventoryItem:
  
    sku: str
  
    name: str
  
    current_stock: int
  
    min_threshold: int
  
    daily_consumption: int
  
    unit_cost: float
  


class SmartInventoryManager:
  
    def __init__(self, warehouse_name: str, items: List[InventoryItem]):
      
        self.warehouse_name = warehouse_name
      
        self.items = items
      
        self.client = OpenAI()
      


    def analyze_stock_status(self) -> List[Dict[str, Any]]:
      
        """Her bir ürün için stok durumunu ve tahmini tükenme gününü hesaplar."""
      
        report = []
      
        for item in self.items:
          
            days_left = item.current_stock // item.daily_consumption if item.daily_consumption > 0 else 999
          
            is_critical = item.current_stock <= item.min_threshold
          
            report.append({
              
                "sku": item.sku,
              
                "name": item.name,
              
                "stock": item.current_stock,
              
                "days_left": days_left,
              
                "critical": is_critical,
              
                "total_value": item.current_stock * item.unit_cost
              
            })
          
        return report
      


    def generate_ai_procurement_strategy(self) -> str:
      
        """OpenAI API kullanarak akıllı tedarik ve stok optimizasyon raporu hazırlar."""
      
        status = self.analyze_stock_status()
      
        critical_items = [i for i in status if i["critical"]]
      


        item_summary = "\n".join([
          
            f"- SKU: {i['sku']}, Ürün: {i['name']}, Mevcut Stok: {i['stock']}, Tükenme Süresi: {i['days_left']} gün, Kritik: {'Evet' if i['critical'] else 'Hayır'}"
          
            for i in status
          
        ])
      


        prompt = f"""
        
Sen üst düzey bir Kıdemli Tedarik Zinciri ve Envanter Yönetimi Uzmanısın.

"{self.warehouse_name}" deposu için aşağıdaki envanter durumuna dayanarak stratejik bir optimizasyon ve satın alma raporu hazırla:



Envanter Durumu:

{item_summary}



Kritik Ürün Sayısı: {len(critical_items)}



Lütfen raporda şunlara yer ver:

1. Kritik seviyedeki ürünler için acil tedarik planı ve bütçe tahmini.

2. Tedarik zinciri riskleri ve depo optimizasyon önerileri.

3. Maliyetleri düşürmek için JIT (Just-in-Time) veya EOQ (Economic Order Quantity) stratejik tavsiyeleri.

"""



        try:
        
            logging.info("OpenAI API üzerinden envanter strateji raporu talep ediliyor...")
            
            response = self.client.chat.completions.create(
            
                model="gpt-4o-mini",
                
                messages=[
                
                    {"role": "system", "content": "Sen profesyonel bir küresel lojistik ve tedarik zinciri direktörüsün."},
                    
                    {"role": "user", "content": prompt}
                    
                ],
                
                temperature=0.7,
                
                max_tokens=1000
                
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
        
            logging.error(f"Rapor üretilirken hata oluştu: {str(e)}")
            
            return f"Hata: {str(e)}"
            


def main():

    print("=== Yapay Zeka Destekli Akıllı Envanter ve Stok Tahmin Sistemi ===")
    

    
    # Örnek Envanter Verileri
    
    sample_inventory = [
    
        InventoryItem(sku="SKU-101", name="Endüstriyel Sensör Modülü", current_stock=15, min_threshold=20, daily_consumption=3, unit_cost=250.0),
        
        InventoryItem(sku="SKU-102", name="Fiber Optik Kablo (100m)", current_stock=8, min_threshold=10, daily_consumption=2, unit_cost=120.0),
        
        InventoryItem(sku="SKU-103", name="Güç Kaynağı (PSU 500W)", current_stock=45, min_threshold=15, daily_consumption=4, unit_cost=450.0),
        
        InventoryItem(sku="SKU-104", name="Hidrolik Valf Contası", current_stock=5, min_threshold=25, daily_consumption=6, unit_cost=45.0),
        
        InventoryItem(sku="SKU-105", name="PLC Kontrol Kartı", current_stock=12, min_threshold=10, daily_consumption=1, unit_cost=1200.0)
        
    ]
    


    manager = SmartInventoryManager(
    
        warehouse_name="Ana Üretim ve Dağıtım Deposu - Marmara",
        
        items=sample_inventory
        
    )
    


    print("\n[Envanter Durum Analizi]")
    
    stock_report = manager.analyze_stock_status()
    
    for row in stock_report:
    
        crit_str = " [KRİTİK STOK!]" if row["critical"] else ""
        
        print(f"- {row['name']} ({row['sku']}): Stok={row['stock']}, Kalan Ömür={row['days_left']} gün{crit_str}")
        


    print("\nYapay Zeka Tedarik ve Optimizasyon Raporu Hazırlanıyor...\n")
    
    ai_report = manager.generate_ai_procurement_strategy()
    

    
    print("--- Yapay Zeka Stratejik Envanter Raporu ---")
    
    print(ai_report)
    
    print("---------------------------------------------")
    


if __name__ == "__main__":

    main()
    













































































