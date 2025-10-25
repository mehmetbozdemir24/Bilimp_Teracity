"""
Basit OpenAI LLM Örneği
TÜBİTAK 1505 Projesi - LLM Tabanlı Sorgulama
Sorumlular: Hasan, Eren

Bu örnek, issue'da belirtilen basit kod örneğini içerir.
"""
import os
from langchain_openai import OpenAI


def main():
    """Basit OpenAI LLM örneği"""
    
    # API anahtarını kontrol et
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("HATA: OPENAI_API_KEY ortam değişkeni ayarlanmalıdır.")
        print("Kullanım: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # OpenAI LLM'yi başlat
    llm = OpenAI(api_key=api_key)
    
    # Basit bir prompt
    prompt = "Türkiye'nin başkenti neresidir?"
    
    print("=" * 60)
    print("TÜBİTAK 1505 - Basit OpenAI LLM Örneği")
    print("=" * 60)
    print(f"\nSoru: {prompt}")
    print("\nYanıt üretiliyor...\n")
    
    # Yanıt al
    response = llm.invoke(prompt)
    
    print("Yanıt:")
    print("-" * 60)
    print(response)
    print("-" * 60)


if __name__ == "__main__":
    main()
