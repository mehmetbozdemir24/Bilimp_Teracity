"""
Yardımcı fonksiyonlar - Güvenlik ve metin işleme
"""
import re
from typing import List, Dict, Any


def safe_text(text: str) -> str:
    """
    LLM çıktısındaki potansiyel olarak zararlı içeriği temizler
    
    Args:
        text: Temizlenecek metin
        
    Returns:
        Güvenli metin
    """
    # Tehlikeli HTML etiketlerini kaldır
    text = text.replace("<script>", "").replace("</script>", "")
    text = text.replace("<iframe>", "").replace("</iframe>", "")
    
    # Gereksiz boşlukları temizle
    text = text.strip()
    
    return text


def format_context(results: List[Dict[str, Any]]) -> str:
    """
    Qdrant'tan alınan sonuçları prompt için formatlar
    
    Args:
        results: Qdrant arama sonuçları
        
    Returns:
        Formatlanmış bağlam metni
    """
    if not results:
        return "İlgili bağlam bulunamadı."
    
    context_parts = []
    for idx, result in enumerate(results, 1):
        # Payload içindeki metin bilgisini al
        text = result.payload.get("text", "") if hasattr(result, 'payload') else ""
        if text:
            context_parts.append(f"[{idx}] {text}")
    
    return "\n\n".join(context_parts) if context_parts else "İlgili bağlam bulunamadı."


def create_prompt_template(context: str, question: str, language: str = "tr") -> str:
    """
    RAG için prompt şablonu oluşturur
    
    Args:
        context: Vektör veritabanından alınan bağlam
        question: Kullanıcının sorusu
        language: Yanıt dili (tr veya en)
        
    Returns:
        Formatlanmış prompt
    """
    if language == "tr":
        template = f"""Aşağıda verilen bağlam bilgisini kullanarak soruyu yanıtlayın. 
Yanıtınızı yalnızca verilen bağlam bilgisine dayandırın. 
Eğer bağlamda yanıt yoksa, "Bu sorunun yanıtı verilen dokümanlarda bulunmamaktadır." şeklinde yanıt verin.

Bağlam:
{context}

Soru: {question}

Yanıt:"""
    else:
        template = f"""Answer the question based on the context provided below.
Base your answer only on the given context.
If the answer is not in the context, respond with "The answer to this question is not found in the provided documents."

Context:
{context}

Question: {question}

Answer:"""
    
    return template


def validate_input(text: str, max_length: int = 2000) -> tuple[bool, str]:
    """
    Kullanıcı girişini doğrular
    
    Args:
        text: Doğrulanacak metin
        max_length: Maksimum karakter uzunluğu
        
    Returns:
        (geçerli_mi, hata_mesajı) tuple
    """
    if not text or not text.strip():
        return False, "Boş giriş geçerli değildir."
    
    if len(text) > max_length:
        return False, f"Giriş {max_length} karakteri aşmamalıdır."
    
    return True, ""
