# 🤖 Bilimp_Teracity

**Terracity Firmasına ait Bilip Yazılımı için Asistan Tasarımı**

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
| **LLM Modelleri** | Gemma3-12B, Qwen3-9B |
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
[Query + Retrieval]
    ↓
[LLM Response] (Hasan, Eren)
    ↓
Kullanıcıya Yanıt
```

---

## 👥 Takım

| İsim | Görev |
|------|-------|
| 👨‍💻 Engin | Doküman Ön İşleme |
| 👨‍💻 Batuhan | Doküman Ön İşleme |
| 👨‍💻 Mehmet | Embedding Vektörleştirme |
| 👨‍💻 Hasan | Embedding + LLM Response |
| 👨‍💻 Süleyman | Qdrant Yönetimi |
| 👨‍💻 Eren | Qdrant Yönetimi + LLM Response |

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
git clone https://github.com/mehmetbozdemir24/Bilimp_Terracity.git
cd Bilimp_Terracity

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

Bu proje Terracity Firması tarafından geliştirilmiştir.

---

## 📞 İletişim

Sorular veya öneriler için lütfen Issues bölümünü kullanınız.

**Geliştirici**: mehmetbozdemir24
