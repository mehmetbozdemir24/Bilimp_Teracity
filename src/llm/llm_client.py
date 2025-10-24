"""
LLM integration module for semantic response generation.
Uses Gemma3-12B and Qwen3-9B models via Ollama.

Authors: Hasan, Eren
"""

import logging
from typing import List, Dict, Any, Optional
import requests
import json

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for interacting with local LLM models via Ollama."""
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        gemma_model: str = "gemma3:12b",
        qwen_model: str = "qwen3:9b",
        default_model: str = "gemma3:12b"
    ):
        """
        Initialize LLM client.
        
        Args:
            base_url: Ollama API base URL
            gemma_model: Gemma model name
            qwen_model: Qwen model name
            default_model: Default model to use
        """
        self.base_url = base_url
        self.gemma_model = gemma_model
        self.qwen_model = qwen_model
        self.default_model = default_model
        
        logger.info(f"Initialized LLM client with base URL: {base_url}")
    
    def _call_ollama(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> str:
        """
        Call Ollama API to generate response.
        
        Args:
            model: Model name
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response text
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {e}")
            raise
    
    def generate_response(
        self,
        query: str,
        context: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Generate response based on query and retrieved context.
        
        Args:
            query: User query
            context: List of relevant documents from vector search
            model: Model to use (gemma or qwen), defaults to gemma
            temperature: Sampling temperature
            
        Returns:
            Generated response
        """
        if model is None:
            model = self.default_model
        
        # Prepare context from retrieved documents
        context_text = "\n\n".join([
            f"Document {i+1}:\n{doc['text']}"
            for i, doc in enumerate(context)
        ])
        
        # Create RAG prompt
        prompt = f"""Aşağıdaki bağlam bilgilerini kullanarak soruyu yanıtla. Eğer cevap bağlamda yoksa, bilmediğini söyle.

Bağlam:
{context_text}

Soru: {query}

Yanıt:"""
        
        logger.info(f"Generating response with model: {model}")
        
        try:
            response = self._call_ollama(
                model=model,
                prompt=prompt,
                temperature=temperature
            )
            
            logger.info("Response generated successfully")
            return response
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def generate_with_gemma(
        self,
        query: str,
        context: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> str:
        """
        Generate response using Gemma3-12B model.
        
        Args:
            query: User query
            context: Retrieved context documents
            temperature: Sampling temperature
            
        Returns:
            Generated response
        """
        return self.generate_response(
            query=query,
            context=context,
            model=self.gemma_model,
            temperature=temperature
        )
    
    def generate_with_qwen(
        self,
        query: str,
        context: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> str:
        """
        Generate response using Qwen3-9B model.
        
        Args:
            query: User query
            context: Retrieved context documents
            temperature: Sampling temperature
            
        Returns:
            Generated response
        """
        return self.generate_response(
            query=query,
            context=context,
            model=self.qwen_model,
            temperature=temperature
        )
    
    def generate_with_both_models(
        self,
        query: str,
        context: List[Dict[str, Any]],
        temperature: float = 0.7
    ) -> Dict[str, str]:
        """
        Generate responses using both Gemma and Qwen models.
        
        Args:
            query: User query
            context: Retrieved context documents
            temperature: Sampling temperature
            
        Returns:
            Dictionary with responses from both models
        """
        logger.info("Generating responses with both models")
        
        responses = {
            "gemma": self.generate_with_gemma(query, context, temperature),
            "qwen": self.generate_with_qwen(query, context, temperature)
        }
        
        return responses
    
    def check_model_availability(self, model: str) -> bool:
        """
        Check if a model is available in Ollama.
        
        Args:
            model: Model name to check
            
        Returns:
            True if model is available, False otherwise
        """
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            models_data = response.json()
            available_models = [m['name'] for m in models_data.get('models', [])]
            
            return model in available_models
        
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False


class RAGSystem:
    """Complete RAG (Retrieval-Augmented Generation) system."""
    
    def __init__(
        self,
        database,
        embedding_generator,
        llm_client,
        top_k: int = 5
    ):
        """
        Initialize RAG system.
        
        Args:
            database: QdrantDatabase instance
            embedding_generator: EmbeddingGenerator instance
            llm_client: LLMClient instance
            top_k: Number of documents to retrieve
        """
        self.database = database
        self.embedding_generator = embedding_generator
        self.llm_client = llm_client
        self.top_k = top_k
        
        logger.info("RAG system initialized")
    
    def query(
        self,
        query: str,
        model: Optional[str] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Process a query through the RAG pipeline.
        
        Args:
            query: User query
            model: Model to use for generation
            temperature: Sampling temperature
            
        Returns:
            Dictionary containing query, retrieved documents, and response
        """
        logger.info(f"Processing query: {query}")
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_generator.generate_query_embedding(query)
            
            # Retrieve relevant documents
            retrieved_docs = self.database.search(
                query_embedding=query_embedding.tolist(),
                limit=self.top_k
            )
            
            # Generate response
            response = self.llm_client.generate_response(
                query=query,
                context=retrieved_docs,
                model=model,
                temperature=temperature
            )
            
            return {
                'query': query,
                'retrieved_documents': retrieved_docs,
                'response': response,
                'model': model or self.llm_client.default_model
            }
        
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise


def main():
    """Example usage of LLM client."""
    logging.basicConfig(level=logging.INFO)
    
    # Initialize client
    client = LLMClient()
    
    # Example context
    example_context = [
        {
            'text': 'Bilimp sistemi doküman yönetimi için kullanılır.',
            'score': 0.95
        }
    ]
    
    # Generate response
    try:
        response = client.generate_with_gemma(
            query="Bilimp sistemi nedir?",
            context=example_context
        )
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Ollama is running and models are installed")


if __name__ == "__main__":
    main()
