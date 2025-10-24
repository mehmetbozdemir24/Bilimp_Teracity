"""
Main pipeline for Bilimp Terracity Assistant.
Orchestrates document processing, embedding generation, and RAG system.
"""

import os
import logging
import argparse
from pathlib import Path
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


class BilimpPipeline:
    """Main pipeline for document processing and RAG system."""
    
    def __init__(self):
        """Initialize all components of the pipeline."""
        logger.info("Initializing Bilimp Pipeline")
        
        # Get configuration from environment
        self.chunk_size = int(os.getenv('CHUNK_SIZE', 512))
        self.chunk_overlap = int(os.getenv('CHUNK_OVERLAP', 50))
        self.embedding_model = os.getenv('EMBEDDING_MODEL', 'intfloat/multilingual-e5-large')
        self.embedding_dim = int(os.getenv('EMBEDDING_DIMENSION', 1024))
        self.batch_size = int(os.getenv('BATCH_SIZE', 32))
        
        # Qdrant configuration
        self.qdrant_host = os.getenv('QDRANT_HOST', 'localhost')
        self.qdrant_port = int(os.getenv('QDRANT_PORT', 6333))
        self.collection_name = os.getenv('QDRANT_COLLECTION_NAME', 'bilimp_documents')
        
        # LLM configuration
        self.ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.gemma_model = os.getenv('GEMMA_MODEL', 'gemma3:12b')
        self.qwen_model = os.getenv('QWEN_MODEL', 'qwen3:9b')
        
        # Initialize components
        self.document_processor = None
        self.embedding_generator = None
        self.database = None
        self.llm_client = None
        self.rag_system = None
    
    def initialize_components(self):
        """Initialize all pipeline components."""
        logger.info("Initializing pipeline components")
        
        # Initialize document processor
        self.document_processor = DocumentProcessor(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        
        # Initialize embedding generator
        self.embedding_generator = EmbeddingGenerator(
            model_name=self.embedding_model,
            batch_size=self.batch_size
        )
        
        # Initialize Qdrant database
        self.database = QdrantDatabase(
            host=self.qdrant_host,
            port=self.qdrant_port,
            collection_name=self.collection_name,
            embedding_dim=self.embedding_dim
        )
        
        # Initialize LLM client
        self.llm_client = LLMClient(
            base_url=self.ollama_url,
            gemma_model=self.gemma_model,
            qwen_model=self.qwen_model
        )
        
        # Initialize RAG system
        self.rag_system = RAGSystem(
            database=self.database,
            embedding_generator=self.embedding_generator,
            llm_client=self.llm_client,
            top_k=5
        )
        
        logger.info("All components initialized successfully")
    
    def process_documents(self, input_dir: str):
        """
        Process documents from input directory.
        
        Args:
            input_dir: Path to directory containing documents
        """
        logger.info(f"Processing documents from: {input_dir}")
        
        if not self.document_processor:
            raise RuntimeError("Document processor not initialized")
        
        # Process all documents
        chunks = self.document_processor.process_directory(input_dir)
        
        logger.info(f"Processed {len(chunks)} chunks")
        return chunks
    
    def generate_embeddings(self, chunks):
        """
        Generate embeddings for document chunks.
        
        Args:
            chunks: List of document chunks
        """
        logger.info("Generating embeddings")
        
        if not self.embedding_generator:
            raise RuntimeError("Embedding generator not initialized")
        
        # Generate embeddings
        processed_chunks = self.embedding_generator.process_chunks(chunks)
        
        logger.info(f"Generated embeddings for {len(processed_chunks)} chunks")
        return processed_chunks
    
    def upload_to_database(self, chunks):
        """
        Upload chunks with embeddings to Qdrant.
        
        Args:
            chunks: List of chunks with embeddings
        """
        logger.info("Uploading to Qdrant database")
        
        if not self.database:
            raise RuntimeError("Database not initialized")
        
        # Upload chunks
        count = self.database.upload_chunks(chunks)
        
        logger.info(f"Uploaded {count} chunks to database")
        return count
    
    def run_full_pipeline(self, input_dir: str):
        """
        Run the complete pipeline: process, embed, and upload.
        
        Args:
            input_dir: Path to directory containing documents
        """
        logger.info("Starting full pipeline")
        
        # Initialize components
        self.initialize_components()
        
        # Process documents
        chunks = self.process_documents(input_dir)
        
        if not chunks:
            logger.warning("No chunks to process")
            return
        
        # Generate embeddings
        processed_chunks = self.generate_embeddings(chunks)
        
        # Upload to database
        self.upload_to_database(processed_chunks)
        
        logger.info("Pipeline completed successfully")
    
    def query_system(self, query: str, model: str = None):
        """
        Query the RAG system.
        
        Args:
            query: User query
            model: Model to use (gemma or qwen)
        """
        if not self.rag_system:
            self.initialize_components()
        
        result = self.rag_system.query(query, model=model)
        return result


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Bilimp Terracity Assistant Pipeline')
    parser.add_argument(
        '--mode',
        choices=['process', 'query', 'info'],
        required=True,
        help='Operation mode: process documents, query system, or show info'
    )
    parser.add_argument(
        '--input-dir',
        type=str,
        default='data/raw',
        help='Input directory for documents (for process mode)'
    )
    parser.add_argument(
        '--query',
        type=str,
        help='Query text (for query mode)'
    )
    parser.add_argument(
        '--model',
        choices=['gemma', 'qwen'],
        help='LLM model to use (for query mode)'
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = BilimpPipeline()
    
    if args.mode == 'process':
        # Run document processing pipeline
        pipeline.run_full_pipeline(args.input_dir)
    
    elif args.mode == 'query':
        if not args.query:
            print("Error: --query is required for query mode")
            return
        
        # Map model names
        model_map = {
            'gemma': pipeline.gemma_model,
            'qwen': pipeline.qwen_model
        }
        model = model_map.get(args.model) if args.model else None
        
        # Query the system
        result = pipeline.query_system(args.query, model=model)
        
        print("\n" + "="*80)
        print(f"Query: {result['query']}")
        print("="*80)
        print(f"\nRetrieved {len(result['retrieved_documents'])} documents")
        print(f"Model: {result['model']}")
        print("\nResponse:")
        print("-"*80)
        print(result['response'])
        print("="*80)
    
    elif args.mode == 'info':
        # Show system information
        pipeline.initialize_components()
        info = pipeline.database.get_collection_info()
        
        print("\n" + "="*80)
        print("Bilimp System Information")
        print("="*80)
        print(f"Collection: {info['name']}")
        print(f"Documents: {info['points_count']}")
        print(f"Status: {info['status']}")
        print(f"Embedding Model: {pipeline.embedding_model}")
        print(f"Embedding Dimension: {pipeline.embedding_dim}")
        print(f"LLM Models: {pipeline.gemma_model}, {pipeline.qwen_model}")
        print("="*80)


if __name__ == "__main__":
    main()
