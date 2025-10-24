# 🤖 Bilimp_Teracity

**Teracity Firmasına ait Bilip Yazılımı için Asistan Tasarımı**

Bilimp, kurumsal dokümanlardan çıkarılan bilgiler üzerinde anlam-temelli aramalar gerçekleştiren ve akıllı yanıtlar üreten bir yapay zeka asistanıdır. Sistem, modern derin öğrenme modelleri ve vektör veritabanı teknolojisini kullanarak hızlı, doğru ve bağlamsal yanıtlar sağlamaktadır.

---

## 📋 Sistem Mimarisi

Bilimp sistemi dört ana aşamadan oluşmaktadır:

### 1️⃣ **Doküman Ön İşleme & Chunking**
- Blimp sistemindeki dokümanların okunması ve temizlenmesi
- Metin parçalarına (chunks) bölünmesi
- **Görevliler**: Engin, Batuhan

### 2️⃣ **Embedding Vektörleştirme**
- Cosmos-e5-large modeliyle metin parçalarının vektörlere dönüştürülmesi
- Anlamsal temsil oluşturulması
- **Görevliler**: Mehmet, Hasan

### 3️⃣ **Vektör Veritabanı Yönetimi**
- Embedding vektörlerinin Docker üzerinden Qdrant veritabanına yüklenmesi
- Hızlı ve ölçeklenebilir arama altyapısı
- **Görevliler**: Süleyman, Eren

### 4️⃣ **Akıllı Yanıt Üretimi**
- Qdrant verilerinden anlam temelli sorgu sonuçlarının alınması
- **Gemma3-12B** ve **Qwen3-9B** modellerinin kullanılarak doğal dil yanıtları oluşturulması
- **Görevliler**: Hasan, Eren

---

## 🛠️ Teknoloji Stack

| Bileşen | Teknoloji |
|---------|-----------|
| **Embedding Modeli** | Cosmos-e5-large |
| **Vektör Veritabanı** | Qdrant (Docker) |
| **LLM Modelleri** | Gemma3-12B, Qwen3-8B |
| **Container Teknolojisi** | Docker |

---

## 🚀 Kullanım Akışı

```
Dokümanlar  
    ↓  
[Chunking] (Engin, Batuhan)  
    ↓  
[Embedding] (Mehmet, Hasan)  
    ↓  
[Qdrant DB] (Süleyman, Eren)  
    ↓  
[LLM Tabanlı Sorgulama ve Yanıt Üretimi] (Hasan, Eren)  
    ↓  
Kullanıcıya Yanıt
```

---

| 👤 **İsim** | 🧩 **Görev Tanımı** |
|--------------|---------------------|
| 👨‍💻 **Engin** | Dokümanların ön işleme alınması ve semantik bütünlüğe uygun şekilde chunk’lara ayrılması |
| 👨‍💻 **Batuhan** | Dokümanların ön işleme süreçlerinde veri temizleme ve chunk oluşturma desteği |
| 👨‍💻 **Mehmet** | Chunk’lanmış metinlerin embedding modeliyle vektörleştirilmesi ve doğrulama işlemleri |
| 👨‍💻 **Hasan** | Embedding süreci ile büyük dil modeli (LLM) tabanlı sorgulama ve yanıt üretiminin yürütülmesi |
| 👨‍💻 **Süleyman** | Qdrant vektör veritabanının Docker ortamında yönetimi, veri yükleme ve indeksleme işlemleri |
| 👨‍💻 **Eren** | Qdrant veritabanı yönetimi ile LLM tabanlı sorgulama ve yanıt üretim süreçlerinin desteklenmesi |

---

## 📦 Gereksinimler

- Python 3.8+
- Docker & Docker Compose
- Qdrant Server
- PyTorch / TensorFlow
- Transformers Library

---

## 🔧 Kurulum

```bash
# Repository'yi klonlayın
git clone https://github.com/mehmetbozdemir24/Bilimp_Teracity.git
cd Bilimp_Teracity

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Docker ile Qdrant başlatın
docker-compose up -d

# Sistemi başlatın
python main.py
```

---

## 📚 Dokümentasyon

Her modül için ayrıntılı dokümantasyon:
- `docs/1_chunking_guide.md` - Doküman işleme
- `docs/2_embedding_guide.md` - Vektörleştirme
- `docs/3_qdrant_setup_guide.md` - Veritabanı yönetimi
- `docs/4_llm_response_guide.md` - Yanıt üretimi
- `docs/5_complete_workflow.md` - Toplu İş Akışı

---

## 📄 Lisans

Bu proje Teracity Firması tarafından geliştirilmiştir.

---

## 📞 İletişim

Sorular veya öneriler için lütfen Issues bölümünü kullanınız.

**Geliştirici**: mehmetbozdemir24
