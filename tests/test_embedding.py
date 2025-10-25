"""
Embedding modülü için test dosyası

⚠️ DİKKAT: Bu testler HuggingFace'den model indirdiği için internet bağlantısı gerektirir.
           Internet bağlantısı olmadan test etmek için test_embedding_unit.py kullanın.

Bu testler docs/2_embedding_guide.md'deki test örneklerine dayanır.
"""

import sys
import os
import tempfile
import numpy as np
from pathlib import Path

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.embedding import EmbeddingProcessor
from langchain_core.documents import Document


def test_model_initialization():
    """Test 1: Model başlatma testi"""
    print("\n" + "="*60)
    print("Test 1: Model Başlatma")
    print("="*60)
    
    processor = EmbeddingProcessor()
    assert processor is not None
    assert processor.embeddings is not None
    print("✅ Test 1 Başarılı: Model başarıyla başlatıldı")


def test_embedding_dimension():
    """Test 2: Embedding boyutu testi (1024 olmalı)"""
    print("\n" + "="*60)
    print("Test 2: Embedding Boyutu")
    print("="*60)
    
    processor = EmbeddingProcessor()
    embedding = processor.embed_query("test metni")
    
    print(f"Embedding boyutu: {len(embedding)}")
    assert len(embedding) == 1024, f"Beklenen: 1024, Gerçek: {len(embedding)}"
    print("✅ Test 2 Başarılı: Embedding boyutu doğru (1024)")


def test_embedding_normalization():
    """Test 3: Normalize edilmiş vektör testi"""
    print("\n" + "="*60)
    print("Test 3: Normalizasyon")
    print("="*60)
    
    processor = EmbeddingProcessor()
    embedding = processor.embed_query("test metni")
    
    magnitude = np.sqrt(np.sum(np.array(embedding) ** 2))
    print(f"Vektör büyüklüğü (magnitude): {magnitude:.6f}")
    
    assert abs(magnitude - 1.0) < 0.01, f"Beklenen: ~1.0, Gerçek: {magnitude}"
    print("✅ Test 3 Başarılı: Vektör normalize edilmiş")


def test_similarity_same_text():
    """Test 4: Aynı metin için benzerlik testi"""
    print("\n" + "="*60)
    print("Test 4: Aynı Metin Benzerliği")
    print("="*60)
    
    processor = EmbeddingProcessor()
    emb1 = processor.embed_query("Makine öğrenmesi")
    emb2 = processor.embed_query("Makine öğrenmesi")
    
    similarity = np.dot(emb1, emb2)
    print(f"Benzerlik skoru: {similarity:.6f}")
    
    assert similarity > 0.99, f"Beklenen: >0.99, Gerçek: {similarity}"
    print("✅ Test 4 Başarılı: Aynı metin için yüksek benzerlik")


def test_similarity_similar_texts():
    """Test 5: Benzer metinler için benzerlik testi"""
    print("\n" + "="*60)
    print("Test 5: Benzer Metinler Benzerliği")
    print("="*60)
    
    processor = EmbeddingProcessor()
    emb1 = processor.embed_query("Makine öğrenmesi yapay zekadır")
    emb2 = processor.embed_query("Yapay zeka makine öğrenmesidir")
    
    similarity = np.dot(emb1, emb2)
    print(f"Benzerlik skoru: {similarity:.6f}")
    
    assert similarity > 0.7, f"Beklenen: >0.7, Gerçek: {similarity}"
    print("✅ Test 5 Başarılı: Benzer metinler için yüksek benzerlik")


def test_similarity_different_texts():
    """Test 6: Farklı metinler için benzerlik testi"""
    print("\n" + "="*60)
    print("Test 6: Farklı Metinler Benzerliği")
    print("="*60)
    
    processor = EmbeddingProcessor()
    emb1 = processor.embed_query("Makine öğrenmesi yapay zekadır")
    emb2 = processor.embed_query("Bugün hava çok güzel")
    
    similarity = np.dot(emb1, emb2)
    print(f"Benzerlik skoru: {similarity:.6f}")
    
    assert similarity < 0.5, f"Beklenen: <0.5, Gerçek: {similarity}"
    print("✅ Test 6 Başarılı: Farklı metinler için düşük benzerlik")


def test_batch_processing():
    """Test 7: Toplu işlem (batch processing) testi"""
    print("\n" + "="*60)
    print("Test 7: Toplu İşlem")
    print("="*60)
    
    processor = EmbeddingProcessor()
    texts = ["Metin 1", "Metin 2", "Metin 3"]
    
    embeddings_list = processor.embed_documents(texts)
    
    print(f"İşlenen metin sayısı: {len(embeddings_list)}")
    assert len(embeddings_list) == 3, f"Beklenen: 3, Gerçek: {len(embeddings_list)}"
    
    # Her embedding'in boyutunu kontrol et
    for i, emb in enumerate(embeddings_list):
        assert len(emb) == 1024, f"Metin {i+1} embedding boyutu hatalı"
    
    print("✅ Test 7 Başarılı: Toplu işlem çalışıyor")


def test_process_chunks():
    """Test 8: Document chunks işleme testi"""
    print("\n" + "="*60)
    print("Test 8: Document Chunks İşleme")
    print("="*60)
    
    processor = EmbeddingProcessor()
    
    chunks = [
        Document(
            page_content="Python programlama dilidir",
            metadata={"source": "ders1.pdf", "page": 1}
        ),
        Document(
            page_content="Makine öğrenmesi yapay zekadır",
            metadata={"source": "ders2.pdf", "page": 2}
        ),
        Document(
            page_content="LangChain bir framework'tür",
            metadata={"source": "ders3.pdf", "page": 3}
        ),
    ]
    
    embeddings_dict = processor.process_chunks(chunks, batch_size=2)
    
    print(f"İşlenen chunk sayısı: {len(embeddings_dict)}")
    assert len(embeddings_dict) == 3, f"Beklenen: 3, Gerçek: {len(embeddings_dict)}"
    
    # İlk chunk'ı kontrol et
    assert "content" in embeddings_dict[0]
    assert "metadata" in embeddings_dict[0]
    assert "embedding" in embeddings_dict[0]
    assert len(embeddings_dict[0]["embedding"]) == 1024
    
    print("✅ Test 8 Başarılı: Document chunks işleme çalışıyor")


def test_save_and_load_embeddings():
    """Test 9: Embedding kaydetme ve yükleme testi"""
    print("\n" + "="*60)
    print("Test 9: Kaydetme ve Yükleme")
    print("="*60)
    
    processor = EmbeddingProcessor()
    
    chunks = [
        Document(page_content="Test metni 1", metadata={"source": "test1.pdf"}),
        Document(page_content="Test metni 2", metadata={"source": "test2.pdf"}),
    ]
    
    embeddings_dict = processor.process_chunks(chunks)
    
    # Geçici dosyaya kaydet
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as tmp_file:
        tmp_path = tmp_file.name
    
    try:
        processor.save_embeddings(embeddings_dict, tmp_path)
        
        # Yükle
        loaded_dict = processor.load_embeddings(tmp_path)
        
        print(f"Kaydedilen: {len(embeddings_dict)} chunk")
        print(f"Yüklenen: {len(loaded_dict)} chunk")
        
        assert len(loaded_dict) == len(embeddings_dict)
        assert loaded_dict[0]["content"] == embeddings_dict[0]["content"]
        assert len(loaded_dict[0]["embedding"]) == 1024
        
        print("✅ Test 9 Başarılı: Kaydetme ve yükleme çalışıyor")
    finally:
        # Geçici dosyayı temizle
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_turkish_text_support():
    """Test 10: Türkçe metin desteği testi"""
    print("\n" + "="*60)
    print("Test 10: Türkçe Metin Desteği")
    print("="*60)
    
    processor = EmbeddingProcessor()
    
    turkish_texts = [
        "Merhaba dünya",
        "Yapay zeka ve makine öğrenmesi",
        "Türkiye'de teknoloji gelişiyor",
    ]
    
    for text in turkish_texts:
        embedding = processor.embed_query(text)
        print(f"'{text}' -> Embedding boyutu: {len(embedding)}")
        assert len(embedding) == 1024
    
    print("✅ Test 10 Başarılı: Türkçe karakterler destekleniyor")


def run_all_tests():
    """Tüm testleri çalıştır"""
    print("\n" + "="*60)
    print("EMBEDDING MODÜLÜ TEST SENARYOLARI")
    print("="*60)
    
    tests = [
        test_model_initialization,
        test_embedding_dimension,
        test_embedding_normalization,
        test_similarity_same_text,
        test_similarity_similar_texts,
        test_similarity_different_texts,
        test_batch_processing,
        test_process_chunks,
        test_save_and_load_embeddings,
        test_turkish_text_support,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"❌ Test başarısız: {test.__name__}")
            print(f"   Hata: {str(e)}")
    
    print("\n" + "="*60)
    print("TEST SONUÇLARI")
    print("="*60)
    print(f"✅ Başarılı: {passed}/{len(tests)}")
    print(f"❌ Başarısız: {failed}/{len(tests)}")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
