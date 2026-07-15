# AI Engineering Learning Context

## Learning plan

- Reference: `AI_Application_Engineering_16_Week_Plan.pdf`
- Current phase: Week 0–1 — Production Python baseline
- Current status: completed, pending GitHub Actions verification
- Goal: establish reproducible Python development practices before using LLM APIs

## Completed

- Created the `ai-engineering-lab` project directory and initialized Git
- Created and activated a Python virtual environment
- Installed Pydantic, pytest, and Ruff
- Created the initial project structure
- Added `.gitignore`
- Created a full Pydantic `Document` model
- Added custom validators for meaningful text and valid HTTP/HTTPS source URLs
- Added unit tests, including whitespace trimming
- Ran pytest successfully: 6 tests passed
- Ran Ruff successfully: lint checks passed and all files are formatted
- Created the first Git commit:
  - `chore: set up Python project baseline`
- Added a GitHub Actions workflow:
  - `ci: add Python quality checks`
- Created and connected the GitHub repository:
  - `https://github.com/malhotrankit/ai-engineering-lab`
- Configured `main` to track `origin/main`

## Current model

```python
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator


class Document(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    content: str = Field(min_length=1)
    page_number: int = Field(ge=1)
    source_url: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("title", "content")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, value: str | None) -> str | None:
        if value is None:
            return value

        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("must be a valid HTTP or HTTPS URL")
        return value
```

```python
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator

class FinancialMetric(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    value: Decimal
    unit: str = Field(min_length=1, max_length=50)
    evidence: str = Field(min_length=1)

    @field_validator("name", "unit", "evidence")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned

class EarningsExtraction(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    reporting_period: str = Field(min_length=1, max_length=100)
    metrics: list[FinancialMetric] = Field(min_length=1)
    guidance: str | None = None
    risks: list[str] = Field(default_factory=list)

    @field_validator("company", "reporting_period")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned

    @field_validator("guidance")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    @field_validator("risks")
    @classmethod
    def clean_risks(cls, values: list[str]) -> list[str]:
        return [risk.strip() for risk in values if risk.strip()]
```


