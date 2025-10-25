"""
RAG (Retrieval-Augmented Generation) Tam Örneği
TÜBİTAK 1505 Projesi

Qdrant vektör veritabanı ile entegre tam RAG örneği.
"""
import sys
import os

# src klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.llm_query import LLMQuerySystem
from qdrant_client import QdrantClient
from src.config import config


def main():
    """RAG sistemi ile tam örnek"""
    
    print("=" * 60)
    print("TÜBİTAK 1505 - RAG Sistemi Örneği")
    print("=" * 60)
    
    try:
        # LLM sistemini başlat (Ollama kullanarak)
        print("\n1. LLM sistemi başlatılıyor...")
        llm_system = LLMQuerySystem(use_openai=False)
        print(f"   ✓ Model: {llm_system.model_name}")
        
        # Qdrant client'ı başlat
        print("\n2. Qdrant bağlantısı kuruluyor...")
        qdrant_client = QdrantClient(
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY
        )
        print(f"   ✓ Bağlantı: {config.QDRANT_URL}")
        
        # Örnek bağlam (gerçek uygulamada Qdrant'tan gelir)
        example_context = """
        TÜBİTAK 1505 Programı, üniversite-sanayi işbirliği kapsamında 
        teknoloji transfer ofisleri aracılığıyla yapılan araştırma ve 
        geliştirme projelerini destekleyen bir programdır. 
        Program, yenilikçi ürün ve süreç geliştirme çalışmalarına 
        destek sağlar ve teknolojik gelişmeyi teşvik eder.
        """
        
        # RAG ile sorgu örneği
        print("\n3. RAG sorgusu yapılıyor...")
        question = "TÜBİTAK 1505 Programı neyi destekler?"
        
        print(f"\n{'=' * 60}")
        print(f"Soru: {question}")
        print("\nBağlam:")
        print("-" * 60)
        print(example_context.strip())
        print("-" * 60)
        print("\nYanıt üretiliyor...\n")
        
        # LLM'den bağlam ile yanıt al
        result = llm_system.query(
            prompt=question,
            context=example_context,
            language="tr"
        )
        
        if result["success"]:
            print("LLM Yanıtı:")
            print("=" * 60)
            print(result["response"])
            print("=" * 60)
            print(f"\nKullanılan Model: {result['model']}")
        else:
            print(f"HATA: {result['error']}")
        
        # Konuşma geçmişi
        print("\n4. Konuşma geçmişi:")
        history = llm_system.get_conversation_history()
        print(f"   Toplam {len(history)} mesaj kaydedildi.")
        
        print("\n" + "=" * 60)
        print("RAG örneği tamamlandı!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nHATA: {e}")
        print("\nGereksinimler:")
        print("1. Ollama'nın çalıştığından emin olun: ollama serve")
        print("2. Model indirilmiş olmalı: ollama pull llama3")
        print("3. Qdrant çalışıyor olmalı (opsiyonel)")


if __name__ == "__main__":
    main()
