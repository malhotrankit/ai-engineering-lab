# Course and Lab Execution Guidelines

Last revised: 8 August 2026

## Purpose

Use Coursera to acquire concepts and the main `ai-engineering-lab` package to prove them. Course completion is not a substitute for implementation, evaluation, or a defensible architecture decision.

## Source-of-truth rule

At the end of a meaningful study or build session, update only the records affected by the work:

- `coursera_notes/progress.md` for course and milestone status.
- `learning_log.md` for concepts learned, decisions, failures, and evidence.
- `docs/session_context.md` for the current checkpoint and exact next action.
- A master note or interview file only when new material is genuinely useful.

Do not edit five files on every conversational turn. Do not regenerate a PDF unless its Markdown source changed. PDF generation is handled by `scripts/generate_learning_pdfs.py`.

## Struggle, skim, skip

### Struggle - implement and explain

Use for skills that employers test and the project needs: Python typing/async, Pydantic boundaries, retrieval, chunking, metadata, hybrid search, reranking, evaluation, FastAPI, retries/timeouts, safe tool calls, LangGraph state, MCP security, observability, and Docker deployment.

The learner should write the key logic, predict failure cases, and explain trade-offs. Assistance should guide and review rather than dump a complete lab solution unless explicitly requested.

### Skim - understand the trade-off

Use for alternate frameworks, UI-only demos, legacy APIs, or features that broaden awareness but do not improve the portfolio. Record the abstraction and one use case; do not reproduce boilerplate.

### Skip - low job value now

Skip repetitive prompt variations, deprecated memory/chain syntax, duplicate multi-agent demos, and provider-specific UI work that does not support a target job.

## Strict sequential workflow

1. Complete one course block with no project work.
2. Pause Coursera completely.
3. Complete the matching project sprint with no course work.
4. Record the verified result and exact next block.
5. Start the next course only when the project sprint is complete.

Do not alternate course and project work by day or combine them in one week. The learner has explicitly rejected parallel or hybrid study workflows.

## Architecture rules

- Treat the repository as a learning prototype until real retrieval, evaluation, service reliability, observability, security controls, and deployment evidence exist.
- Prefer direct Python for known workflows; add LangGraph when state, branching, recovery, or approvals provide clear value.
- Pydantic validates structure, not factual support or authorization.
- Retrieved documents are candidate evidence, not proof of a correct answer.
- The application, not the model, authorizes and executes tools.
- Use FastAPI for the Python service boundary; a Java/Spring service may consume it later, but is not required for the first portfolio release.
- Introduce Postgres/pgvector as the durable store. Add Redis only for a demonstrated job-state, rate-limit, or cache requirement.
- Prefer one well-evaluated system over multiple shallow framework demos.

## Current order

Complete Course 3 only. Then pause Coursera for the financial-project retrieval sprint. Complete Course 4 only, then pause for the advanced-RAG/evaluation sprint. Complete a service sprint before starting Course 6. Courses 5 and 8 remain optional unless a target job makes them relevant.
