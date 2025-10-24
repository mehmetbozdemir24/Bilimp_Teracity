# 📊 Embedding & Vektörleştirme Rehberi

**Görevliler**: Mehmet, Hasan

## 🎯 Amaç

Bu rehber, LangChain HuggingFaceEmbeddings kullanarak metin parçalarını (chunks) anlamsal vektörlere dönüştürmeyi anlatır. Cosmos-E5-Large modeliyle yüksek kalitede embedding oluşturacaksınız.

## 📚 Teori & Konsept

### Embedding Nedir?
Embedding, metni sayısal bir vektöre dönüştürme işlemidir. Bu sayede:
- ✅ Benzer metinler birbirine yakın vektörler oluşturur
- ✅ Anlamsal benzerlik matematiksel olarak hesaplanabilir
- ✅ Hızlı arama yapılabilir

### Cosmos-E5-Large Modeli
- **Boyut**: 1024-dimensional vektör
- **Dil**: Türkçe ve İngilizce destekli
- **Performans**: Yüksek kalite, orta hız
- **Model ID**: `ytu-ce-cosmos/turkish-e5-large`

## 🔧 Kurulum

### Adım 1: Gerekli Kütüphaneleri Yükleyin

```bash
pip install langchain
pip install langchain-huggingface
pip install torch
pip install sentence-transformers
```

### Adım 2: GPU/CPU Kontrol

```python
import torch
print(f"GPU Kullanılabilir: {torch.cuda.is_available()}")
```

## 💡 Kod Örnekleri

### ADIM 1: Modeli Yükleyin

```python
import torch
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="ytu-ce-cosmos/turkish-e5-large",
    model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)
print("✅ Model yüklendi!")
```

### ADIM 2: Tek Metni Vektörle

```python
text = "Python programlama dilidir"
embedding = embeddings.embed_query(text)
print(f"Embedding boyutu: {len(embedding)}")  # 1024
```

### ADIM 3: Chunks Vektörle

```python
from langchain.schema import Document

chunks = [
    Document(page_content="Python programlama dilidir", metadata={"source": "ders1.pdf"}),
    Document(page_content="Makine öğrenmesi yapay zekadır", metadata={"source": "ders2.pdf"}),
]

embeddings_dict = {}
for i, chunk in enumerate(chunks):
    embedding = embeddings.embed_query(chunk.page_content)
    embeddings_dict[i] = {
        "content": chunk.page_content,
        "metadata": chunk.metadata,
        "embedding": embedding
    }
print(f"✅ {len(embeddings_dict)} chunk vektörleştirildi!")
```

### ADIM 4: Toplu İşlem (Batch Processing)

```python
texts = ["Metin 1", "Metin 2", "Metin 3"] * 100

# embed_documents() - toplu metinler için
embeddings_list = embeddings.embed_documents(texts)
print(f"✅ {len(embeddings_list)} metin vektörleştirildi!")
```

### ADIM 5: Benzerlik Hesapla

```python
import numpy as np

emb1 = embeddings.embed_query("Makine öğrenmesi yapay zekadır")
emb2 = embeddings.embed_query("Yapay zeka makine öğrenmesidir")

similarity = np.dot(emb1, emb2)
print(f"Benzerlik: {similarity:.4f}")
```

## 📁 Gerçek Proje

```python
import pickle
import torch
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingProcessor:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="ytu-ce-cosmos/turkish-e5-large",
            model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
    
    def process_chunks(self, chunks, batch_size=32):
        embeddings_dict = {}
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            texts = [doc.page_content for doc in batch]
            batch_embeddings = self.embeddings.embed_documents(texts)
            for j, embedding in enumerate(batch_embeddings):
                embeddings_dict[i+j] = {
                    "content": batch[j].page_content,
                    "metadata": batch[j].metadata,
                    "embedding": embedding
                }
        return embeddings_dict
    
    def save(self, embeddings_dict, path):
        with open(path, "wb") as f:
            pickle.dump(embeddings_dict, f)
        print(f"✅ {len(embeddings_dict)} embedding kaydedildi!")

# Kullanım
processor = EmbeddingProcessor()
embeddings_dict = processor.process_chunks(chunks)
processor.save(embeddings_dict, "embeddings.pkl")
```

## ⚡ Performans

| GPU | 1000 Metin | 10000 Metin |
|-----|-----------|------------|
| CPU | 5-10 min | 50-100 min |
| RTX 3090 | 10-15 sn | 1-2 dakika |
| T4 GPU | 20-30 sn | 2-3 dakika |

## 🧪 Test

```python
import numpy as np

# Test 1: Boyut
embedding = embeddings.embed_query("test")
assert len(embedding) == 1024
print("✅ Test 1: Boyut doğru")

# Test 2: Normalize
magnitude = np.sqrt(np.sum(np.array(embedding) ** 2))
assert abs(magnitude - 1.0) < 0.01
print("✅ Test 2: Normalize ediliş doğru")

# Test 3: Benzerlik
emb1 = embeddings.embed_query("Makine öğrenmesi")
emb2 = embeddings.embed_query("Makine öğrenmesi")
assert np.dot(emb1, emb2) > 0.99
print("✅ Test 3: Benzerlik doğru")
```

## 🐛 Sorun Giderme

### CUDA Hafızası
```python
embeddings = HuggingFaceEmbeddings(
    model_name="ytu-ce-cosmos/turkish-e5-large",
    model_kwargs={"device": "cpu"},  # CPU kullan
    encode_kwargs={"normalize_embeddings": True}
)
```

### Yavaş İşlem
```python
# embed_documents() kullan (toplu işlem)
embeddings_list = embeddings.embed_documents(texts)
```

## 📝 Kontrol Listesi

- [ ] LangChain kurulu
- [ ] langchain-huggingface kurulu
- [ ] Model yüklendi
- [ ] GPU/CPU ayarı doğru
- [ ] embed_query() test edildi
- [ ] embed_documents() test edildi
- [ ] Embedding boyutu 1024
- [ ] Normalization aktif
- [ ] Benzerlik hesabı çalışıyor
- [ ] Embedding'ler kaydedildi
