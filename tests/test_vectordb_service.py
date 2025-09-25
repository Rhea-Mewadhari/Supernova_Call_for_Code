import pytest
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document

from Supernova_Call_for_Code.services.vectordb_service import VectorDBService

@pytest.fixture
def fake_doc():
    return Document(page_content="doc content", metadata={"page": 1})

@pytest.fixture
def fake_vectordb():
    return MagicMock()

@pytest.fixture
def fake_chain():
    chain = MagicMock()
    chain.run.return_value = "mocked answer"
    return chain

@patch("Supernova_Call_for_Code.services.vectordb_service.LLMChain")
@patch("Supernova_Call_for_Code.services.vectordb_service.Ollama")
@patch("Supernova_Call_for_Code.services.vectordb_service.PromptTemplate")
@patch("Supernova_Call_for_Code.services.vectordb_service.Chroma")
@patch("Supernova_Call_for_Code.services.vectordb_service.HuggingFaceEmbeddings")
def test_from_config_success(mock_embed, mock_chroma, mock_prompt, mock_ollama, mock_llmchain, monkeypatch):
    class DummyApp:
        config = {
            "CHROMA_DB_DIR": "mydb",
            "CHROMA_COLLECTION": "mycol",
            "EMBEDDING_MODEL": "my-embed",
            "LLM_MODEL": "llama3"
        }
    import Supernova_Call_for_Code.services.vectordb_service as vdb
    monkeypatch.setattr(vdb, "current_app", DummyApp)

    fake_vectordb = MagicMock()
    fake_chain = MagicMock()
    mock_chroma.return_value = fake_vectordb
    mock_llmchain.return_value = fake_chain

    service = VectorDBService.from_config()

    assert isinstance(service, VectorDBService)
    assert service.vectordb is fake_vectordb
    assert service.qa_chain is fake_chain
    mock_embed.assert_called_once_with(model_name="my-embed")
    mock_chroma.assert_called_once()
    mock_llmchain.assert_called_once()

def test_ask_success(fake_vectordb, fake_chain, fake_doc):
    fake_vectordb.similarity_search.return_value = [fake_doc]
    service = VectorDBService(fake_vectordb, fake_chain, "dbdir", "col", "embed")

    result = service.ask("What is this?")
    assert result["answer"] == "mocked answer"
    assert len(result["sources"]) == 1
    fake_chain.run.assert_called_once()

def test_ask_no_results(fake_vectordb, fake_chain):
    fake_vectordb.similarity_search.return_value = []
    service = VectorDBService(fake_vectordb, fake_chain, "dbdir", "col", "embed")

    result = service.ask("unknown?")
    assert "I do not know" in result["answer"]
    assert result["sources"] == []
    fake_chain.run.assert_not_called()

def test_ask_similarity_search_error(fake_vectordb, fake_chain):
    fake_vectordb.similarity_search.side_effect = Exception("db fail")
    service = VectorDBService(fake_vectordb, fake_chain, "dbdir", "col", "embed")

    with pytest.raises(Exception, match="db fail"):
        service.ask("boom")

def test_similarity_search_returns_results(fake_vectordb, fake_doc):
    fake_vectordb.similarity_search.return_value = [fake_doc]
    service = VectorDBService(fake_vectordb, MagicMock(), "dbdir", "col", "embed")

    results = service.similarity_search("query", k=2)
    assert results == [fake_doc]
    fake_vectordb.similarity_search.assert_called_once_with("query", k=2)

def test_get_document_count(fake_vectordb):
    fake_vectordb.get.return_value = {"documents": ["a", "b", "c"]}
    service = VectorDBService(fake_vectordb, MagicMock(), "dbdir", "col", "embed")

    count = service.get_document_count()
    assert count == 3
    fake_vectordb.get.assert_called_once()

def test_get_document_count_no_documents_key(fake_vectordb):
    fake_vectordb.get.return_value = {}
    service = VectorDBService(fake_vectordb, MagicMock(), "dbdir", "col", "embed")

    count = service.get_document_count()
    assert count == 0