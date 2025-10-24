# Embedding Vektörleştirme

## Genel Bakış

Embedding modülü, metin parçalarını (chunks) sayısal vektörlere dönüştürür. Bu vektörler, anlamsal benzerlik aramalarını mümkün kılar.

## Görevliler

- **Mehmet**: Model entegrasyonu
- **Hasan**: Batch işleme ve optimizasyon

## Model

**Kullanılan Model**: intfloat/multilingual-e5-large
- Çok dilli destek (Türkçe dahil)
- 1024 boyutlu vektörler
- Yüksek kaliteli anlamsal temsil

## Özellikler

### 1. Tek Metin Vektörleştirme

```python
from src.embedding import TextEmbedder

embedder = TextEmbedder()
vector = embedder.embed_text("Merhaba dünya")
print(f"Vektör boyutu: {len(vector)}")
```

### 2. Toplu Vektörleştirme

```python
texts = ["Metin 1", "Metin 2", "Metin 3"]
vectors = embedder.embed_batch(texts, batch_size=32)
print(f"Toplam {len(vectors)} vektör oluşturuldu")
```

### 3. Model Bilgileri

```python
dimension = embedder.get_embedding_dimension()
print(f"Embedding boyutu: {dimension}")
```

## Performans Optimizasyonu

### Batch Size

- Daha büyük batch size = Daha hızlı işleme
- Ancak daha fazla bellek kullanımı
- Önerilen: 32-64 arası

### GPU Kullanımı

Model otomatik olarak CUDA varsa GPU'yu kullanır:

```python
import torch
print(f"CUDA kullanılabilir: {torch.cuda.is_available()}")
```

## Kullanım Örneği

```python
from src.chunking import DocumentProcessor
from src.embedding import TextEmbedder

# Doküman işle
processor = DocumentProcessor()
chunks = processor.process_document("dokuman.pdf")

# Embedding oluştur
embedder = TextEmbedder()
embeddings = embedder.embed_batch(chunks, batch_size=32)

print(f"{len(embeddings)} vektör oluşturuldu")
print(f"Vektör boyutu: {embeddings.shape}")
```

## Hata Yönetimi

### Boş Metin

```python
try:
    vector = embedder.embed_text("")
except ValueError as e:
    print(f"Hata: {e}")
```

### Model Yükleme Hatası

```python
try:
    embedder = TextEmbedder(model_name="mevcut_olmayan_model")
except RuntimeError as e:
    print(f"Model yüklenemedi: {e}")
```

## Teknik Detaylar

### Normalizasyon

Vektörler otomatik olarak L2 normalize edilir:
- Cosine benzerlik hesaplamaları için optimize
- Vektör büyüklükleri normalize

### Dil Desteği

Model, 100+ dili destekler:
- Türkçe
- İngilizce
- Almanca
- Fransızca
- ve daha fazlası

## İleriye Dönük Geliştirmeler

- [ ] Farklı model seçenekleri (OpenAI, Cohere)
- [ ] Özel fine-tuned model desteği
- [ ] Vektör önbellekleme
- [ ] Paralel işleme optimizasyonu
