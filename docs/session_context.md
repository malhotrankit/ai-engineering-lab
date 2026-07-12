# AI Engineering Learning Context

## Learning plan

- Reference: `AI_Application_Engineering_16_Week_Plan.pdf`
- Current phase: Week 0–1 — Production Python baseline
- Goal: establish reproducible Python development practices before using LLM APIs

## Completed

- Created the `ai-engineering-lab` project directory and initialized Git
- Created and activated a Python virtual environment
- Installed Pydantic, pytest, and Ruff
- Created the initial project structure
- Added `.gitignore`
- Discussed Pydantic `BaseModel` versus a standard Python dataclass
- Simplified the first `Document` model to `title`, `content`, and `page_number`

## Current model

```python
from pydantic import BaseModel, Field


class Document(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    page_number: int = Field(ge=1)

