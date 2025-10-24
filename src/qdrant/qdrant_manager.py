"""
Qdrant vector database management module
Görevliler: Süleyman, Eren
"""

from typing import List, Dict, Any, Optional
import numpy as np


class QdrantManager:
    """Qdrant vektör veritabanı yönetimi"""
    
    def __init__(self, host: str = "localhost", port: int = 6333):
        """
        Args:
            host: Qdrant sunucu adresi
            port: Qdrant sunucu portu
        """
        self.host = host
        self.port = port
        self.client = None
        
    def connect(self):
        """Qdrant veritabanına bağlanır"""
        try:
            # Qdrant kütüphanesi gerektiğinde import edilecek
            from qdrant_client import QdrantClient
            self.client = QdrantClient(host=self.host, port=self.port)
            print(f"Qdrant'a bağlanıldı: {self.host}:{self.port}")
        except ImportError:
            print("Uyarı: qdrant-client kurulu değil. 'pip install qdrant-client' ile yükleyin.")
            self.client = None
        except Exception as e:
            raise ConnectionError(f"Qdrant bağlantı hatası: {str(e)}")
    
    def create_collection(
        self,
        collection_name: str,
        vector_size: int,
        distance: str = "Cosine"
    ):
        """
        Yeni koleksiyon oluşturur
        
        Args:
            collection_name: Koleksiyon adı
            vector_size: Vektör boyutu
            distance: Mesafe metriği (Cosine, Euclid, Dot)
        """
        if not self.client:
            raise RuntimeError("Qdrant bağlantısı yok. Önce connect() çağırın.")
        
        from qdrant_client.models import Distance, VectorParams
        
        distance_map = {
            "Cosine": Distance.COSINE,
            "Euclid": Distance.EUCLID,
            "Dot": Distance.DOT
        }
        
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=distance_map.get(distance, Distance.COSINE)
            )
        )
        print(f"Koleksiyon oluşturuldu: {collection_name}")
    
    def upload_vectors(
        self,
        collection_name: str,
        vectors: np.ndarray,
        payloads: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[int]] = None
    ):
        """
        Vektörleri Qdrant'a yükler
        
        Args:
            collection_name: Koleksiyon adı
            vectors: Vektörler (numpy array)
            payloads: Her vektör için metadata
            ids: Vektör ID'leri
        """
        if not self.client:
            raise RuntimeError("Qdrant bağlantısı yok. Önce connect() çağırın.")
        
        from qdrant_client.models import PointStruct
        
        num_vectors = len(vectors)
        
        if ids is None:
            ids = list(range(num_vectors))
        
        if payloads is None:
            payloads = [{}] * num_vectors
        
        points = [
            PointStruct(
                id=ids[i],
                vector=vectors[i].tolist(),
                payload=payloads[i]
            )
            for i in range(num_vectors)
        ]
        
        self.client.upsert(
            collection_name=collection_name,
            points=points
        )
        print(f"{num_vectors} vektör yüklendi: {collection_name}")
    
    def search(
        self,
        collection_name: str,
        query_vector: np.ndarray,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Benzer vektörleri arar
        
        Args:
            collection_name: Koleksiyon adı
            query_vector: Sorgu vektörü
            limit: Döndürülecek sonuç sayısı
            
        Returns:
            Arama sonuçları
        """
        if not self.client:
            raise RuntimeError("Qdrant bağlantısı yok. Önce connect() çağırın.")
        
        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector.tolist(),
            limit=limit
        )
        
        return [
            {
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload
            }
            for hit in results
        ]
    
    def collection_exists(self, collection_name: str) -> bool:
        """
        Koleksiyonun var olup olmadığını kontrol eder
        
        Args:
            collection_name: Koleksiyon adı
            
        Returns:
            Koleksiyon varsa True
        """
        if not self.client:
            return False
        
        try:
            collections = self.client.get_collections().collections
            return any(c.name == collection_name for c in collections)
        except:
            return False
