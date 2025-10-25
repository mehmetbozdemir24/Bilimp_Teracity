"""
EmbeddingProcessor - Cosmos-E5-Large modeli ile embedding işlemleri

Bu modül, LangChain HuggingFaceEmbeddings kullanarak metin parçalarını
1024-boyutlu vektörlere dönüştürür.
"""

import pickle
from typing import List, Dict, Any, Optional
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


class EmbeddingProcessor:
    """
    Türkçe metinler için embedding işlemleri gerçekleştirir.
    
    Model: ytu-ce-cosmos/turkish-e5-large
    Vektör Boyutu: 1024
    Normalizasyon: Aktif
    """
    
    def __init__(
        self,
        model_name: str = "ytu-ce-cosmos/turkish-e5-large",
        device: Optional[str] = None
    ):
        """
        EmbeddingProcessor başlatıcı.
        
        Args:
            model_name: HuggingFace model ismi
            device: "cuda", "cpu" veya None (otomatik seçim)
        """
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.model_name = model_name
        self.device = device
        
        # Model yükleme
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": True}
        )
        print(f"✅ Model yüklendi: {model_name} (Device: {device})")
    
    def embed_query(self, text: str) -> List[float]:
        """
        Tek bir metni vektöre dönüştürür.
        
        Args:
            text: Vektörleştirilecek metin
            
        Returns:
            1024-boyutlu normalize edilmiş vektör
        """
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Birden fazla metni toplu olarak vektörleştirir.
        
        Args:
            texts: Vektörleştirilecek metinler listesi
            
        Returns:
            Her metin için 1024-boyutlu vektör listesi
        """
        return self.embeddings.embed_documents(texts)
    
    def process_chunks(
        self,
        chunks: List[Document],
        batch_size: int = 32
    ) -> Dict[int, Dict[str, Any]]:
        """
        Document chunk'larını batch işleme ile vektörleştirir.
        
        Args:
            chunks: LangChain Document listesi
            batch_size: Her batch'te işlenecek chunk sayısı
            
        Returns:
            Chunk index'lerine göre embedding sözlüğü:
            {
                0: {
                    "content": "metin içeriği",
                    "metadata": {"source": "dosya.pdf", ...},
                    "embedding": [0.1, 0.2, ...]
                },
                ...
            }
        """
        embeddings_dict = {}
        total_chunks = len(chunks)
        
        for i in range(0, total_chunks, batch_size):
            batch = chunks[i:i+batch_size]
            texts = [doc.page_content for doc in batch]
            
            # Batch embedding
            batch_embeddings = self.embeddings.embed_documents(texts)
            
            # Sonuçları kaydet
            for j, embedding in enumerate(batch_embeddings):
                idx = i + j
                embeddings_dict[idx] = {
                    "content": batch[j].page_content,
                    "metadata": batch[j].metadata,
                    "embedding": embedding
                }
            
            print(f"✅ İşlenen: {min(i+batch_size, total_chunks)}/{total_chunks} chunk")
        
        return embeddings_dict
    
    def save_embeddings(self, embeddings_dict: Dict[int, Dict[str, Any]], path: str):
        """
        Embedding'leri pickle formatında kaydeder.
        
        Args:
            embeddings_dict: process_chunks() çıktısı
            path: Kaydedilecek dosya yolu
        """
        with open(path, "wb") as f:
            pickle.dump(embeddings_dict, f)
        print(f"✅ {len(embeddings_dict)} embedding '{path}' dosyasına kaydedildi!")
    
    def load_embeddings(self, path: str) -> Dict[int, Dict[str, Any]]:
        """
        Kaydedilmiş embedding'leri yükler.
        
        Args:
            path: Yüklenecek dosya yolu
            
        Returns:
            Embedding sözlüğü
        """
        with open(path, "rb") as f:
            embeddings_dict = pickle.load(f)
        print(f"✅ {len(embeddings_dict)} embedding '{path}' dosyasından yüklendi!")
        return embeddings_dict
    
    def get_embedding_dimension(self) -> int:
        """
        Embedding vektör boyutunu döndürür.
        
        Returns:
            Vektör boyutu (Cosmos-E5-Large için 1024)
        """
        test_embedding = self.embed_query("test")
        return len(test_embedding)
