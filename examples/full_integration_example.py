"""
Tam Entegrasyon Örneği: Embedding + Qdrant

Bu script, embedding modelinden gelen vektörlerin Qdrant'a nasıl kaydedileceğini
ve nasıl aranacağını gösterir.

Bu örnek, docs/5_complete_workflow.md dosyasındaki "Adım 2: Veri Toplama ve Ön İşleme"
kısmını simüle eder.

Görevliler: Süleyman, Eren (Qdrant), Mehmet, Hasan (Embedding)
"""

import sys
import os

# src klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from qdrant_client_manager import QdrantManager


def simulate_embedding_workflow():
    """
    Embedding modülünden gelen vektörlerin Qdrant'a kaydedilmesi
    
    Bu fonksiyon, gerçek uygulamada şu şekilde çalışacak:
    1. Chunking modülü (Engin, Batuhan) dokümanları parçalara ayırır
    2. Embedding modülü (Mehmet, Hasan) her parçayı vektörleştirir
    3. Qdrant modülü (Süleyman, Eren) vektörleri kaydeder
    """
    
    print("=" * 70)
    print("🔄 TAM ENTEGRASYON ÖRNEĞİ: EMBEDDING + QDRANT")
    print("=" * 70)
    
    # Simüle edilmiş chunking çıktısı (Engin, Batuhan'ın çalışması)
    print("\n1️⃣ Dokümanlar parçalanıyor (Chunking)...")
    chunks = [
        {
            "id": 1,
            "content": "Python programlama dili, yüksek seviyeli bir dildir.",
            "metadata": {
                "source": "python_kitap.pdf",
                "page": 15,
                "chapter": "Giriş"
            }
        },
        {
            "id": 2,
            "content": "Makine öğrenmesi, yapay zekanın bir alt dalıdır.",
            "metadata": {
                "source": "ml_kitap.pdf",
                "page": 3,
                "chapter": "Temel Kavramlar"
            }
        },
        {
            "id": 3,
            "content": "Qdrant, vektör veritabanı için kullanılan bir araçtır.",
            "metadata": {
                "source": "veritabani_kitap.pdf",
                "page": 42,
                "chapter": "Vektör Veritabanları"
            }
        },
        {
            "id": 4,
            "content": "TÜBİTAK 1505 projesi, kurumsal doküman danışmanı geliştiriyor.",
            "metadata": {
                "source": "proje_dokuman.pdf",
                "page": 1,
                "chapter": "Özet"
            }
        }
    ]
    print(f"   ✅ {len(chunks)} chunk oluşturuldu")
    
    # Simüle edilmiş embedding çıktısı (Mehmet, Hasan'ın çalışması)
    # Gerçek uygulamada: turkish-e5-large modeli ile 1024 boyutlu vektörler
    print("\n2️⃣ Chunk'lar vektörleştiriliyor (Embedding - Turkish-E5-Large)...")
    embeddings_data = []
    for chunk in chunks:
        # Simüle edilmiş embedding vektörü
        # Gerçekte: embeddings.embed_query(chunk["content"]) kullanılacak
        simulated_vector = [float(chunk["id"]) * 0.1] * 1024
        
        embeddings_data.append({
            "id": chunk["id"],
            "vector": simulated_vector,
            "content": chunk["content"],
            "metadata": chunk["metadata"]
        })
    print(f"   ✅ {len(embeddings_data)} vektör oluşturuldu (1024-dimensional)")
    
    # Qdrant'a kaydetme (Süleyman, Eren'in çalışması)
    print("\n3️⃣ Vektörler Qdrant'a kaydediliyor...")
    qdrant = QdrantManager(host="localhost", port=6333)
    
    collection_name = "tubitak_documents"
    
    # Koleksiyon oluştur (eğer yoksa)
    if qdrant.collection_exists(collection_name):
        print(f"   ⚠️ '{collection_name}' zaten mevcut")
    else:
        qdrant.create_collection(
            collection_name=collection_name,
            vector_size=1024  # Cosmos-E5-Large için
        )
    
    # Vektörleri Qdrant'a ekle
    points = []
    for item in embeddings_data:
        points.append({
            "id": item["id"],
            "vector": item["vector"],
            "payload": {
                "content": item["content"],
                "source": item["metadata"]["source"],
                "page": item["metadata"]["page"],
                "chapter": item["metadata"]["chapter"]
            }
        })
    
    qdrant.upsert_points(collection_name, points)
    
    # Koleksiyon bilgilerini göster
    print("\n4️⃣ Koleksiyon bilgileri:")
    info = qdrant.get_collection_info(collection_name)
    if info:
        print(f"   📊 Koleksiyon: {info['name']}")
        print(f"   📊 Toplam Vektör: {info['vectors_count']}")
        print(f"   📊 Vektör Boyutu: {info['vector_size']}")
        print(f"   📊 Mesafe: {info['distance']}")
    
    # Kullanıcı sorgusunu simüle et
    print("\n5️⃣ Kullanıcı sorgusu simülasyonu...")
    user_query = "Makine öğrenmesi nedir?"
    print(f"   👤 Kullanıcı Sorusu: '{user_query}'")
    
    # Sorgu vektörü oluştur (gerçekte embedding modeli kullanılacak)
    # query_vector = embeddings.embed_query(user_query)
    query_vector = [0.2] * 1024  # Simüle edilmiş sorgu vektörü
    
    # Qdrant'ta arama yap
    print("\n6️⃣ Qdrant'ta semantik arama yapılıyor...")
    results = qdrant.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=3
    )
    
    print(f"\n   📝 En İlgili {len(results)} Sonuç:")
    for i, result in enumerate(results, 1):
        print(f"\n   {i}. Sonuç (Benzerlik: {result['score']:.4f})")
        print(f"      💬 İçerik: {result['payload']['content']}")
        print(f"      📄 Kaynak: {result['payload']['source']}")
        print(f"      📖 Sayfa: {result['payload']['page']}")
        print(f"      📚 Bölüm: {result['payload']['chapter']}")
    
    # Filtrelenmiş arama örneği
    print("\n7️⃣ Filtrelenmiş arama (sadece 'ml_kitap.pdf')...")
    filtered_results = qdrant.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5,
        filter_conditions={"source": "ml_kitap.pdf"}
    )
    
    print(f"   📝 Filtrelenmiş Sonuçlar: {len(filtered_results)} sonuç")
    for result in filtered_results:
        print(f"      - {result['payload']['content'][:50]}...")
    
    # Gerçek workflow'da sonraki adım (Hasan, Eren'in çalışması)
    print("\n8️⃣ Sonraki Adım: LLM ile Yanıt Üretimi")
    print("   🤖 Bulunan context'ler LLM'e (Gemma3-12B/Qwen3-8B) gönderilecek")
    print("   🤖 LLM, bu bilgilere dayanarak kullanıcıya yanıt üretecek")
    
    # Bağlantıyı kapat
    qdrant.close()
    
    print("\n" + "=" * 70)
    print("✅ Entegrasyon örneği tamamlandı!")
    print("=" * 70)
    
    # Gerçek workflow özeti
    print("\n📋 GERÇEK İŞ AKIŞI ÖZETİ:")
    print("   1. Engin, Batuhan → Chunking")
    print("   2. Mehmet, Hasan → Embedding (turkish-e5-large)")
    print("   3. Süleyman, Eren → Qdrant'a kaydetme (bu modül)")
    print("   4. Kullanıcı sorgusu → Embedding")
    print("   5. Qdrant'ta arama → Context bulma")
    print("   6. Hasan, Eren → LLM ile yanıt üretimi")
    print("   7. Kullanıcıya yanıt sunumu")


def real_world_example_with_notes():
    """
    Gerçek projede nasıl kullanılacağına dair kod örneği
    """
    print("\n\n" + "=" * 70)
    print("📖 GERÇEK PROJE KULLANIMI")
    print("=" * 70)
    
    print("""
Bu modül gerçek projede şu şekilde kullanılacak:

# 1. Chunking modülünden chunks al (Engin, Batuhan)
from chunking_module import ChunkingProcessor
chunking = ChunkingProcessor()
chunks = chunking.process_documents(['doc1.pdf', 'doc2.pdf'])

# 2. Embedding modülü ile vektörleştir (Mehmet, Hasan)
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="ytu-ce-cosmos/turkish-e5-large"
)

# 3. Qdrant'a kaydet (Süleyman, Eren)
from qdrant_client_manager import QdrantManager
qdrant = QdrantManager()
qdrant.create_collection("documents", vector_size=1024)

points = []
for i, chunk in enumerate(chunks):
    vector = embeddings.embed_query(chunk.page_content)
    points.append({
        "id": i,
        "vector": vector,
        "payload": {
            "content": chunk.page_content,
            "metadata": chunk.metadata
        }
    })

qdrant.upsert_points("documents", points)

# 4. Kullanıcı sorgusunu işle
user_query = "TÜBİTAK 1505 nedir?"
query_vector = embeddings.embed_query(user_query)

# 5. İlgili dokümanları bul
results = qdrant.search("documents", query_vector, limit=5)

# 6. LLM ile yanıt üret (Hasan, Eren)
from llm_module import LLMGenerator
llm = LLMGenerator(model="gemma3-12b")
context = "\n".join([r['payload']['content'] for r in results])
response = llm.generate_response(user_query, context)

print(response)
    """)


if __name__ == "__main__":
    try:
        simulate_embedding_workflow()
        real_world_example_with_notes()
    except KeyboardInterrupt:
        print("\n\n⚠️ İşlem kullanıcı tarafından iptal edildi.")
    except Exception as e:
        print(f"\n\n❌ Hata oluştu: {e}")
        import traceback
        traceback.print_exc()
