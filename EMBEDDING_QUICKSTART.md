# Embedding Modülü - Hızlı Başlangıç

Bu kılavuz, embedding modülünü hızlıca kullanmaya başlamanız için hazırlanmıştır.

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Projeyi test edin:
```bash
# Birim testler (internet gerektirmez)
python tests/test_embedding_unit.py

# Fonksiyonel testler (internet gerektirir - model indirir)
python tests/test_embedding.py
```

## Hızlı Kullanım

### Temel Kullanım

```python
from src.embedding import EmbeddingProcessor

# Model başlatma
processor = EmbeddingProcessor()

# Tek metin vektörleme
text = "Python programlama dilidir"
embedding = processor.embed_query(text)
print(f"Embedding boyutu: {len(embedding)}")  # 1024
```

### Toplu İşlem (Batch Processing)

```python
# Birden fazla metin
chunks = [
    "Python programlama dilidir",
    "Makine öğrenmesi yapay zekadır"
]

embeddings_list = processor.embed_documents(chunks)
print(f"✅ {len(embeddings_list)} chunk vektörleştirildi!")
```

### LangChain Document Chunks

```python
from langchain_core.documents import Document

chunks = [
    Document(
        page_content="Python programlama dilidir",
        metadata={"source": "ders1.pdf", "page": 1}
    ),
    Document(
        page_content="Makine öğrenmesi yapay zekadır",
        metadata={"source": "ders2.pdf", "page": 2}
    ),
]

# Batch işleme ile vektörleştir
embeddings_dict = processor.process_chunks(chunks, batch_size=32)

# Kaydet
processor.save_embeddings(embeddings_dict, "embeddings.pkl")

# Yükle
loaded_dict = processor.load_embeddings("embeddings.pkl")
```

### Benzerlik Hesaplama

```python
import numpy as np

emb1 = processor.embed_query("Makine öğrenmesi yapay zekadır")
emb2 = processor.embed_query("Yapay zeka makine öğrenmesidir")

# Cosine similarity (vektörler normalize olduğu için dot product)
similarity = np.dot(emb1, emb2)
print(f"Benzerlik: {similarity:.4f}")  # ~0.85-0.95 arası
```

## Örnek Script

Tam bir kullanım örneği için:
```bash
python examples/embedding_example.py
```

## API Referansı

### EmbeddingProcessor

**Başlatma Parametreleri:**
- `model_name` (str): HuggingFace model ismi (varsayılan: "ytu-ce-cosmos/turkish-e5-large")
- `device` (str, optional): "cuda", "cpu" veya None (otomatik)

**Metodlar:**

#### `embed_query(text: str) -> List[float]`
Tek bir metni vektöre dönüştürür.

#### `embed_documents(texts: List[str]) -> List[List[float]]`
Birden fazla metni toplu olarak vektörleştirir.

#### `process_chunks(chunks: List[Document], batch_size: int = 32) -> Dict`
LangChain Document'ları batch işleme ile vektörleştirir.

#### `save_embeddings(embeddings_dict: Dict, path: str)`
Embedding'leri pickle formatında kaydeder.

#### `load_embeddings(path: str) -> Dict`
Kaydedilmiş embedding'leri yükler.

#### `get_embedding_dimension() -> int`
Embedding vektör boyutunu döndürür (1024).

## Model Bilgileri

- **Model**: ytu-ce-cosmos/turkish-e5-large
- **Vektör Boyutu**: 1024
- **Dil Desteği**: Türkçe ve İngilizce
- **Normalizasyon**: L2 normalize (cosine similarity için hazır)
- **Performans**: GPU ile ~10-15 sn/1000 metin

## Sık Karşılaşılan Sorunlar

### CUDA Hafızası Yetersiz
```python
# CPU kullan
processor = EmbeddingProcessor(device="cpu")
```

### Yavaş İşlem
```python
# embed_documents() kullan (tek tek değil)
embeddings = processor.embed_documents(texts)  # ✅ Hızlı
# Yerine:
# embeddings = [processor.embed_query(t) for t in texts]  # ❌ Yavaş
```

## Daha Fazla Bilgi

- Detaylı rehber: `docs/2_embedding_guide.md`
- Test dosyaları: `tests/README.md`
- Örnek kodlar: `examples/README.md`
- Kaynak kod: `src/README.md`

## Görevliler

Mehmet, Hasan

## Lisans

TÜBİTAK 1505 Projesi
