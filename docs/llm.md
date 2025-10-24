# LLM Yanıt Üretimi

## Genel Bakış

LLM modülü, Qdrant'tan alınan ilgili doküman parçalarını kullanarak kullanıcı sorularına doğal dil yanıtları üretir.

## Görevliler

- **Hasan**: LLM entegrasyonu ve prompt engineering
- **Eren**: Yanıt optimizasyonu ve kalite kontrolü

## Desteklenen Modeller

### Gemma3-12B
- Google tarafından geliştirildi
- 12 milyar parametre
- Yüksek kaliteli Türkçe desteği

### Qwen3-9B
- Alibaba tarafından geliştirildi
- 9 milyar parametre
- Çok dilli uzman model

## Kullanım

### Temel Yanıt Üretimi

```python
from src.llm import ResponseGenerator

# LLM oluştur
llm = ResponseGenerator(model_name="gemma3-12b", temperature=0.7)

# Yanıt üret
context = ["Doküman parçası 1", "Doküman parçası 2"]
response = llm.generate_response(
    question="Sorum nedir?",
    context_chunks=context,
    max_tokens=512
)

print(response)
```

### Retrieval ile Yanıt Üretimi

```python
# Qdrant'tan sonuçlar al
results = qdrant.search(collection_name, query_vector, limit=5)

# Yanıt üret
response = llm.generate_with_retrieval(
    question="Sorum nedir?",
    retrieved_results=results,
    max_tokens=512
)

print(f"Yanıt: {response['answer']}")
print(f"Güven: {response['confidence']:.2f}")
print(f"Kaynak sayısı: {response['num_sources']}")
```

## Prompt Engineering

### Şablon Yapısı

```python
template = """Sen Terracity firmasının Bilimp yapay zeka asistanısın. 
Verilen bağlam bilgilerini kullanarak soruyu yanıtla.

Bağlam:
{context}

Soru: {question}

Yanıt:"""
```

### Özel Şablon

```python
from langchain.prompts import PromptTemplate

custom_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""[Özel prompt metni]
    
    Bağlam: {context}
    Soru: {question}
    """
)
```

## Parametreler

### Temperature (Sıcaklık)

Yaratıcılık seviyesini kontrol eder:

- **0.0-0.3**: Deterministik, tutarlı yanıtlar
- **0.4-0.7**: Dengeli, önerilen (varsayılan: 0.7)
- **0.8-1.0**: Yaratıcı, çeşitli yanıtlar

```python
# Daha tutarlı yanıtlar için
llm = ResponseGenerator(temperature=0.3)

# Daha yaratıcı yanıtlar için
llm = ResponseGenerator(temperature=0.9)
```

### Max Tokens

Maksimum yanıt uzunluğu:

```python
response = llm.generate_response(
    question=question,
    context_chunks=context,
    max_tokens=1024  # Daha uzun yanıtlar
)
```

## Tam Sistem Entegrasyonu

```python
from src.chunking import DocumentProcessor
from src.embedding import TextEmbedder
from src.qdrant import QdrantManager
from src.llm import ResponseGenerator

# Bileşenleri başlat
doc_processor = DocumentProcessor()
embedder = TextEmbedder()
qdrant = QdrantManager()
qdrant.connect()
llm = ResponseGenerator()

# 1. Doküman işle
chunks = doc_processor.process_document("dokuman.pdf")

# 2. Embedding oluştur
embeddings = embedder.embed_batch(chunks)

# 3. Qdrant'a yükle
payloads = [{"text": chunk} for chunk in chunks]
qdrant.upload_vectors("bilimp_docs", embeddings, payloads)

# 4. Soru sor
question = "Doküman ne hakkında?"
query_vector = embedder.embed_text(question)
results = qdrant.search("bilimp_docs", query_vector, limit=5)

# 5. Yanıt üret
response = llm.generate_with_retrieval(question, results)
print(response['answer'])
```

## Yanıt Kalitesi

### Güven Skoru

Yanıtın güvenilirliğini gösterir:

```python
confidence = response['confidence']

if confidence > 0.8:
    print("Yüksek güven: Yanıt çok güvenilir")
elif confidence > 0.6:
    print("Orta güven: Yanıt makul")
else:
    print("Düşük güven: Yanıt şüpheli olabilir")
```

### Kaynak Takibi

Yanıtın hangi dokümanlardan geldiğini izler:

```python
print(f"Kullanılan kaynak sayısı: {response['num_sources']}")
for i, source in enumerate(response['sources']):
    print(f"\nKaynak {i+1}:")
    print(source[:200] + "...")
```

## Hata Yönetimi

### İlgili Bilgi Bulunamadı

```python
if response['confidence'] < 0.3:
    print("Üzgünüm, bu soruyla ilgili yeterli bilgi bulunamadı.")
```

### Model Yükleme Hatası

```python
try:
    llm = ResponseGenerator(model_name="model_adı")
except RuntimeError as e:
    print(f"Model yüklenemedi: {e}")
```

## Performans Optimizasyonu

### Batch İşleme

Birden fazla soru için:

```python
questions = ["Soru 1", "Soru 2", "Soru 3"]
responses = []

for question in questions:
    query_vector = embedder.embed_text(question)
    results = qdrant.search(collection, query_vector)
    response = llm.generate_with_retrieval(question, results)
    responses.append(response)
```

### Önbellekleme

Sık sorulan sorular için:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(question):
    # ... arama ve yanıt üretimi
    return response
```

## Model Karşılaştırması

| Özellik | Gemma3-12B | Qwen3-9B |
|---------|------------|----------|
| Parametre | 12B | 9B |
| Türkçe | Çok iyi | İyi |
| Hız | Orta | Hızlı |
| Bellek | 24GB+ | 18GB+ |
| Önerilen | Kalite öncelikli | Hız öncelikli |

## İleriye Dönük Geliştirmeler

- [ ] Streaming yanıtlar (gerçek zamanlı)
- [ ] Çoklu model desteği (ensemble)
- [ ] Fine-tuning domain-specific data ile
- [ ] Konuşma geçmişi (chat history)
- [ ] Çok dilli yanıt üretimi
- [ ] Fact-checking ve hallucination detection
