"""
Example usage script for Bilimp Terracity Assistant.
Demonstrates all main functionalities.
"""

import os
import logging
from dotenv import load_dotenv

from src.preprocessing.document_processor import DocumentProcessor
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.database.qdrant_client import QdrantDatabase
from src.llm.llm_client import LLMClient, RAGSystem

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_document_processing():
    """Example: Process documents and create chunks."""
    print("\n" + "="*80)
    print("Example 1: Document Processing")
    print("="*80)
    
    # Initialize document processor
    processor = DocumentProcessor(chunk_size=512, chunk_overlap=50)
    
    # Create sample document
    sample_file = "data/raw/sample.txt"
    os.makedirs("data/raw", exist_ok=True)
    
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write("""
Bilimp Sistemi Hakkında

Bilimp, Terracity firması tarafından geliştirilen modern bir doküman yönetim sistemidir.
Bu sistem, şirketlerin dokümanlarını dijital ortamda güvenli bir şekilde saklamasına,
organize etmesine ve yönetmesine olanak tanır.

Temel Özellikler:
- Güvenli doküman depolama
- Gelişmiş arama özellikleri
- Kullanıcı yetkilendirme sistemi
- Versiyon kontrolü
- İş akışı yönetimi

Bilimp sistemi bulut tabanlı çalışır ve her yerden erişim imkanı sunar.
Kullanıcı dostu arayüzü sayesinde kolayca öğrenilebilir ve kullanılabilir.
        """)
    
    # Process the document
    documents = processor.load_document(sample_file)
    chunks = processor.chunk_documents(documents)
    
    print(f"\nProcessed {len(chunks)} chunks from document")
    print(f"First chunk preview: {chunks[0]['text'][:100]}...")
    
    return chunks


def example_embedding_generation(chunks):
    """Example: Generate embeddings for chunks."""
    print("\n" + "="*80)
    print("Example 2: Embedding Generation")
    print("="*80)
    
    # Initialize embedding generator
    generator = EmbeddingGenerator(
        model_name="intfloat/multilingual-e5-large",
        batch_size=8
    )
    
    # Generate embeddings
    processed_chunks = generator.process_chunks(chunks)
    
    print(f"\nGenerated embeddings for {len(processed_chunks)} chunks")
    print(f"Embedding dimension: {len(processed_chunks[0]['embedding'])}")
    
    return processed_chunks


def example_database_upload(chunks_with_embeddings):
    """Example: Upload chunks to Qdrant database."""
    print("\n" + "="*80)
    print("Example 3: Database Upload")
    print("="*80)
    
    # Initialize Qdrant database
    db = QdrantDatabase(
        host=os.getenv('QDRANT_HOST', 'localhost'),
        port=int(os.getenv('QDRANT_PORT', 6333)),
        collection_name='bilimp_example',
        embedding_dim=1024
    )
    
    # Upload chunks
    count = db.upload_chunks(chunks_with_embeddings)
    
    print(f"\nUploaded {count} chunks to Qdrant")
    
    # Get collection info
    info = db.get_collection_info()
    print(f"Collection: {info['name']}")
    print(f"Total documents: {info['points_count']}")
    
    return db


def example_search_and_query(db, embedding_generator):
    """Example: Search and generate response."""
    print("\n" + "="*80)
    print("Example 4: Search and Query")
    print("="*80)
    
    # Initialize LLM client
    llm_client = LLMClient(
        base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
        gemma_model=os.getenv('GEMMA_MODEL', 'gemma3:12b'),
        qwen_model=os.getenv('QWEN_MODEL', 'qwen3:9b')
    )
    
    # Initialize RAG system
    rag_system = RAGSystem(
        database=db,
        embedding_generator=embedding_generator,
        llm_client=llm_client,
        top_k=3
    )
    
    # Query the system
    queries = [
        "Bilimp sistemi nedir?",
        "Bilimp'in temel özellikleri nelerdir?",
        "Bilimp nasıl çalışır?"
    ]
    
    for query in queries:
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print("-"*80)
        
        try:
            result = rag_system.query(query, model=llm_client.gemma_model)
            
            print(f"\nRetrieved {len(result['retrieved_documents'])} documents")
            print(f"Model: {result['model']}")
            print(f"\nResponse:\n{result['response']}")
            
        except Exception as e:
            print(f"Error: {e}")
            print("Note: Make sure Ollama is running and models are installed")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("Bilimp Terracity Assistant - Example Usage")
    print("="*80)
    
    try:
        # Example 1: Process documents
        chunks = example_document_processing()
        
        # Example 2: Generate embeddings
        chunks_with_embeddings = example_embedding_generation(chunks)
        
        # Example 3: Upload to database
        db = example_database_upload(chunks_with_embeddings)
        
        # Example 4: Search and query
        generator = EmbeddingGenerator(
            model_name="intfloat/multilingual-e5-large",
            batch_size=8
        )
        example_search_and_query(db, generator)
        
        print("\n" + "="*80)
        print("All examples completed successfully!")
        print("="*80)
        
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        print("\n" + "="*80)
        print("Error running examples. Please check:")
        print("1. Docker services are running (docker-compose up -d)")
        print("2. Ollama models are installed")
        print("3. All dependencies are installed (pip install -r requirements.txt)")
        print("="*80)


if __name__ == "__main__":
    main()
