from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import re

class AdvancedChunking:
    """Gelişmiş metin bölümleme ve işleme sistemi"""
    
    def __init__(self, chunk_size=1000, chunk_overlap=250):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name="ytu-ce-cosmos/turkish-e5-large"
        )
    
    def enrich_metadata(self, doc, pdf_name, page_num, processed_date=None):
        """Metadata'yı zenginleştir"""
        if processed_date is None:
            processed_date = datetime.now().isoformat()
        
        return {
            "source": pdf_name,
            "page_number": page_num,
            "processed_date": processed_date,
            "language": "turkish",
            "content_type": self._detect_content_type(doc)
        }
    
    def _detect_content_type(self, text):
        """İçerik tipini tespit et"""
        if re.search(r'^\d+\.', text):
            return "list"
        elif re.search(r'^#{1,6}\s', text):
            return "heading"
        elif '|' in text and text.count('\n') > 2:
            return "table"
        else:
            return "paragraph"
    
    def validate_chunk_quality(self, chunk_text, min_length=50, min_words=5):
        """Chunk kalitesini kontrol et"""
        if len(chunk_text.strip()) < min_length:
            return False
        if chunk_text.count(' ') < min_words:
            return False
        if chunk_text.count('\n') > 50:
            return False
        return True
    
    def process_chunks_batch(self, documents, batch_size=32):
        """Chunk'ları batch halinde işle"""
        valid_chunks = []
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            for doc in batch:
                if self.validate_chunk_quality(doc.page_content):
                    valid_chunks.append(doc)
        return valid_chunks
    
    def add_semantic_tags(self, chunk_text):
        """Semantik etiketler ekle"""
        tags = []
        if re.search(r'\d+\.\d+', chunk_text):
            tags.append("mathematical")
        if re.search(r'[A-Z]{2,}', chunk_text):
            tags.append("acronym")
        if re.search(r'\(\d+\)', chunk_text):
            tags.append("reference")
        return tags