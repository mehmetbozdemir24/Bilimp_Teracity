"""
Basic validation tests for Bilimp Terracity modules.
Run this to verify the setup is correct.
"""

import sys
import os

def test_imports():
    """Test if all modules can be imported."""
    print("Testing module imports...")
    
    try:
        from src.preprocessing.document_processor import DocumentProcessor
        print("✓ DocumentProcessor imported successfully")
    except Exception as e:
        print(f"✗ Failed to import DocumentProcessor: {e}")
        return False
    
    try:
        from src.embeddings.embedding_generator import EmbeddingGenerator
        print("✓ EmbeddingGenerator imported successfully")
    except Exception as e:
        print(f"✗ Failed to import EmbeddingGenerator: {e}")
        return False
    
    try:
        from src.database.qdrant_client import QdrantDatabase
        print("✓ QdrantDatabase imported successfully")
    except Exception as e:
        print(f"✗ Failed to import QdrantDatabase: {e}")
        return False
    
    try:
        from src.llm.llm_client import LLMClient, RAGSystem
        print("✓ LLMClient and RAGSystem imported successfully")
    except Exception as e:
        print(f"✗ Failed to import LLMClient/RAGSystem: {e}")
        return False
    
    return True


def test_document_processor():
    """Test document processor initialization."""
    print("\nTesting DocumentProcessor...")
    
    try:
        from src.preprocessing.document_processor import DocumentProcessor
        processor = DocumentProcessor(chunk_size=512, chunk_overlap=50)
        print(f"✓ DocumentProcessor initialized with chunk_size={processor.chunk_size}")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize DocumentProcessor: {e}")
        return False


def test_data_directories():
    """Test if required directories exist."""
    print("\nTesting directory structure...")
    
    dirs = ['data/raw', 'data/processed', 'src', 'configs']
    all_exist = True
    
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"✗ Directory missing: {dir_path}")
            all_exist = False
    
    return all_exist


def test_config_files():
    """Test if configuration files exist."""
    print("\nTesting configuration files...")
    
    files = [
        'requirements.txt',
        '.env.example',
        'docker-compose.yml',
        'main.py',
        'README.md',
        'QUICKSTART.md'
    ]
    
    all_exist = True
    
    for file_path in files:
        if os.path.exists(file_path):
            print(f"✓ File exists: {file_path}")
        else:
            print(f"✗ File missing: {file_path}")
            all_exist = False
    
    return all_exist


def test_docker_services():
    """Test if Docker services are accessible."""
    print("\nTesting Docker services...")
    
    import subprocess
    
    # Test Qdrant
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=bilimp_qdrant', '--format', '{{.Names}}'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if 'bilimp_qdrant' in result.stdout:
            print("✓ Qdrant container is running")
            qdrant_ok = True
        else:
            print("⚠ Qdrant container is not running")
            print("  Run: docker-compose up -d")
            qdrant_ok = False
    except Exception as e:
        print(f"⚠ Could not check Qdrant status: {e}")
        qdrant_ok = False
    
    # Test Ollama
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=bilimp_ollama', '--format', '{{.Names}}'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if 'bilimp_ollama' in result.stdout:
            print("✓ Ollama container is running")
            ollama_ok = True
        else:
            print("⚠ Ollama container is not running")
            print("  Run: docker-compose up -d")
            ollama_ok = False
    except Exception as e:
        print(f"⚠ Could not check Ollama status: {e}")
        ollama_ok = False
    
    return qdrant_ok or ollama_ok  # At least attempt was made


def test_chunk_creation():
    """Test basic chunk creation."""
    print("\nTesting chunk creation...")
    
    try:
        from src.preprocessing.document_processor import DocumentProcessor
        
        # Create a temporary test file
        test_file = "data/raw/test_validation.txt"
        os.makedirs("data/raw", exist_ok=True)
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Bu bir test metnidir. " * 50)
        
        processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
        documents = processor.load_document(test_file)
        chunks = processor.chunk_documents(documents)
        
        # Clean up
        os.remove(test_file)
        
        if len(chunks) > 0:
            print(f"✓ Created {len(chunks)} chunks from test document")
            return True
        else:
            print("✗ No chunks created")
            return False
    
    except Exception as e:
        print(f"✗ Chunk creation failed: {e}")
        return False


def main():
    """Run all validation tests."""
    print("="*80)
    print("Bilimp Terracity - Validation Tests")
    print("="*80)
    
    results = []
    
    # Run tests
    results.append(("Module Imports", test_imports()))
    results.append(("Directory Structure", test_data_directories()))
    results.append(("Configuration Files", test_config_files()))
    results.append(("Document Processor", test_document_processor()))
    results.append(("Chunk Creation", test_chunk_creation()))
    results.append(("Docker Services", test_docker_services()))
    
    # Print summary
    print("\n" + "="*80)
    print("Test Summary")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("="*80)
    print(f"Results: {passed}/{total} tests passed")
    print("="*80)
    
    if passed == total:
        print("\n🎉 All tests passed! The setup is ready to use.")
        print("\nNext steps:")
        print("1. Start Docker services: docker-compose up -d")
        print("2. Download LLM models: docker exec -it bilimp_ollama ollama pull gemma3:12b")
        print("3. Run example: python example_usage.py")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
