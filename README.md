# 🤖 TÜBİTAK 1505 Projesi

**TÜBİTAK 1505 için Asistan Tasarımı**

TÜBİTAK 1505 Projesi, kurumsal dokümanlardan çıkarılan bilgiler üzerinde anlam-temelli aramalar yapan ve akıllı yanıtlar üreten bir yapay zekâ asistanıdır. Sistem, modern derin öğrenme modelleri ve vektör veritabanı teknolojileriyle hızlı, doğru ve bağlamsal yanıtlar sağlar.

---

## 📋 Sistem Mimarisi

TÜBİTAK 1505 Projesi sistemi dört ana aşamadan oluşur.

### 1️⃣ Doküman Ön İşleme & Chunking
- Proje kapsamındaki dokümanların okunması ve temizlenmesi  
- Metinlerin anlamlı parçalara (chunks) bölünmesi  
- **Görevliler:** Engin, Batuhan

### 2️⃣ Embedding Vektörleştirme
- Cosmos-e5-large ile metin parçalarının vektörleştirilmesi  
- Anlamsal temsil oluşturulması  
- **Görevliler:** Mehmet, Hasan

### 3️⃣ Vektör Veritabanı Yönetimi
- Embedding’lerin Docker üzerinden Qdrant’a yüklenmesi  
- Hızlı ve ölçeklenebilir arama altyapısının sağlanması  
- **Görevliler:** Süleyman, Eren

### 4️⃣ Akıllı Yanıt Üretimi
- Qdrant’tan bağlama uygun sonuçların çağrılması  
- **Gemma3-12B** ve **Qwen3-9B** ile doğal dil yanıtlarının üretilmesi  
- **Görevliler:** Hasan, Eren

---

## 🚀 Kullanım Akışı

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

---

## 🛠️ Teknoloji Stack

| Bileşen | Teknoloji |
|---|---|
| **Embedding Modeli** | Cosmos-e5-large |
| **Vektör Veritabanı** | Qdrant (Docker) |
| **LLM Modelleri** | Gemma3-12B, Qwen3-9B |
| **Container** | Docker |

---

## 👥 Görev Dağılımı

| 👤 **İsim** | 🧩 **Görev Tanımı** |
|---|---|
| **Engin** | Dokümanların ön işlenmesi ve chunk’lara ayrılması |
| **Batuhan** | Chunk oluşturma ve veri temizleme desteği |
| **Mehmet** | Metinlerin embedding modeliyle vektörleştirilmesi |
| **Hasan** | Embedding ve LLM tabanlı yanıt üretimi |
| **Süleyman** | Qdrant yönetimi, veri yükleme ve indeksleme |
| **Eren** | Qdrant yönetimi ve LLM tabanlı yanıt desteği |

---

## 📦 Gereksinimler

- Python 3.8+
- Docker & Docker Compose
- Qdrant Server
- PyTorch / TensorFlow
- Transformers

---

## 🔧 Kurulum

```bash
git clone https://github.com/mehmetbozdemir24/Tubitak_1505_Projesi.git
cd Tubitak_1505_Projesi
pip install -r requirements.txt
docker-compose up -d
python main.py


## 📚 Dokümantasyon

- `docs/1_chunking_guide.md` — Doküman işleme
- `docs/2_embedding_guide.md` — Vektörleştirme
- `docs/3_qdrant_setup_guide.md` — Veritabanı yönetimi
- `docs/4_llm_response_guide.md` — Yanıt üretimi
- `docs/5_complete_workflow.md` — Toplu İş Akışı

---

## 📄 Lisans

Bu proje **TÜBİTAK 1505 Projesi** kapsamında geliştirilmiştir.

---

## 📞 İletişim

Sorular/öneriler için lütfen **Issues** bölümünü kullanınız.  
**Geliştirici:** mehmetbozdemir24
