# Bilimp Terracity - Teknik Dokümantasyon

## 📋 Proje Özeti

Bu proje, Terracity firmasının Bilimp yazılımı için geliştirilmiş AI destekli doküman asistanı sistemidir. Sistem dört ana modülden oluşmaktadır ve her modül belirli ekip üyeleri tarafından geliştirilmiştir.

## 🏗️ Mimari Tasarım

### Genel Akış

```
Dokümanlar (PDF, DOCX, TXT, XLSX)
         ↓
[1. Preprocessing Module] → Chunk'lara ayırma
         ↓
[2. Embedding Module] → Vektör dönüşümü (1024-dim)
         ↓
[3. Database Module] → Qdrant'a yükleme
         ↓
[4. LLM Module] → Sorgulama & Yanıt üretimi
```

## 📦 Modül Detayları

### 1. Document Preprocessing Module
**Dosya**: `src/preprocessing/document_processor.py`  
**Sorumlular**: Engin, Batuhan

**Özellikler**:
- Çoklu format desteği (PDF, DOCX, TXT, XLSX)
- LangChain tabanlı doküman yükleme
- RecursiveCharacterTextSplitter ile akıllı chunking
- Özelleştirilebilir chunk boyutu ve overlap
- Metadata yönetimi

**Temel Sınıflar**:
```python
class DocumentProcessor:
    def __init__(self, chunk_size=512, chunk_overlap=50)
    def load_document(self, file_path) -> List[Dict]
    def chunk_documents(self, documents) -> List[Dict]
    def process_directory(self, directory_path) -> List[Dict]
```

**Kullanım**:
```python
processor = DocumentProcessor(chunk_size=512, chunk_overlap=50)
chunks = processor.process_directory("data/raw")
```

### 2. Embedding Generation Module
**Dosya**: `src/embeddings/embedding_generator.py`  
**Sorumlular**: Mehmet, Hasan

**Özellikler**:
- Multilingual-e5-large model (Cosmos-e5-large olarak referans edilir)
- 1024 boyutlu embedding vektörleri
- Batch processing ile yüksek performans
- GPU/CPU otomatik algılama
- Query ve passage embedding ayrımı

**Temel Sınıflar**:
```python
class EmbeddingGenerator:
    def __init__(self, model_name="intfloat/multilingual-e5-large", batch_size=32)
    def generate_embedding(self, text) -> np.ndarray
    def generate_embeddings_batch(self, texts) -> List[np.ndarray]
    def process_chunks(self, chunks) -> List[Dict]
    def generate_query_embedding(self, query) -> np.ndarray
```

**Kullanım**:
```python
generator = EmbeddingGenerator()
chunks_with_embeddings = generator.process_chunks(chunks)
```

**Model Detayları**:
- Model: intfloat/multilingual-e5-large
- Embedding Boyutu: 1024
- Dil Desteği: Çoklu dil (Türkçe dahil)
- Prefix: "passage:" (dokümanlar için), "query:" (sorgular için)

### 3. Qdrant Database Module
**Dosya**: `src/database/qdrant_client.py`  
**Sorumlular**: Süleyman, Eren

**Özellikler**:
- Qdrant vektör veritabanı entegrasyonu
- Otomatik collection yönetimi
- Batch upload desteği
- Cosine similarity search
- Metadata filtreleme
- Collection bilgi sorgulama

**Temel Sınıflar**:
```python
class QdrantDatabase:
    def __init__(self, host="localhost", port=6333, collection_name="bilimp_documents", embedding_dim=1024)
    def upload_chunks(self, chunks, batch_size=100) -> int
    def search(self, query_embedding, limit=5, score_threshold=None, filters=None) -> List[Dict]
    def get_collection_info() -> Dict
    def delete_collection()
```

**Kullanım**:
```python
db = QdrantDatabase(host="localhost", port=6333)
db.upload_chunks(chunks_with_embeddings)
results = db.search(query_embedding, limit=5)
```

**Veritabanı Yapısı**:
- Distance Metric: Cosine Similarity
- Vector Size: 1024
- Payload: text (string), metadata (dict)

### 4. LLM Integration Module
**Dosya**: `src/llm/llm_client.py`  
**Sorumlular**: Hasan, Eren

**Özellikler**:
- Ollama API entegrasyonu
- Çoklu model desteği (Gemma3-12B, Qwen3-9B)
- RAG (Retrieval-Augmented Generation) pipeline
- Context-aware response generation
- Türkçe prompt optimizasyonu

**Temel Sınıflar**:
```python
class LLMClient:
    def __init__(self, base_url="http://localhost:11434", gemma_model="gemma3:12b", qwen_model="qwen3:9b")
    def generate_response(self, query, context, model=None) -> str
    def generate_with_gemma(self, query, context) -> str
    def generate_with_qwen(self, query, context) -> str
    def generate_with_both_models(self, query, context) -> Dict[str, str]

class RAGSystem:
    def __init__(self, database, embedding_generator, llm_client, top_k=5)
    def query(self, query, model=None, temperature=0.7) -> Dict
```

**Kullanım**:
```python
llm_client = LLMClient()
rag_system = RAGSystem(db, generator, llm_client, top_k=5)
result = rag_system.query("Bilimp nedir?")
```

**RAG Pipeline**:
1. Query embedding üretimi
2. Qdrant'tan benzer dokümanları getirme
3. Context oluşturma
4. LLM ile yanıt üretimi

## 🐳 Docker Altyapısı

### docker-compose.yml

İki temel servis:

1. **Qdrant**: Vektör veritabanı
   - Port: 6333 (REST), 6334 (gRPC)
   - Volume: ./qdrant_storage
   - Otomatik restart

2. **Ollama**: LLM runtime
   - Port: 11434
   - Volume: ./ollama_models
   - GPU desteği
   - Otomatik restart

### Servis Yönetimi

```bash
# Başlat
docker-compose up -d

# Durdur
docker-compose down

# Logları görüntüle
docker-compose logs -f

# Servis durumu
docker-compose ps
```

## 🔄 Main Pipeline

**Dosya**: `main.py`

Ana orchestration sınıfı tüm modülleri koordine eder.

### BilimpPipeline Sınıfı

```python
class BilimpPipeline:
    def initialize_components()           # Tüm modülleri başlat
    def process_documents(input_dir)      # Dokümanları işle
    def generate_embeddings(chunks)       # Embedding üret
    def upload_to_database(chunks)        # Qdrant'a yükle
    def run_full_pipeline(input_dir)      # Tüm pipeline'ı çalıştır
    def query_system(query, model)        # Sistemi sorgula
```

### Kullanım Modları

1. **Process Mode**: Dokümanları işle ve yükle
```bash
python main.py --mode process --input-dir data/raw
```

2. **Query Mode**: Sistemi sorgula
```bash
python main.py --mode query --query "Soru" --model gemma
```

3. **Info Mode**: Sistem bilgisi
```bash
python main.py --mode info
```

## ⚙️ Konfigürasyon

### Ortam Değişkenleri (.env)

```env
# Embedding Ayarları
EMBEDDING_MODEL=intfloat/multilingual-e5-large
EMBEDDING_DIMENSION=1024
CHUNK_SIZE=512
CHUNK_OVERLAP=50

# Qdrant Ayarları
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=bilimp_documents

# LLM Ayarları
GEMMA_MODEL=gemma3:12b
QWEN_MODEL=qwen3:9b
OLLAMA_BASE_URL=http://localhost:11434

# İşlem Ayarları
MAX_WORKERS=4
BATCH_SIZE=32
```

### Varsayılan Değerler

Eğer .env dosyası yoksa veya bir değişken tanımlı değilse, kod içinde varsayılan değerler kullanılır.

## 📊 Performans Metrikleri

### Beklenen Performans

- **Doküman İşleme**: ~50-100 sayfa/saniye
- **Embedding Üretimi**: 
  - GPU: ~100 chunk/saniye
  - CPU: ~10-20 chunk/saniye
- **Vektör Upload**: ~1000 chunk/saniye
- **Similarity Search**: <100ms (1M vektör)
- **LLM Response**: 2-5 saniye

### Sistem Gereksinimleri

**Minimum**:
- CPU: 4 cores
- RAM: 8GB
- Disk: 20GB

**Önerilen**:
- CPU: 8+ cores
- RAM: 16GB+
- GPU: NVIDIA 8GB+ VRAM
- Disk: 50GB+ SSD

## 🔐 Güvenlik Notları

1. `.env` dosyası git'e commit edilmemeli
2. Üretim ortamında Qdrant authentication aktif edilmeli
3. Ollama sadece güvenilir ağlardan erişilebilir olmalı
4. API rate limiting uygulanmalı

## 🧪 Test Stratejisi

### Birim Testleri
Her modül için ayrı test dosyaları oluşturulabilir:
- `tests/test_preprocessing.py`
- `tests/test_embeddings.py`
- `tests/test_database.py`
- `tests/test_llm.py`

### Entegrasyon Testi
`example_usage.py` dosyası tam pipeline'ı test eder.

### Test Komutu
```bash
python example_usage.py
```

## 📈 Ölçeklendirme

### Horizontal Scaling
- Qdrant cluster kurulumu
- Multiple Ollama instances
- Load balancing

### Vertical Scaling
- GPU upgrade
- RAM artırımı
- Batch size optimizasyonu

## 🔧 Bakım ve İzleme

### Log Yönetimi
Tüm modüller Python logging kullanır:
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Monitoring
- Qdrant metrics: http://localhost:6333/metrics
- Docker stats: `docker stats`
- Application logs: Python logging output

## 📚 Bağımlılıklar

### Ana Kütüphaneler
- **langchain**: Document loading ve processing
- **sentence-transformers**: Embedding generation
- **qdrant-client**: Vector database
- **requests**: HTTP communication
- **torch**: Deep learning backend

### Tam Liste
Tüm bağımlılıklar `requirements.txt` dosyasında.

## 🚀 Deployment

### Development
```bash
./setup.sh
python example_usage.py
```

### Production
1. Environment variables ayarla
2. Docker compose ile servisleri başlat
3. Systemd service oluştur
4. Nginx reverse proxy
5. SSL/TLS yapılandır

## 📝 Versiyon Geçmişi

- **v1.0.0** (2024-10-24): İlk release
  - Tüm temel modüller implementasyonu
  - Docker altyapısı
  - Dokümantasyon

## 👥 Katkıda Bulunanlar

| Modül | Sorumlular |
|-------|------------|
| Document Processing | Engin, Batuhan |
| Embedding Generation | Mehmet, Hasan |
| Database Management | Süleyman, Eren |
| LLM Integration | Hasan, Eren |

## 🎯 Gelecek Geliştirmeler

- [ ] Web UI eklenmesi
- [ ] REST API endpoint'leri
- [ ] Çoklu dil desteği genişletme
- [ ] Streaming response support
- [ ] Fine-tuning capabilities
- [ ] Advanced analytics dashboard
- [ ] User authentication system
- [ ] Document update/delete operations
- [ ] Incremental indexing
- [ ] A/B testing framework

## 📞 Destek

Teknik destek için:
- GitHub Issues: [Bilimp_Terracity/issues](https://github.com/mehmetbozdemir24/Bilimp_Terracity/issues)
- Repository: [Bilimp_Terracity](https://github.com/mehmetbozdemir24/Bilimp_Terracity)
