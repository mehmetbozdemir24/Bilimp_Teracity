"""
Embedding Modülü Kullanım Örneği

⚠️ DİKKAT: Bu script HuggingFace'den model indirdiği için internet bağlantısı gerektirir.

Bu script, docs/2_embedding_guide.md'deki örnekleri gösterir.
"""

import sys
import os

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
from langchain_core.documents import Document
from src.embedding import EmbeddingProcessor


def main():
    print("="*60)
    print("EMBEDDING MODÜLÜ KULLANIM ÖRNEĞİ")
    print("="*60)
    
    # GPU/CPU kontrolü
    print(f"\n🖥️  GPU Kullanılabilir: {torch.cuda.is_available()}")
    
    # Model yükleme
    print("\n📥 Model yükleniyor...")
    processor = EmbeddingProcessor()
    
    # Test 1: Tek metin vektörleme
    print("\n" + "="*60)
    print("TEST 1: Tek Metin Vektörleme")
    print("="*60)
    
    text = "Python programlama dilidir"
    embedding = processor.embed_query(text)
    print(f"Metin: '{text}'")
    print(f"Embedding boyutu: {len(embedding)}")
    print(f"İlk 5 değer: {embedding[:5]}")
    
    # Test 2: Basit chunk listesi
    print("\n" + "="*60)
    print("TEST 2: Basit Chunk Listesi")
    print("="*60)
    
    chunks = [
        "Python programlama dilidir",
        "Makine öğrenmesi yapay zekadır"
    ]
    embeddings_list = processor.embed_documents(chunks)
    print(f"✅ {len(embeddings_list)} chunk vektörleştirildi!")
    
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings_list)):
        print(f"  Chunk {i+1}: '{chunk}' -> Vektör boyutu: {len(emb)}")
    
    # Test 3: LangChain Document chunks
    print("\n" + "="*60)
    print("TEST 3: LangChain Document Chunks")
    print("="*60)
    
    documents = [
        Document(
            page_content="Python programlama dilidir",
            metadata={"source": "ders1.pdf", "page": 1}
        ),
        Document(
            page_content="Makine öğrenmesi yapay zekadır",
            metadata={"source": "ders2.pdf", "page": 2}
        ),
        Document(
            page_content="LangChain güçlü bir framework'tür",
            metadata={"source": "ders3.pdf", "page": 3}
        ),
    ]
    
    embeddings_dict = processor.process_chunks(documents, batch_size=2)
    print(f"\n📊 İşlenen dokümantasyon:")
    for idx, data in embeddings_dict.items():
        print(f"  [{idx}] {data['content'][:50]}...")
        print(f"      Kaynak: {data['metadata']['source']}")
        print(f"      Vektör boyutu: {len(data['embedding'])}")
    
    # Test 4: Benzerlik hesaplama
    print("\n" + "="*60)
    print("TEST 4: Benzerlik Hesaplama")
    print("="*60)
    
    import numpy as np
    
    emb1 = processor.embed_query("Makine öğrenmesi yapay zekadır")
    emb2 = processor.embed_query("Yapay zeka makine öğrenmesidir")
    emb3 = processor.embed_query("Bugün hava çok güzel")
    
    similarity_high = np.dot(emb1, emb2)
    similarity_low = np.dot(emb1, emb3)
    
    print(f"Benzer metinler arası benzerlik: {similarity_high:.4f}")
    print(f"Farklı metinler arası benzerlik: {similarity_low:.4f}")
    
    # Test 5: Kaydetme ve yükleme
    print("\n" + "="*60)
    print("TEST 5: Embedding Kaydetme ve Yükleme")
    print("="*60)
    
    output_path = "/tmp/embeddings_example.pkl"
    processor.save_embeddings(embeddings_dict, output_path)
    
    loaded_dict = processor.load_embeddings(output_path)
    print(f"✅ Yükleme başarılı! {len(loaded_dict)} embedding bulundu.")
    
    # Test 6: Model bilgileri
    print("\n" + "="*60)
    print("MODEL BİLGİLERİ")
    print("="*60)
    print(f"Model: {processor.model_name}")
    print(f"Device: {processor.device}")
    print(f"Embedding boyutu: {processor.get_embedding_dimension()}")
    
    print("\n" + "="*60)
    print("✅ TÜM TESTLER TAMAMLANDI!")
    print("="*60)


if __name__ == "__main__":
    main()
