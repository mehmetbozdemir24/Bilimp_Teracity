# Bilimp Terracity Asistan

Terracity Firmasına ait Bilimp Yazılımı için geliştirilmiş AI Asistan Sistemi. Bu sistem, dokümanların işlenmesi, embedding vektörlerine dönüştürülmesi ve semantik arama/yanıt üretimi için tasarlanmıştır.

## 🎯 Proje Özellikleri

### 1. Doküman İşleme ve Chunking (Engin, Batuhan)
- PDF, DOCX, TXT, XLSX formatlarında doküman desteği
- Akıllı metin bölümleme (chunking) algoritması
- Metadata yönetimi ve kaynak takibi

### 2. Embedding Üretimi (Mehmet, Hasan)
- **Cosmos-e5-large** (multilingual-e5-large) modeli ile embedding üretimi
- Batch processing desteği
- GPU acceleration
- 1024 boyutlu vektör desteği

### 3. Vektör Veritabanı Yönetimi (Süleyman, Eren)
- **Qdrant** vektör veritabanı entegrasyonu
- Docker ile kolay kurulum
- Yüksek performanslı cosine similarity arama
- Metadata filtreleme

### 4. LLM Tabanlı Yanıt Üretimi (Hasan, Eren)
- **Gemma3-12B** ve **Qwen3-9B** model desteği
- RAG (Retrieval-Augmented Generation) mimarisi
- Türkçe dil desteği
- Ollama ile local deployment

## 📋 Gereksinimler

- Python 3.8+
- Docker ve Docker Compose
- CUDA destekli GPU (opsiyonel, performans için önerilir)
- En az 16GB RAM
- Ollama (LLM çalıştırma için)

## 🚀 Kurulum

### 1. Repository'yi Klonlayın

```bash
git clone https://github.com/mehmetbozdemir24/Bilimp_Terracity.git
cd Bilimp_Terracity
```

### 2. Python Sanal Ortamı Oluşturun

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Ayarlayın

```bash
cp .env.example .env
# .env dosyasını düzenleyin
```

### 5. Docker Servislerini Başlatın

```bash
# Qdrant ve Ollama servislerini başlat
docker-compose up -d
```

### 6. Ollama Modellerini Yükleyin

```bash
# Gemma3-12B modelini yükle
docker exec -it bilimp_ollama ollama pull gemma3:12b

# Qwen3-9B modelini yükle
docker exec -it bilimp_ollama ollama pull qwen3:9b
```

## 💻 Kullanım

### Dokümanları İşleme

1. Dokümanlarınızı `data/raw/` klasörüne yerleştirin
2. Pipeline'ı çalıştırın:

```bash
python main.py --mode process --input-dir data/raw
```

Bu işlem:
- Dokümanları okuyup chunk'lara ayırır
- Her chunk için embedding üretir
- Embedding'leri Qdrant'a yükler

### Sistemi Sorgulama

```bash
# Gemma3 modeli ile sorgulama
python main.py --mode query --query "Bilimp sistemi nedir?" --model gemma

# Qwen3 modeli ile sorgulama
python main.py --mode query --query "Bilimp sistemi nedir?" --model qwen
```

### Sistem Bilgisi

```bash
python main.py --mode info
```

## 📁 Proje Yapısı

```
Bilimp_Terracity/
├── src/
│   ├── preprocessing/        # Doküman işleme modülü (Engin, Batuhan)
│   │   └── document_processor.py
│   ├── embeddings/          # Embedding üretimi (Mehmet, Hasan)
│   │   └── embedding_generator.py
│   ├── database/            # Qdrant entegrasyonu (Süleyman, Eren)
│   │   └── qdrant_client.py
│   └── llm/                 # LLM entegrasyonu (Hasan, Eren)
│       └── llm_client.py
├── data/
│   ├── raw/                 # Ham dokümanlar
│   └── processed/           # İşlenmiş veri
├── configs/                 # Konfigürasyon dosyaları
├── main.py                  # Ana pipeline
├── docker-compose.yml       # Docker servisleri
├── requirements.txt         # Python bağımlılıkları
└── .env.example            # Örnek ortam değişkenleri
```

## 🔧 Konfigürasyon

`.env` dosyasındaki önemli parametreler:

```env
# Embedding Ayarları
EMBEDDING_MODEL=intfloat/multilingual-e5-large
EMBEDDING_DIMENSION=1024
CHUNK_SIZE=512
CHUNK_OVERLAP=50

# Qdrant Ayarları
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=bilimp_documents

# LLM Ayarları
GEMMA_MODEL=gemma3:12b
QWEN_MODEL=qwen3:9b
OLLAMA_BASE_URL=http://localhost:11434
```

## 🧪 Test

Sistemi test etmek için örnek bir doküman ekleyin:

```bash
# Örnek metin dosyası oluştur
echo "Bilimp sistemi doküman yönetimi için kullanılır." > data/raw/test.txt

# Pipeline'ı çalıştır
python main.py --mode process --input-dir data/raw

# Sistemi sorgula
python main.py --mode query --query "Bilimp nedir?"
```

## 🔍 Modül Detayları

### 1. Document Processor
- **Sorumlular**: Engin, Batuhan
- Çeşitli formatlarda doküman okuma
- RecursiveCharacterTextSplitter ile akıllı chunking
- Metadata yönetimi

### 2. Embedding Generator
- **Sorumlular**: Mehmet, Hasan
- Multilingual-e5-large model
- Batch processing ile yüksek performans
- Query ve passage embedding'leri

### 3. Qdrant Client
- **Sorumlular**: Süleyman, Eren
- Collection yönetimi
- Batch upload
- Similarity search
- Metadata filtreleme

### 4. LLM Client
- **Sorumlular**: Hasan, Eren
- Ollama API entegrasyonu
- Çoklu model desteği (Gemma3, Qwen3)
- RAG pipeline
- Context-aware response generation

## 📊 Performans

- **Embedding Üretimi**: ~100 chunks/saniye (GPU ile)
- **Vektör Arama**: <100ms (1M vektör için)
- **Response Generation**: 2-5 saniye (model boyutuna bağlı)

## 🛠️ Geliştirme

### Yeni Doküman Formatı Ekleme

`src/preprocessing/document_processor.py` içinde `loaders` dictionary'sine yeni format ekleyin:

```python
self.loaders = {
    '.pdf': PyPDFLoader,
    '.yeni_format': YeniFormatLoader,  # Yeni format
    ...
}
```

### Yeni LLM Modeli Ekleme

Ollama ile yeni model ekleyin:

```bash
docker exec -it bilimp_ollama ollama pull yeni_model:tag
```

## 🐛 Sorun Giderme

### Qdrant Bağlantı Hatası
```bash
# Qdrant servisini kontrol edin
docker ps | grep qdrant
docker logs bilimp_qdrant
```

### Ollama Model Bulunamadı
```bash
# Mevcut modelleri listeleyin
docker exec -it bilimp_ollama ollama list

# Model yükleyin
docker exec -it bilimp_ollama ollama pull gemma3:12b
```

### GPU Kullanılamıyor
```bash
# NVIDIA Docker runtime'ı kontrol edin
nvidia-smi
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

## 📝 Lisans

Bu proje Terracity firması için özel olarak geliştirilmiştir.

## 👥 Ekip

- **Doküman İşleme**: Engin, Batuhan
- **Embedding Üretimi**: Mehmet, Hasan
- **Veritabanı Yönetimi**: Süleyman, Eren
- **LLM Entegrasyonu**: Hasan, Eren

## 📧 İletişim

Sorularınız için: [mehmetbozdemir24](https://github.com/mehmetbozdemir24)
