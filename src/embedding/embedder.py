"""
Text embedding module using sentence transformers
Görevliler: Mehmet, Hasan
"""

from typing import List, Union
from sentence_transformers import SentenceTransformer
import numpy as np


class TextEmbedder:
    """Cosmos-e5-large modeli ile metin vektörleştirme"""
    
    def __init__(self, model_name: str = 'intfloat/multilingual-e5-large'):
        """
        Args:
            model_name: Kullanılacak embedding modeli
            Not: Cosmos-e5-large yerine herkese açık multilingual-e5-large kullanılıyor
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Modeli yükler"""
        try:
            print(f"Embedding modeli yükleniyor: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print("Model başarıyla yüklendi!")
        except Exception as e:
            raise RuntimeError(f"Model yükleme hatası: {str(e)}")
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Tek bir metni vektöre dönüştürür
        
        Args:
            text: Vektörleştirilecek metin
            
        Returns:
            Embedding vektörü (numpy array)
        """
        if not text or not text.strip():
            raise ValueError("Boş metin vektörleştirilemez")
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def embed_batch(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Birden fazla metni toplu olarak vektörleştirir
        
        Args:
            texts: Vektörleştirilecek metinler listesi
            batch_size: Her seferde işlenecek metin sayısı
            
        Returns:
            Embedding matrisi (numpy array)
        """
        if not texts:
            raise ValueError("Boş liste vektörleştirilemez")
        
        # Boş metinleri filtrele
        valid_texts = [t for t in texts if t and t.strip()]
        
        if not valid_texts:
            raise ValueError("Geçerli metin bulunamadı")
        
        embeddings = self.model.encode(
            valid_texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """
        Embedding vektörünün boyutunu döndürür
        
        Returns:
            Vektör boyutu
        """
        return self.model.get_sentence_embedding_dimension()
