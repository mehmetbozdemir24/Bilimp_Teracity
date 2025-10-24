# Basit örnek: LangChain ile doküman yükleme ve chunk'lara ayırma
# Gereksinimler: langchain (ve gerekli loader paketleri)
from langchain.document_loaders import PyPDFLoader, DocxLoader, PowerPointLoader, ExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os

def load_documents(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(path)
    elif ext in [".docx", ".doc"]:
        loader = DocxLoader(path)
    elif ext in [".pptx", ".ppt"]:
        loader = PowerPointLoader(path)
    elif ext in [".xlsx", ".xls"]:
        loader = ExcelLoader(path)
    else:
        # düz metin dosyası için basit yükleme
        with open(path, "r", encoding="utf-8") as f:
            return [Document(page_content=f.read(), metadata={"source": path})]
    return loader.load()

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = []
    for doc in documents:
        texts = splitter.split_text(doc.page_content)
        for i, t in enumerate(texts):
            chunks.append(Document(page_content=t, metadata={**doc.metadata, "chunk": i}))
    return chunks

if __name__ == "__main__":
    # Örnek kullanım: path'i değiştir
    path = "path/to/your/document.pdf"
    docs = load_documents(path)
    chunked = chunk_documents(docs, chunk_size=800, chunk_overlap=100)
    print(f"Toplam chunk sayısı: {len(chunked)}")
    # İstersen chunk'ları dosyaya yaz
    out_dir = "chunks_output"
    os.makedirs(out_dir, exist_ok=True)
    for i, c in enumerate(chunked):
        fname = os.path.join(out_dir, f"chunk_{i}.txt")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(c.page_content)
    print(f"Chunk'lar {out_dir} içine kaydedildi.")