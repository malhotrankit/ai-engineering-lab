# Coursera and Portfolio Progress

Last reconciled: 8 August 2026

Subscription started: 17 July 2026 (€42/month)

Authoritative ten-course curriculum: `coursera_notes/certificate_curriculum.md`, captured from the learner-provided Coursera PDF on 8 August 2026.

## Current source of truth

- Plan position: Week 4 of 16 (7-13 August).
- Course 1: complete.
- Course 2: complete, including revision labs.
- Course 6: not started. The learner was about to begin it but corrected the earlier record.
- Course 3: in progress and the current, only focus.
- Course 4: not started.
- Main project: typed structured extraction and introductory prompt/chunking utilities exist; production retrieval, API, evaluation, observability, agents, MCP, and deployment do not yet exist.

## Course tracker

### Course 1 - Develop Generative AI Applications: Get Started (10 hours)

- [x] Generative AI foundations
- [x] Prompt engineering, in-context learning, and templates
- [x] LangChain introduction
- [x] Master revision guide corrected and regenerated

### Course 2 - Build RAG Applications: Get Started (7 hours)

- [x] RAG components and summarization lab
- [x] LangChain retrieval application and Gradio lab
- [x] LlamaIndex/Granite bot lab
- [x] LangChain and LlamaIndex revision challenges
- [x] Master revision guide corrected and regenerated

### Course 3 - Vector Databases for RAG: An Introduction (9 hours, in progress)

- [ ] Vector databases versus traditional databases
- [ ] ChromaDB collections, update, delete, and management operations
- [ ] Manual and ChromaDB similarity search
- [ ] Vector-similarity recommendation system
- [ ] Key internal RAG mechanisms
- [ ] After course completion, transfer the concepts into Project Sprint A under `src/`

### Course 4 - Advanced RAG with Vector Databases and Retrievers (8 hours)

- [ ] Advanced retrieval patterns
- [ ] FAISS, ChromaDB, and HNSW concepts
- [ ] Advanced retrievers with LlamaIndex and LangChain
- [ ] LangChain/FAISS/Gradio RAG application
- [ ] Add hybrid retrieval/reranking and measure retrieval quality

### Course 5 - Build Multimodal Generative AI Applications (8 hours, optional breadth)

- [ ] Skim unless target roles require PDF vision, audio, or multimodal search

### Course 6 - Fundamentals of Building AI Agents (11 hours, not started)

- [ ] Function calling, chaining, and tool orchestration
- [ ] Manual tool-call handling and parsing
- [ ] Built-in agent labs
- [ ] Start only after the Course 4 project sprint and service foundation

### Course 7 - Agentic AI with LangChain and LangGraph (11 hours)

- [ ] Stateful workflows
- [ ] ReAct architecture
- [ ] Agentic RAG and multi-agent design

### Course 8 - Agentic AI with LangGraph, CrewAI, AutoGen and BeeAI (13 hours, optional breadth)

- [ ] Compare patterns and frameworks
- [ ] Do not build duplicate demos unless a target job explicitly asks for a framework

### Course 9 - Build AI Agents using MCP (10 hours)

- [ ] MCP architecture, tools, resources, and prompts
- [ ] FastMCP server
- [ ] STDIO and Streamable HTTP clients
- [ ] Sampling, roots, permissions, and user approval
- [ ] Build a least-privilege, read-only MCP capability with security tests

### Course 10 - RAG and Agentic AI Capstone Project (14 hours)

- [ ] Adapt relevant capstone requirements into the financial document system

## Revised milestone sequence

`Course 3 only -> Project Sprint A: real retrieval -> Course 4 only -> Project Sprint B: retrieval quality/evals -> service sprint -> Course 6 only -> tools sprint -> Course 7 only -> LangGraph sprint -> Course 9 only -> MCP/security sprint -> deployment/portfolio/interviews`

Every arrow is a handoff between exclusive focus blocks. Course study and project implementation do not run simultaneously.

## Portfolio milestones

### Milestone A - Project Sprint A after Course 3 (Week 5 target)

- [ ] Clean install runs tests and lint
- [ ] Chunking handles long paragraphs and overlap correctly
- [ ] Versioned extraction/retrieval test cases exist
- [ ] README describes the repository as a learning prototype

### Milestone B - Project Sprint B after Course 4 (Week 7 target)

- [ ] Real ingestion, embeddings, persistent vector index, and retrieval under `src/`
- [ ] Stable document/chunk metadata and citations
- [ ] Dense plus sparse retrieval and optional reranking
- [ ] Retrieval and answer metrics reported separately
- [ ] Injection, conflict, missing-fact, and refusal cases included

### Milestone C - service and operations sprint (Week 8 target)

- [ ] FastAPI endpoints and provider adapters
- [ ] Background ingestion, Postgres/pgvector, bounded retries/timeouts
- [ ] Unit, integration, and contract tests without live API calls
- [ ] Structured logs and OpenTelemetry-compatible traces

### Milestone D - tools, LangGraph, and MCP project sprints (Weeks 10, 12, and 14 targets)

- [ ] Direct Python tool workflow with Pydantic schemas and authorization
- [ ] LangGraph only where state/recovery is useful
- [ ] Iteration, token, time, and tool budgets
- [ ] Read-only MCP capability and security boundary tests

### Milestone E - deployment and job package (Weeks 13-16)

- [ ] Docker/cloud deployment, health checks, limits, and rollback notes
- [ ] Threat model and red-team regression cases
- [ ] Evaluation table, architecture diagram, runbook, and demo video
- [ ] Two project deep dives and two system-design mocks
- [ ] Targeted applications underway

## Immediate next actions

1. Begin the Course 3 module on vector databases and Chroma architecture, then continue Course 3 as the only active block.
2. After Course 3, pause Coursera and begin Project Sprint A.
3. In Project Sprint A, restore the environment, fix chunking, add embeddings/vector retrieval, and create the first retrieval evaluation set.
4. Start Course 4 only after Project Sprint A is complete.
