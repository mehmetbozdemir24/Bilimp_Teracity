# Kaynak Kod (Source Code)

Bu klasör, projenin ana kaynak kodunu içerir.

## Modüller

### embedding/
Metin parçalarını (chunks) anlamsal vektörlere dönüştüren embedding modülü.

**Ana Sınıf**: `EmbeddingProcessor`

**Özellikler**:
- Cosmos-E5-Large Türkçe embedding modeli
- 1024-boyutlu normalize edilmiş vektörler
- Batch processing desteği
- GPU/CPU otomatik seçimi
- Pickle formatında kaydetme/yükleme

**Kullanım**:
```python
from src.embedding import EmbeddingProcessor

# Model başlatma
processor = EmbeddingProcessor()

# Tek metin
embedding = processor.embed_query("Python programlama dilidir")

# Toplu işlem
texts = ["Metin 1", "Metin 2", "Metin 3"]
embeddings = processor.embed_documents(texts)

# Document chunks
from langchain_core.documents import Document

chunks = [
    Document(page_content="Python programlama dilidir", 
             metadata={"source": "ders1.pdf"}),
]
embeddings_dict = processor.process_chunks(chunks)

# Kaydet
processor.save_embeddings(embeddings_dict, "embeddings.pkl")

# Yükle
loaded = processor.load_embeddings("embeddings.pkl")
```

**Dokümantasyon**: `docs/2_embedding_guide.md`

## Kurulum

```bash
pip install -r requirements.txt
```

## Testler

```bash
# Birim testler (internet gerektirmez)
python tests/test_embedding_unit.py

# Fonksiyonel testler (internet gerektirir)
python tests/test_embedding.py
```

## Örnekler

```bash
python examples/embedding_example.py
```
