import pytest
from unittest.mock import patch, MagicMock

from Supernova_Call_for_Code.services import chroma_status

@patch.object(chroma_status, "HuggingFaceEmbeddings")
@patch.object(chroma_status, "Chroma")
def test_print_chroma_status_with_documents(mock_chroma, mock_embeddings, capsys):
    mock_embeddings.return_value = MagicMock()

    mock_vectordb = MagicMock()
    mock_vectordb.get.return_value = {
        "ids": ["doc1"],
        "documents": ["This is a sample document text."],
        "metadatas": [{"page": 1, "heading": "Intro"}],
    }
    mock_chroma.return_value = mock_vectordb

    chroma_status.print_chroma_status()

    captured = capsys.readouterr()
    assert "ChromaDB Status" in captured.out
    assert "Total Chunks      : 1" in captured.out
    assert "Sample Document" in captured.out
    assert "This is a sample document text." in captured.out

@patch.object(chroma_status, "HuggingFaceEmbeddings")
@patch.object(chroma_status, "Chroma")
def test_print_chroma_status_with_zero_docs(mock_chroma, mock_embeddings, capsys):
    mock_embeddings.return_value = MagicMock()

    mock_vectordb = MagicMock()
    mock_vectordb.get.return_value = {"ids": [], "documents": [], "metadatas": []}
    mock_chroma.return_value = mock_vectordb

    chroma_status.print_chroma_status()

    captured = capsys.readouterr()
    assert "Total Chunks      : 0" in captured.out
    assert "Sample Document" not in captured.out

@patch.object(chroma_status, "HuggingFaceEmbeddings", side_effect=Exception("embedding fail"))
def test_print_chroma_status_embedding_failure(mock_embed):
    with pytest.raises(Exception, match="embedding fail"):
        chroma_status.print_chroma_status()

@patch.object(chroma_status, "HuggingFaceEmbeddings")
@patch.object(chroma_status, "Chroma", side_effect=Exception("chroma init fail"))
def test_print_chroma_status_chroma_failure(mock_chroma, mock_embed):
    mock_embed.return_value = MagicMock()
    with pytest.raises(Exception, match="chroma init fail"):
        chroma_status.print_chroma_status()