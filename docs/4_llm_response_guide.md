# Ollama + Qdrant RAG Pipeline

## ADIM 1: Ayarlar
- Gerekli ayarların yapılması.

## ADIM 2: Qdrant'tan Benzer İçerik Çekme
- Qdrant veritabanından benzer içeriklerin çekilmesi için gerekli adımlar.

## ADIM 3: Prompt Hazırlama
- Kullanıcıdan alınan bilgiye göre uygun prompt'un hazırlanması.

## ADIM 4: LLM Cevap Alma
- Hazırlanan prompt ile LLM'den cevap alınması.

## FastAPI Örneği
- Aşağıda basit bir FastAPI örneği verilmiştir:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/get_answer/")
async def get_answer(collection_name: str):
    context = get_context(collection_name)
    prompt = create_prompt(context)
    answer = get_answer(prompt)
    return answer
```

## Test Kodları
- Aşağıda test kodlarına örnek verilmiştir:

```python
def test_get_answer():
    response = client.get("/get_answer/?collection_name=test")
    assert response.status_code == 200
    assert "expected_answer" in response.json()
```
