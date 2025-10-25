# Test Dosyaları

Bu klasör, projenin test dosyalarını içerir.

## Test Dosyaları

### test_embedding_unit.py
Embedding modülünün yapısal testleri (internet bağlantısı gerektirmez):
```bash
python tests/test_embedding_unit.py
```

Bu testler şunları doğrular:
- Sınıf ve metodların varlığı
- Metod imzalarının doğruluğu
- Type hints kullanımı
- Dokümantasyonun varlığı
- Import'ların doğruluğu

### test_embedding.py
Embedding modülünün fonksiyonel testleri (internet bağlantısı gerektirir):
```bash
python tests/test_embedding.py
```

⚠️ **Not**: Bu testler HuggingFace'den model indirdiği için internet bağlantısı gerektirir.

Bu testler şunları doğrular:
- Model yükleme
- Embedding boyutu (1024)
- Vektör normalizasyonu
- Benzerlik hesaplama
- Batch processing
- Document chunks işleme
- Kaydetme/yükleme
- Türkçe metin desteği

## Tüm Testleri Çalıştırma

```bash
# Sadece birim testler (internet gerektirmez)
python tests/test_embedding_unit.py

# Fonksiyonel testler (internet gerektirir)
python tests/test_embedding.py
```
