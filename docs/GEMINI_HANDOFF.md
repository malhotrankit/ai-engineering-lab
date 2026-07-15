Create `docs/GEMINI_HANDOFF.md`, then paste the following Markdown exactly. It gives Gemini the roadmap, project state, learning style, key files, completed work, and immediate next task. Your existing `docs/session_context.md` is incomplete, so this handoff should be the primary starting document.[1]

````markdown
# Gemini Handoff — AI Application Engineering Learning Plan

**Purpose:** Give Gemini complete context to continue this structured, project-first AI engineering learning plan without repeating completed work or losing the learner’s preferred teaching style.

**Last updated:** 2026-07-15

---

## Instructions for Gemini

Act as a patient, technically rigorous mentor for a backend engineer transitioning into AI application engineering.

- Explain concepts incrementally and in plain language. Do not assume Python or AI concepts are understood merely because code was copied.
- Before each session, read:
  1. `docs/GEMINI_HANDOFF.md` — this complete handoff
  2. `docs/session_context.md` — concise cross-session state, but note that it is currently outdated/incomplete
  3. `learning_log.md` — concepts and learner explanations already covered
  4. Relevant source and test files before suggesting code changes
- At the end of **every** session, provide an exact Markdown block to append to `docs/session_context.md`. Include date/session number, completed tasks, commands/outcomes, concepts/questions, changed files, and exact next step.
- Ask the learner to run tests, lint, formatting, Git status, commit coherent milestones, and push to GitHub.
- Never ask for API tokens, passwords, or secrets. Later, use `.env` and `.gitignore` for credentials.
- Teach direct Python/API calls before LangChain or LangGraph.
- Do not rush to agents or multi-agent systems. Prefer deterministic workflows, explicit validation, security boundaries, and human approval for sensitive operations.
- Do not repeat the Week 0–1 setup lessons unless the learner asks.

---

## Learner Profile

The learner is a backend-oriented engineer with prior experience in APIs, Docker, databases, monitoring, and Java/Spring-style engineering.

The transition goal is to become credible for:

- AI Application Engineer
- GenAI Backend Engineer
- AI Automation Engineer
- Backend Engineer with an AI/LLM focus

The plan is production-oriented. It prioritizes two strong projects rather than many shallow demos:

1. **Filing RAG Service** — FastAPI, document ingestion, Postgres/pgvector, hybrid retrieval, citations/refusal, Docker, tests, evaluation, and observability.
2. **Financial Research Workflow** — typed safe tools, deterministic calculations, LangGraph later, MCP later, permissions/audit trail, human approval, and evaluation.

The current first project component is named **`earnings_extractor`**. It will extract structured financial claims from text before any RAG work begins.

---

## Full 16-Week Roadmap

### Weeks 0–1 — Production Python Baseline

**Goal:** Establish reproducible Python development practices before using LLM APIs.

**Learning:** Python environments, typing, Pydantic, pytest, Ruff, Git, GitHub Actions, and basic SQL/Docker refresh.

**Build:** `ai-engineering-lab` repository with typed models, unit tests, linting/formatting, CI, learning log, and session handoff document.

**Status:** Completed locally. GitHub CI was configured and the repository was pushed. Confirm the GitHub Actions run is green if that has not been checked.

### Weeks 2–3 — LLM Foundations and Structured Outputs

**IBM:** Course 1 — *Develop Generative AI Applications: Get Started*.

**Learning sources:** Full Stack LLM Bootcamp; Anthropic prompt-engineering tutorial; OpenAI structured outputs and function-calling documentation.

**Build:** `earnings_extractor` with direct API calls only—no LangChain initially—Pydantic schemas, structured output, retries/errors, and approximately 20 test cases including incomplete, contradictory, irrelevant, and prompt-injection-like inputs.

**Current position:** Early in this phase. The schema and unit-test foundation are complete. Next, build a fake extractor that simulates valid, malformed, and unsupported LLM outputs before using a live model API.

**Mental model:** An LLM is an untrusted producer of proposed data. A Pydantic schema validates structure and basic rules, but does not prove factual grounding. Deterministic code handles validation and calculations.

### Weeks 4–6 — RAG From First Principles

**IBM:** Courses 2–4 — introductory RAG, vector databases, advanced RAG/retrievers.

**Build:** `filing-rag-service` using public annual reports/transcripts. Preserve document/page/section/chunk metadata; implement baseline chunking; use Postgres + pgvector; compare keyword and dense retrieval; add hybrid ranking and citations/refusal; create at least 35 question/evidence cases.

**Key concepts:** Parsing → chunking/metadata → embeddings/index → retrieve → rerank → evidence-grounded prompt → answer/citations. Measure retrieval independently from generation.

### Weeks 7–8 — Productionize RAG

**IBM:** Course 5 selectively for multimodal/OCR/transcription awareness.

**Build:** FastAPI ingest/status/query/health endpoints; async ingestion; Docker Compose with FastAPI, Postgres/pgvector, Redis; structured logs; timeouts/retries; auth stub; unit/integration tests; GitHub Actions.

### Weeks 9–10 — Tools and Safe Workflows

**IBM:** Course 6 — *Fundamentals of Building AI Agents*.

**Build:** `financial-research-workflow` with read-only document search, deterministic ratio calculator, metrics lookup, typed tool schemas, allow-lists, timeouts, retries, tool-call budget, and audit logs.

**Key concept:** The model can propose a tool call; application code independently validates authorization and arguments, executes the tool, and logs results.

### Weeks 11–12 — LangGraph and MCP

**IBM:** Courses 7–9.

**Build:** First a direct Python workflow, then LangGraph implementation with explicit states: interpret query, retrieve, calculate, draft, validate evidence, request human approval, finish. Add a read-only FastMCP server with explicit access rules.

**Key concept:** A workflow is code controlling known steps. An agent is a model dynamically choosing constrained steps. MCP is an integration protocol, not a security boundary itself.

### Weeks 13–14 — Evaluation, Security, Observability

**IBM:** Start Course 10 capstone, adapted to the existing financial-document projects.

**Build:** 50–70 case versioned evaluation dataset. Measure retrieval/evidence hit rate, citation correctness, refusal correctness, schema/tool success, latency, and cost. Add Langfuse traces, CI regression checks, and a threat model covering prompt injection, secrets, access control, unsafe tools, and data retention.

### Weeks 15–16 — Deployment and Interview Readiness

**Build:** Deploy a Dockerized service to AWS or GCP. Keep reproducible Docker Compose setup. Publish strong READMEs, architecture diagrams, evaluation results, threat model, API examples, cost/latency assumptions, and a 5–7 minute walkthrough.

**Interview benchmark:** Explain RAG end to end, distinguish retrieval/generation/tool failures, explain RAG versus long context versus fine-tuning, design safe tools, explain agent control/approvals, demonstrate MCP boundaries, show evals/traces, and defend design decisions.

---

## Required Learning Sources

Use official or primary sources preferentially:

- IBM RAG and Agentic AI Professional Certificate: https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai
- Full Stack LLM Bootcamp: https://fullstackdeeplearning.com/llm-bootcamp/
- Anthropic interactive prompt tutorial: https://github.com/anthropics/prompt-eng-interactive-tutorial
- Anthropic courses: https://github.com/anthropics/courses
- OpenAI Structured Outputs: https://developers.openai.com/api/docs/guides/structured-outputs
- OpenAI Function Calling: https://developers.openai.com/api/docs/guides/function-calling
- OpenAI structured-output evaluation example: https://developers.openai.com/cookbook/examples/evaluation/use-cases/structured-outputs-evaluation
- FastAPI tutorial: https://fastapi.tiangolo.com/tutorial/
- FastAPI testing: https://fastapi.tiangolo.com/tutorial/testing/
- FastAPI Docker deployment: https://fastapi.tiangolo.com/deployment/docker/
- Hugging Face learning hub: https://huggingface.co/learn
- Hugging Face Agents Course: https://huggingface.co/agents-course
- pgvector: https://github.com/pgvector/pgvector
- Supabase pgvector: https://supabase.com/docs/guides/database/extensions/pgvector
- LangGraph Essentials: https://academy.langchain.com/courses/langgraph-essentials-python
- Introduction to LangGraph: https://academy.langchain.com/courses/intro-to-langgraph
- Model Context Protocol: https://modelcontextprotocol.io/docs/getting-started/intro
- Langfuse tracing docs: https://github.com/langfuse/langfuse-docs/blob/main/pages/docs/tracing.mdx
- Python documentation: https://docs.python.org/3/
- pytest documentation: https://docs.pytest.org/
- Pydantic documentation: https://docs.pydantic.dev/
- Docker documentation: https://docs.docker.com/
- GitHub Actions documentation: https://docs.github.com/actions

---

## Repository and Context Files

**Repository:** https://github.com/malhotrankit/ai-engineering-lab

Gemini must read these files before each session:

```text
docs/GEMINI_HANDOFF.md
docs/session_context.md
learning_log.md
AI_Application_Engineering_16_Week_Plan.pdf
```

Additional important files:

```text
src/ai_engineering_lab/models.py
tests/test_models.py
src/ai_engineering_lab/earnings_models.py
tests/test_earnings_models.py
.github/workflows/ci.yml
```

### Current Known Git State

- Branch: `main`, tracking `origin/main`
- Remote: `https://github.com/malhotrankit/ai-engineering-lab.git`
- Commits known to be pushed before earnings schema work:
  - `42f8e68 chore: set up Python project baseline`
  - `650d15f ci: add Python quality checks`
- The learner was instructed to commit the earnings-schema files with:

```text
feat: add earnings extraction schemas
```

Gemini should run `git status` and `git log --oneline -5` before assuming whether that commit occurred.

### Existing Context-File Issue

`docs/session_context.md` is outdated/incomplete. It records the Week 0–1 foundation but ends the `Current model` code block inline as:

```text
return value```
```

Gemini should fix the closing code fence and update it with later work before relying on it as the sole source of truth.

---

## Completed Implementation

### General Document Model

**File:** `src/ai_engineering_lab/models.py`

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

Validated behavior:

- `title` and `content` cannot be blank or whitespace-only, and are trimmed
- `title` has a maximum length of 300
- `page_number` must be at least 1
- `source_url` can be omitted; if supplied, it must be HTTP/HTTPS with a hostname
- Each `Document` receives its own metadata dictionary

### Earnings Extraction Schema

**File:** `src/ai_engineering_lab/earnings_models.py`

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

Validated behavior:

- Every numeric metric includes name, `Decimal` value, unit, and exact evidence text
- An extraction requires company, reporting period, and at least one metric
- Guidance is optional; blank guidance normalizes to `None`
- Risks normalize by trimming entries and removing blank entries
- `metrics` is a list because one passage may contain several metrics

### Tests and Quality Status

- `tests/test_models.py` tests the general `Document` model
- `tests/test_earnings_models.py` tests valid metrics/extractions, invalid required data, nested Pydantic conversion, whitespace normalization, optional guidance, and risk cleanup
- Last verified result: **12 tests passed**
- Last verified local checks: Ruff lint passed; formatting reported **5 files already formatted**
- Ignore occasional assistant-sandbox cache write warnings. The learner’s local Terminal checks pass normally

---

## Concepts Already Understood

- A class is a blueprint; an object or instance is concrete data created from it
- `BaseModel` is Pydantic’s model base class, distinct from standard `@dataclass`
- Virtual environments isolate dependencies and make projects reproducible
- Parsing converts input into usable Python data; validation checks it meets application rules
- Pydantic is useful at boundaries receiving untrusted data: users, APIs, PDF parsers, databases, and future LLM responses
- Unit tests test one component in isolation; integration tests test components working together
- `Field(min_length=1)` is a structural constraint; custom validators can strip/normalize text and enforce business rules, such as rejecting whitespace-only input
- `source_url` is optional because sources can be internal or user-uploaded
- `default_factory=dict` creates a separate dictionary per model instance
- `metrics` is a list; access the first metric with `extraction.metrics[0].name`, not `extraction.metrics.name`
- `Decimal` is preferred over `float` for financial values due to decimal precision
- Evidence preserves the source support for a financial claim; schema validity alone does not verify factual grounding

---

## Immediate Next Session

**Do not call a paid LLM API yet.**

### Goal

Build a fake extractor to teach the distinction among:

1. Valid and grounded-looking structured output
2. Structurally malformed or incomplete output that Pydantic rejects
3. Structurally valid output whose evidence is unsupported by the input text

### Suggested Implementation Path

1. Verify and commit/push earnings-schema files if needed:

```bash
PYTHONPATH=src pytest -q
ruff check .
ruff format --check .
git status
git add src/ai_engineering_lab/earnings_models.py tests/test_earnings_models.py
git commit -m "feat: add earnings extraction schemas"
git push
```

2. Create:

```text
src/ai_engineering_lab/fake_extractor.py
```

It should take a scenario or source text and return ordinary Python dictionaries representing fake LLM JSON. Do not use an LLM SDK.

3. Create:

```text
tests/test_fake_extractor.py
```

Test that:

- Valid output is accepted by `EarningsExtraction.model_validate(...)`
- Missing fields or malformed values cause `ValidationError`
- A fabricated but structurally valid metric can pass Pydantic, proving schema validation does not establish grounding

4. Teach this distinction:

```text
Schema validation:
Does this data match the required structure and rules?

Grounding validation:
Is this claim supported by the source text?
```

5. Only after the fake extractor, create a simple deterministic evidence-support baseline. For example, require the evidence string to be a substring of the source text.

Be clear: this is a baseline, not complete semantic fact verification.

6. Update `learning_log.md` and `docs/session_context.md`, then commit and push the milestone.

### Questions to Ask Afterwards

- Why can Pydantic accept a fabricated claim?
- What does a schema prove, and what does it not prove?
- Why is an evidence quote useful but not automatically enough?
- Why must financial calculations remain deterministic Python code rather than LLM arithmetic?

---

## Required End-of-Session Format

```markdown
## Session <N> — Date: YYYY-MM-DD

### Completed

- ...

### Commands and outcomes

- `...` → ...

### Concepts understood / questions remaining

- ...

### Files created or changed

- ...

### Exact next step

- ...
```
````

Sources
