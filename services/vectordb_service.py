# services/vectordb_service.py

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from flask import current_app

class VectorDBService:
    def __init__(self, vectordb, qa_chain, persist_directory, collection_name, embed_model):
        self.vectordb = vectordb
        self.qa_chain = qa_chain
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embed_model = embed_model

    @staticmethod
    def from_config():
        persist_directory = current_app.config.get("CHROMA_DB_DIR", "chroma_db")
        collection_name = current_app.config.get("CHROMA_COLLECTION", "default")
        model_name = current_app.config.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        llm_name = current_app.config.get("LLM_MODEL", "llama3")

        print("=" * 60)
        print(" VectorDBService.from_config() called")
        print(f" persist_directory = {persist_directory}")
        print(f" collection_name   = {collection_name}")
        print(f" embedding model   = {model_name}")
        print(f" LLM model         = {llm_name}")
        print("=" * 60)

        # Embeddings + Chroma
        embedding = HuggingFaceEmbeddings(model_name=model_name)
        vectordb = Chroma(
            persist_directory=persist_directory,
            collection_name=collection_name,  
            embedding_function=embedding
        )

        # Custom system prompt
        QA_TEMPLATE = """You are a helpful health assistant.

Using the context provided, answer the question below.

Context:
{context}

Question:
{question}

If the context does not contain the answer, say:
"I do not know. Please seek out advice from the nearest healthcare practitioner."
"""
        qa_prompt = PromptTemplate(
            template=QA_TEMPLATE,
            input_variables=["context", "question"]
        )

        llm = Ollama(model=llm_name)
        qa_chain = LLMChain(llm=llm, prompt=qa_prompt)

        return VectorDBService(vectordb, qa_chain, persist_directory, collection_name, model_name)

    def ask(self, query: str):
        print("=" * 60)
        print(f" Received query: {repr(query)}")
        print(f" Persist dir: {self.persist_directory}")
        print(f" Collection: {self.collection_name}")
        print(f" Embed model: {self.embed_model}")

        # Step 1: Direct similarity search
        try:
            results = self.vectordb.similarity_search(query, k=5)
        except Exception as e:
            print(f" similarity_search raised error: {e}")
            raise

        print(f" similarity_search retrieved {len(results)} results")
        for i, r in enumerate(results, 1):
            print(f"[{i}] {r.page_content[:200]}...")
            print(f"    Metadata: {r.metadata}\n")

        if not results:
            print(" No documents retrieved from similarity search.")
            return {
                "answer": "I do not know. Please seek out advice from the nearest healthcare practitioner.",
                "sources": []
            }

        # Step 2: Build context
        context = "\n\n".join([d.page_content for d in results])
        print(" Context being passed to LLM (truncated to 500 chars):")
        print(context[:500] + "...\n")

        # Step 3: Run LLM
        result = self.qa_chain.run({"context": context, "question": query})
        print(" LLM Response:")
        print(result)
        print("=" * 60)

        return {
            "answer": result,
            "sources": [
                {"content": d.page_content[:200], "metadata": d.metadata}
                for d in results
            ]
        }

    def similarity_search(self, query: str, k: int = 5):
        print(f" Running direct similarity search for: {repr(query)}")
        results = self.vectordb.similarity_search(query, k=k)
        for i, r in enumerate(results, 1):
            print(f"[{i}] {r.page_content[:200]} ... (metadata={r.metadata})")
        return results

    def get_document_count(self) -> int:
        store = self.vectordb.get()
        count = len(store.get("documents", []))
        print(f" Chroma contains {count} chunks in collection '{self.collection_name}'")
        return count