"""
Issue #1'de belirtilen basit kod örneği

Bu script, issue'da verilen Qdrant örnek kodunun çalışan versiyonudur.

Görevliler: Süleyman, Eren
"""

from qdrant_client import QdrantClient

def main():
    print("🚀 Qdrant Basit Örnek (Issue #1)")
    print("=" * 50)
    
    # Client oluştur
    client = QdrantClient("localhost", port=6333)
    print("✅ Client oluşturuldu")
    
    # Koleksiyon oluştur
    collection_name = "my_collection"
    
    try:
        # Eğer varsa sil
        client.delete_collection(collection_name)
    except:
        pass
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": 1024, "distance": "Cosine"}
    )
    print(f"✅ Koleksiyon '{collection_name}' oluşturuldu")
    
    # Vektör ekle
    client.upsert(
        collection_name=collection_name,
        points=[
            {
                "id": 1,
                "vector": [0.1] * 1024,
                "payload": {"source": "test.pdf"}
            }
        ]
    )
    print("✅ Vektör eklendi")
    
    # Basit sorgu
    hits = client.search(
        collection_name=collection_name,
        query_vector=[0.1] * 1024,
        limit=5
    )
    print(f"✅ Arama tamamlandı, {len(hits)} sonuç bulundu")
    print("\n📝 Sonuçlar:")
    for hit in hits:
        print(f"   - ID: {hit.id}, Score: {hit.score:.4f}, Payload: {hit.payload}")
    
    print("\n" + "=" * 50)
    print("✅ Örnek başarıyla tamamlandı!")


if __name__ == "__main__":
    main()
