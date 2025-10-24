# Qdrant Vektör Veritabanı

## Genel Bakış

Qdrant, embedding vektörlerini saklar ve hızlı benzerlik aramaları gerçekleştirir. Docker üzerinde çalışır ve yüksek performanslı arama altyapısı sağlar.

## Görevliler

- **Süleyman**: Qdrant kurulum ve yapılandırma
- **Eren**: Veri yükleme ve sorgulama

## Kurulum

### Docker ile Başlatma

```bash
# Docker Compose ile başlat
docker-compose up -d

# Durumu kontrol et
docker ps | grep qdrant

# Logları görüntüle
docker logs bilimp_qdrant
```

### Manuel Docker Kurulumu

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```

## Bağlantı

### Python İstemci

```python
from src.qdrant import QdrantManager

# Bağlantı oluştur
qdrant = QdrantManager(host="localhost", port=6333)
qdrant.connect()
```

### REST API

Qdrant ayrıca REST API üzerinden erişilebilir:

```bash
# Koleksiyonları listele
curl http://localhost:6333/collections

# Koleksiyon bilgisi
curl http://localhost:6333/collections/bilimp_docs
```

## Koleksiyon Yönetimi

### Koleksiyon Oluşturma

```python
qdrant.create_collection(
    collection_name="bilimp_docs",
    vector_size=1024,
    distance="Cosine"
)
```

#### Mesafe Metrikleri

- **Cosine**: Açı tabanlı benzerlik (önerilen)
- **Euclid**: Öklid mesafesi
- **Dot**: Nokta çarpımı

### Koleksiyon Kontrolü

```python
if qdrant.collection_exists("bilimp_docs"):
    print("Koleksiyon mevcut")
else:
    print("Koleksiyon bulunamadı")
```

## Vektör Yükleme

### Tek Vektör

```python
import numpy as np

vector = np.random.rand(1024)
payload = {"text": "Örnek metin", "source": "dokuman.pdf"}

qdrant.upload_vectors(
    collection_name="bilimp_docs",
    vectors=np.array([vector]),
    payloads=[payload],
    ids=[1]
)
```

### Toplu Yükleme

```python
vectors = np.random.rand(100, 1024)  # 100 vektör
payloads = [{"text": f"Metin {i}"} for i in range(100)]

qdrant.upload_vectors(
    collection_name="bilimp_docs",
    vectors=vectors,
    payloads=payloads
)
```

## Arama İşlemleri

### Benzer Vektör Arama

```python
# Sorgu vektörü oluştur
query_vector = embedder.embed_text("Arama sorgusu")

# Ara
results = qdrant.search(
    collection_name="bilimp_docs",
    query_vector=query_vector,
    limit=5
)

# Sonuçları göster
for result in results:
    print(f"Score: {result['score']:.3f}")
    print(f"Text: {result['payload']['text']}")
    print()
```

### Sonuç Formatı

```python
{
    "id": 42,
    "score": 0.95,
    "payload": {
        "text": "Bulunan metin parçası",
        "source": "dokuman.pdf",
        "chunk_id": 5
    }
}
```

## Performans İpuçları

### 1. Batch Upload

Büyük veri setleri için batch'ler halinde yükleyin:

```python
batch_size = 100
for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i+batch_size]
    qdrant.upload_vectors(collection_name, batch)
```

### 2. Vektör Boyutu

- Daha küçük vektörler = Daha hızlı arama
- Daha büyük vektörler = Daha iyi doğruluk
- Önerilen: 512-1024 arası

### 3. İndeksleme

Qdrant otomatik olarak HNSW indeksi oluşturur:
- Hızlı yaklaşık en yakın komşu araması
- Milyonlarca vektör için optimize

## Web Arayüzü

Qdrant bir web arayüzü sunar:

```
http://localhost:6333/dashboard
```

Özellikler:
- Koleksiyon yönetimi
- Vektör görselleştirme
- API testleri

## Backup ve Restore

### Backup

```bash
# Snapshot oluştur
curl -X POST http://localhost:6333/collections/bilimp_docs/snapshots

# Snapshot'ları listele
curl http://localhost:6333/collections/bilimp_docs/snapshots
```

### Restore

```bash
# Snapshot'tan geri yükle
curl -X PUT http://localhost:6333/collections/bilimp_docs/snapshots/upload \
    -H 'Content-Type: multipart/form-data' \
    -F 'snapshot=@snapshot.tar'
```

## Sorun Giderme

### Bağlantı Hatası

```python
# Qdrant çalışıyor mu kontrol et
docker ps | grep qdrant

# Logları incele
docker logs bilimp_qdrant
```

### Bellek Sorunları

```yaml
# docker-compose.yml'de bellek limiti artır
services:
  qdrant:
    deploy:
      resources:
        limits:
          memory: 4G
```

## İleriye Dönük Geliştirmeler

- [ ] Sharding desteği (büyük veri setleri için)
- [ ] Replikasyon (yüksek erişilebilirlik için)
- [ ] Filtreleme seçenekleri
- [ ] Çoklu koleksiyon yönetimi
