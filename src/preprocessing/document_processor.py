"""
Document preprocessing and chunking module.
Handles document loading, text extraction, and chunking for the Bilimp system.

Authors: Engin, Batuhan
"""

import os
from typing import List, Dict, Any
from pathlib import Path
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredExcelLoader
)

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Processes documents from various formats and splits them into chunks."""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: Size of each text chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        self.loaders = {
            '.pdf': PyPDFLoader,
            '.docx': Docx2txtLoader,
            '.txt': TextLoader,
            '.xlsx': UnstructuredExcelLoader,
            '.xls': UnstructuredExcelLoader
        }
    
    def load_document(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load a document from file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of document objects with page content and metadata
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = path.suffix.lower()
        
        if extension not in self.loaders:
            raise ValueError(f"Unsupported file format: {extension}")
        
        try:
            loader_class = self.loaders[extension]
            loader = loader_class(file_path)
            documents = loader.load()
            
            logger.info(f"Successfully loaded {len(documents)} pages from {file_path}")
            return documents
        
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {e}")
            raise
    
    def chunk_documents(self, documents: List[Any]) -> List[Dict[str, Any]]:
        """
        Split documents into smaller chunks.
        
        Args:
            documents: List of document objects
            
        Returns:
            List of chunked documents with metadata
        """
        try:
            chunks = self.text_splitter.split_documents(documents)
            
            # Add chunk metadata
            chunked_docs = []
            for i, chunk in enumerate(chunks):
                chunked_doc = {
                    'id': f"chunk_{i}",
                    'text': chunk.page_content,
                    'metadata': {
                        **chunk.metadata,
                        'chunk_id': i,
                        'chunk_size': len(chunk.page_content)
                    }
                }
                chunked_docs.append(chunked_doc)
            
            logger.info(f"Created {len(chunked_docs)} chunks from documents")
            return chunked_docs
        
        except Exception as e:
            logger.error(f"Error chunking documents: {e}")
            raise
    
    def process_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Process all supported documents in a directory.
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of all chunked documents
        """
        all_chunks = []
        directory = Path(directory_path)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        supported_extensions = self.loaders.keys()
        files = [f for f in directory.rglob('*') if f.suffix.lower() in supported_extensions]
        
        logger.info(f"Found {len(files)} supported files in {directory_path}")
        
        for file_path in files:
            try:
                logger.info(f"Processing file: {file_path}")
                documents = self.load_document(str(file_path))
                chunks = self.chunk_documents(documents)
                
                # Add file path to metadata
                for chunk in chunks:
                    chunk['metadata']['source_file'] = str(file_path)
                
                all_chunks.extend(chunks)
                
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
                continue
        
        logger.info(f"Total chunks created: {len(all_chunks)}")
        return all_chunks


def main():
    """Example usage of the document processor."""
    logging.basicConfig(level=logging.INFO)
    
    # Initialize processor
    processor = DocumentProcessor(chunk_size=512, chunk_overlap=50)
    
    # Process documents from raw data directory
    data_dir = "data/raw"
    if os.path.exists(data_dir):
        chunks = processor.process_directory(data_dir)
        print(f"Processed {len(chunks)} chunks from documents")
    else:
        print(f"Data directory not found: {data_dir}")


if __name__ == "__main__":
    main()
