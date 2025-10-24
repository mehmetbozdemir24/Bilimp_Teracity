import os
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r') as file:
                documents.append(file.read())
    return documents

def chunk_text(documents):
    text_splitter = RecursiveCharacterTextSplitter()
    chunks = []
    for doc in documents:
        chunks.extend(text_splitter.split_text(doc))
    return chunks

def handle_metadata(chunks):
    metadata = [{'chunk_id': i, 'length': len(chunk)} for i, chunk in enumerate(chunks)]
    return metadata

def serialize_data(chunks, metadata, output_file):
    with open(output_file, 'wb') as f:
        pickle.dump({'chunks': chunks, 'metadata': metadata}, f)

# Example usage:
# documents = load_documents('path_to_documents')
# chunks = chunk_text(documents)
# metadata = handle_metadata(chunks)
# serialize_data(chunks, metadata, 'output_data.pkl')
