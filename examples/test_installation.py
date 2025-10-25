"""
Kurulum Test Scripti
Bu script, LLM sisteminin düzgün kurulup kurulmadığını kontrol eder.
"""
import sys
import os

# src klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def check_imports():
    """Gerekli kütüphanelerin yüklenip yüklenmediğini kontrol et"""
    print("=" * 60)
    print("Kütüphane Kontrolü")
    print("=" * 60)
    
    required_packages = [
        ("langchain", "langchain"),
        ("langchain_openai", "langchain-openai"),
        ("langchain_community", "langchain-community"),
        ("fastapi", "fastapi"),
        ("pydantic", "pydantic"),
        ("qdrant_client", "qdrant-client"),
        ("uvicorn", "uvicorn"),
    ]
    
    all_ok = True
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"✓ {package_name:25} - Yüklü")
        except ImportError:
            print(f"✗ {package_name:25} - Eksik")
            all_ok = False
    
    return all_ok


def check_modules():
    """Proje modüllerinin çalışıp çalışmadığını kontrol et"""
    print("\n" + "=" * 60)
    print("Modül Kontrolü")
    print("=" * 60)
    
    all_ok = True
    
    # Config modülü
    try:
        from src.config import config
        print(f"✓ config modülü - Yüklü")
    except Exception as e:
        print(f"✗ config modülü - Hata: {e}")
        all_ok = False
    
    # Utils modülü
    try:
        from src.utils import safe_text, format_context
        print(f"✓ utils modülü - Yüklü")
    except Exception as e:
        print(f"✗ utils modülü - Hata: {e}")
        all_ok = False
    
    # LLM Query modülü
    try:
        from src.llm_query import LLMQuerySystem
        print(f"✓ llm_query modülü - Yüklü")
    except Exception as e:
        print(f"✗ llm_query modülü - Hata: {e}")
        all_ok = False
    
    # API Service modülü
    try:
        from src.api_service import app
        print(f"✓ api_service modülü - Yüklü")
    except Exception as e:
        print(f"✗ api_service modülü - Hata: {e}")
        all_ok = False
    
    return all_ok


def check_config():
    """Yapılandırma ayarlarını kontrol et"""
    print("\n" + "=" * 60)
    print("Yapılandırma Kontrolü")
    print("=" * 60)
    
    try:
        from src.config import config
        
        print(f"QDRANT_URL: {config.QDRANT_URL}")
        print(f"OLLAMA_BASE_URL: {config.OLLAMA_BASE_URL}")
        print(f"OLLAMA_MODEL: {config.OLLAMA_MODEL}")
        
        if config.OPENAI_API_KEY:
            print(f"OPENAI_API_KEY: Ayarlanmış ✓")
            print(f"OPENAI_MODEL: {config.OPENAI_MODEL}")
        else:
            print(f"OPENAI_API_KEY: Ayarlanmamış (Opsiyonel)")
        
        print(f"\nLLM Parametreleri:")
        print(f"  Temperature: {config.LLM_TEMPERATURE}")
        print(f"  Max Tokens: {config.LLM_MAX_TOKENS}")
        print(f"  Memory Window: {config.MEMORY_WINDOW_SIZE}")
        
        return True
    except Exception as e:
        print(f"✗ Yapılandırma hatası: {e}")
        return False


def main():
    """Ana test fonksiyonu"""
    print("\n" + "=" * 60)
    print("TÜBİTAK 1505 - LLM Sistemi Kurulum Testi")
    print("=" * 60 + "\n")
    
    # Testleri çalıştır
    imports_ok = check_imports()
    modules_ok = check_modules()
    config_ok = check_config()
    
    # Sonuç
    print("\n" + "=" * 60)
    print("Test Sonuçları")
    print("=" * 60)
    
    if imports_ok and modules_ok and config_ok:
        print("✓ Tüm testler başarılı!")
        print("\nSistem kullanıma hazır.")
        print("\nÖrnekleri çalıştırmak için:")
        print("  python examples/ollama_example.py")
        print("  python examples/rag_example.py")
        print("\nAPI servisini başlatmak için:")
        print("  python src/api_service.py")
        return 0
    else:
        print("✗ Bazı testler başarısız oldu.")
        print("\nLütfen eksik paketleri yükleyin:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
