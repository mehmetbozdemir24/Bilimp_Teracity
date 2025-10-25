"""
Qdrant Veritabanı Entegrasyon Modülü

Bu modül, Qdrant vektör veritabanı ile etkileşimi sağlar.
Koleksiyon yönetimi, vektör yazma/okuma ve arama fonksiyonlarını içerir.

Görevliler: Süleyman, Eren
"""

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue


class QdrantManager:
    """Qdrant veritabanı yönetimi için ana sınıf"""
    
    def __init__(self, host: str = "localhost", port: int = 6333, api_key: Optional[str] = None):
        """
        Qdrant client'ını başlatır
        
        Args:
            host: Qdrant sunucusunun adresi (varsayılan: localhost)
            port: Qdrant sunucusunun portu (varsayılan: 6333)
            api_key: Qdrant API anahtarı (opsiyonel)
        """
        self.host = host
        self.port = port
        self.client = QdrantClient(host=host, port=port, api_key=api_key)
        
    def create_collection(
        self, 
        collection_name: str, 
        vector_size: int = 1024, 
        distance: Distance = Distance.COSINE
    ) -> bool:
        """
        Yeni bir koleksiyon oluşturur
        
        Args:
            collection_name: Koleksiyon adı
            vector_size: Vektör boyutu (varsayılan: 1024 - Cosmos-E5-Large için)
            distance: Mesafe metriği (varsayılan: Cosine)
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance)
            )
            print(f"✅ Koleksiyon '{collection_name}' başarıyla oluşturuldu!")
            return True
        except Exception as e:
            print(f"❌ Koleksiyon oluşturma hatası: {e}")
            return False
    
    def collection_exists(self, collection_name: str) -> bool:
        """
        Koleksiyonun var olup olmadığını kontrol eder
        
        Args:
            collection_name: Kontrol edilecek koleksiyon adı
            
        Returns:
            bool: Koleksiyon varsa True
        """
        try:
            collections = self.client.get_collections()
            return any(col.name == collection_name for col in collections.collections)
        except Exception as e:
            print(f"❌ Koleksiyon kontrol hatası: {e}")
            return False
    
    def delete_collection(self, collection_name: str) -> bool:
        """
        Koleksiyonu siler
        
        Args:
            collection_name: Silinecek koleksiyon adı
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            self.client.delete_collection(collection_name=collection_name)
            print(f"✅ Koleksiyon '{collection_name}' başarıyla silindi!")
            return True
        except Exception as e:
            print(f"❌ Koleksiyon silme hatası: {e}")
            return False
    
    def list_collections(self) -> List[str]:
        """
        Tüm koleksiyonları listeler
        
        Returns:
            List[str]: Koleksiyon isimleri listesi
        """
        try:
            collections = self.client.get_collections()
            return [col.name for col in collections.collections]
        except Exception as e:
            print(f"❌ Koleksiyon listeleme hatası: {e}")
            return []
    
    def upsert_points(
        self, 
        collection_name: str, 
        points: List[Dict[str, Any]]
    ) -> bool:
        """
        Vektörleri koleksiyona ekler veya günceller
        
        Args:
            collection_name: Hedef koleksiyon adı
            points: Eklenecek vektörler listesi. Her öğe şu yapıda olmalı:
                {
                    "id": int veya str,
                    "vector": List[float],
                    "payload": Dict[str, Any] (opsiyonel)
                }
                
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            # PointStruct nesnelerine dönüştür
            point_structs = []
            for point in points:
                point_structs.append(
                    PointStruct(
                        id=point["id"],
                        vector=point["vector"],
                        payload=point.get("payload", {})
                    )
                )
            
            self.client.upsert(
                collection_name=collection_name,
                points=point_structs
            )
            print(f"✅ {len(points)} vektör başarıyla eklendi/güncellendi!")
            return True
        except Exception as e:
            print(f"❌ Vektör ekleme hatası: {e}")
            return False
    
    def search(
        self, 
        collection_name: str, 
        query_vector: List[float], 
        limit: int = 5,
        filter_conditions: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Vektör benzerlik araması yapar
        
        Args:
            collection_name: Arama yapılacak koleksiyon adı
            query_vector: Sorgu vektörü
            limit: Döndürülecek maksimum sonuç sayısı
            filter_conditions: Filtreleme koşulları (opsiyonel)
                Örnek: {"source": "test.pdf"}
                
        Returns:
            List[Dict]: Arama sonuçları. Her sonuç şu yapıda:
                {
                    "id": int/str,
                    "score": float,
                    "payload": Dict[str, Any]
                }
        """
        try:
            # Filtre oluştur (varsa)
            search_filter = None
            if filter_conditions:
                must_conditions = []
                for key, value in filter_conditions.items():
                    must_conditions.append(
                        FieldCondition(key=key, match=MatchValue(value=value))
                    )
                search_filter = Filter(must=must_conditions)
            
            # Arama yap
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                query_filter=search_filter
            )
            
            # Sonuçları formatla
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                })
            
            print(f"✅ {len(formatted_results)} sonuç bulundu!")
            return formatted_results
        except Exception as e:
            print(f"❌ Arama hatası: {e}")
            return []
    
    def get_point(self, collection_name: str, point_id: int) -> Optional[Dict[str, Any]]:
        """
        Belirli bir ID'ye sahip vektörü getirir
        
        Args:
            collection_name: Koleksiyon adı
            point_id: Vektör ID'si
            
        Returns:
            Dict veya None: Vektör bilgileri
        """
        try:
            result = self.client.retrieve(
                collection_name=collection_name,
                ids=[point_id]
            )
            if result:
                return {
                    "id": result[0].id,
                    "vector": result[0].vector,
                    "payload": result[0].payload
                }
            return None
        except Exception as e:
            print(f"❌ Vektör getirme hatası: {e}")
            return None
    
    def get_collection_info(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """
        Koleksiyon hakkında bilgi döndürür
        
        Args:
            collection_name: Koleksiyon adı
            
        Returns:
            Dict veya None: Koleksiyon bilgileri
        """
        try:
            info = self.client.get_collection(collection_name=collection_name)
            return {
                "name": collection_name,
                "vectors_count": info.points_count,
                "vector_size": info.config.params.vectors.size,
                "distance": info.config.params.vectors.distance
            }
        except Exception as e:
            print(f"❌ Koleksiyon bilgisi alma hatası: {e}")
            return None
    
    def close(self):
        """Client bağlantısını kapatır"""
        try:
            self.client.close()
            print("✅ Qdrant bağlantısı kapatıldı!")
        except Exception as e:
            print(f"❌ Bağlantı kapatma hatası: {e}")
