import fitz
import pytest
from unittest.mock import patch, MagicMock

from langchain_core.documents import Document

from Supernova_Call_for_Code.services import build_chroma_db

@pytest.fixture
def sample_pdf(tmp_path):
    """Create a temporary PDF with two pages of text for testing."""
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    for i in range(2):
        page = doc.new_page()
        page.insert_text((72, 72), f"Heading Page {i+1}\nThis is some text content.")
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path

@pytest.fixture
def sample_pages():
    """Mocked page text returned from extract_text_from_pdf."""
    return [
        (1, "Heading 1\nSome body text here."),
        (2, "Heading 2\nMore body text here."),
    ]

def test_extract_text_from_pdf_reads_pages(sample_pdf):
    pages = build_chroma_db.extract_text_from_pdf(str(sample_pdf))
    assert len(pages) == 2
    assert isinstance(pages[0][0], int)  
    assert isinstance(pages[0][1], str)  
    assert "Heading Page 1" in pages[0][1]

def test_extract_text_from_pdf_skips_empty_pages(tmp_path):
    pdf_path = tmp_path / "empty.pdf"
    doc = fitz.open()
    doc.new_page()  
    doc.save(str(pdf_path))
    doc.close()

    pages = build_chroma_db.extract_text_from_pdf(str(pdf_path))
    assert pages == []

def test_extract_text_from_pdf_invalid_path_raises():
    with pytest.raises(Exception):
        build_chroma_db.extract_text_from_pdf("non_existent.pdf")

def test_split_text_to_documents_creates_documents(sample_pages):
    docs = build_chroma_db.split_text_to_documents(sample_pages)
    assert all(isinstance(doc, Document) for doc in docs)
    assert docs[0].metadata["page"] == 1
    assert "Heading 1" in docs[0].page_content

def test_split_text_to_documents_handles_empty_text():
    pages = [(1, ""), (2, "  \n  ")]
    docs = build_chroma_db.split_text_to_documents(pages)
    assert all("Page" in d.metadata["heading"] for d in docs)

@patch.object(build_chroma_db, "HuggingFaceEmbeddings")
@patch.object(build_chroma_db, "Chroma")
def test_build_chroma_from_pdf_success(mock_chroma, mock_embeddings, sample_pdf, tmp_path):
    build_chroma_db.build_chroma_from_pdf(
        str(sample_pdf),
        str(tmp_path),
        "fake-model",
        "test-collection"
    )
    mock_embeddings.assert_called_once_with(model_name="fake-model")
    mock_chroma.from_documents.assert_called_once()
    _, kwargs = mock_chroma.from_documents.call_args
    assert kwargs["persist_directory"] == str(tmp_path)
    assert kwargs["collection_name"] == "test-collection"

@patch.object(build_chroma_db, "HuggingFaceEmbeddings")
@patch.object(build_chroma_db, "Chroma")
def test_build_chroma_from_pdf_chroma_failure(mock_chroma, mock_embeddings, sample_pdf, tmp_path):
    mock_embeddings.return_value = MagicMock()

    mock_chroma.from_documents.side_effect = Exception("db fail")

    with pytest.raises(Exception, match="db fail"):
        build_chroma_db.build_chroma_from_pdf(
            str(sample_pdf), str(tmp_path), "fake-model", "default"
        )

@patch.object(build_chroma_db, "HuggingFaceEmbeddings", side_effect=Exception("model fail"))
def test_build_chroma_from_pdf_embedding_failure(mock_embed, sample_pdf, tmp_path):
    with pytest.raises(Exception, match="model fail"):
        build_chroma_db.build_chroma_from_pdf(
            str(sample_pdf), str(tmp_path), "bad-model", "default"
        )