# services/build_chroma_db.py

import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Load environment variables from .env if needed
load_dotenv()

# Configuration
PDF_PATH = "documents/First-Aid-Quick-Guide.pdf"
CHROMA_DIR = "chroma_db"
EMBED_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "default"

def extract_text_from_pdf(pdf_path):
    """Extract raw text page by page."""
    print("Extracting text from PDF using PyMuPDF...")
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            pages.append((i + 1, text))
    return pages


def split_text_to_documents(pages):
    """Split text into chunks and attach metadata with headings."""
    print("Splitting text into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    documents = []
    for page_number, text in pages:
        # Simple heading detection: take the first line as a "heading"
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        heading = lines[0] if lines else f"Page {page_number}"

        # Prepend heading to each chunk for better semantic retrieval
        chunks = splitter.split_text(text)
        for chunk in chunks:
            doc = Document(
                page_content=f"{heading}\n{chunk}",
                metadata={"page": page_number, "heading": heading}
            )
            documents.append(doc)

    return documents

def build_chroma_from_pdf(pdf_path, chroma_dir, model_name, collection_name):
    # Step 1: Extract + chunk
    pages = extract_text_from_pdf(pdf_path)
    documents = split_text_to_documents(pages)

    print(f"Created {len(documents)} document chunks.")

    # Step 2: Load embedding model
    print("Generating embeddings...")
    embedding = HuggingFaceEmbeddings(model_name=model_name)

    # Step 3: Store in persistent Chroma vector DB
    print("Creating ChromaDB...")
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        persist_directory=chroma_dir,
        collection_name=collection_name
    )

    print(f"ChromaDB created and stored at: {chroma_dir} (collection: {collection_name})")

if __name__ == "__main__":
    build_chroma_from_pdf(PDF_PATH, CHROMA_DIR, EMBED_MODEL, COLLECTION_NAME)