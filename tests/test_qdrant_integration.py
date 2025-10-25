"""
Qdrant Entegrasyon Testleri

Bu modül, Qdrant veritabanı entegrasyonunun doğru çalışıp çalışmadığını test eder.

Görevliler: Süleyman, Eren

Not: Bu testleri çalıştırmadan önce Qdrant sunucusunun çalışıyor olması gerekir:
    docker run -p 6333:6333 qdrant/qdrant
"""

import unittest
import sys
import os

# src klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from qdrant_client_manager import QdrantManager


class TestQdrantIntegration(unittest.TestCase):
    """Qdrant entegrasyonu için test sınıfı"""
    
    @classmethod
    def setUpClass(cls):
        """Test sınıfı başlatılırken çalışır"""
        cls.test_collection = "test_collection"
        cls.qdrant = QdrantManager(host="localhost", port=6333)
        
    @classmethod
    def tearDownClass(cls):
        """Test sınıfı sonlandırılırken çalışır"""
        # Test koleksiyonunu temizle
        if cls.qdrant.collection_exists(cls.test_collection):
            cls.qdrant.delete_collection(cls.test_collection)
        cls.qdrant.close()
    
    def setUp(self):
        """Her test öncesi çalışır"""
        # Eğer test koleksiyonu varsa sil
        if self.qdrant.collection_exists(self.test_collection):
            self.qdrant.delete_collection(self.test_collection)
    
    def test_01_create_collection(self):
        """Test: Koleksiyon oluşturma"""
        result = self.qdrant.create_collection(
            collection_name=self.test_collection,
            vector_size=1024
        )
        self.assertTrue(result, "Koleksiyon oluşturulamadı")
        self.assertTrue(
            self.qdrant.collection_exists(self.test_collection),
            "Koleksiyon oluşturuldu ama mevcut değil"
        )
    
    def test_02_collection_exists(self):
        """Test: Koleksiyon var mı kontrolü"""
        # Önce koleksiyon oluştur
        self.qdrant.create_collection(self.test_collection, vector_size=1024)
        
        # Var olan koleksiyon kontrolü
        exists = self.qdrant.collection_exists(self.test_collection)
        self.assertTrue(exists, "Mevcut koleksiyon bulunamadı")
        
        # Olmayan koleksiyon kontrolü
        not_exists = self.qdrant.collection_exists("nonexistent_collection")
        self.assertFalse(not_exists, "Olmayan koleksiyon bulundu")
    
    def test_03_list_collections(self):
        """Test: Koleksiyonları listeleme"""
        # Test koleksiyonu oluştur
        self.qdrant.create_collection(self.test_collection, vector_size=1024)
        
        # Koleksiyonları listele
        collections = self.qdrant.list_collections()
        self.assertIsInstance(collections, list, "Liste döndürülmedi")
        self.assertIn(self.test_collection, collections, "Oluşturulan koleksiyon listede yok")
    
    def test_04_upsert_points(self):
        """Test: Vektör ekleme"""
        # Koleksiyon oluştur
        self.qdrant.create_collection(self.test_collection, vector_size=128)
        
        # Test vektörleri
        points = [
            {
                "id": 1,
                "vector": [0.1] * 128,
                "payload": {"text": "Test vektörü 1"}
            },
            {
                "id": 2,
                "vector": [0.2] * 128,
                "payload": {"text": "Test vektörü 2"}
            }
        ]
        
        # Vektörleri ekle
        result = self.qdrant.upsert_points(self.test_collection, points)
        self.assertTrue(result, "Vektörler eklenemedi")
        
        # Koleksiyon bilgisini kontrol et
        info = self.qdrant.get_collection_info(self.test_collection)
        self.assertIsNotNone(info, "Koleksiyon bilgisi alınamadı")
        self.assertEqual(info["vectors_count"], 2, "Vektör sayısı yanlış")
    
    def test_05_search(self):
        """Test: Vektör arama"""
        # Koleksiyon oluştur ve vektör ekle
        self.qdrant.create_collection(self.test_collection, vector_size=128)
        points = [
            {
                "id": 1,
                "vector": [0.1] * 128,
                "payload": {"source": "doc1.pdf", "text": "Metin 1"}
            },
            {
                "id": 2,
                "vector": [0.5] * 128,
                "payload": {"source": "doc2.pdf", "text": "Metin 2"}
            }
        ]
        self.qdrant.upsert_points(self.test_collection, points)
        
        # Arama yap
        query_vector = [0.1] * 128
        results = self.qdrant.search(
            collection_name=self.test_collection,
            query_vector=query_vector,
            limit=2
        )
        
        self.assertIsInstance(results, list, "Arama sonucu liste değil")
        self.assertGreater(len(results), 0, "Hiç sonuç bulunamadı")
        self.assertIn("id", results[0], "Sonuçta ID yok")
        self.assertIn("score", results[0], "Sonuçta skor yok")
        self.assertIn("payload", results[0], "Sonuçta payload yok")
    
    def test_06_search_with_filter(self):
        """Test: Filtrelenmiş arama"""
        # Koleksiyon oluştur ve vektör ekle
        self.qdrant.create_collection(self.test_collection, vector_size=128)
        points = [
            {
                "id": 1,
                "vector": [0.1] * 128,
                "payload": {"source": "test.pdf", "page": 1}
            },
            {
                "id": 2,
                "vector": [0.1] * 128,
                "payload": {"source": "other.pdf", "page": 1}
            }
        ]
        self.qdrant.upsert_points(self.test_collection, points)
        
        # Filtrelenmiş arama
        query_vector = [0.1] * 128
        results = self.qdrant.search(
            collection_name=self.test_collection,
            query_vector=query_vector,
            limit=5,
            filter_conditions={"source": "test.pdf"}
        )
        
        self.assertEqual(len(results), 1, "Filtre çalışmadı")
        self.assertEqual(results[0]["payload"]["source"], "test.pdf", "Yanlış kaynak döndü")
    
    def test_07_get_point(self):
        """Test: Belirli bir vektörü getirme"""
        # Koleksiyon oluştur ve vektör ekle
        self.qdrant.create_collection(self.test_collection, vector_size=128)
        points = [
            {
                "id": 42,
                "vector": [0.1] * 128,
                "payload": {"text": "Test vektörü"}
            }
        ]
        self.qdrant.upsert_points(self.test_collection, points)
        
        # Vektörü getir
        point = self.qdrant.get_point(self.test_collection, 42)
        
        self.assertIsNotNone(point, "Vektör bulunamadı")
        self.assertEqual(point["id"], 42, "Yanlış ID")
        self.assertIn("vector", point, "Vektör bilgisi yok")
        self.assertIn("payload", point, "Payload bilgisi yok")
    
    def test_08_get_collection_info(self):
        """Test: Koleksiyon bilgilerini alma"""
        # Koleksiyon oluştur
        vector_size = 256
        self.qdrant.create_collection(self.test_collection, vector_size=vector_size)
        
        # Koleksiyon bilgisini al
        info = self.qdrant.get_collection_info(self.test_collection)
        
        self.assertIsNotNone(info, "Koleksiyon bilgisi alınamadı")
        self.assertEqual(info["name"], self.test_collection, "Koleksiyon adı yanlış")
        self.assertEqual(info["vector_size"], vector_size, "Vektör boyutu yanlış")
        self.assertIn("vectors_count", info, "Vektör sayısı bilgisi yok")
    
    def test_09_delete_collection(self):
        """Test: Koleksiyon silme"""
        # Koleksiyon oluştur
        self.qdrant.create_collection(self.test_collection, vector_size=1024)
        self.assertTrue(self.qdrant.collection_exists(self.test_collection))
        
        # Koleksiyonu sil
        result = self.qdrant.delete_collection(self.test_collection)
        self.assertTrue(result, "Koleksiyon silinemedi")
        self.assertFalse(
            self.qdrant.collection_exists(self.test_collection),
            "Koleksiyon hala mevcut"
        )


def run_tests():
    """Testleri çalıştır"""
    print("=" * 70)
    print("🧪 Qdrant Entegrasyon Testleri")
    print("=" * 70)
    print("\n⚠️ Not: Qdrant sunucusunun localhost:6333'te çalışıyor olması gerekir!")
    print("   Başlatmak için: docker run -p 6333:6333 qdrant/qdrant\n")
    
    # Test suite oluştur
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestQdrantIntegration)
    
    # Testleri çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Sonuçları yazdır
    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("✅ Tüm testler başarılı!")
    else:
        print("❌ Bazı testler başarısız!")
        print(f"   Başarısız: {len(result.failures)}")
        print(f"   Hata: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
