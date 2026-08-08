# Week 0–1 — Production Python Baseline

## Why use a virtual environment?

A virtual environment creates an isolated set of Python packages for one project.
It prevents package versions from different projects from conflicting with each
other. It also makes the project reproducible because the needed dependencies
can be installed separately for this project.

## Parsing versus validation

Parsing means reading input and converting it into a usable Python value or
object. For example, JSON from an API can be parsed into Python data.

Validation checks whether that data follows the application's rules. For the
Document model, validation ensures that title and content are meaningful, the
page number is at least 1, and a supplied source URL uses HTTP or HTTPS.

## Why is a Pydantic model useful in an AI application?

AI applications receive data from sources that cannot be fully trusted, such as
user requests, PDF parsers, APIs, databases, and LLM responses. A Pydantic model
defines the expected structure and validates the data before the rest of the
application uses it. This catches invalid or incomplete data early.

## Unit test versus integration test

A unit test checks one small part of the system in isolation. For example, a
unit test can check that the Document model rejects a page number of 0.

An integration test checks whether multiple components work together. Later, an
integration test could check whether a FastAPI endpoint receives a document,
validates it with Pydantic, and stores it in a database.

## One failure case my Document model prevents

The Document model prevents invalid document data such as a whitespace-only
title, an empty content field, a page number of 0, or a malformed source URL.
Rejecting these values early stops bad data from entering later RAG or AI
processing steps.


## Session 2 — Date: 2026-07-12

### Completed

- Reviewed the full Pydantic `Document` model
- Understood its fields: title, content, page number, optional source URL, and metadata
- Understood custom validators for whitespace-only text and HTTP/HTTPS URLs
- Added `test_document_trims_title_and_content`
- Ran the test suite successfully: 6 tests passed
- Checked Ruff formatting successfully

### Concepts understood

- A URL is optional because documents can originate from local uploads or internal systems
- `default_factory=dict` creates a separate empty metadata dictionary for every Document object
- `Field(min_length=1)` checks string length; the custom validator trims whitespace and rejects text that has no meaningful characters

### Files changed

- `tests/test_models.py`
- `learning_log.md`
- `docs/session_context.md`

### Next step

Set up Git configuration if needed, create the first Git commit, then add GitHub Actions so tests and Ruff checks run automatically on every push.


## Session 2 Answers to Conceptual Questions

1. **Why must every extracted metric include an `evidence` field?**
The evidence field provides the exact source text from which the data was fetched, allowing us to verify the LLM's claim and ensure it isn't hallucinated.

2. **Why does a metric need both `value` and `unit`?**
A raw number isn't enough; the unit specifies whether the value is in millions, billions, percentages, or another currency, giving it necessary context.

3. **Why is `metrics` a list rather than a single `FinancialMetric`?**
Earnings reports contain multiple financial metrics (like Revenue, EPS, Gross Margin), not just one, so we need a list to capture all of them.

4. **Why may `guidance` be `None`, while `company` may not?**
Not all companies provide future guidance in every report, making it optional, whereas the company name is a fundamental requirement for the extraction to be valid.

## Session 4 — Date: 2026-07-17

### Completed
- Configured `.env` file securely and installed `google-genai` and `python-dotenv`.
- Built `live_extractor.py` to call the Gemini API using the new structured outputs feature.
- Passed our Pydantic `EarningsExtraction` schema directly into the `response_schema` config to force the LLM to return perfectly structured data.
- Tested the live API successfully against a sample Apple earnings report.

### Concepts understood
- **API Security:** API keys must be kept in `.env` files and ignored by Git to prevent massive accidental billing charges from leaked credentials.
- **Structured Outputs via API:** We can force modern LLMs to conform to Pydantic schemas natively through the API configuration, ensuring we get a clean object without manual string parsing.
- **The Grounding Reality:** Even with the live API enforcing the schema perfectly, the LLM can still hallucinate numbers that fit the structure. The deterministic `verify_evidence` function we wrote earlier remains mandatory to prove factual grounding!
- **Hallucinated Evidence:** The LLM can easily hallucinate the `evidence` string itself. Pydantic will accept the hallucinated string because it's technically a valid string. Our deterministic `verify_evidence` function is the only way to prove the LLM's quoted evidence actually exists in the original raw text.



## Session 3 — Date: 2026-07-16

### Completed

- Implemented a clean, simple, keyword-based `extract_earnings_fake` and `verify_evidence` in [fake_extractor.py](file:///Users/ankitmalhotra/Developer/ai-engineering-lab/src/ai_engineering_lab/fake_extractor.py).
- Created unit tests in [test_fake_extractor.py](file:///Users/ankitmalhotra/Developer/ai-engineering-lab/tests/test_fake_extractor.py) to cover:
  - Valid structured outputs that pass Pydantic validation and grounding checks.
  - Malformed structured outputs that fail Pydantic validation.
  - Ungrounded structured outputs that pass Pydantic validation but fail grounding checks.
- Formatted and linted files with Ruff.
- Ran test suite successfully (15 tests passed).

### Session 3 Answers to Conceptual Questions

1. **Why can Pydantic accept a fabricated claim?**
   Pydantic validates the data structure, field types, and constraints (e.g. string length, non-empty fields). It does not check if the content of the data matches the reality of the source text.

2. **What does a schema prove, and what does it not prove?**
   A schema proves structural conformity and type correctness (e.g., this is a list of financial metrics with required fields). It does not prove that the data is true, grounded in the source document, or mathematically correct.

3. **Why is an evidence quote useful but not automatically enough?**
   An evidence quote allows verification (so humans or automated systems can verify the claim against the source document). It is not enough on its own because the model might have fabricated the quote itself (hallucination) or selected a quote that doesn't actually support the extracted value.


## Session 5 — Date: 2026-07-27

### Completed
- Completed **Course 2 (RAG Applications)** of the Coursera AI Engineering Certificate.
- Mastered full RAG pipeline implementations in both **LangChain** (`RetrievalQA`, LCEL, `stuff`) and **LlamaIndex** (`SimpleDirectoryReader`, `SentenceSplitter`, `VectorStoreIndex`, `QueryEngine`, `ChatEngine`).
- Generated distilled, PDF cheat sheets for all Course 2 labs ([lab_2_cheatsheet.pdf](file:///Users/ankitmalhotra/Developer/ai-engineering-lab/coursera_notes/lab_2_cheatsheet.pdf), [lab_course2_mod1_cheatsheet.pdf](file:///Users/ankitmalhotra/Developer/ai-engineering-lab/coursera_notes/lab_course2_mod1_cheatsheet.pdf), [lab_course2_mod3_cheatsheet.pdf](file:///Users/ankitmalhotra/Developer/ai-engineering-lab/coursera_notes/lab_course2_mod3_cheatsheet.pdf)).
- Generated annotated reference scripts for RAG and LlamaIndex ([rag_lab_explained.py](file:///Users/ankitmalhotra/Developer/ai-engineering-lab/coursera_notes/rag_lab_explained.py), [icebreaker_bot_explained.py](file:///Users/ankitmalhotra/Developer/ai-engineering-lab/coursera_notes/icebreaker_bot_explained.py)).
- Historical decision (superseded on 8 August): complete courses first, then use project sprints. The current rule pairs one course topic with one matching portfolio proof each week.

### Key Concepts Mastered
- **LangChain vs. LlamaIndex Design Philosophies:** LangChain is granular & modular; LlamaIndex is integrated & batteries-included.
- **`query_engine.query()` vs. `chat_engine.chat()`:** `.query()` is stateless (single-shot lookups); `.chat()` is stateful (multi-turn memory).
- **LlamaIndex Relationships:** Graph pointers stored directly in `TextNode.relationships`, enabling 1-database parent-child retrieval.

## Session 7 — Date: 2026-08-07

### Completed
- **Course 2 Revision Labs Completed:** Successfully completed the LangChain LCEL Challenge (`langchain_scratch_challenge.py`) and LlamaIndex Engine Challenge (`llamaindex_scratch_challenge.py`). Built a dual-framework reference (`dual_framework_rag_lab.py`).
- **Agent Collaboration Safety:** Identified root cause of AI code overwriting. Established strict rules: AI must run `view_file` before edits, and must use `replace_file_content` for surgical updates rather than overwriting entire files (documented in `rca_code_loss_fix.md`).
- **Security Audit & Hardening:** Stripped all hardcoded API keys (`AIzaSy...`, `sk-or-v1...`) from scripts. Implemented a robust `sys.exit()` guard ensuring keys are only loaded from the `.env` file.
- **Git Repository Organization:** Secured `.gitignore` against accidental key leaks and excluded large binary vector DB folders (`chroma_db`, `llama_storage`). Created an `.env.example` file for safe collaboration.
- **Master Notes Compiled:** Finalized formatting of `course_2_master_revision.md` and compiled the Executive Edition PDF.
- **Git Push:** Successfully committed and pushed 31 files representing all of the Course 1 and Course 2 materials to the remote repository.

### Next Step
- Historical next step (superseded on 8 August): start Course 6. The learner later clarified that Course 6 had not started; the current focus is Course 3 only.

## Session 8 - Date: 2026-08-08

### Completed

- Audited the entire repository, progress records, revision PDFs, project implementation, dependency surface, and original 16-week plan against current AI application engineering expectations.
- Initially recorded Course 6 as started; this was corrected later the same day. Courses 1-2 are complete, while Courses 3, 4, and 6 have not started.
- Reordered the remaining plan around the missing retrieval foundation before agent work.
- Replaced the “courses first, project later” rule with one weekly course topic plus one matching portfolio proof to reduce context switching while retaining hands-on progress.
- Corrected master notes that overstated determinism, grounding, production adoption percentages, caching latency/savings, self-consistency, and framework capabilities.
- Reframed the repository and README honestly as a learning/portfolio prototype.
- Attempted to rerun the project tests. The checkout had no `.venv/bin/pytest`, and the bundled document runtime also lacked pytest; restoring and validating the development environment is therefore the first Week 4 engineering task.

### Industry-aligned decisions

- Evaluation begins with the first retrieval baseline, not at the end of the plan.
- Retrieval and generation will be measured separately.
- FastAPI/reliability/observability precede complex agents.
- Direct Python workflows precede LangGraph; agents are added only when dynamic routing/state provides value.
- Tool authorization remains in application code, with explicit budgets and auditability.
- MCP work includes least privilege and denied-case security tests.
- Deployment evidence includes threat modeling, current NIST/OWASP guidance, OpenTelemetry-compatible traces, and EU AI Act awareness.

### Exact next step

Superseded later on 8 August: the learner clarified that Course 6 had not started and requested fully sequential work blocks.

## Session 9 - Date: 2026-08-08

### Progress correction and working preference

- Confirmed that Course 6 has not started; the learner was only about to begin it.
- Confirmed that course study and project implementation must never be scheduled simultaneously.
- Adopted the exclusive block sequence: complete one course, pause Coursera, complete its project sprint, then begin the next course.
- Set the current single goal to Course 3 only.
- Set the existing financial earnings project to resume immediately after Course 3 in a dedicated retrieval sprint.
- Added root-level project instructions so future Codex tasks read and maintain the same progress files automatically after meaningful milestones.

### Exact next step

Complete Course 3. Do not work on the project or Course 6 during this block.

## Session 10 - Date: 2026-08-08

### Course 3 started

- Started Course 3, Vector Databases for RAG, as the sole active learning block.
- Kept the financial-project retrieval sprint and all other courses paused in accordance with the sequential-work rule.
- Set the first focus to the module on vector databases and Chroma architecture.

### Exact next step

Begin the Course 3 module on vector databases and Chroma architecture.

## Curriculum reference - Date: 2026-08-08

- Reviewed the learner-provided Coursera certificate curriculum covering all ten courses.
- Recorded exact course titles, durations, and advertised learning outcomes in `coursera_notes/certificate_curriculum.md`.
- Confirmed Course 3 is a nine-hour course covering vector/traditional database differences, ChromaDB operations, similarity search, recommendation systems, and internal RAG mechanisms.
- Confirmed Course 6 is an eleven-hour course and remains not started.
- Preserved the newer shared-workspace state: Course 3 is in progress as the sole active block.

## Credential guardrails - Date: 2026-08-08

- Confirmed local `.env` files are ignored and not tracked without reading or displaying their contents.
- Added persistent API-key safety rules for every future task and generated practice lab.
- Added a value-redacting repository secret scanner covering common provider keys, GitHub/AWS credentials, private keys, sensitive filenames, and generic hardcoded secret assignments.
- Activated pre-commit and pre-push hooks and added the same scanner to GitHub Actions.
- Added `SECURITY.md` with safe environment-variable usage and an immediate revoke/rotate procedure for suspected exposure.
- Verified the current repository passes the scan and the scanner's detection self-test.
