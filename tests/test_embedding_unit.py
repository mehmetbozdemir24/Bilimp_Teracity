"""
Embedding modülü için birim testleri (internet bağlantısı gerektirmez)

Bu testler, embedding modülünün yapısını ve API'sini doğrular.
Gerçek model testleri için internet bağlantısı gereklidir.
"""

import sys
import os

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.embedding.embedding_processor import EmbeddingProcessor


def test_class_exists():
    """Test 1: EmbeddingProcessor sınıfının var olduğunu kontrol et"""
    print("\n" + "="*60)
    print("Test 1: EmbeddingProcessor Sınıfı")
    print("="*60)
    
    assert EmbeddingProcessor is not None
    print("✅ Test 1 Başarılı: EmbeddingProcessor sınıfı tanımlı")


def test_class_has_required_methods():
    """Test 2: Gerekli metodların varlığını kontrol et"""
    print("\n" + "="*60)
    print("Test 2: Gerekli Metodlar")
    print("="*60)
    
    required_methods = [
        'embed_query',
        'embed_documents',
        'process_chunks',
        'save_embeddings',
        'load_embeddings',
        'get_embedding_dimension'
    ]
    
    for method in required_methods:
        assert hasattr(EmbeddingProcessor, method), f"Metod eksik: {method}"
        print(f"  ✓ {method}")
    
    print("✅ Test 2 Başarılı: Tüm gerekli metodlar mevcut")


def test_init_parameters():
    """Test 3: __init__ parametrelerini kontrol et"""
    print("\n" + "="*60)
    print("Test 3: Başlatma Parametreleri")
    print("="*60)
    
    import inspect
    
    # __init__ metodunun parametrelerini al
    sig = inspect.signature(EmbeddingProcessor.__init__)
    params = list(sig.parameters.keys())
    
    print(f"Parametreler: {params}")
    
    assert 'self' in params
    assert 'model_name' in params
    assert 'device' in params
    
    # Varsayılan değerleri kontrol et
    assert sig.parameters['model_name'].default == "ytu-ce-cosmos/turkish-e5-large"
    assert sig.parameters['device'].default is None
    
    print("✅ Test 3 Başarılı: Başlatma parametreleri doğru")


def test_method_signatures():
    """Test 4: Metod imzalarını kontrol et"""
    print("\n" + "="*60)
    print("Test 4: Metod İmzaları")
    print("="*60)
    
    import inspect
    
    # embed_query
    sig = inspect.signature(EmbeddingProcessor.embed_query)
    assert 'text' in sig.parameters
    print("  ✓ embed_query(text) imzası doğru")
    
    # embed_documents
    sig = inspect.signature(EmbeddingProcessor.embed_documents)
    assert 'texts' in sig.parameters
    print("  ✓ embed_documents(texts) imzası doğru")
    
    # process_chunks
    sig = inspect.signature(EmbeddingProcessor.process_chunks)
    assert 'chunks' in sig.parameters
    assert 'batch_size' in sig.parameters
    assert sig.parameters['batch_size'].default == 32
    print("  ✓ process_chunks(chunks, batch_size=32) imzası doğru")
    
    # save_embeddings
    sig = inspect.signature(EmbeddingProcessor.save_embeddings)
    assert 'embeddings_dict' in sig.parameters
    assert 'path' in sig.parameters
    print("  ✓ save_embeddings(embeddings_dict, path) imzası doğru")
    
    # load_embeddings
    sig = inspect.signature(EmbeddingProcessor.load_embeddings)
    assert 'path' in sig.parameters
    print("  ✓ load_embeddings(path) imzası doğru")
    
    print("✅ Test 4 Başarılı: Tüm metod imzaları doğru")


def test_imports():
    """Test 5: Gerekli import'ların yapıldığını kontrol et"""
    print("\n" + "="*60)
    print("Test 5: Import'lar")
    print("="*60)
    
    import src.embedding.embedding_processor as module
    
    # Gerekli import'lar
    assert hasattr(module, 'pickle')
    assert hasattr(module, 'torch')
    assert hasattr(module, 'HuggingFaceEmbeddings')
    assert hasattr(module, 'Document')
    
    print("  ✓ pickle")
    print("  ✓ torch")
    print("  ✓ HuggingFaceEmbeddings")
    print("  ✓ Document")
    
    print("✅ Test 5 Başarılı: Tüm import'lar mevcut")


def test_module_exports():
    """Test 6: Modül export'larını kontrol et"""
    print("\n" + "="*60)
    print("Test 6: Modül Export'ları")
    print("="*60)
    
    import src.embedding as embedding_module
    
    assert hasattr(embedding_module, 'EmbeddingProcessor')
    assert hasattr(embedding_module, '__all__')
    assert 'EmbeddingProcessor' in embedding_module.__all__
    
    print("  ✓ EmbeddingProcessor export edilmiş")
    print("  ✓ __all__ tanımlanmış")
    
    print("✅ Test 6 Başarılı: Modül export'ları doğru")


def test_docstrings():
    """Test 7: Docstring'lerin varlığını kontrol et"""
    print("\n" + "="*60)
    print("Test 7: Dokümantasyon")
    print("="*60)
    
    assert EmbeddingProcessor.__doc__ is not None
    print("  ✓ Sınıf docstring'i var")
    
    assert EmbeddingProcessor.__init__.__doc__ is not None
    print("  ✓ __init__ docstring'i var")
    
    assert EmbeddingProcessor.embed_query.__doc__ is not None
    print("  ✓ embed_query docstring'i var")
    
    assert EmbeddingProcessor.process_chunks.__doc__ is not None
    print("  ✓ process_chunks docstring'i var")
    
    print("✅ Test 7 Başarılı: Dokümantasyon mevcut")


def test_type_hints():
    """Test 8: Type hint'lerin varlığını kontrol et"""
    print("\n" + "="*60)
    print("Test 8: Type Hints")
    print("="*60)
    
    import inspect
    
    # embed_query
    sig = inspect.signature(EmbeddingProcessor.embed_query)
    assert sig.return_annotation != inspect.Parameter.empty
    print("  ✓ embed_query dönüş tipi belirtilmiş")
    
    # embed_documents
    sig = inspect.signature(EmbeddingProcessor.embed_documents)
    assert sig.return_annotation != inspect.Parameter.empty
    print("  ✓ embed_documents dönüş tipi belirtilmiş")
    
    # process_chunks
    sig = inspect.signature(EmbeddingProcessor.process_chunks)
    assert sig.return_annotation != inspect.Parameter.empty
    print("  ✓ process_chunks dönüş tipi belirtilmiş")
    
    print("✅ Test 8 Başarılı: Type hints kullanılmış")


def run_all_tests():
    """Tüm testleri çalıştır"""
    print("\n" + "="*60)
    print("EMBEDDING MODÜLÜ BİRİM TESTLERİ")
    print("="*60)
    print("\nNot: Bu testler kod yapısını doğrular.")
    print("Gerçek model testleri için internet bağlantısı gereklidir.")
    
    tests = [
        test_class_exists,
        test_class_has_required_methods,
        test_init_parameters,
        test_method_signatures,
        test_imports,
        test_module_exports,
        test_docstrings,
        test_type_hints,
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
            import traceback
            traceback.print_exc()
    
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
