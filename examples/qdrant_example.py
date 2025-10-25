"""
Qdrant Veritabanı Kullanım Örneği

Bu script, Qdrant entegrasyonunun nasıl kullanılacağını gösterir.
Issue #1'de belirtilen örnek kodu içerir.

Görevliler: Süleyman, Eren
"""

import sys
import os

# src klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from qdrant_client_manager import QdrantManager


def main():
    """Ana örnek fonksiyon"""
    
    print("=" * 60)
    print("🚀 Qdrant Veritabanı Entegrasyon Örneği")
    print("=" * 60)
    
    # 1. Qdrant Manager'ı başlat
    print("\n1️⃣ Qdrant Client'ı başlatılıyor...")
    qdrant = QdrantManager(host="localhost", port=6333)
    
    # 2. Koleksiyon oluştur
    print("\n2️⃣ Koleksiyon oluşturuluyor...")
    collection_name = "my_collection"
    
    # Eğer koleksiyon varsa sil (temiz başlangıç için)
    if qdrant.collection_exists(collection_name):
        print(f"⚠️ '{collection_name}' zaten mevcut, siliniyor...")
        qdrant.delete_collection(collection_name)
    
    # Yeni koleksiyon oluştur (1024 boyutlu vektörler için - Cosmos-E5-Large)
    qdrant.create_collection(
        collection_name=collection_name,
        vector_size=1024
    )
    
    # 3. Vektör ekle
    print("\n3️⃣ Vektörler ekleniyor...")
    
    # Örnek vektörler (gerçek uygulamada embedding modelinden gelecek)
    points = [
        {
            "id": 1,
            "vector": [0.1] * 1024,
            "payload": {
                "source": "test.pdf",
                "page": 1,
                "content": "Python programlama dilidir"
            }
        },
        {
            "id": 2,
            "vector": [0.2] * 1024,
            "payload": {
                "source": "document.pdf",
                "page": 5,
                "content": "Makine öğrenmesi yapay zekadır"
            }
        },
        {
            "id": 3,
            "vector": [0.15] * 1024,
            "payload": {
                "source": "test.pdf",
                "page": 2,
                "content": "Qdrant vektör veritabanıdır"
            }
        }
    ]
    
    qdrant.upsert_points(collection_name, points)
    
    # 4. Koleksiyon bilgilerini göster
    print("\n4️⃣ Koleksiyon bilgileri:")
    info = qdrant.get_collection_info(collection_name)
    if info:
        print(f"   📊 Koleksiyon: {info['name']}")
        print(f"   📊 Vektör Sayısı: {info['vectors_count']}")
        print(f"   📊 Vektör Boyutu: {info['vector_size']}")
        print(f"   📊 Mesafe Metriği: {info['distance']}")
    
    # 5. Basit arama yap
    print("\n5️⃣ Benzerlik araması yapılıyor...")
    query_vector = [0.1] * 1024  # Test sorgu vektörü
    
    results = qdrant.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5
    )
    
    print(f"\n📝 Arama Sonuçları ({len(results)} sonuç):")
    for i, result in enumerate(results, 1):
        print(f"\n   {i}. Sonuç:")
        print(f"      ID: {result['id']}")
        print(f"      Benzerlik Skoru: {result['score']:.4f}")
        print(f"      Kaynak: {result['payload'].get('source', 'N/A')}")
        print(f"      Sayfa: {result['payload'].get('page', 'N/A')}")
        print(f"      İçerik: {result['payload'].get('content', 'N/A')}")
    
    # 6. Filtrelenmiş arama
    print("\n6️⃣ Filtrelenmiş arama yapılıyor (source='test.pdf')...")
    filtered_results = qdrant.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5,
        filter_conditions={"source": "test.pdf"}
    )
    
    print(f"\n📝 Filtrelenmiş Sonuçlar ({len(filtered_results)} sonuç):")
    for i, result in enumerate(filtered_results, 1):
        print(f"\n   {i}. Sonuç:")
        print(f"      ID: {result['id']}")
        print(f"      Benzerlik Skoru: {result['score']:.4f}")
        print(f"      Kaynak: {result['payload'].get('source', 'N/A')}")
        print(f"      İçerik: {result['payload'].get('content', 'N/A')}")
    
    # 7. Belirli bir ID'ye göre vektör getir
    print("\n7️⃣ ID=1 olan vektör getiriliyor...")
    point = qdrant.get_point(collection_name, 1)
    if point:
        print(f"   ✅ Vektör bulundu!")
        print(f"   ID: {point['id']}")
        print(f"   Payload: {point['payload']}")
    
    # 8. Tüm koleksiyonları listele
    print("\n8️⃣ Tüm koleksiyonlar:")
    collections = qdrant.list_collections()
    for col in collections:
        print(f"   📁 {col}")
    
    # 9. Bağlantıyı kapat
    print("\n9️⃣ Bağlantı kapatılıyor...")
    qdrant.close()
    
    print("\n" + "=" * 60)
    print("✅ Örnek başarıyla tamamlandı!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ İşlem kullanıcı tarafından iptal edildi.")
    except Exception as e:
        print(f"\n\n❌ Hata oluştu: {e}")
        import traceback
        traceback.print_exc()
