"""
LLM response generation module
Görevliler: Hasan, Eren
"""

from typing import List, Dict, Any, Optional
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class ResponseGenerator:
    """Gemma3-12B ve Qwen3-9B modelleriyle yanıt üretimi"""
    
    def __init__(self, model_name: str = "gemma3-12b", temperature: float = 0.7):
        """
        Args:
            model_name: Kullanılacak LLM modeli (gemma3-12b veya qwen3-9b)
            temperature: Model sıcaklığı (yaratıcılık seviyesi)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.llm = None
        
    def _load_model(self):
        """LLM modelini yükler"""
        # Model yükleme gerçek implementasyonda yapılacak
        # Şimdilik placeholder
        print(f"LLM modeli yüklenecek: {self.model_name}")
        pass
    
    def create_prompt_template(self) -> PromptTemplate:
        """
        Yanıt üretimi için prompt şablonu oluşturur
        
        Returns:
            Prompt şablonu
        """
        template = """Sen Terracity firmasının Bilimp yapay zeka asistanısın. 
        Verilen bağlam bilgilerini kullanarak soruyu yanıtla.
        
        Bağlam:
        {context}
        
        Soru: {question}
        
        Yanıt:"""
        
        return PromptTemplate(
            input_variables=["context", "question"],
            template=template
        )
    
    def generate_response(
        self,
        question: str,
        context_chunks: List[str],
        max_tokens: int = 512
    ) -> str:
        """
        Soru ve bağlam bilgilerine göre yanıt üretir
        
        Args:
            question: Kullanıcı sorusu
            context_chunks: İlgili doküman parçaları
            max_tokens: Maksimum token sayısı
            
        Returns:
            Üretilen yanıt
        """
        # Bağlam oluştur
        context = "\n\n".join(context_chunks)
        
        # Prompt oluştur
        prompt = self.create_prompt_template()
        formatted_prompt = prompt.format(context=context, question=question)
        
        # Yanıt üret (gerçek implementasyonda LLM çağrısı yapılacak)
        response = self._call_llm(formatted_prompt, max_tokens)
        
        return response
    
    def _call_llm(self, prompt: str, max_tokens: int) -> str:
        """
        LLM'i çağırır ve yanıt alır
        
        Args:
            prompt: Formatlanmış prompt
            max_tokens: Maksimum token sayısı
            
        Returns:
            Model yanıtı
        """
        # Gerçek implementasyonda model çağrısı yapılacak
        # Şimdilik placeholder yanıt
        return f"[{self.model_name} ile üretilen yanıt buraya gelecek]"
    
    def generate_with_retrieval(
        self,
        question: str,
        retrieved_results: List[Dict[str, Any]],
        max_tokens: int = 512
    ) -> Dict[str, Any]:
        """
        Qdrant'tan alınan sonuçlarla yanıt üretir
        
        Args:
            question: Kullanıcı sorusu
            retrieved_results: Qdrant arama sonuçları
            max_tokens: Maksimum token sayısı
            
        Returns:
            Yanıt ve metadata
        """
        # Chunk'ları çıkar
        chunks = [result.get("payload", {}).get("text", "") for result in retrieved_results]
        chunks = [c for c in chunks if c]  # Boş olanları filtrele
        
        if not chunks:
            return {
                "answer": "Üzgünüm, sorunuzla ilgili bilgi bulunamadı.",
                "sources": [],
                "confidence": 0.0
            }
        
        # Yanıt üret
        answer = self.generate_response(question, chunks, max_tokens)
        
        # Güven skoru hesapla (ortalama benzerlik skoru)
        scores = [result.get("score", 0.0) for result in retrieved_results]
        confidence = sum(scores) / len(scores) if scores else 0.0
        
        return {
            "answer": answer,
            "sources": chunks[:3],  # İlk 3 kaynağı göster
            "confidence": confidence,
            "num_sources": len(chunks)
        }
