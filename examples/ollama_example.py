"""
Ollama ile Yerel LLM Örneği
TÜBİTAK 1505 Projesi

Gemma3-12B veya Qwen3-8B gibi yerel modeller ile kullanım örneği.
"""
import sys
import os

# src klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.llm_query import LLMQuerySystem


def main():
    """Ollama LLM ile basit örnek"""
    
    print("=" * 60)
    print("TÜBİTAK 1505 - Ollama LLM Örneği")
    print("=" * 60)
    
    try:
        # Ollama LLM sistemini başlat
        print("\nOllama LLM sistemi başlatılıyor...")
        llm_system = LLMQuerySystem(use_openai=False)
        print(f"Model: {llm_system.model_name}")
        
        # Örnek sorular
        questions = [
            "Türkiye'nin başkenti neresidir?",
            "TÜBİTAK 1505 programı nedir?",
            "Yapay zeka nedir?"
        ]
        
        for question in questions:
            print(f"\n{'=' * 60}")
            print(f"Soru: {question}")
            print("Yanıt üretiliyor...\n")
            
            result = llm_system.query(prompt=question, language="tr")
            
            if result["success"]:
                print("Yanıt:")
                print("-" * 60)
                print(result["response"])
                print("-" * 60)
            else:
                print(f"HATA: {result['error']}")
        
        print(f"\n{'=' * 60}")
        print("Örnek tamamlandı.")
        
    except Exception as e:
        print(f"\nHATA: {e}")
        print("\nOllama'nın çalıştığından emin olun:")
        print("  ollama serve")
        print("\nVe gerekli modelin indirildiğinden emin olun:")
        print("  ollama pull llama3")


if __name__ == "__main__":
    main()
