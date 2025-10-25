# LLM Sistemi - Hızlı Başlangıç

**TÜBİTAK 1505 Projesi**  
**Sorumlular:** Hasan, Eren

## 📦 Kurulum (1 Dakika)

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Ortam değişkenlerini ayarla
cp .env.example .env
# .env dosyasını düzenleyin

# 3. Test et
python examples/test_installation.py
```

## 🚀 Kullanım

### Seçenek 1: Basit OpenAI Örneği (Issue'daki kod)

```bash
export OPENAI_API_KEY="your-key-here"
python examples/simple_openai_example.py
```

### Seçenek 2: Ollama (Yerel LLM)

```bash
# Terminal 1: Ollama'yı başlat
ollama serve

# Terminal 2: Model indir ve örneği çalıştır
ollama pull llama3
python examples/ollama_example.py
```

### Seçenek 3: RAG Sistemi

```bash
python examples/rag_example.py
```

### Seçenek 4: API Servisi

```bash
# Servisi başlat
python src/api_service.py

# Başka bir terminalde test et
curl -X POST "http://localhost:8000/ask/" \
  -H "Content-Type: application/json" \
  -d '{"question": "Python nedir?", "language": "tr"}'

# Swagger UI: http://localhost:8000/docs
```

## 📚 Kullanım Örnekleri

### Python Kodu ile Kullanım

```python
from src.llm_query import LLMQuerySystem

# LLM sistemi oluştur
llm = LLMQuerySystem(use_openai=False)  # Ollama için
# llm = LLMQuerySystem(use_openai=True)  # OpenAI için

# Basit sorgu
result = llm.query(prompt="Python nedir?", language="tr")
print(result["response"])

# RAG ile sorgu (bağlam ile)
context = "Python, yüksek seviyeli bir programlama dilidir..."
result = llm.query(
    prompt="Python neye benzer?",
    context=context,
    language="tr"
)
print(result["response"])
```

## 🔧 Yapılandırma

`.env` dosyasında:

```bash
# Ollama için (yerel)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# OpenAI için (bulut)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo

# Qdrant için (opsiyonel)
QDRANT_URL=http://localhost:6333
```

## 📖 Dokümantasyon

- **Detaylı Kılavuz:** [src/README.md](src/README.md)
- **LLM Yanıt Rehberi:** [docs/4_llm_response_guide.md](docs/4_llm_response_guide.md)
- **Tam İş Akışı:** [docs/5_complete_workflow.md](docs/5_complete_workflow.md)

## 🎯 Desteklenen Modeller

### OpenAI
- gpt-3.5-turbo
- gpt-4
- gpt-4-turbo

### Ollama (Yerel)
- llama3
- gemma3:12b (Gemma3-12B)
- qwen2:8b (Qwen3-8B)
- mistral

## ✅ Test

```bash
# Kurulum testi
python examples/test_installation.py

# Syntax kontrolü
python -m py_compile src/*.py examples/*.py
```

## 🆘 Sorun Giderme

### "No module named 'langchain'"
```bash
pip install -r requirements.txt
```

### Ollama bağlantı hatası
```bash
# Ollama'nın çalıştığından emin olun
ollama serve
```

### OpenAI API hatası
```bash
# API anahtarını kontrol edin
echo $OPENAI_API_KEY
```

## 📞 Yardım

Sorularınız için:
- Issue açın: GitHub Issues
- Dokümantasyon: [src/README.md](src/README.md)

---

**Hazır! Sisteminiz kullanıma hazır.** 🎉
