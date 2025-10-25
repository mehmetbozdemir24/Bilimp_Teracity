# Qdrant Veritabanı Entegrasyonu

Bu modül, TÜBİTAK 1505 projesi için Qdrant vektör veritabanı entegrasyonunu sağlar.

**Görevliler:** Süleyman, Eren

## 📋 İçerik

- `qdrant_client_manager.py` - Ana Qdrant yönetim modülü
- Koleksiyon oluşturma/silme/listeleme
- Vektör ekleme/güncelleme (upsert)
- Vektör arama (benzerlik araması)
- Filtrelenmiş arama
- Koleksiyon bilgilerini alma

## 🚀 Kurulum

### 1. Qdrant Sunucusunu Başlatın

Docker ile:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 2. Python Bağımlılıklarını Yükleyin

```bash
pip install qdrant-client
```

## 💻 Kullanım

### Temel Kullanım

```python
from src.qdrant_client_manager import QdrantManager

# Client'ı başlat
qdrant = QdrantManager(host="localhost", port=6333)

# Koleksiyon oluştur
qdrant.create_collection(
    collection_name="my_collection",
    vector_size=1024  # Cosmos-E5-Large için
)

# Vektör ekle
points = [
    {
        "id": 1,
        "vector": [0.1] * 1024,
        "payload": {"source": "test.pdf", "page": 1}
    }
]
qdrant.upsert_points("my_collection", points)

# Arama yap
results = qdrant.search(
    collection_name="my_collection",
    query_vector=[0.1] * 1024,
    limit=5
)

# Bağlantıyı kapat
qdrant.close()
```

### Filtrelenmiş Arama

```python
# Belirli bir kaynaktan arama
results = qdrant.search(
    collection_name="my_collection",
    query_vector=query_vector,
    limit=5,
    filter_conditions={"source": "test.pdf"}
)
```

## 📝 API Referansı

### QdrantManager

#### `__init__(host, port, api_key)`
Qdrant client'ını başlatır.

**Parametreler:**
- `host` (str): Qdrant sunucu adresi (varsayılan: "localhost")
- `port` (int): Qdrant portu (varsayılan: 6333)
- `api_key` (str, opsiyonel): API anahtarı

#### `create_collection(collection_name, vector_size, distance)`
Yeni koleksiyon oluşturur.

**Parametreler:**
- `collection_name` (str): Koleksiyon adı
- `vector_size` (int): Vektör boyutu (varsayılan: 1024)
- `distance` (Distance): Mesafe metriği (varsayılan: COSINE)

**Dönüş:** bool

#### `collection_exists(collection_name)`
Koleksiyonun var olup olmadığını kontrol eder.

**Dönüş:** bool

#### `delete_collection(collection_name)`
Koleksiyonu siler.

**Dönüş:** bool

#### `list_collections()`
Tüm koleksiyonları listeler.

**Dönüş:** List[str]

#### `upsert_points(collection_name, points)`
Vektörleri ekler veya günceller.

**Parametreler:**
- `collection_name` (str): Hedef koleksiyon
- `points` (List[Dict]): Eklenecek vektörler

**Point formatı:**
```python
{
    "id": int veya str,
    "vector": List[float],
    "payload": Dict[str, Any]  # opsiyonel
}
```

**Dönüş:** bool

#### `search(collection_name, query_vector, limit, filter_conditions)`
Benzerlik araması yapar.

**Parametreler:**
- `collection_name` (str): Arama yapılacak koleksiyon
- `query_vector` (List[float]): Sorgu vektörü
- `limit` (int): Maksimum sonuç sayısı (varsayılan: 5)
- `filter_conditions` (Dict, opsiyonel): Filtreleme koşulları

**Dönüş:** List[Dict]

#### `get_point(collection_name, point_id)`
Belirli bir vektörü getirir.

**Dönüş:** Dict veya None

#### `get_collection_info(collection_name)`
Koleksiyon bilgilerini döndürür.

**Dönüş:** Dict veya None

#### `close()`
Bağlantıyı kapatır.

## 🧪 Testler

Testleri çalıştırmak için:

```bash
# Önce Qdrant sunucusunu başlatın
docker run -p 6333:6333 qdrant/qdrant

# Testleri çalıştırın
python tests/test_qdrant_integration.py
```

## 📚 Örnekler

Detaylı kullanım örnekleri için:
```bash
python examples/qdrant_example.py
```

## 🔗 Entegrasyon

### Embedding ile Entegrasyon

```python
from src.qdrant_client_manager import QdrantManager
from langchain_huggingface import HuggingFaceEmbeddings

# Embedding modeli yükle
embeddings = HuggingFaceEmbeddings(
    model_name="ytu-ce-cosmos/turkish-e5-large"
)

# Qdrant başlat
qdrant = QdrantManager()
qdrant.create_collection("documents", vector_size=1024)

# Metinleri vektörleştir ve kaydet
texts = ["Metin 1", "Metin 2", "Metin 3"]
points = []
for i, text in enumerate(texts):
    vector = embeddings.embed_query(text)
    points.append({
        "id": i,
        "vector": vector,
        "payload": {"text": text}
    })

qdrant.upsert_points("documents", points)
```

## ⚠️ Önemli Notlar

- Qdrant sunucusunun çalışıyor olması gerekir
- Vector boyutu koleksiyon oluşturulurken belirlenir ve sonradan değiştirilemez
- Cosmos-E5-Large modeli için vektör boyutu: 1024
- Tüm aramalar cosine benzerlik metriği kullanır

## 📖 Daha Fazla Bilgi

- Qdrant Dokümantasyonu: https://qdrant.tech/documentation/
- Issue: https://github.com/mehmetbozdemir24/Tubitak_1505_Proje/issues/1
- Kurulum Kılavuzu: `docs/3_qdrant_setup_guide.md`
