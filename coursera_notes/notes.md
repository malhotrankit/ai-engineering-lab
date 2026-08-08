# Job-Focused Notes: RAG and Agentic AI

Last curated: 8 August 2026

This is a living technical reference for interviews and the financial-document portfolio project. It intentionally omits repetitive course material and labels concepts that are not yet implemented.

## 1. Current project reality

Implemented:

- Python/Pydantic models for documents and earnings extraction.
- Direct Gemini structured output.
- Fake valid, malformed, and fabricated-evidence scenarios.
- Verbatim evidence-substring validation.
- Basic paragraph chunking and an augmented prompt builder.
- Course-level LangChain and LlamaIndex practice scripts.

Not yet implemented in the main package:

- Embeddings, vector search, retrieval, hybrid search, reranking, and citations.
- Evaluation harness and versioned golden cases.
- FastAPI, persistence, background ingestion, observability, and deployment.
- Production tools/agents, LangGraph state, and MCP.

Interview rule: describe this as a prototype with a measured roadmap. Never claim the application is production RAG before those capabilities exist.

## 2. LLM application boundaries

An LLM is a probabilistic dependency. Reliable applications place deterministic boundaries around it:

- Input validation and size limits.
- Structured outputs or tool schemas.
- Application-side authorization and business rules.
- Timeouts, bounded retries, concurrency limits, and fallbacks.
- Evaluation datasets and release thresholds.
- Logs, traces, metrics, cost accounting, and incident handling.

Structured output constrains shape and types. It does not prove correctness, source support, authorization, or safe intent.

Temperature zero or greedy decoding can reduce sampling variability, but identical outputs are not universally guaranteed across providers, infrastructure, model versions, or tie-breaking behavior.

## 3. Prompting, long context, RAG, and fine-tuning

Use prompting when the model already has the required capability and only task instructions, examples, or output constraints are missing.

Use long context when the corpus is small, changes slowly during a request, fits comfortably inside the context window, and repeated retrieval infrastructure would add little value. Evaluate lost-in-the-middle behavior and token cost.

Use RAG when knowledge is private, dynamic, too large for each prompt, requires access control, or needs source attribution. RAG can improve grounding by supplying evidence; it does not guarantee factual answers.

Use fine-tuning when repeated examples should change behavior, style, domain patterns, or task performance. Fine-tuning is not the normal way to keep frequently changing facts current.

Use tools when the system must query an authoritative live system, perform deterministic computation, or take an action.

## 4. RAG pipeline

Offline ingestion:

1. Acquire and authorize the source.
2. Parse text, tables, and layout while preserving provenance.
3. Normalize and deduplicate.
4. Chunk with stable document/chunk IDs and metadata.
5. Compute embeddings.
6. Write vectors, searchable text, and metadata to durable storage.
7. Record parser/embedding versions so re-indexing is reproducible.

Online query:

1. Authenticate and apply access filters.
2. Normalize or rewrite the query only when measured useful.
3. Retrieve dense and/or sparse candidates.
4. Fuse and optionally rerank candidates.
5. Enforce a context/token budget.
6. Generate or extract with a clear refusal instruction.
7. Return stable citations.
8. Validate output and citation support.
9. Trace latency, retrieval results, model usage, and errors safely.

Retrieval makes candidate evidence available. The generator can still ignore, distort, or combine it incorrectly.

## 5. Chunking and metadata

Chunking is an evaluation problem, not a universal character-count rule.

- Small chunks improve match specificity but may lose context.
- Large chunks preserve context but can dilute similarity and waste tokens.
- Overlap can preserve continuity but increases storage and duplicate retrieval.
- Structure-aware chunking should preserve headings, tables, lists, and page/source identity.
- Parent-child retrieval can search small child chunks and return a larger parent context.

For financial documents, useful metadata includes company, filing/report type, reporting period, source URL, page, section, document ID, chunk ID, access scope, parser version, and ingestion timestamp.

Current code limitation: `chunk_overlap` is accepted but unused, and long paragraphs may exceed the requested size. This must be fixed and tested before describing the splitter as production-ready.

## 6. Embeddings, vector databases, and search

Embeddings map inputs into vectors where distance approximates model-learned similarity.

- Cosine similarity compares direction and ignores magnitude.
- Dot product is equivalent to cosine for normalized vectors and may be used by a model/index by design.
- Euclidean distance measures geometric distance; smaller is closer.

Do not select a metric from memory alone. Use the embedding model's recommendation and the vector store/index configuration.

Vector index concepts:

- Exact search compares every vector and is simple but expensive at scale.
- Approximate nearest-neighbor indexes trade some recall for latency and scale.
- HNSW provides tunable construction/search parameters and memory/recall trade-offs.
- Metadata filters must be applied correctly for tenancy, authorization, document type, and time.

Chroma and FAISS are useful learning/local tools. PostgreSQL plus pgvector is a strong portfolio choice because it combines durable relational metadata, filters, and vector search. The choice still needs measured latency, scale, and operational reasoning.

## 7. Hybrid retrieval and reranking

Dense retrieval is good at semantic similarity. Sparse retrieval such as BM25 is good at exact phrases, identifiers, names, codes, and rare terms. Financial-document search often needs both.

A common pipeline is:

`dense candidates + sparse candidates -> rank fusion -> metadata/security filters -> reranker -> context budget`

Reciprocal-rank fusion is a simple score-independent way to combine ranked lists. A cross-encoder reranker can improve final relevance but adds latency and cost. Measure the delta before keeping it.

Top-k is not “higher is better.” Increasing k can improve recall while reducing precision, increasing cost, and worsening lost-in-the-middle effects.

## 8. RAG evaluation

Create the evaluation set before extensive tuning so changes are compared against a stable baseline.

Retrieval metrics:

- Recall@k: whether the relevant source appears in the first k results.
- Precision@k: how many of the first k results are relevant.
- Mean reciprocal rank: how early the first relevant result appears.
- nDCG: useful when relevance is graded rather than binary.
- Filter/access correctness and no-result behavior.

Generation/application metrics:

- Answer correctness against expected facts.
- Citation correctness/support.
- Faithfulness or groundedness.
- Refusal accuracy when evidence is insufficient.
- Schema/tool-call success.
- Latency, tokens, cost, retries, and error rate.

Use deterministic graders where possible. LLM-as-judge is useful for nuanced quality but has bias, variance, prompt sensitivity, and model-version drift; calibrate it against human labels and retain representative manual review.

An eval set should include happy paths, missing answers, conflicts, ambiguous periods, units, exact IDs, table-derived facts, prompt injection in sources, long documents, duplicates, access-controlled content, and provider failures.

## 9. Evidence and citations

A returned source document is not proof that the answer is supported.

Useful citation checks include:

- The document/chunk identifier resolves to the original source.
- The cited span contains the claimed company, period, metric, value, and unit.
- The citation supports the wording of the answer rather than merely sharing a topic.
- Multiple claims have appropriately scoped citations.
- Conflicting evidence is surfaced rather than silently selected.

The current substring verifier is a first guard. It detects fabricated quotes, but can accept a real quote paired with an incorrect parsed value or period. Add claim-to-evidence consistency tests.

## 10. LangChain and LlamaIndex

LangChain provides composable runnables, model/tool adapters, retrievers, and broader orchestration. LCEL makes dataflow explicit with runnables and pipe composition.

LlamaIndex centers on data ingestion, nodes, indexes, retrieval, and response synthesis. Its high-level query/chat engines are useful for rapid retrieval prototypes.

Framework choice should follow the use case, team experience, debuggability, version stability, and operational needs. Frameworks do not remove the need for evaluation, security, observability, or application boundaries.

Course APIs may be legacy. Learn the concept, confirm the current official API before implementing, and isolate framework-specific code behind project interfaces.

## 11. Tools, workflows, and agents

A tool schema describes an operation and its arguments. The model can propose a call, but application code must:

- Authenticate the user and authorize the operation.
- Validate arguments and resource scope.
- Enforce allowlists, budgets, timeouts, and rate limits.
- Handle retries and idempotency based on side effects.
- Sanitize or constrain tool outputs.
- Record an audit event.
- Require approval for consequential actions.

Use a deterministic workflow when steps and branches are known. Use an agent when dynamic selection among constrained actions provides measured value. Start with the simplest solution and add agentic complexity only when it improves outcomes.

Agent termination requires explicit success/failure states plus maximum steps, time, tokens, and tool-call budgets. A prompt saying “stop when done” is not a control.

## 12. LangGraph and state

LangGraph is useful when an application benefits from explicit state, branching, cycles, checkpointing, recovery, interrupts, or human approval.

A financial research workflow might use:

`interpret -> retrieve -> calculate -> draft -> validate -> approve -> finish`

State should contain only what downstream nodes need, with clear ownership and update rules. Test individual nodes, routing conditions, terminal states, replay behavior, and denied tool calls.

Do not use a graph to hide a simple three-step function. Compare the direct Python implementation with the graph and keep the framework only if it improves control or maintainability.

## 13. MCP

MCP standardizes how hosts/clients discover and invoke server-provided tools, resources, and prompts. It is an integration protocol, not an authorization or trust boundary.

Security concerns include token theft/passthrough, confused-deputy attacks, malicious metadata, excessive tool permissions, local-server compromise, SSRF, data exfiltration, and indirect prompt injection.

Use least privilege, explicit consent, audience-bound tokens, secure storage, HTTPS/transport controls, validated redirect URIs, no token passthrough, and strong separation between model input and authorization decisions.

For the portfolio, one read-only MCP capability with denied-case tests is more credible than a wide tool surface.

## 14. FastAPI and reliability

Recommended service boundary:

- Typed request/response models.
- Thin endpoint handlers calling domain services.
- Provider adapters for model, embedding, and storage dependencies.
- Async only for genuine I/O concurrency.
- Explicit timeouts, bounded retries with jitter, circuit/bulkhead thinking, and backpressure.
- Idempotency for retried ingestion/actions.
- Background processing for long ingestion.
- Unit tests without network calls; integration/contract tests for boundaries.

Streaming improves perceived latency but complicates error semantics, moderation, cancellation, tracing, and clients. Use it only if the product needs it.

## 15. Observability and cost

Trace the full request with correlated spans for retrieval, reranking, model calls, tool calls, and validation. OpenTelemetry GenAI conventions provide common attribute names, but semantic conventions evolve; pin and document what is emitted.

Useful signals:

- Request count, latency percentiles, errors, retries, and timeouts.
- Model/provider, token usage, estimated cost, and cache behavior.
- Retrieved chunk IDs/scores and reranker decisions, subject to privacy controls.
- Tool name, result status, duration, and denied calls.
- Evaluation version and regression status.

Avoid logging secrets, raw credentials, or unnecessary sensitive prompts/documents.

Caching claims must be measured. Provider prompt caching depends on vendor rules and repeated prefixes. Semantic caching can return stale, incorrectly matched, or cross-user data; include tenant isolation, TTL, invalidation, similarity thresholds, and a bypass for sensitive/dynamic queries.

Self-hosted serving tools such as vLLM can improve throughput through techniques such as PagedAttention and continuous batching, but gains depend on model, hardware, workload, and configuration. Do not quote universal multipliers without a benchmark.

## 16. Security and governance

Map system threats to controls and tests using current NIST and OWASP guidance.

High-priority cases:

- Direct and indirect prompt injection.
- Sensitive information disclosure.
- Excessive agency and over-permissioned tools.
- Improper output handling.
- Supply-chain/model/parser dependencies.
- Data/vector poisoning.
- Unbounded token, tool, and compute consumption.
- Weak authentication/authorization and tenant filtering.

Governance evidence includes data provenance, retention/deletion, access control, evaluation coverage, human oversight, model/dependency versions, incident response, and change approval. For EU-facing work, understand current EU AI Act transparency and deployment obligations relevant to the use case; seek legal advice for actual compliance decisions.

## 17. Interview narrative for this project

Use this structure:

1. Problem: extract and answer questions over earnings documents with attributable evidence.
2. Constraint: model outputs are probabilistic and financial facts require exact period/value/unit support.
3. Current solution: typed extraction, direct structured output, and a first deterministic evidence check.
4. Discovered limitation: source presence is weaker than claim support; the main package also lacks real retrieval.
5. Next measured step: build retrievable stable chunks, evaluate recall@k/citations, then expose a reliable API.
6. Production path: safe tools, traces, security tests, Docker deployment, and release thresholds.

This is stronger than claiming a finished production system because it shows accurate engineering judgment and a disciplined path from prototype to reliable service.

## Primary references

- NIST Generative AI Profile: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- OWASP Top 10 for LLM/GenAI Applications: https://genai.owasp.org/llm-top-10/
- MCP Security Best Practices: https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
- OpenTelemetry GenAI semantic conventions: https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/
- Google Cloud generative AI application lifecycle: https://docs.cloud.google.com/docs/ai-ml/generative-ai/develop-generative-ai-application
- Anthropic agent design and evaluation: https://www.anthropic.com/engineering/building-effective-agents and https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

