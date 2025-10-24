# Tam Python Kodu Örneği

Aşağıda FastAPI uygulaması, güvenli metin işleme, Qdrant yapılandırması ve diğer bileşenlerin nasıl kullanılacağını gösteren tam bir Python kodu örneği bulunmaktadır.

```python
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from qdrant_client import QdrantClient
from langchain.llms import OllamaLLM
from langchain.memory import ConversationBufferWindowMemory

# FastAPI uygulamasının başlatılması
app = FastAPI()

# Qdrant yapılandırması
qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

# OllamaLLM ayarları
def create_llm():
    return OllamaLLM(model="gpt-oss:20b")

llm = create_llm()

# Bellek yapılandırması
memory = ConversationBufferWindowMemory(size=5)

# QueryInput Modeli
class QueryInput(BaseModel):
    document_id: str
    collection_name: str
    question: str

# Güvenli metin işleme fonksiyonu
def safe_text(text: str) -> str:
    # Metin üzerindeki tehlikeli içerikleri temizler
    return text.replace("<script>", "").replace("</script>", "")

# Bağlamı vektör veritabanından alma fonksiyonu
def get_context_from_vector_db(document_id: str, chunk_no: int):
    # Semantik arama ve anahtar kelime araması ile veri al
    results = qdrant_client.search(
        collection_name="my_collection",
        query=document_id,
        filter={"chunk_no": chunk_no}
    )
    # Sonuçları döndür
    return results

# POST /ask/ endpoint’i
@app.post("/ask/")
def ask(query_input: QueryInput):
    try:
        # Önceden kaydedilen sohbet geçmişini yükle
        chat_history = memory.load_context()
        # Vektör veritabanından bağlam al
        context = get_context_from_vector_db(query_input.document_id, 0)
        # Formatlanmış istem oluştur
        prompt = f"{context}\nSoru: {query_input.question}"
        # LLM’i çağır ve yanıtı al
        response = llm.invoke(prompt)
        # Güvenli metin uygulaması
        safe_response = safe_text(response)
        # Belleğe kaydet
        memory.save_context(chat_history + [safe_response])
        # JSON yanıtı döndür
        return JSONResponse(content={"response": safe_response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```  

Bu kod, FastAPI'yi kullanarak bir API oluşturur ve Qdrant ile etkileşimde bulunur. Kullanıcıdan gelen soruları işler ve güvenli bir şekilde yanıt döndürür.