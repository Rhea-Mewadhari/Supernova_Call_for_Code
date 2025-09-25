# services/chroma_status.py

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "default"
EMBED_MODEL = "all-MiniLM-L6-v2"

def print_chroma_status():
    # Reload embeddings + vectordb
    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embedding
    )

    # Get raw data
    store = vectordb.get()
    doc_count = len(store.get("ids", []))

    print("===  ChromaDB Status ===")
    print(f"Persist Directory : {CHROMA_DIR}")
    print(f"Collection Name   : {COLLECTION_NAME}")
    print(f"Embedding Model   : {EMBED_MODEL}")
    print(f"Total Chunks      : {doc_count}")

    # Sample preview
    if doc_count > 0:
        print("\n--- Sample Document ---")
        print(f"ID: {store['ids'][0]}")
        print(f"Content: {store['documents'][0][:200]}...")
        print(f"Metadata: {store['metadatas'][0]}")

if __name__ == "__main__":
    print_chroma_status()