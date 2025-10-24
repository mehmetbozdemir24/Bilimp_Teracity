# Bilimp Terracity - Hızlı Başlangıç Kılavuzu

Bu kılavuz, Bilimp Terracity Asistan sistemini hızlıca kurmak ve kullanmaya başlamak için adım adım talimatlar içerir.

## ⚡ Hızlı Kurulum (Linux/Mac)

```bash
# 1. Kurulum scriptini çalıştır
chmod +x setup.sh
./setup.sh

# 2. LLM modellerini indir (bu işlem uzun sürebilir)
docker exec -it bilimp_ollama ollama pull gemma3:12b
docker exec -it bilimp_ollama ollama pull qwen3:9b

# 3. Örnek kullanımı test et
python example_usage.py
```

## 📝 Manuel Kurulum Adımları

### 1. Ön Gereksinimler
```bash
# Python versiyonunu kontrol et
python3 --version  # 3.8 veya üzeri olmalı

# Docker'ı kontrol et
docker --version
docker-compose --version

# Git'i kontrol et
git --version
```

### 2. Projeyi İndir
```bash
git clone https://github.com/mehmetbozdemir24/Bilimp_Terracity.git
cd Bilimp_Terracity
```

### 3. Python Ortamını Hazırla
```bash
# Sanal ortam oluştur
python3 -m venv venv

# Sanal ortamı aktifleştir
source venv/bin/activate  # Linux/Mac
# VEYA
venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Ayarla
```bash
# .env dosyasını oluştur
cp .env.example .env

# İsteğe bağlı: .env dosyasını düzenle
nano .env  # veya başka bir editör
```

### 5. Docker Servislerini Başlat
```bash
# Qdrant ve Ollama'yı başlat
docker-compose up -d

# Servislerin durumunu kontrol et
docker ps

# Logları kontrol et
docker logs bilimp_qdrant
docker logs bilimp_ollama
```

### 6. LLM Modellerini İndir
```bash
# Gemma3-12B (yaklaşık 7GB)
docker exec -it bilimp_ollama ollama pull gemma3:12b

# Qwen3-9B (yaklaşık 5GB)
docker exec -it bilimp_ollama ollama pull qwen3:9b

# İndirilen modelleri kontrol et
docker exec -it bilimp_ollama ollama list
```

## 🎯 Temel Kullanım

### Adım 1: Doküman Ekleme
```bash
# Dokümanlarınızı data/raw/ klasörüne kopyalayın
cp /path/to/your/documents/*.pdf data/raw/
cp /path/to/your/documents/*.docx data/raw/
```

### Adım 2: Dokümanları İşleme
```bash
# Pipeline'ı çalıştır (bu işlem zaman alabilir)
python main.py --mode process --input-dir data/raw
```

Bu komut:
- Tüm dokümanları okur
- Her dokümanı chunk'lara ayırır
- Her chunk için embedding üretir
- Embedding'leri Qdrant'a yükler

### Adım 3: Sistemi Sorgulama
```bash
# Gemma3 modeli ile sorgulama
python main.py --mode query --query "Bilimp sistemi nedir?" --model gemma

# Qwen3 modeli ile sorgulama
python main.py --mode query --query "Doküman yönetimi nasıl çalışır?" --model qwen

# Model belirtmeden sorgulama (varsayılan: Gemma3)
python main.py --mode query --query "Temel özellikler nelerdir?"
```

### Adım 4: Sistem Bilgisi
```bash
# Veritabanı ve sistem bilgilerini göster
python main.py --mode info
```

## 📊 Örnek Çıktılar

### Process Mode
```
INFO - Processing documents from: data/raw
INFO - Found 3 supported files in data/raw
INFO - Processing file: data/raw/document1.pdf
INFO - Successfully loaded 10 pages from data/raw/document1.pdf
INFO - Created 45 chunks from documents
INFO - Generating embeddings
INFO - Generated 45 embeddings
INFO - Uploading to Qdrant database
INFO - Uploaded 45 chunks to database
INFO - Pipeline completed successfully
```

### Query Mode
```
================================================================================
Query: Bilimp sistemi nedir?
================================================================================

Retrieved 5 documents
Model: gemma3:12b

Response:
--------------------------------------------------------------------------------
Bilimp, Terracity firması tarafından geliştirilen modern bir doküman yönetim
sistemidir. Sistem, şirketlerin dokümanlarını dijital ortamda güvenli bir 
şekilde saklamasına, organize etmesine ve yönetmesine olanak tanır...
================================================================================
```

### Info Mode
```
================================================================================
Bilimp System Information
================================================================================
Collection: bilimp_documents
Documents: 145
Status: green
Embedding Model: intfloat/multilingual-e5-large
Embedding Dimension: 1024
LLM Models: gemma3:12b, qwen3:9b
================================================================================
```

## 🔧 Yapılandırma İpuçları

### Chunk Boyutunu Ayarlama
`.env` dosyasında:
```env
CHUNK_SIZE=512        # Daha küçük parçalar için azaltın (örn: 256)
CHUNK_OVERLAP=50      # Bağlam korunması için overlap ayarlayın
```

### Batch Size Optimizasyonu
```env
BATCH_SIZE=32         # GPU varsa artırın (64), yoksa azaltın (16)
```

### LLM Model Ayarları
```bash
# Farklı model versiyonları kullanmak için
docker exec -it bilimp_ollama ollama pull gemma:7b  # Daha hızlı
docker exec -it bilimp_ollama ollama pull llama2:13b  # Alternatif
```

## 🐛 Yaygın Sorunlar ve Çözümler

### Problem: "Connection refused" hatası
```bash
# Çözüm: Servislerin çalıştığından emin olun
docker-compose ps
docker-compose up -d
```

### Problem: Model bulunamadı
```bash
# Çözüm: Modeli indirin
docker exec -it bilimp_ollama ollama pull gemma3:12b
```

### Problem: Out of memory (OOM)
```bash
# Çözüm 1: Batch size'ı azaltın (.env dosyasında)
BATCH_SIZE=8

# Çözüm 2: Daha küçük model kullanın
docker exec -it bilimp_ollama ollama pull gemma:7b
```

### Problem: Yavaş embedding üretimi
```bash
# Çözüm: GPU kullanımını kontrol edin
nvidia-smi  # CUDA var mı?

# CUDA yoksa, CPU için batch size'ı azaltın
BATCH_SIZE=16
```

## 📚 Ek Kaynaklar

### Python API Kullanımı
```python
from main import BilimpPipeline

# Pipeline oluştur
pipeline = BilimpPipeline()
pipeline.initialize_components()

# Dokümanları işle
chunks = pipeline.process_documents("data/raw")
processed = pipeline.generate_embeddings(chunks)
pipeline.upload_to_database(processed)

# Sorgula
result = pipeline.query_system("Bilimp nedir?", model="gemma")
print(result['response'])
```

### Örnek Script Çalıştırma
```bash
# Tüm örnekleri görmek için
python example_usage.py
```

## 🎓 Öğrenme Yolu

1. **Başlangıç**: `example_usage.py` dosyasını inceleyin
2. **Modül Detayları**: `src/` klasöründeki modülleri keşfedin
3. **Özelleştirme**: Kendi kullanım durumunuz için kod yazın
4. **Optimizasyon**: Performans ayarlarını yapın

## 📞 Yardım

Sorun yaşarsanız:
1. `docker logs bilimp_qdrant` ve `docker logs bilimp_ollama` loglarını kontrol edin
2. `.env` dosyasının doğru yapılandırıldığından emin olun
3. Python bağımlılıklarının yüklü olduğunu kontrol edin: `pip list`
4. GitHub Issues'da yeni bir issue açın

## ✅ Başarı Kontrolü

Kurulum başarılı olduysa:
- ✓ `docker ps` Qdrant ve Ollama containerlarını gösterir
- ✓ `python main.py --mode info` sistem bilgilerini gösterir
- ✓ `example_usage.py` hatasız çalışır
- ✓ Test sorgusu yanıt döner

Tebrikler! Sistem kullanıma hazır. 🎉
