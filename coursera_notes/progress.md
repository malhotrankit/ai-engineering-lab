# Coursera Course Progress: Professional Certificate in RAG and Agentic AI

**Subscription Date:** July 17, 2026
**Cost:** €42/month

*Note: Since I cannot directly connect to your Coursera account, I will track your progress here manually as you update me.*

## Courses & Modules

### Course 1: Generative AI Applications
- [x] Overview Video
- [x] Basics of Generative AI
- [x] Prompt Engineering, In-Context Learning, and Prompt Templates
- [x] Langchain Framework for GenAI Workflows (Course 1 Completed! 🎉)

### Course 2: RAG Applications (COMPLETED! 🎉)
- [x] Key Components of Retrieval Augmented Generation (RAG) & Document Summarization Lab
- [x] Implementing RAG with Langchain & Building Interfaces with Gradio
- [x] Bot Building with LlamaIndex & IBM Granite Model (Course 2 Completed! 🎉)

### Course 3: Vector Databases for RAG
- [ ] Introduction to Vector Databases & ChromaDB Architecture
- [ ] Coding Vector Operations & Similarity Search
- [ ] Building a Recommendation System (Vector DB + Embedding Model)

### Course 4: Advanced RAG with Vector Databases and Retrievers
- [ ] Advanced Retrievers and Retrieval Patterns
- [ ] Working with FAISS Vector Database
- [ ] Building RAG Application (FAISS, Langchain, Gradio)

### Course 5: Multimodal Generative AI Applications
- [ ] Processing Multiple Data Types (Audio, Vision, Text)
- [ ] Speech Recognition & Text-to-Speech (OpenAI Whisper, Mistral)
- [ ] Image Generation (DALL-E) and Image Captioning
- [ ] Multimodal Retrieval, Cross-Modal Search, and Chatbots

### Course 6: AI Agents (In Progress 🔄)
- [/] Function Calling, Chaining, and Tool Orchestration (In Progress 🔄)
- [ ] Manual Tool Call Handling & Parsing
- [ ] Langchain's Built-in Agents (DataFrame, SQL Agents)

### Course 7: Agentic AI Fundamentals with Langchain and Langgraph
- [ ] Stateful Workflows using Langchain and Langgraph
- [ ] ReAct Agents Architecture
- [ ] Multi-Agent System Design & Agentic RAG Architecture

### Course 8: Agentic AI Frameworks
- [ ] State-of-the-Art Design Patterns
- [ ] Multi-Agent Orchestration with Crew AI & Langgraph
- [ ] IBM BAI Framework & AG2 (formerly Autogen)

### Course 9: Build AI Agents using MCP (Model Context Protocol)
- [ ] Understanding Model Context Protocol (MCP)
- [ ] Integrating agents with local data and APIs via MCP

### Course 10: RAG and Agentic AI Capstone Project
- [ ] Real-world application deployment
- [ ] Multi-agent system / RAG pipeline project

## 🎯 Scheduled Project Coding Sprint Milestones (Zero Context-Switching)

```
[Course 1 & 2: RAG] ➔ [Course 6 & 7: Agents & LangGraph] ➔ 🚀 SPRINT 1 (Build LangGraph Agent) ➔ [Course 9: MCP] ➔ 🚀 SPRINT 2 (FastAPI & Deployment)
```

- **🚀 SPRINT 1 (Right after Course 7 - LangGraph):**
  - *Goal:* Combine Course 1, 2, 6, and 7 knowledge into `ai-engineering-lab`.
  - *Deliverable:* Build `src/ai_engineering_lab/agent.py` (Autonomous LangGraph Agent with RAG + SEC Search Tools + Pydantic validation).
- **🚀 SPRINT 2 (Right after Course 9 - MCP & Capstone):**
  - *Goal:* Turn your codebase into a production-grade microservice.
  - *Deliverable:* Build `src/ai_engineering_lab/api.py` (FastAPI REST service with streaming responses & live Swagger UI).
## Critical Job-Hunting Supplements (High Priority for July 31st Deadline)
*These topics are heavily tested in 2026 AI Engineer interviews but are often skipped in introductory courses.*

### Supplement 1: Evaluation & Metrics (The "Prove it works" round)
- [ ] Evaluating generation quality vs. retrieval quality separately
- [ ] Building a "Golden Dataset" for RAG and Agents
- [ ] Using Evaluation Frameworks (e.g., Ragas, TruLens)
- [ ] Understanding LLM-as-a-judge (and its failure modes)

### Supplement 2: Production Ops & Cost Management
- [ ] Observability & Tracing (e.g., LangSmith, Phoenix, Datadog for LLMs)
- [ ] Cost containment strategies (model routing, caching, iteration caps for agents)
- [ ] Guardrails and prompt injection defenses (e.g., NeMo Guardrails)
- [ ] Managing latency budgets for multi-step workflows

### Supplement 3: Advanced Architecture Taste
- [ ] Hybrid Search (Dense + Sparse) & Re-ranking (e.g., Cohere)
- [ ] Understanding the Agentic Loop (Reason -> Act -> Observe cycle)
- [ ] Agentic state management & preventing "runaway tool loops"
- [ ] When to use Multi-Agent Swarms vs. single agents vs. simple scripts

### Supplement 4: Real-World Data & Tooling (New!)
- [ ] Structured Outputs (forcing JSON/Pydantic schemas for tool calling)
- [ ] Advanced RAG Chunking (Handling messy PDFs, tables, and images)
- [ ] Handling Multi-hop queries (queries requiring multiple document lookups)
