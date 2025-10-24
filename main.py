import os
import pickle
import logging
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

try:
    from src.preprocessing.normalization import normalize_text
except Exception:
    # fallback if module path not yet available
    def normalize_text(txt):
        import re
        text = re.sub(r'-\s*\n\s*', '', txt)
        text = re.sub(r'([\.\!\?…])\s*\n\s*', r'\1\n\n', text)
        text = re.sub(r'\s*\n\s*', ' ', text)
        return re.sub(r' {2,}', ' ', text).strip()

# Configuration (adjust or move to config.py)
PDF_FOLDER = os.environ.get('PDF_FOLDER', 'birlesik_pdf')
OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER', 'outputs')
CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', 1000))
CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', 250))

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

def process_pdf_file(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    raw_docs = loader.load()
    docs = []
    for d in raw_docs:
        content = normalize_text(d.page_content)
        docs.append({'content': content, 'metadata': getattr(d, 'metadata', {})})
    return docs

def create_chunks_from_docs(docs, source_filename: str, start_chunk_no=1):
    chunks = []
    chunk_no = start_chunk_no
    for d in docs:
        split_docs = splitter.split_text(d['content'])
        for s in split_docs:
            chunks.append({
                'page_content': s,
                'metadata': {
                    'source': source_filename,
                    'chunk_no': chunk_no,
                    'chunk_type': 'text'
                }
            })
            chunk_no += 1
    return chunks

def save_pickle(obj, out_path: str):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as f:
        pickle.dump(obj, f)

def orchestrate(pdf_dir: str = PDF_FOLDER, output_dir: str = OUTPUT_FOLDER):
    pdf_dir = Path(pdf_dir)
    output_dir = Path(output_dir)
    all_chunks = []
    total_chunk_count = 0

    if not pdf_dir.exists():
        logging.error(f"PDF klasörü bulunamadı: {pdf_dir}")
        return

    for pdf_file in sorted(pdf_dir.glob('**/*.pdf')):
        logging.info(f"İşleniyor: {pdf_file.name}")
        docs = process_pdf_file(str(pdf_file))
        chunks = create_chunks_from_docs(docs, pdf_file.name, start_chunk_no=total_chunk_count+1)
        total_chunk_count += len(chunks)
        all_chunks.extend(chunks)

        out_pkl = output_dir / f"{pdf_file.stem}.pkl"
        save_pickle(chunks, str(out_pkl))
        logging.info(f"  -> {len(chunks)} chunk oluşturuldu, kaydedildi: {out_pkl}")

    # Ayrıca tüm chunk'ları tek bir dosyaya da kaydet
    all_out = output_dir / "all_chunks.pkl"
    save_pickle(all_chunks, str(all_out))
    logging.info(f"Toplam {len(all_chunks)} chunk kaydedildi: {all_out}")


if __name__ == '__main__':
    orchestrate()