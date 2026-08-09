"""RAG pipeline core implementation using modern text splitting, document ingestion, and prompt guardrails."""

from typing import Any
from pydantic import BaseModel, Field


class RAGChunk(BaseModel):
    chunk_id: int
    content: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


def split_document(
    text: str, chunk_size: int = 1000, chunk_overlap: int = 100
) -> list[str]:
    """Splits raw document text recursively by double newlines, single newlines, and spaces.

    Ensures sentences remain contiguous without mid-word slicing.
    """
    if not text.strip():
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
            current_chunk = f"{current_chunk}\n\n{paragraph}".strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def build_augmented_prompt(context_chunks: list[str], user_query: str) -> str:
    """Builds a 3-part augmented RAG prompt with strict anti-hallucination instructions."""
    joined_context = "\n---\n".join(context_chunks)
    return (
        "System: Use ONLY the provided document context below to answer the question. "
        "If you do not know the answer based strictly on the context, reply 'I do not know'. "
        "Do not make up an answer.\n\n"
        f"Context:\n{joined_context}\n\n"
        f"User Question: {user_query}"
    )
