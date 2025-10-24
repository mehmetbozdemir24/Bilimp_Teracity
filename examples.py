"""
Bilimp Kullanım Örnekleri
"""

# Örnek 1: Doküman İşleme
print("=== Örnek 1: Doküman İşleme ===\n")

from src.chunking import DocumentProcessor

processor = DocumentProcessor(chunk_size=512, chunk_overlap=50)

# Test metni
test_text = """
Bilimp, Terracity firması için geliştirilmiş bir yapay zeka asistanıdır.
Sistem, dokümanlardan bilgi çıkararak kullanıcı sorularına yanıt verir.
Modern derin öğrenme modelleri ve vektör veritabanı teknolojisi kullanır.
Cosmos-e5-large embedding modeli ile metinler vektörleştirilir.
Qdrant vektör veritabanı hızlı arama sağlar.
Gemma3-12B ve Qwen3-9B modelleri yanıt üretir.
""" * 3

# Metni temizle ve chunk'lara böl
clean = processor.clean_text(test_text)
chunks = processor.chunk_text(clean)

print(f"Oluşturulan chunk sayısı: {len(chunks)}")
print(f"\nİlk chunk:")
print(chunks[0])

# Örnek 2: Embedding
print("\n\n=== Örnek 2: Embedding Oluşturma ===\n")

from src.embedding import TextEmbedder

embedder = TextEmbedder()

# Tek metin vektörleştirme
text = "Bilimp yapay zeka asistanı"
vector = embedder.embed_text(text)

print(f"Metin: {text}")
print(f"Vektör boyutu: {vector.shape}")
print(f"İlk 5 değer: {vector[:5]}")

# Toplu vektörleştirme
texts = chunks[:3]
vectors = embedder.embed_batch(texts)
print(f"\n{len(texts)} metin için embedding oluşturuldu")
print(f"Embedding matrisi boyutu: {vectors.shape}")

# Örnek 3: Qdrant (Docker gerekli)
print("\n\n=== Örnek 3: Qdrant Veritabanı ===\n")

from src.qdrant import QdrantManager
import numpy as np

qdrant = QdrantManager(host="localhost", port=6333)

try:
    qdrant.connect()
    print("✓ Qdrant'a bağlanıldı")
    
    collection_name = "test_collection"
    
    # Koleksiyon oluştur (yoksa)
    if not qdrant.collection_exists(collection_name):
        embedding_dim = embedder.get_embedding_dimension()
        qdrant.create_collection(collection_name, embedding_dim)
        print(f"✓ Koleksiyon oluşturuldu: {collection_name}")
    else:
        print(f"✓ Koleksiyon zaten mevcut: {collection_name}")
    
    # Vektörleri yükle
    payloads = [{"text": chunk, "index": i} for i, chunk in enumerate(chunks[:5])]
    qdrant.upload_vectors(collection_name, vectors[:5], payloads)
    print(f"✓ {len(vectors[:5])} vektör yüklendi")
    
    # Arama yap
    query_text = "Bilimp nedir?"
    query_vector = embedder.embed_text(query_text)
    results = qdrant.search(collection_name, query_vector, limit=3)
    
    print(f"\nSoru: {query_text}")
    print(f"Bulunan sonuç sayısı: {len(results)}")
    for i, result in enumerate(results):
        print(f"\nSonuç {i+1}:")
        print(f"  Score: {result['score']:.3f}")
        print(f"  Text: {result['payload']['text'][:100]}...")
    
except Exception as e:
    print(f"✗ Qdrant hatası: {e}")
    print("  Docker ile Qdrant'ı başlatın: docker-compose up -d")

# Örnek 4: LLM Yanıt Üretimi
print("\n\n=== Örnek 4: LLM Yanıt Üretimi ===\n")

from src.llm import ResponseGenerator

llm = ResponseGenerator(model_name="gemma3-12b", temperature=0.7)

question = "Bilimp hangi teknolojileri kullanır?"
context = [
    "Bilimp, Cosmos-e5-large embedding modeli kullanır.",
    "Qdrant vektör veritabanı ile hızlı arama yapar.",
    "Gemma3-12B ve Qwen3-9B modelleri ile yanıt üretir."
]

print(f"Soru: {question}")
print(f"Bağlam chunk sayısı: {len(context)}")

# Not: Gerçek LLM modeli yüklenmediği için placeholder yanıt döner
response = llm.generate_response(question, context)
print(f"\nYanıt: {response}")

# Tam sistem örneği
print("\n\n=== Tam Sistem Akışı ===\n")

print("""
1. Doküman yüklenir (PDF) → chunk'lara bölünür
2. Chunk'lar → embedding vektörlerine dönüştürülür
3. Vektörler → Qdrant'a yüklenir
4. Kullanıcı sorusu → embedding'e dönüştürülür
5. Qdrant'ta benzer vektörler aranır
6. Bulunan chunk'lar → LLM'e bağlam olarak verilir
7. LLM → doğal dil yanıtı üretir
""")

print("Tüm örnekler tamamlandı! ✓")
