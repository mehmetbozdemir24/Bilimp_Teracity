"""
Embedding generation module using multilingual-e5-large model.
Converts text chunks into embedding vectors.

Authors: Mehmet, Hasan
"""

import logging
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from tqdm import tqdm

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generates embeddings using the multilingual-e5-large model."""
    
    def __init__(self, model_name: str = "intfloat/multilingual-e5-large", batch_size: int = 32):
        """
        Initialize the embedding generator.
        
        Args:
            model_name: Name of the sentence transformer model
            batch_size: Batch size for processing
        """
        self.model_name = model_name
        self.batch_size = batch_size
        
        # Check if CUDA is available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Load the model
        logger.info(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name, device=self.device)
        
        # Get embedding dimension
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(f"Model loaded. Embedding dimension: {self.embedding_dim}")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as numpy array
        """
        # Add instruction prefix for e5 models (improves performance)
        prefixed_text = f"passage: {text}"
        
        try:
            embedding = self.model.encode(prefixed_text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str], show_progress: bool = True) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts in batches.
        
        Args:
            texts: List of input texts
            show_progress: Whether to show progress bar
            
        Returns:
            List of embedding vectors
        """
        # Add instruction prefix for e5 models
        prefixed_texts = [f"passage: {text}" for text in texts]
        
        try:
            embeddings = self.model.encode(
                prefixed_texts,
                batch_size=self.batch_size,
                show_progress_bar=show_progress,
                convert_to_numpy=True
            )
            
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
        
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise
    
    def process_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process document chunks and add embeddings.
        
        Args:
            chunks: List of document chunks with text and metadata
            
        Returns:
            List of chunks with embeddings added
        """
        if not chunks:
            logger.warning("No chunks to process")
            return []
        
        logger.info(f"Processing {len(chunks)} chunks")
        
        # Extract texts from chunks
        texts = [chunk['text'] for chunk in chunks]
        
        # Generate embeddings
        embeddings = self.generate_embeddings_batch(texts)
        
        # Add embeddings to chunks
        processed_chunks = []
        for chunk, embedding in zip(chunks, embeddings):
            processed_chunk = {
                **chunk,
                'embedding': embedding.tolist()  # Convert to list for JSON serialization
            }
            processed_chunks.append(processed_chunk)
        
        logger.info(f"Successfully processed {len(processed_chunks)} chunks with embeddings")
        return processed_chunks
    
    def generate_query_embedding(self, query: str) -> np.ndarray:
        """
        Generate embedding for a search query.
        Uses 'query:' prefix instead of 'passage:' for better retrieval.
        
        Args:
            query: Search query text
            
        Returns:
            Query embedding vector
        """
        # Use query prefix for e5 models
        prefixed_query = f"query: {query}"
        
        try:
            embedding = self.model.encode(prefixed_query, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            raise


def main():
    """Example usage of the embedding generator."""
    logging.basicConfig(level=logging.INFO)
    
    # Initialize generator
    generator = EmbeddingGenerator()
    
    # Example texts
    example_chunks = [
        {
            'id': 'chunk_0',
            'text': 'Bu bir örnek metindir.',
            'metadata': {'source': 'example'}
        },
        {
            'id': 'chunk_1',
            'text': 'Bilimp sistemi için doküman işleme.',
            'metadata': {'source': 'example'}
        }
    ]
    
    # Process chunks
    processed = generator.process_chunks(example_chunks)
    
    print(f"Processed {len(processed)} chunks")
    print(f"Embedding dimension: {len(processed[0]['embedding'])}")


if __name__ == "__main__":
    main()
