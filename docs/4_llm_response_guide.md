# Ollama + Qdrant RAG Pipeline

Bu rehber, Ollama ve Qdrant kullanarak basit bir RAG (Retrieve and Generate) pipeline'ını anlatmaktadır. Bu pipeline, çalışanların şirketten ayrılma süreleri gibi sorulara yanıt vermek için kullanılabilir.

## Süreç

1. **Soru Gömme**: Kullanıcıdan gelen soru, gömme (embedding) yöntemiyle vektör haline getirilir. Örneğin:
   - Soru: "Terracity şirketinden çalışanların ayrılma süreleri nedir?"
   - Gömme: `embed(question)`

2. **Qdrant Vektör Depolama**: Gömme vektörü, Qdrant vektör deposunda aranır. Bu işlem, benzer içeriklerin bulunmasını sağlar.
   - Arama: `search_in_qdrant(embedded_question)`

3. **Benzer İçerikleri Alma**: Qdrant, verilen gömme ile benzer olan içerik parçalarını döndürür.
   - Benzer İçerikler: `get_similar_chunks()`

4. **Ollama LLM Modeli**: Elde edilen içerikler, Ollama LLM modeli (Gemma3/Qwen3) ile işlenir.
   - Model: `ollama_model.process(similar_chunks)`

5. **Yanıt Dönüşü**: Model, kullanıcıya yanıt olarak döndürür.
   - Yanıt: `return answer`

## FastAPI Endpoint

Aşağıda, yukarıdaki süreci gerçekleştiren bir FastAPI endpoint örneği verilmiştir:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/ask/")
async def ask_question(q: Question):
    # Soru gömme
    embedded_question = embed(q.question)
    
    # Qdrant'ta arama yap
    similar_chunks = search_in_qdrant(embedded_question)
    
    # Ollama modelinden yanıt al
    answer = ollama_model.process(similar_chunks)
    
    return {"answer": answer}
```

Bu endpoint, kullanıcıdan bir soru alır, bunu gömer, Qdrant'ta arar ve benzer içerikler ile Ollama modelini kullanarak yanıt döndürür. 

---