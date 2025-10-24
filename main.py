"""
Bilimp - Terracity AI Assistant
Ana giriş noktası
"""

import argparse
from pathlib import Path
from src.chunking import DocumentProcessor
from src.embedding import TextEmbedder
from src.qdrant import QdrantManager
from src.llm import ResponseGenerator


def setup_system(collection_name: str = "bilimp_docs"):
    """
    Bilimp sistemini başlatır
    
    Args:
        collection_name: Qdrant koleksiyon adı
        
    Returns:
        Sistem bileşenleri (tuple)
    """
    print("=== Bilimp Sistemi Başlatılıyor ===\n")
    
    # Bileşenleri oluştur
    doc_processor = DocumentProcessor(chunk_size=512, chunk_overlap=50)
    embedder = TextEmbedder()
    qdrant = QdrantManager(host="localhost", port=6333)
    llm = ResponseGenerator(model_name="gemma3-12b")
    
    # Qdrant'a bağlan
    try:
        qdrant.connect()
    except Exception as e:
        print(f"Uyarı: Qdrant bağlantısı kurulamadı: {e}")
        print("Docker ile Qdrant'ı başlattığınızdan emin olun: docker-compose up -d\n")
    
    # Koleksiyon oluştur (yoksa)
    if qdrant.client and not qdrant.collection_exists(collection_name):
        embedding_dim = embedder.get_embedding_dimension()
        qdrant.create_collection(collection_name, embedding_dim)
    
    return doc_processor, embedder, qdrant, llm, collection_name


def process_documents(doc_processor, embedder, qdrant, collection_name, document_paths):
    """
    Dokümanları işler ve Qdrant'a yükler
    
    Args:
        doc_processor: Doküman işleyici
        embedder: Embedding üretici
        qdrant: Qdrant yöneticisi
        collection_name: Koleksiyon adı
        document_paths: İşlenecek doküman yolları
    """
    print("\n=== Dokümanlar İşleniyor ===\n")
    
    all_chunks = []
    all_metadata = []
    
    for doc_path in document_paths:
        print(f"İşleniyor: {doc_path}")
        try:
            # Dokümanı chunk'lara böl
            chunks = doc_processor.process_document(doc_path)
            print(f"  - {len(chunks)} chunk oluşturuldu")
            
            # Metadata ekle
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadata.append({
                    "text": chunk,
                    "source": str(doc_path),
                    "chunk_id": i
                })
        except Exception as e:
            print(f"  - Hata: {e}")
    
    if not all_chunks:
        print("İşlenecek chunk bulunamadı.")
        return
    
    # Embedding'leri oluştur
    print(f"\n{len(all_chunks)} chunk için embedding oluşturuluyor...")
    embeddings = embedder.embed_batch(all_chunks)
    
    # Qdrant'a yükle
    if qdrant.client:
        print("Vektörler Qdrant'a yükleniyor...")
        qdrant.upload_vectors(collection_name, embeddings, all_metadata)
        print("✓ Yükleme tamamlandı!\n")
    else:
        print("Qdrant bağlantısı yok, vektörler yüklenemedi.\n")


def query_system(embedder, qdrant, llm, collection_name, question):
    """
    Sisteme soru sorar ve yanıt alır
    
    Args:
        embedder: Embedding üretici
        qdrant: Qdrant yöneticisi
        llm: Yanıt üretici
        collection_name: Koleksiyon adı
        question: Kullanıcı sorusu
        
    Returns:
        Yanıt dictionary'si
    """
    print(f"\nSoru: {question}\n")
    
    # Soruyu vektörleştir
    query_vector = embedder.embed_text(question)
    
    # Qdrant'ta ara
    if qdrant.client:
        results = qdrant.search(collection_name, query_vector, limit=5)
        print(f"✓ {len(results)} ilgili sonuç bulundu\n")
        
        # Yanıt üret
        response = llm.generate_with_retrieval(question, results)
        
        print("Yanıt:")
        print(response["answer"])
        print(f"\nGüven skoru: {response['confidence']:.2f}")
        print(f"Kaynak sayısı: {response['num_sources']}")
        
        return response
    else:
        print("Qdrant bağlantısı yok, sorgulama yapılamadı.")
        return None


def interactive_mode(embedder, qdrant, llm, collection_name):
    """
    Etkileşimli soru-cevap modu
    """
    print("\n=== Etkileşimli Mod ===")
    print("Çıkmak için 'quit' veya 'exit' yazın.\n")
    
    while True:
        try:
            question = input("Soru: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("Çıkılıyor...")
                break
            
            if not question:
                continue
            
            query_system(embedder, qdrant, llm, collection_name, question)
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nÇıkılıyor...")
            break
        except Exception as e:
            print(f"Hata: {e}\n")


def main():
    parser = argparse.ArgumentParser(description="Bilimp - Terracity AI Assistant")
    parser.add_argument(
        "--mode",
        choices=["process", "query", "interactive"],
        default="interactive",
        help="Çalışma modu"
    )
    parser.add_argument(
        "--documents",
        nargs="+",
        help="İşlenecek doküman yolları (process modu için)"
    )
    parser.add_argument(
        "--question",
        help="Sorulacak soru (query modu için)"
    )
    parser.add_argument(
        "--collection",
        default="bilimp_docs",
        help="Qdrant koleksiyon adı"
    )
    
    args = parser.parse_args()
    
    # Sistemi başlat
    doc_processor, embedder, qdrant, llm, collection_name = setup_system(args.collection)
    
    # Moda göre işlem yap
    if args.mode == "process":
        if not args.documents:
            print("Hata: --documents parametresi gerekli")
            return
        process_documents(doc_processor, embedder, qdrant, collection_name, args.documents)
    
    elif args.mode == "query":
        if not args.question:
            print("Hata: --question parametresi gerekli")
            return
        query_system(embedder, qdrant, llm, collection_name, args.question)
    
    elif args.mode == "interactive":
        interactive_mode(embedder, qdrant, llm, collection_name)


if __name__ == "__main__":
    main()
