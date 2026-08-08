# AI Engineering Session Context

Last reconciled: 8 August 2026

## Current source of truth

- Calendar: Week 4 of the 16-week plan (7-13 August 2026).
- Coursera: Courses 1 and 2 complete. Course 3 is in progress. Courses 4 and 6 have not started.
- Strategy: fully sequential focus blocks. Complete Course 3 only, then pause Coursera for a dedicated retrieval sprint in the existing project.
- Portfolio status: learning prototype, not production-ready.
- Exact current goal: complete Course 3. No project work or other course work during this block.
- Exact next action: begin the Course 3 module on vector databases and Chroma architecture.
- Exact project return point: immediately after Course 3, run Project Sprint A for environment repair, chunking, embeddings, vector retrieval, and the first retrieval evaluation set.

## What is actually implemented

### Main package

- Pydantic `Document`, `FinancialMetric`, and `EarningsExtraction` models.
- Validators for required text, URLs, optional guidance, and risk cleanup.
- Fake extraction scenarios for valid, malformed, and fabricated evidence.
- A substring-based `verify_evidence` check.
- Direct Gemini structured output using a Pydantic response schema.
- A basic paragraph splitter and augmented prompt builder.
- Unit tests for models, fake extraction, and current RAG utilities.
- Ruff/pytest CI configuration.

### Course/revision artifacts

- Courses 1 and 2 completed; Course 3 started on 8 August 2026.
- Learner-provided ten-course Coursera curriculum captured in `coursera_notes/certificate_curriculum.md` with exact titles, durations, and advertised learning outcomes.
- LangChain and LlamaIndex practice scripts and cheat sheets.
- Course 2 scratch challenges and dual-framework reference code.
- Course 6 has not started.

### Repository credential safety

- Real API keys remain in ignored local `.env` files; `.env` and `coursera_notes/.env` are not tracked.
- `scripts/check_secrets.py` scans tracked and unignored files without printing suspected values.
- Repository pre-commit and pre-push hooks run the scanner through `.githooks`.
- GitHub Actions runs the same scan before dependency installation, linting, and tests.
- `AGENTS.md` requires every future practice lab, commit, and push to use environment variables and pass the secret scan.

## What is not yet implemented

- No embedding model or vector index in the main package.
- No real query-time retrieval, hybrid search, reranking, or citation pipeline in `src/`.
- No versioned evaluation dataset or automated retrieval/generation metrics.
- No FastAPI service, background ingestion, Postgres/pgvector, or Redis integration.
- No model-provider abstraction, systematic timeouts/retries, or concurrency controls.
- No LangGraph state machine, production agent loop, or MCP server/client.
- No application traces/metrics, threat model, red-team suite, Docker release, or cloud deployment.

## Known limitations to fix first

1. `split_document` accepts `chunk_overlap` but does not use it, and a long paragraph can exceed `chunk_size`.
2. `verify_evidence` proves only verbatim presence. It can still accept a quote that does not support the claimed value, unit, period, or company.
3. The direct model call is coupled to Gemini and currently lacks explicit timeout/retry/error mapping.
4. Course RAG scripts demonstrate frameworks, but they do not make the main application a RAG system.
5. Setup and dependency claims must be revalidated from a clean environment before the README promises reproducibility. During the 8 August audit, `.venv/bin/pytest` was absent and the bundled document runtime did not include pytest, so the application suite could not be rerun in this session.

## Immediate sequence

### Current block - Course 3 only

- Complete Course 3 without simultaneous project or Course 6 work.
- Track module completion when the learner reports it.

### Next block - Project Sprint A: retrieval foundation

- Pause Coursera.
- Reproduce install/test/lint from a clean environment.
- Repair and test chunk-size/overlap behavior.
- Implement stable IDs, metadata, embeddings, persistent vector search, and ranked retrieval in the main package.
- Create 15 retrieval and 10 extraction cases, including refusals and adversarial inputs.

### Following blocks

- Complete Course 4 only.
- Pause Coursera for Project Sprint B: hybrid retrieval, reranking, citations, and grounded-answer evaluation.
- Complete a service/reliability sprint.
- Start Course 6 only after those foundations.
- Use LangGraph only where explicit state/recovery/approval benefits are demonstrated.
- Add MCP with least privilege and security tests.

## Durable mental models

- A schema proves shape and types, not truth.
- Retrieval makes relevant context available; it does not force the model to use it correctly.
- A citation is useful only if it is stable, accessible, and actually supports the answer.
- Evaluate retrieval and generation separately before tuning the whole pipeline.
- The model proposes actions; application code validates authorization and executes them.
- Prefer a deterministic workflow when the steps are known.
- Evals, traces, and failure handling turn a demo into credible engineering evidence.

## Session history

- 12 July: Python/Pydantic baseline, tests, formatting, and CI foundations.
- 16 July: fake extraction scenarios, schema failure tests, and evidence-substring validation.
- 17 July: live Gemini structured extraction and environment-variable key handling.
- 27 July: Course 2 completed; LangChain/LlamaIndex course labs and notes added.
- 5 August: Course 1-2 revision resumed after a one-week break.
- 7 August: Course 2 revision challenges completed; key audit and Git hygiene improved; master notes compiled.
- 8 August: full curriculum/repository/job-readiness audit completed. Plan reordered around the current Week 4 checkpoint; notes corrected to remove unsupported production claims.
- 8 August correction: Course 6 had not started. The learner confirmed a strict sequential preference: one complete course block, followed by one dedicated project sprint, never both simultaneously.
- 8 August: Course 3 started as the sole active learning block; the first focus is vector databases and Chroma architecture.
