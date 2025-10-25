# Qdrant Entegrasyon Testleri

Bu dizin, Qdrant veritabanı entegrasyonunun doğru çalışıp çalışmadığını test eden dosyaları içerir.

## 📋 Test Dosyaları

### `test_qdrant_integration.py`
Qdrant modülünün tüm fonksiyonlarını test eden kapsamlı test suite.

## 🧪 Testler

Test suite 9 temel test içerir:

1. ✅ **test_01_create_collection** - Koleksiyon oluşturma
2. ✅ **test_02_collection_exists** - Koleksiyon varlık kontrolü
3. ✅ **test_03_list_collections** - Koleksiyonları listeleme
4. ✅ **test_04_upsert_points** - Vektör ekleme/güncelleme
5. ✅ **test_05_search** - Benzerlik araması
6. ✅ **test_06_search_with_filter** - Filtrelenmiş arama
7. ✅ **test_07_get_point** - Belirli vektörü getirme
8. ✅ **test_08_get_collection_info** - Koleksiyon bilgilerini alma
9. ✅ **test_09_delete_collection** - Koleksiyon silme

## 🚀 Testleri Çalıştırma

### Ön Gereksinimler

1. **Qdrant sunucusu çalışıyor olmalı:**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

2. **Python bağımlılıkları yüklü olmalı:**
```bash
pip install -r requirements.txt
```

### Tüm Testleri Çalıştır

```bash
python tests/test_qdrant_integration.py
```

### Unittest ile Çalıştır

```bash
python -m unittest tests.test_qdrant_integration
```

### Verbose Mod

```bash
python -m unittest tests.test_qdrant_integration -v
```

### Belirli Bir Testi Çalıştır

```bash
python -m unittest tests.test_qdrant_integration.TestQdrantIntegration.test_01_create_collection
```

## 📊 Beklenen Çıktı

Başarılı test çalıştırması şöyle görünür:

```
======================================================================
🧪 Qdrant Entegrasyon Testleri
======================================================================

⚠️ Not: Qdrant sunucusunun localhost:6333'te çalışıyor olması gerekir!
   Başlatmak için: docker run -p 6333:6333 qdrant/qdrant

test_01_create_collection (__main__.TestQdrantIntegration) ... ok
test_02_collection_exists (__main__.TestQdrantIntegration) ... ok
test_03_list_collections (__main__.TestQdrantIntegration) ... ok
test_04_upsert_points (__main__.TestQdrantIntegration) ... ok
test_05_search (__main__.TestQdrantIntegration) ... ok
test_06_search_with_filter (__main__.TestQdrantIntegration) ... ok
test_07_get_point (__main__.TestQdrantIntegration) ... ok
test_08_get_collection_info (__main__.TestQdrantIntegration) ... ok
test_09_delete_collection (__main__.TestQdrantIntegration) ... ok

----------------------------------------------------------------------
Ran 9 tests in 2.345s

OK
======================================================================
✅ Tüm testler başarılı!
======================================================================
```

## 🔧 Sorun Giderme

### Qdrant Sunucusuna Bağlanılamıyor

**Hata:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Çözüm:**
1. Qdrant sunucusunun çalıştığından emin olun:
```bash
docker ps | grep qdrant
```

2. Eğer çalışmıyorsa başlatın:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### Test Koleksiyonu Zaten Var

**Hata:**
```
CollectionAlreadyExists: Collection test_collection already exists
```

**Çözüm:**
Bu normal bir durumdur. Test suite otomatik olarak temizleme yapar. Eğer sorun devam ederse:

```bash
# Manuel temizlik
curl -X DELETE http://localhost:6333/collections/test_collection
```

### Testler Yavaş Çalışıyor

**Neden:** Qdrant Docker container'ı ilk başlatıldığında daha yavaş olabilir.

**Çözüm:** Container'ın ısınması için birkaç saniye bekleyin veya testleri tekrar çalıştırın.

## 📝 Test Yazma Kılavuzu

Yeni test eklemek için:

```python
def test_10_new_feature(self):
    """Test: Yeni özellik testi"""
    # Arrange (Hazırlık)
    self.qdrant.create_collection(self.test_collection, vector_size=128)
    
    # Act (İşlem)
    result = self.qdrant.some_new_method()
    
    # Assert (Doğrulama)
    self.assertTrue(result, "Hata mesajı")
```

## 🎯 Test Kapsamı

Mevcut testler şu fonksiyonları kapsar:

| Fonksiyon | Test Durumu |
|-----------|-------------|
| `__init__` | ✅ Dolaylı test |
| `create_collection` | ✅ Test edildi |
| `collection_exists` | ✅ Test edildi |
| `delete_collection` | ✅ Test edildi |
| `list_collections` | ✅ Test edildi |
| `upsert_points` | ✅ Test edildi |
| `search` | ✅ Test edildi |
| `search` (filtered) | ✅ Test edildi |
| `get_point` | ✅ Test edildi |
| `get_collection_info` | ✅ Test edildi |
| `close` | ✅ Dolaylı test |

## 🔄 CI/CD Entegrasyonu

Bu testler CI/CD pipeline'ında kullanılabilir:

```yaml
# .github/workflows/test.yml örneği
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      qdrant:
        image: qdrant/qdrant
        ports:
          - 6333:6333
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python tests/test_qdrant_integration.py
```

## 📚 Daha Fazla Bilgi

- Ana modül dokümantasyonu: `../src/README.md`
- Örnek kullanımlar: `../examples/`
- Python unittest dokümantasyonu: https://docs.python.org/3/library/unittest.html

## 🤝 Katkıda Bulunanlar

**Görevliler:** Süleyman, Eren
