#!/usr/bin/env python3

"""

Modern Yapay Zeka Asistanı (Modern AI Assistant)

Bu betik, OpenAI API kullanarak metin tabanlı akıllı yanıtlar üreten,

güncel ve modüler bir yapay zeka entegrasyon örneğidir.

"""



import os

from openai import OpenAI



def initialize_client():
  
    """OpenAI istemcisini yapılandırır (Sandbox ortamı anahtarlarını kullanır)."""
  
    # Ortam değişkenlerinden otomatik olarak anahtar ve base URL alınır

    return OpenAI()
  


def ask_ai(prompt, model="gpt-4o-mini"):
  
    """Yapay zeka modeline prompt gönderir ve yanıt alır."""
  
    try:
      
        client = initialize_client()
      
        response = client.chat.completions.create(
          
            model=model,
          
            messages=[
              
                {"role": "system", "content": "Sen yardımcı ve bilgili bir yapay zeka asistanısın."},
              
                {"role": "user", "content": prompt}
              
            ],
          
            temperature=0.7,
          
            max_tokens=500
          
          ]
          
        return response.choices[0].message.content
      
    except Exception as e:
      
        return f"Yapay zeka yanıt üretirken bir hata oluştu: {str(e)}"
      


def main():
  
    print("=== Modern Yapay Zeka Asistanına Hoş Geldiniz ===")
  
    sample_prompt = "Yapay zekanın yazılım geliştirme süreçlerindeki rolünü 3 maddede açıkla."
  
    print(f"\nÖrnek Soru: {sample_prompt}\n")
  


    print("Yapay zeka yanıtı hesaplanıyor...")
  
    answer = ask_ai(sample_prompt)
  


    print("\n--- Yapay Zeka Yanıtı ---")
  
    print(answer)
  
    print("-------------------------")
  


if __name__ == "__main__":
  
    main()
  






























