#!/usr/bin/env python3

"""

SAP Funds Management (FM) Modülü Simülatör Sistemi

(SAP FM Core & Budget Availability Control Simulator)



Bu sistem; SAP FM modülünün temel taşları olan Fon Yönetimi, Fon Merkezleri (Funds Centers),

Taahhüt Kalemleri (Commitment Items), Bütçe Tahsisi, Uygunluk Kontrolü (Availability Control - AVC)

ve Satın Alma Yaşam Döngüsü (PR -> PO -> Invoice Actuals) süreçlerini nesne tabanlı mimariyle simüle eder.

"""



import logging

from typing import List, Dict, Any

from dataclasses import dataclass, field



# Loglama yapılandırması

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')



@dataclass

class BudgetAccount:
  
    fund_center: str
  
    commitment_item: str
  
    total_budget: float
  
    released_budget: float = 0.0
  
    commitment_amount: float = 0.0  # PR ve PO aşamasındaki bloke tutar
  
    actual_amount: float = 0.0      # Fatura/Ödeme aşamasındaki fiili harcama
  


    @property
  
    def available_budget(self) -> float:
      
        """Kullanılabilir bütçeyi hesaplar: Serbest Bütçe - (Taahhüt + Fiili)"""
      
        return self.released_budget - (self.commitment_amount + self.actual_amount)
      


@dataclass

class TransactionDocument:
  
    doc_type: str  # PR, PO, INVOICE
  
    doc_id: str
  
    fund_center: str
  
    commitment_item: str
  
    amount: float
  
    vendor: str = ""
  


class SAPFMSimulator:
  
    def __init__(self, fm_area: str):
      
        self.fm_area = fm_area
      
        self.accounts: Dict[str, BudgetAccount] = {}
      
        self.documents: List[TransactionDocument] = []
      


    def create_budget(self, fund_center: str, commitment_item: str, total_amount: float, released_amount: float):
      
        """Bütçe tahsisi yapar (FMBB / FR51 simülasyonu)."""
      
        key = f"{fund_center}:{commitment_item}"
      
        self.accounts[key] = BudgetAccount(
          
            fund_center=fund_center,
          
            commitment_item=commitment_item,
          
            total_budget=total_amount,
          
            released_amount=released_amount
          
        )
      
        logging.info(f"Bütçe Tanımlandı -> Fon Merkezi: {fund_center}, Kalem: {commitment_item}, Tutar: {released_amount:,.2f} TL")
      


    def check_availability(self, fund_center: str, commitment_item: str, amount: float) -> bool:
      
        """Kullanılabilirlik Kontrolü (Availability Control - AVC) yapar."""
      
        key = f"{fund_center}:{commitment_item}"
      
        if key not in self.accounts:
          
            logging.warning(f"AVC Uyarısı: {fund_center} ve {commitment_item} için bütçe hesabı bulunamadı!")
          
            return False
          


        account = self.accounts[key]
      
        if account.available_budget >= amount:
          
            return True
          
        else:
          
            logging.error(f"AVC Bütçe Aşımı! İşlem reddedildi. Talep: {amount:,.2f} TL, Kullanılabilir: {account.available_budget:,.2f} TL")
          
            return False
          


    def post_document(self, doc: TransactionDocument) -> bool:
      
        """Belge işleme (PR, PO, Fatura) ve FM bütçe güncelleme süreci."""
      
        logging.info(f"İşlem Başlatıldı [{doc.doc_type}] - Belge No: {doc.doc_id} | Tutar: {doc.amount:,.2f} TL")
      


        key = f"{doc.fund_center}:{doc.commitment_item}"
      


        # PR veya PO aşamasında taahhüt (commitment) yaratılır

        if doc.doc_type in ["PR", "PO"]:
          
            if not self.check_availability(doc.fund_center, doc.commitment_item, doc.amount):
              
                return False
              
            self.accounts[key].commitment_amount += doc.amount
          
            logging.info(f"Taahhüt Oluşturuldu [{doc.doc_type}]. Bloke Tutar güncellendi.")
          


        # Fatura aşamasında (Invoice / Actual) taahhüt düşer, fiili harcama (actual) artar

        elif doc.doc_type == "INVOICE":
          
            # Eğer doğrudan PO üzerinden geldiyse taahhütten düşülür
          
            if self.accounts[key].commitment_amount >= doc.amount:
              
                self.accounts[key].commitment_amount -= doc.amount
              
            else:
              
                # Doğrudan fatura ise bütçe kontrolü yapılır
              
                if not self.check_availability(doc.fund_center, doc.commitment_item, doc.amount):
                  
                    return False
                  


            self.accounts[key].actual_amount += doc.amount
          
            logging.info(f"Fiili Harcama Kaydedildi [Actual]. Kasa/Satıcı borçlandırıldı.")
          


        self.documents.append(doc)
      
        return True
      


    def print_budget_report(self):
      
        """FM Bütçe ve Durum Raporunu yazdırır (S_ALR_87013558 simülasyonu)."""
      
        print("\n" + "="*85)
      
        print(f" SAP FM BÜTÇE VE FİİLİ DURUM RAPORU (FM Area: {self.fm_area})")
      
        print("="*85)
      
        print(f"{'Fon Merkezi':<15} | {'Taahhüt Kalemi':<15} | {'Serbest Bütçe':<14} | {'Taahhüt':<10} | {'Fiili Harcama':<12} | {'Kalan Bütçe':<12}")
      
        print("-" * 85)
      
        for key, acc in self.accounts.items():
          
            print(f"{acc.fund_center:<15} | {acc.commitment_item:<15} | {acc.released_budget:>13,.2f} | {acc.commitment_amount:>9,.2f} | {acc.actual_amount:>11,.2f} | {acc.available_budget:>11,.2f}")
          
        print("="*85 + "\n")
      


def main():
  
    print("=== SAP Funds Management (FM) Simülatör Sistemi Çalıştırılıyor ===\n")
  


    # 1. FM Alanı Tanımlama

    fm_sim = SAPFMSimulator(fm_area="TR01")



    # 2. Bütçe Tahsis Etme (FMBB)

    fm_sim.create_budget(fund_center="DEPT_IT", commitment_item="IT_EQUIPMENT", total_amount=500000.0, released_amount=500000.0)

    fm_sim.create_budget(fund_center="DEPT_HR", commitment_item="TRAINING", total_amount=200000.0, released_amount=200000.0)



    # Başlangıç Raporu

    fm_sim.print_budget_report()



    # 3. Senaryo 1: Bilgisayar Alımı için Satın Alma Talebi (PR) - 150.000 TL

    pr_doc = TransactionDocument(doc_type="PR", doc_id="PR-9001", fund_center="DEPT_IT", commitment_item="IT_EQUIPMENT", amount=150000.0)

    fm_sim.post_document(pr_doc)



    # Rapor kontrolü (Taahhüt oluştu, kalan bütçe azaldı)

    fm_sim.print_budget_report()



    # 4. Senaryo 2: PR'ın Satın Alma Siparişine (PO) Dönüşmesi ve Fatura Girişi (Invoice) - 150.000 TL

    inv_doc = TransactionDocument(doc_type="INVOICE", doc_id="INV-5001", fund_center="DEPT_IT", commitment_item="IT_EQUIPMENT", amount=150000.0, vendor="Teknoloji A.Ş.")

    fm_sim.post_document(inv_doc)



    # Rapor kontrolü (Taahhüt kapandı, fiili harcama kesinleşti)

    fm_sim.print_budget_report()















































































