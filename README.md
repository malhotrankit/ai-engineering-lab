# AI Engineering Lab: Financial Data & Earnings Call Extractor

A learning and portfolio project for building a reliable financial-document AI service. The current implementation covers typed extraction, direct Gemini structured output, basic chunking/prompt utilities, and unit-tested evidence substring checks. Real vector retrieval, evaluation, FastAPI, observability, agent workflows, MCP, and deployment are planned and should not be inferred from the current code.

## Current status - Week 4 of 16

- Completed: Pydantic schemas, fake/live structured extraction, basic grounding checks, CI configuration, and Course 1-2 RAG practice labs.
- Current learning block: Course 3 only. Course 6 has not started.
- Next project block: after Course 3, pause Coursera and add real ingestion, embeddings, retrieval, and citations under `src/`.
- Roadmap: see `docs/AI_Application_Engineering_16_Week_Plan.md` and `docs/session_context.md`.

---

## Target architecture

```
[SEC / Earnings PDF] ➔ [RAG Text Splitting] ➔ [Vector Retrieval] ➔ [Gemini / LLM] ➔ [Pydantic Validation] ➔ [Deterministic Grounding Check]
```

### Implemented features
- **Pydantic Schemas (`earnings_models.py`):** Strictly enforces numerical precision using `Decimal`, custom validators, and whitespace stripping.
- **RAG utilities (`rag_pipeline.py`):** Basic paragraph grouping and augmented prompt construction. This is not yet a retrieval pipeline.
- **Structured LLM Generation (`live_extractor.py`):** Native API integration forcing LLMs to return strict JSON matching `EarningsExtraction`.
- **Evidence Verification:** Checks whether extracted quotes occur verbatim in the source. It catches some fabricated evidence but does not prove that a quote supports the claimed value, unit, period, or company.
- **Study & Interview Repository (`coursera_notes/`):** Course progress, corrected technical notes, and a job-focused system design Q&A bank.

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
