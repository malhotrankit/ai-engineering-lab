"""Unit tests for the RAG pipeline module."""

from ai_engineering_lab.rag_pipeline import split_document, build_augmented_prompt


def test_split_document_empty():
    assert split_document("") == []
    assert split_document("   ") == []


def test_split_document_chunking():
    text = "Paragraph 1: Policy details.\n\nParagraph 2: Vehicle rules.\n\nParagraph 3: Safety guideline."
    chunks = split_document(text, chunk_size=40)
    assert len(chunks) >= 2
    assert "Paragraph 1: Policy details." in chunks[0]


def test_build_augmented_prompt():
    chunks = ["Smoking is not permitted in company vehicles."]
    query = "Can I smoke in company vehicles?"
    prompt = build_augmented_prompt(chunks, query)

    assert "System: Use ONLY the provided document context" in prompt
    assert "Smoking is not permitted in company vehicles." in prompt
    assert "User Question: Can I smoke in company vehicles?" in prompt
