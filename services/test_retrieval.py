# services/test_retrieval.py

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "default"
EMBED_MODEL = "all-MiniLM-L6-v2"

def test_retrieval(query, k=5):
    print(f"🔎 Query: {query}")

    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embedding
    )

    results = vectordb.similarity_search(query, k=k)
    if not results:
        print("⚠️ No results found.")
    else:
        print(f"✅ Retrieved {len(results)} results:\n")
        for i, r in enumerate(results, 1):
            print(f"[{i}] Content: {r.page_content[:200]}...")
            print(f"    Metadata: {r.metadata}\n")

if __name__ == "__main__":
    test_retrieval("How to treat bug bite?")
    #test_retrieval("insect bite")
    #test_retrieval("first aid for bites")