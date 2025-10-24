# Bilimp - Hızlı Başlangıç Kılavuzu

Bu kılavuz, Bilimp sistemini kurmanız ve kullanmanız için adım adım talimatlar içerir.

## Kurulum

### 1. Python Ortamını Hazırlayın

```bash
# Python 3.8 veya üzeri gereklidir
python --version

# Sanal ortam oluşturun (önerilir)
python -m venv venv

# Sanal ortamı aktif edin
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. Bağımlılıkları Yükleyin

```bash
# Gerekli paketleri yükleyin
pip install -r requirements.txt

# İndirme uzun sürebilir (özellikle PyTorch)
```

### 3. Qdrant'ı Başlatın

```bash
# Docker Compose ile başlatın
docker-compose up -d

# Durum kontrolü
docker ps | grep qdrant

# Qdrant web arayüzü: http://localhost:6333/dashboard
```

## Kullanım

### Mod 1: Doküman İşleme

Dokümanları sisteme yükleyin:

```bash
python main.py --mode process --documents dokuman1.pdf dokuman2.pdf
```

### Mod 2: Tek Soru

Tek bir soru sorun:

```bash
python main.py --mode query --question "Bilimp nedir?"
```

### Mod 3: Etkileşimli Mod

Sürekli soru-cevap yapın:

```bash
python main.py --mode interactive

# Veya sadece
python main.py
```

Çıkmak için `quit` veya `exit` yazın.

## Örnekler

Sistem özelliklerini test etmek için:

```bash
python examples.py
```

Bu komut şunları gösterir:
- Doküman işleme
- Embedding oluşturma
- Qdrant kullanımı
- LLM yanıt üretimi

## Modül Kullanımı

### Python Kodu ile Kullanım

```python
from src.chunking import DocumentProcessor
from src.embedding import TextEmbedder
from src.qdrant import QdrantManager
from src.llm import ResponseGenerator

# 1. Doküman işle
processor = DocumentProcessor()
chunks = processor.process_document("dokuman.pdf")

# 2. Embedding oluştur
embedder = TextEmbedder()
embeddings = embedder.embed_batch(chunks)

# 3. Qdrant'a yükle
qdrant = QdrantManager()
qdrant.connect()
qdrant.create_collection("docs", embedder.get_embedding_dimension())

payloads = [{"text": chunk} for chunk in chunks]
qdrant.upload_vectors("docs", embeddings, payloads)

# 4. Soru sor
question = "Doküman ne hakkında?"
query_vector = embedder.embed_text(question)
results = qdrant.search("docs", query_vector, limit=5)

# 5. Yanıt al
llm = ResponseGenerator()
response = llm.generate_with_retrieval(question, results)
print(response['answer'])
```

## Yapılandırma

`.env` dosyası oluşturun (`.env.example`'dan):

```bash
cp .env.example .env
```

Değerleri ihtiyacınıza göre düzenleyin:

```
QDRANT_HOST=localhost
QDRANT_PORT=6333
EMBEDDING_MODEL=intfloat/multilingual-e5-large
LLM_MODEL=gemma3-12b
```

## Sorun Giderme

### Qdrant bağlanamıyor

```bash
# Qdrant çalışıyor mu kontrol edin
docker ps | grep qdrant

# Logları inceleyin
docker logs bilimp_qdrant

# Yeniden başlatın
docker-compose restart
```

### GPU kullanılamıyor

PyTorch CUDA desteğini kontrol edin:

```python
import torch
print(torch.cuda.is_available())
```

CUDA yoksa CPU kullanılacaktır (daha yavaş).

### Bellek hatası

Daha küçük batch size kullanın:

```python
embedder.embed_batch(texts, batch_size=16)  # Varsayılan: 32
```

## Dokümantasyon

Detaylı dokümantasyon için:

- [Doküman İşleme](docs/chunking.md)
- [Embedding](docs/embedding.md)
- [Qdrant](docs/qdrant.md)
- [LLM Yanıtları](docs/llm.md)

## Destek

Sorunlar için GitHub Issues kullanın:
https://github.com/mehmetbozdemir24/Bilimp_Terracity/issues
