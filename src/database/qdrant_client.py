"""
Qdrant database integration module.
Handles connection, collection creation, and data upload to Qdrant vector database.

Authors: Süleyman, Eren
"""

import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
import uuid

logger = logging.getLogger(__name__)


class QdrantDatabase:
    """Manages Qdrant vector database operations."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "bilimp_documents",
        embedding_dim: int = 1024
    ):
        """
        Initialize Qdrant database connection.
        
        Args:
            host: Qdrant server host
            port: Qdrant server port
            collection_name: Name of the collection to use
            embedding_dim: Dimension of embedding vectors
        """
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        
        # Initialize client
        logger.info(f"Connecting to Qdrant at {host}:{port}")
        self.client = QdrantClient(host=host, port=port)
        
        # Create collection if it doesn't exist
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Create collection if it doesn't exist."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                logger.info(f"Creating collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_dim,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Collection {self.collection_name} created successfully")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise
    
    def upload_chunks(self, chunks: List[Dict[str, Any]], batch_size: int = 100) -> int:
        """
        Upload document chunks with embeddings to Qdrant.
        
        Args:
            chunks: List of chunks with embeddings and metadata
            batch_size: Number of chunks to upload in each batch
            
        Returns:
            Number of successfully uploaded chunks
        """
        if not chunks:
            logger.warning("No chunks to upload")
            return 0
        
        logger.info(f"Uploading {len(chunks)} chunks to Qdrant")
        
        uploaded_count = 0
        
        try:
            # Process in batches
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                points = []
                
                for chunk in batch:
                    # Generate unique ID if not present
                    point_id = chunk.get('id', str(uuid.uuid4()))
                    
                    # Prepare point
                    point = PointStruct(
                        id=point_id,
                        vector=chunk['embedding'],
                        payload={
                            'text': chunk['text'],
                            'metadata': chunk.get('metadata', {})
                        }
                    )
                    points.append(point)
                
                # Upload batch
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                
                uploaded_count += len(points)
                logger.info(f"Uploaded batch: {uploaded_count}/{len(chunks)}")
            
            logger.info(f"Successfully uploaded {uploaded_count} chunks")
            return uploaded_count
        
        except Exception as e:
            logger.error(f"Error uploading chunks: {e}")
            raise
    
    def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents using embedding vector.
        
        Args:
            query_embedding: Query embedding vector
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score threshold
            filters: Optional metadata filters
            
        Returns:
            List of search results with scores and metadata
        """
        try:
            # Prepare filter if provided
            query_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        FieldCondition(
                            key=f"metadata.{key}",
                            match=MatchValue(value=value)
                        )
                    )
                if conditions:
                    query_filter = Filter(must=conditions)
            
            # Perform search
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=query_filter
            )
            
            # Format results
            results = []
            for scored_point in search_result:
                result = {
                    'id': scored_point.id,
                    'score': scored_point.score,
                    'text': scored_point.payload.get('text', ''),
                    'metadata': scored_point.payload.get('metadata', {})
                }
                results.append(result)
            
            logger.info(f"Found {len(results)} results")
            return results
        
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.
        
        Returns:
            Collection information including count and configuration
        """
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return {
                'name': self.collection_name,
                'points_count': info.points_count,
                'vectors_count': info.vectors_count,
                'status': info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            raise
    
    def delete_collection(self):
        """Delete the collection."""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            logger.info(f"Collection {self.collection_name} deleted")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise


def main():
    """Example usage of Qdrant database."""
    logging.basicConfig(level=logging.INFO)
    
    # Initialize database
    db = QdrantDatabase()
    
    # Get collection info
    info = db.get_collection_info()
    print(f"Collection info: {info}")


if __name__ == "__main__":
    main()
