"""
Document processing and chunking module
Görevliler: Engin, Batuhan
"""

from typing import List, Optional
import nltk
from pypdf import PdfReader


class DocumentProcessor:
    """Doküman okuma ve chunk'lara ayırma işlemlerini gerçekleştirir"""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """
        Args:
            chunk_size: Her chunk'ın maksimum karakter sayısı
            chunk_overlap: Chunk'lar arası örtüşme miktarı
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # NLTK için gerekli verileri indir
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
    
    def read_pdf(self, file_path: str) -> str:
        """
        PDF dosyasını okur ve metin olarak döndürür
        
        Args:
            file_path: PDF dosyasının yolu
            
        Returns:
            Çıkarılan metin
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"PDF okuma hatası: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        """
        Metni temizler (gereksiz boşluklar, özel karakterler vb.)
        
        Args:
            text: Ham metin
            
        Returns:
            Temizlenmiş metin
        """
        # Çoklu boşlukları tek boşluğa indir
        text = ' '.join(text.split())
        return text
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Metni belirli boyutta chunk'lara böler
        
        Args:
            text: Bölünecek metin
            
        Returns:
            Chunk listesi
        """
        chunks = []
        text_length = len(text)
        start = 0
        
        while start < text_length:
            end = start + self.chunk_size
            
            # Son chunk kontrolü
            if end >= text_length:
                chunks.append(text[start:].strip())
                break
            
            # Kelime ortasında kesmemek için
            while end > start and text[end] not in [' ', '\n', '.', '!', '?']:
                end -= 1
            
            if end == start:  # Çok uzun kelime durumu
                end = start + self.chunk_size
            
            chunks.append(text[start:end].strip())
            start = end - self.chunk_overlap
        
        return [chunk for chunk in chunks if chunk]  # Boş chunk'ları filtrele
    
    def process_document(self, file_path: str) -> List[str]:
        """
        Dokümanı okur, temizler ve chunk'lara böler
        
        Args:
            file_path: Doküman dosya yolu
            
        Returns:
            Chunk listesi
        """
        # PDF oku
        text = self.read_pdf(file_path)
        
        # Metni temizle
        clean = self.clean_text(text)
        
        # Chunk'lara böl
        chunks = self.chunk_text(clean)
        
        return chunks
