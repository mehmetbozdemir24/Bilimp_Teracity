"""
Yapılandırma modülü - Sistem ayarları ve ortam değişkenleri
"""
import os
from typing import Optional


class Config:
    """Sistem yapılandırma sınıfı"""
    
    # Qdrant Yapılandırması
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY", None)
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "my_collection")
    
    # OpenAI Yapılandırması
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Ollama Yapılandırması (Yerel LLM için)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    
    # LLM Parametreleri
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "500"))
    
    # Bellek Yapılandırması
    MEMORY_WINDOW_SIZE: int = int(os.getenv("MEMORY_WINDOW_SIZE", "5"))
    
    # Retrieval Parametreleri
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "5"))
    
    @classmethod
    def validate(cls) -> bool:
        """Zorunlu yapılandırma ayarlarını doğrula"""
        if not cls.OPENAI_API_KEY and not cls.OLLAMA_BASE_URL:
            raise ValueError(
                "En az bir LLM yapılandırması gerekli: "
                "OPENAI_API_KEY veya OLLAMA_BASE_URL"
            )
        return True


config = Config()
