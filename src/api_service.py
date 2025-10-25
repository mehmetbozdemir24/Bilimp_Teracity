"""
FastAPI Servis - LLM tabanlı sorgulama API'si
Sorumlular: Hasan, Eren
"""
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient
from qdrant_client.http import models

from .config import config
from .llm_query import LLMQuerySystem
from .utils import format_context, safe_text


# FastAPI uygulaması
app = FastAPI(
    title="TÜBİTAK 1505 LLM API",
    description="LLM tabanlı sorgulama ve yanıt üretim servisi",
    version="1.0.0"
)


# Request/Response modelleri
class QueryInput(BaseModel):
    """Sorgu giriş modeli"""
    question: str = Field(..., description="Kullanıcının sorusu")
    document_id: Optional[str] = Field(None, description="Belge ID (opsiyonel)")
    collection_name: Optional[str] = Field(None, description="Koleksiyon adı")
    use_openai: bool = Field(False, description="OpenAI kullan (varsayılan: Ollama)")
    language: str = Field("tr", description="Yanıt dili (tr/en)")


class QueryResponse(BaseModel):
    """Sorgu yanıt modeli"""
    success: bool
    response: Optional[str]
    model: Optional[str]
    sources: Optional[List[str]] = None
    error: Optional[str] = None


# Global değişkenler
qdrant_client: Optional[QdrantClient] = None
llm_system_openai: Optional[LLMQuerySystem] = None
llm_system_ollama: Optional[LLMQuerySystem] = None


@app.on_event("startup")
async def startup_event():
    """Uygulama başlangıcında çalışır"""
    global qdrant_client, llm_system_ollama, llm_system_openai
    
    # Qdrant client'ı başlat
    try:
        qdrant_client = QdrantClient(
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY
        )
        print(f"Qdrant bağlantısı başarılı: {config.QDRANT_URL}")
    except Exception as e:
        print(f"Qdrant bağlantısı kurulamadı: {e}")
        qdrant_client = None
    
    # Ollama LLM sistemini başlat
    try:
        llm_system_ollama = LLMQuerySystem(use_openai=False)
        print(f"Ollama LLM sistemi başlatıldı: {config.OLLAMA_MODEL}")
    except Exception as e:
        print(f"Ollama LLM başlatılamadı: {e}")
    
    # OpenAI LLM sistemini başlat (API key varsa)
    if config.OPENAI_API_KEY:
        try:
            llm_system_openai = LLMQuerySystem(use_openai=True)
            print(f"OpenAI LLM sistemi başlatıldı: {config.OPENAI_MODEL}")
        except Exception as e:
            print(f"OpenAI LLM başlatılamadı: {e}")


def get_context_from_qdrant(
    question: str,
    collection_name: str,
    document_id: Optional[str] = None,
    top_k: int = 5
) -> tuple[str, List[str]]:
    """
    Qdrant'tan ilgili bağlamı alır
    
    Args:
        question: Kullanıcı sorusu
        collection_name: Qdrant koleksiyon adı
        document_id: Filtrelenecek belge ID'si
        top_k: Döndürülecek sonuç sayısı
        
    Returns:
        (formatlanmış_bağlam, kaynak_listesi) tuple
    """
    if not qdrant_client:
        return "Vektör veritabanı bağlantısı mevcut değil.", []
    
    try:
        # Basit arama (gerçek uygulamada question'ı embedding'e çevirmek gerekir)
        # Bu örnekte text-based filter kullanıyoruz
        search_filter = None
        if document_id:
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=document_id)
                    )
                ]
            )
        
        # Not: Gerçek uygulamada query_vector yerine question'ın embedding'i kullanılmalıdır
        # Bu örnek için basitleştirilmiş bir yaklaşım kullanılıyor
        
        # Koleksiyon bilgilerini al
        collection_info = qdrant_client.get_collection(collection_name)
        
        # Formatlanmış bağlam oluştur
        context = f"Koleksiyon '{collection_name}' üzerinde arama yapıldı."
        sources = [collection_name]
        
        return context, sources
        
    except Exception as e:
        print(f"Qdrant arama hatası: {e}")
        return f"Vektör veritabanı araması sırasında hata: {str(e)}", []


@app.get("/")
async def root():
    """Ana sayfa"""
    return {
        "message": "TÜBİTAK 1505 LLM API",
        "version": "1.0.0",
        "endpoints": {
            "POST /ask/": "Soru sor ve yanıt al",
            "GET /health/": "Sistem durumu",
            "POST /clear-memory/": "Konuşma geçmişini temizle"
        }
    }


@app.get("/health/")
async def health_check():
    """Sistem sağlık kontrolü"""
    return {
        "status": "healthy",
        "qdrant_connected": qdrant_client is not None,
        "ollama_available": llm_system_ollama is not None,
        "openai_available": llm_system_openai is not None,
        "config": {
            "qdrant_url": config.QDRANT_URL,
            "ollama_model": config.OLLAMA_MODEL,
            "openai_model": config.OPENAI_MODEL if config.OPENAI_API_KEY else "Not configured"
        }
    }


@app.post("/ask/", response_model=QueryResponse)
async def ask(query_input: QueryInput):
    """
    Kullanıcı sorusunu işler ve yanıt döndürür
    
    RAG akışı:
    1. Soruyu al
    2. Qdrant'tan ilgili bağlamı çek (varsa)
    3. LLM ile yanıt üret
    4. Güvenli yanıtı döndür
    """
    try:
        # LLM sistemini seç
        llm_system = llm_system_openai if query_input.use_openai else llm_system_ollama
        
        if llm_system is None:
            raise HTTPException(
                status_code=503,
                detail="LLM servisi kullanılabilir değil"
            )
        
        # Bağlam al (Qdrant'tan)
        context = None
        sources = None
        if qdrant_client and query_input.collection_name:
            context, sources = get_context_from_qdrant(
                question=query_input.question,
                collection_name=query_input.collection_name,
                document_id=query_input.document_id,
                top_k=config.TOP_K_RESULTS
            )
        
        # LLM ile yanıt üret
        result = llm_system.query(
            prompt=query_input.question,
            context=context,
            language=query_input.language
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "LLM yanıt üretiminde hata")
            )
        
        return QueryResponse(
            success=True,
            response=result["response"],
            model=result["model"],
            sources=sources,
            error=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"İşlem sırasında hata: {str(e)}"
        )


@app.post("/clear-memory/")
async def clear_memory(use_openai: bool = False):
    """Konuşma geçmişini temizler"""
    try:
        llm_system = llm_system_openai if use_openai else llm_system_ollama
        
        if llm_system is None:
            raise HTTPException(
                status_code=503,
                detail="LLM servisi kullanılabilir değil"
            )
        
        llm_system.clear_memory()
        
        return {
            "success": True,
            "message": "Konuşma geçmişi temizlendi"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Bellek temizleme hatası: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
