# AI Engineering Lab: Financial Data & Earnings Call Extractor

An end-to-end production AI system that ingests corporate earnings reports and SEC filings, performs RAG document retrieval, enforces structured Pydantic schema validation, and runs deterministic evidence grounding verification.

---

## 🎯 Architecture Overview

```
[SEC / Earnings PDF] ➔ [RAG Text Splitting] ➔ [Vector Retrieval] ➔ [Gemini / LLM] ➔ [Pydantic Validation] ➔ [Deterministic Grounding Check]
```

### Core Features:
- **Pydantic Schemas (`earnings_models.py`):** Strictly enforces numerical precision using `Decimal`, custom validators, and whitespace stripping.
- **RAG Pipeline (`rag_pipeline.py`):** Custom recursive paragraph splitter + 3-part augmented prompts with anti-hallucination system guardrails.
- **Structured LLM Generation (`live_extractor.py`):** Native API integration forcing LLMs to return strict JSON matching `EarningsExtraction`.
- **Deterministic Evidence Verification:** Post-API grounding checks verifying that extracted quotes exist verbatim in raw source documents to catch structured hallucinations.
- **Study & Interview Repository (`coursera_notes/`):** Complete course progress tracker, master technical study notes, and high-yield system design Q&A bank for AI Engineer roles.

---

## 📂 Project Structure

```
ai-engineering-lab/
├── coursera_notes/                # Master study notes, cheat sheets & interview bank
│   ├── progress.md                # Live curriculum & deadline tracker
│   ├── notes.md                   # 16-section master technical reference
│   ├── interview_questions.md     # System design Q&A bank
│   └── lab_guidelines.md          # Master operating framework
├── src/ai_engineering_lab/        # Core Python source code
│   ├── earnings_models.py         # Pydantic schemas (FinancialMetric, EarningsExtraction)
│   ├── rag_pipeline.py            # RAG text splitters & augmented prompt builder
│   ├── live_extractor.py          # Gemini API driver with structured outputs
│   └── fake_extractor.py          # Grounding verification testing drivers
├── tests/                         # Pytest unit testing suite
├── docs/                          # Architecture context & session logs
├── .env                           # API environment configuration (git-ignored)
└── requirements.txt               # Python package dependencies
```

---

## 🚀 Quickstart & Testing

### 1. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Test Suite & Linting
```bash
PYTHONPATH=src pytest
ruff check .
```

### 3. Run Live Gemini Extraction Test
Ensure your `GEMINI_API_KEY` is set in `.env`, then run:
```bash
PYTHONPATH=src python run_live_test.py
```
