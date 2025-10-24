# LLM Yanıt Sistemi - Teknik Uygulama Rehberi

Bu doküman, RAG (Retrieval-Augmented Generation) mimarisine dayalı kurumsal döküman asistanının temel API servisinin nasıl oluşturulduğunu adım adım açıklamaktadır. FastAPI kullanılarak geliştirilen bu servis, kullanıcı sorgularını alır, Qdrant vektör veritabanından ilgili bağlamı çeker, büyük dil modelini (LLM) kullanarak bir yanıt üretir ve sonucu kullanıcıya güvenli bir şekilde döndürür.

Aşağıda, sistemin her bir parçasını detaylandıran kod blokları ve açıklamaları bulunmaktadır.

## 1. Gerekli Kütüphanelerin Yüklenmesi (Imports)

Uygulamanın temelini oluşturan kütüphaneler bu bölümde içeri aktarılır. `FastAPI` web sunucusu için, `QdrantClient` vektör veritabanı iletişimi için, `OllamaLLM` ise büyük dil modeliyle etkileşim için kullanılır.

```python
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from qdrant_client import QdrantClient
from langchain.llms import OllamaLLM
from langchain.memory import ConversationBufferWindowMemory
```

## 2. Sistem Yapılandırması ve Başlatma

Bu adımda, sistemin temel bileşenleri yapılandırılır ve başlatılır.

- **FastAPI Uygulaması**: `API Servisi`'nin giriş noktasıdır.
- **Qdrant İstemcisi**: `Retriever` katmanının bir parçası olarak, doküman parçalarını (chunk) ve vektörlerini saklayan Qdrant veritabanına bağlanır. Bağlantı bilgileri ortam değişkenlerinden (`environment variables`) güvenli bir şekilde alınır.
- **Büyük Dil Modeli (LLM)**: `Reader` katmanını temsil eder. Bu örnekte, yerel olarak çalışan bir `OllamaLLM` modeli kullanılmaktadır.
- **Konuşma Belleği (Memory)**: Kullanıcıyla olan etkileşimin kısa süreli geçmişini tutarak daha tutarlı diyaloglar kurulmasını sağlar.

```python
# FastAPI uygulamasının başlatılması
app = FastAPI()

# Qdrant yapılandırması
# Vektör veritabanına bağlanmak için istemci oluşturulur.
qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

# OllamaLLM ayarları
# Reader (Okuyucu) katmanını temsil eden büyük dil modeli.
def create_llm():
    return OllamaLLM(model="gpt-oss:20b")

llm = create_llm()

# Bellek yapılandırması
# Sohbet geçmişini tutmak için bir bellek nesnesi oluşturulur.
memory = ConversationBufferWindowMemory(size=5)
```

## 3. Veri Modelleri (Pydantic)

API'ye gelecek olan isteklerin yapısını tanımlamak için Pydantic modelleri kullanılır. Bu, veri doğrulamasını otomatikleştirir ve kodun daha güvenilir olmasını sağlar. `QueryInput` modeli, kullanıcının sorusunu ve ilgili doküman bilgilerini içerir.

```python
# QueryInput Modeli
# API'ye gönderilecek sorgunun formatını tanımlar.
class QueryInput(BaseModel):
    document_id: str
    collection_name: str
    question: str
```

## 4. Yardımcı Fonksiyonlar

Sistemin ana mantığını destekleyen çekirdek fonksiyonlar bu bölümde yer alır.

### Güvenli Metin İşleme

LLM tarafından üretilen yanıtlarda bulunabilecek olası zararlı kodları (örn: `<script>` etiketleri) temizleyerek güvenliği artırır.

```python
# Güvenli metin işleme fonksiyonu
def safe_text(text: str) -> str:
    # Metin üzerindeki tehlikeli içerikleri temizler
    return text.replace("<script>", "").replace("</script>", "")
```

### Vektör Veritabanından Bağlam Alma (Retriever)

Bu fonksiyon, RAG mimarisinin "Retrieval" (Geri Getirme) adımını gerçekleştirir. Kullanıcının sorusuyla ilgili en alakalı doküman parçalarını (context) bulmak için Qdrant veritabanında anlamsal arama yapar. Bu, LLM'in daha doğru ve kanıta dayalı yanıtlar üretmesini sağlar.

```python
# Bağlamı vektör veritabanından alma fonksiyonu
def get_context_from_vector_db(document_id: str, chunk_no: int):
    # Semantik arama ve anahtar kelime araması ile veri al
    # Not: Gerçek bir uygulamada sorgu, sorunun kendisinin vektör temsili olmalıdır.
    results = qdrant_client.search(
        collection_name="my_collection",
        query_vector=document_id, # Örnek amaçlıdır, normalde buraya bir vektör gelmelidir.
        filter={"chunk_no": chunk_no}
    )
    # Sonuçları döndür
    return results
```

## 5. API Endpoint: Sorgu ve Yanıt (/ask)

Bu bölüm, sistemin "Orkestrasyon" katmanının temel bir versiyonunu temsil eder. Kullanıcıdan gelen isteği karşılar ve RAG akışını yönetir.

1.  **Sohbet Geçmişini Yükle**: Önceki konuşmaları belleğe yükler.
2.  **Bağlamı Al (Retrieve)**: `get_context_from_vector_db` fonksiyonu ile Qdrant'tan ilgili doküman parçalarını çeker.
3.  **İstem (Prompt) Oluştur**: Elde edilen bağlam (context) ve kullanıcının sorusu birleştirilerek LLM'e gönderilecek olan istem (prompt) hazırlanır.
4.  **Yanıt Üret (Generate)**: LLM, hazırlanan istemi işleyerek bir yanıt üretir.
5.  **Güvenliği Sağla ve Kaydet**: Üretilen yanıt `safe_text` fonksiyonundan geçirilir ve sohbet geçmişine eklenir.
6.  **Yanıtı Döndür**: Sonuç, JSON formatında kullanıcıya gönderilir.

```python
# POST /ask/ endpoint’i
@app.post("/ask/")
def ask(query_input: QueryInput):
    try:
        # 1. Önceden kaydedilen sohbet geçmişini yükle
        chat_history = memory.load_context()
        
        # 2. Vektör veritabanından bağlam al (Retrieval)
        context = get_context_from_vector_db(query_input.document_id, 0)
        
        # 3. Formatlanmış istem oluştur
        prompt = f"Bağlam: {context}\n\nSoru: {query_input.question}"
        
        # 4. LLM’i çağır ve yanıtı al (Generation)
        response = llm.invoke(prompt)
        
        # 5. Güvenli metin uygulaması ve belleğe kaydetme
        safe_response = safe_text(response)
        memory.save_context(chat_history + [safe_response])
        
        # 6. JSON yanıtı döndür
        return JSONResponse(content={"response": safe_response})
    except Exception as e:
        # Hata durumunda istemciye 500 kodu ile detaylı bilgi döndür.
        raise HTTPException(status_code=500, detail=str(e))
```