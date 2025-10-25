# LLM Tabanlı Sorgulama ve Yanıt Üretimi

**TÜBİTAK 1505 Projesi**  
**Sorumlular:** Hasan, Eren

## 📋 İçindekiler

- [Genel Bakış](#genel-bakış)
- [Kurulum](#kurulum)
- [Hızlı Başlangıç](#hızlı-başlangıç)
- [Kullanım Örnekleri](#kullanım-örnekleri)
- [API Dokümantasyonu](#api-dokümantasyonu)
- [Yapılandırma](#yapılandırma)

## 🎯 Genel Bakış

Bu modül, TÜBİTAK 1505 Projesi kapsamında LLM (Large Language Model) tabanlı sorgulama ve yanıt üretim altyapısını sağlar. Sistem, iki farklı LLM seçeneği sunar:

1. **OpenAI API** - Bulut tabanlı GPT modelleri
2. **Ollama** - Yerel olarak çalışan açık kaynak modeller (Llama3, Gemma3-12B, Qwen2-8B)

### Temel Özellikler

- ✅ OpenAI ve Ollama LLM desteği
- ✅ RAG (Retrieval-Augmented Generation) mimarisi
- ✅ Qdrant vektör veritabanı entegrasyonu
- ✅ Konuşma geçmişi yönetimi
- ✅ FastAPI tabanlı REST API
- ✅ Güvenli metin işleme
- ✅ Türkçe ve İngilizce dil desteği

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- Ollama (yerel LLM için) veya OpenAI API anahtarı
- Qdrant (opsiyonel, RAG için)

### Adımlar

1. **Bağımlılıkları yükleyin:**

```bash
pip install -r requirements.txt
```

2. **Ortam değişkenlerini ayarlayın:**

```bash
cp .env.example .env
# .env dosyasını düzenleyin ve API anahtarlarınızı ekleyin
```

3. **Ollama'yı yükleyin ve başlatın (yerel LLM için):**

```bash
# Ollama'yı indirin: https://ollama.ai
ollama serve

# Model indirin
ollama pull llama3
# veya
ollama pull gemma3:12b
# veya
ollama pull qwen2:8b
```

## ⚡ Hızlı Başlangıç

### 1. Basit OpenAI Örneği

```python
from langchain_openai import OpenAI

llm = OpenAI(api_key="YOUR_OPENAI_API_KEY")
prompt = "Türkiye'nin başkenti neresidir?"
response = llm.invoke(prompt)
print(response)
```

Veya örnek scripti çalıştırın:

```bash
export OPENAI_API_KEY="your-key-here"
python examples/simple_openai_example.py
```

### 2. Ollama ile Yerel LLM

```python
from src.llm_query import LLMQuerySystem

# Sistem oluştur
llm_system = LLMQuerySystem(use_openai=False)

# Sorgu yap
result = llm_system.query(
    prompt="TÜBİTAK 1505 programı nedir?",
    language="tr"
)

print(result["response"])
```

Veya örnek scripti çalıştırın:

```bash
python examples/ollama_example.py
```

### 3. RAG ile Bağlam Tabanlı Yanıt

```python
from src.llm_query import LLMQuerySystem

llm_system = LLMQuerySystem(use_openai=False)

# Bağlam ile sorgu
context = "TÜBİTAK 1505 Programı, üniversite-sanayi işbirliği projelerini destekler..."
result = llm_system.query(
    prompt="TÜBİTAK 1505 neyi destekler?",
    context=context,
    language="tr"
)

print(result["response"])
```

Veya örnek scripti çalıştırın:

```bash
python examples/rag_example.py
```

### 4. FastAPI Servisi

```bash
# Servisi başlat
cd src
python api_service.py

# Veya uvicorn ile
uvicorn src.api_service:app --reload --host 0.0.0.0 --port 8000
```

API'ye istek gönder:

```bash
curl -X POST "http://localhost:8000/ask/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Türkiye'\''nin başkenti neresidir?",
    "use_openai": false,
    "language": "tr"
  }'
```

## 📚 Kullanım Örnekleri

### Temel Sorgu

```python
from src.llm_query import LLMQuerySystem

# LLM sistemi oluştur
llm = LLMQuerySystem(use_openai=False)

# Sorgu yap
result = llm.query(prompt="Python nedir?")

if result["success"]:
    print(f"Yanıt: {result['response']}")
    print(f"Model: {result['model']}")
else:
    print(f"Hata: {result['error']}")
```

### LangChain Chain Kullanımı

```python
from src.llm_query import LLMQuerySystem

llm = LLMQuerySystem(use_openai=False)

# Özel şablon ile sorgu
template = """Sen bir yapay zeka asistanısın.
Soru: {question}
Yanıt:"""

result = llm.query_with_chain(
    prompt="Yapay zeka nedir?",
    template=template
)

print(result["response"])
```

### Konuşma Geçmişi

```python
from src.llm_query import LLMQuerySystem

llm = LLMQuerySystem(use_openai=False)

# İlk sorgu
llm.query(prompt="Python nedir?")

# İkinci sorgu (bağlam korunur)
llm.query(prompt="Hangi alanlarda kullanılır?")

# Geçmişi görüntüle
history = llm.get_conversation_history()
print(f"Toplam {len(history)} mesaj")

# Geçmişi temizle
llm.clear_memory()
```

## 🔌 API Dokümantasyonu

### Endpoint'ler

#### `POST /ask/`

Soru sor ve yanıt al.

**İstek Gövdesi:**
```json
{
  "question": "Soru metni",
  "document_id": "optional-doc-id",
  "collection_name": "optional-collection",
  "use_openai": false,
  "language": "tr"
}
```

**Yanıt:**
```json
{
  "success": true,
  "response": "LLM yanıtı",
  "model": "llama3",
  "sources": ["kaynak1", "kaynak2"],
  "error": null
}
```

#### `GET /health/`

Sistem durumu kontrolü.

**Yanıt:**
```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "ollama_available": true,
  "openai_available": false
}
```

#### `POST /clear-memory/`

Konuşma geçmişini temizle.

**Parametreler:**
- `use_openai`: boolean (varsayılan: false)

### Swagger Dokümantasyonu

API çalışırken şu adreste interaktif dokümantasyon bulunur:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## ⚙️ Yapılandırma

### Ortam Değişkenleri

`.env` dosyasında aşağıdaki değişkenleri ayarlayın:

```bash
# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=my_collection

# OpenAI
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# LLM Parametreleri
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=500
MEMORY_WINDOW_SIZE=5
TOP_K_RESULTS=5
```

### Model Seçenekleri

#### OpenAI Modelleri
- `gpt-3.5-turbo` (hızlı, ekonomik)
- `gpt-4` (daha güçlü, pahalı)
- `gpt-4-turbo`

#### Ollama Modelleri
- `llama3` - Meta'nın güçlü modeli
- `gemma3:12b` - Google'ın 12B parametreli modeli
- `qwen2:8b` - Alibaba'nın 8B parametreli modeli
- `mistral` - Mistral AI modeli

## 📖 Detaylı Dokümantasyon

Daha fazla bilgi için:

- [LLM Yanıt Sistemi Teknik Rehberi](../docs/4_llm_response_guide.md)
- [Tam İş Akışı](../docs/5_complete_workflow.md)
- [Genel README](../README.md)

## 🤝 Katkıda Bulunanlar

- **Hasan** - LLM entegrasyonu ve yanıt üretimi
- **Eren** - Qdrant entegrasyonu ve API geliştirme

## 📞 Destek

Sorular için lütfen GitHub Issues bölümünü kullanın.
