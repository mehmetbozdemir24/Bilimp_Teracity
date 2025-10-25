# Qdrant Entegrasyon Örnekleri

Bu dizin, Qdrant veritabanı entegrasyonunun nasıl kullanılacağını gösteren örnek scriptler içerir.

## 📁 Örnek Dosyalar

### 1. `issue_example.py`
Issue #1'de belirtilen basit kod örneğinin çalışan versiyonu.

**Çalıştırmak için:**
```bash
python examples/issue_example.py
```

**İçerik:**
- Koleksiyon oluşturma
- Tek vektör ekleme
- Basit arama

### 2. `qdrant_example.py`
Temel Qdrant operasyonlarını gösteren kapsamlı örnek.

**Çalıştırmak için:**
```bash
python examples/qdrant_example.py
```

**İçerik:**
- Koleksiyon yönetimi
- Çoklu vektör ekleme
- Benzerlik araması
- Filtrelenmiş arama
- Koleksiyon bilgilerini alma

### 3. `full_integration_example.py`
Tam iş akışını simüle eden entegrasyon örneği.

**Çalıştırmak için:**
```bash
python examples/full_integration_example.py
```

**İçerik:**
- Chunking simülasyonu (Engin, Batuhan)
- Embedding simülasyonu (Mehmet, Hasan)
- Qdrant'a kaydetme (Süleyman, Eren)
- Semantik arama
- Filtrelenmiş arama
- Gerçek proje kullanım örnekleri

## 🚀 Başlamadan Önce

### 1. Qdrant Sunucusunu Başlatın

Docker ile:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

Docker Compose ile (detached mode):
```bash
docker run -d -p 6333:6333 qdrant/qdrant
```

### 2. Python Bağımlılıklarını Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Örnekleri Çalıştırın

```bash
# Basit örnek
python examples/issue_example.py

# Detaylı örnek
python examples/qdrant_example.py

# Tam entegrasyon
python examples/full_integration_example.py
```

## 📊 Beklenen Çıktı

Her örnek başarıyla çalıştığında şu tür çıktılar göreceksiniz:

```
🚀 Qdrant Veritabanı Entegrasyon Örneği
============================================================

1️⃣ Qdrant Client'ı başlatılıyor...
✅ Koleksiyon 'my_collection' başarıyla oluşturuldu!

2️⃣ Koleksiyon oluşturuluyor...
✅ 3 vektör başarıyla eklendi/güncellendi!

...

✅ Örnek başarıyla tamamlandı!
```

## 🔧 Sorun Giderme

### Qdrant Sunucusuna Bağlanılamıyor

**Hata:**
```
❌ Koleksiyon oluşturma hatası: Connection refused
```

**Çözüm:**
- Qdrant sunucusunun çalıştığından emin olun
- Docker container'ın ayakta olduğunu kontrol edin: `docker ps`
- Port 6333'ün kullanılabilir olduğunu kontrol edin

### Port Zaten Kullanımda

**Hata:**
```
Error: port is already allocated
```

**Çözüm:**
```bash
# Çalışan container'ı durdurun
docker ps
docker stop <container_id>

# Veya farklı bir port kullanın
docker run -p 6334:6333 qdrant/qdrant
```

Python kodunda:
```python
qdrant = QdrantManager(host="localhost", port=6334)
```

## 🎓 Öğrenme Yolu

Önerilen öğrenme sırası:

1. ✅ `issue_example.py` - Temel kavramlar
2. ✅ `qdrant_example.py` - Detaylı özellikler
3. ✅ `full_integration_example.py` - Gerçek kullanım

## 📚 Daha Fazla Bilgi

- Ana modül dokümantasyonu: `../src/README.md`
- Qdrant kurulum kılavuzu: `../docs/3_qdrant_setup_guide.md`
- Tam iş akışı: `../docs/5_complete_workflow.md`
- Test dosyaları: `../tests/test_qdrant_integration.py`

## 💡 İpuçları

1. **Vektör Boyutu**: Cosmos-E5-Large modeli 1024 boyutlu vektörler üretir
2. **Mesafe Metriği**: Cosine benzerlik önerilir
3. **Batch İşleme**: Çok sayıda vektör eklerken batch'ler halinde ekleyin
4. **Filtreleme**: Metadata kullanarak filtreleme yapabilirsiniz
5. **ID Yönetimi**: Benzersiz ID'ler kullanın (int veya str)

## 🤝 Katkıda Bulunanlar

**Görevliler:** Süleyman, Eren
