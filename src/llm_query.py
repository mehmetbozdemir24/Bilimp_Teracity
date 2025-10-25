"""
LLM Sorgulama Modülü - Prompt işleme ve yanıt üretimi
Sorumlular: Hasan, Eren
"""
from typing import Optional, Dict, Any, List
from langchain_community.llms import Ollama
from langchain_openai import OpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from .config import config
from .utils import safe_text, create_prompt_template, validate_input


class LLMQuerySystem:
    """
    LLM tabanlı sorgulama sistemi
    
    OpenAI veya Ollama LLM'lerini kullanarak prompt işleme 
    ve yanıt üretimi gerçekleştirir.
    """
    
    def __init__(
        self, 
        use_openai: bool = False,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        """
        LLM sorgulama sistemini başlatır
        
        Args:
            use_openai: True ise OpenAI, False ise Ollama kullanır
            model_name: Kullanılacak model adı (None ise config'ten alınır)
            temperature: LLM temperature parametresi
            max_tokens: Maksimum token sayısı
        """
        self.use_openai = use_openai
        self.temperature = temperature or config.LLM_TEMPERATURE
        self.max_tokens = max_tokens or config.LLM_MAX_TOKENS
        
        # LLM'yi başlat
        if use_openai:
            if not config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY ortam değişkeni ayarlanmalıdır")
            
            self.model_name = model_name or config.OPENAI_MODEL
            self.llm = OpenAI(
                api_key=config.OPENAI_API_KEY,
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
        else:
            self.model_name = model_name or config.OLLAMA_MODEL
            self.llm = Ollama(
                base_url=config.OLLAMA_BASE_URL,
                model=self.model_name,
                temperature=self.temperature
            )
        
        # Konuşma belleğini başlat
        self.memory = ConversationBufferWindowMemory(
            k=config.MEMORY_WINDOW_SIZE,
            return_messages=True
        )
    
    def query(
        self, 
        prompt: str, 
        context: Optional[str] = None,
        language: str = "tr"
    ) -> Dict[str, Any]:
        """
        LLM'ye sorgu gönderir ve yanıt alır
        
        Args:
            prompt: Kullanıcı sorusu veya prompt
            context: İsteğe bağlı bağlam bilgisi (RAG için)
            language: Yanıt dili (tr veya en)
            
        Returns:
            Yanıt bilgilerini içeren dictionary
        """
        # Girişi doğrula
        is_valid, error_msg = validate_input(prompt)
        if not is_valid:
            return {
                "success": False,
                "error": error_msg,
                "response": None
            }
        
        try:
            # Eğer bağlam verilmişse RAG prompt'u oluştur
            if context:
                formatted_prompt = create_prompt_template(context, prompt, language)
            else:
                formatted_prompt = prompt
            
            # LLM'den yanıt al
            response = self.llm.invoke(formatted_prompt)
            
            # Güvenli metin işleme
            safe_response = safe_text(response)
            
            # Belleğe kaydet
            self.memory.save_context(
                {"input": prompt},
                {"output": safe_response}
            )
            
            return {
                "success": True,
                "response": safe_response,
                "model": self.model_name,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }
    
    def query_with_chain(
        self,
        prompt: str,
        template: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        LangChain chain kullanarak sorgu yapar
        
        Args:
            prompt: Kullanıcı sorusu
            template: İsteğe bağlı prompt şablonu
            
        Returns:
            Yanıt bilgilerini içeren dictionary
        """
        try:
            # Varsayılan şablon
            if template is None:
                template = "Soru: {question}\n\nYanıt:"
            
            # Prompt şablonu oluştur
            prompt_template = PromptTemplate(
                input_variables=["question"],
                template=template
            )
            
            # Chain oluştur
            chain = LLMChain(
                llm=self.llm,
                prompt=prompt_template,
                memory=self.memory
            )
            
            # Sorguyu çalıştır
            response = chain.run(question=prompt)
            
            # Güvenli metin işleme
            safe_response = safe_text(response)
            
            return {
                "success": True,
                "response": safe_response,
                "model": self.model_name,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Konuşma geçmişini döndürür
        
        Returns:
            Konuşma geçmişi listesi
        """
        try:
            messages = self.memory.load_memory_variables({})
            return messages.get("history", [])
        except Exception:
            return []
    
    def clear_memory(self):
        """Konuşma geçmişini temizler"""
        self.memory.clear()


def create_llm_system(use_openai: bool = False) -> LLMQuerySystem:
    """
    LLM sorgulama sistemi factory fonksiyonu
    
    Args:
        use_openai: True ise OpenAI, False ise Ollama kullanır
        
    Returns:
        LLMQuerySystem instance
    """
    return LLMQuerySystem(use_openai=use_openai)
