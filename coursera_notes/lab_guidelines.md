# Course & Lab Execution Guidelines (Antigravity Study Rules)

These are the strict operating rules for how the AI assistant and user collaborate on Coursera courses and labs.

## 0. Mandatory Rule 0: Autonomous Silent Updates
- **Rule 0:** Automatically update `notes.md`, `interview_questions.md`, `progress.md`, `learning_log.md`, and `session_context.md` on **every single turn** as new concepts are introduced, WITHOUT waiting to be asked or reminded.
- **Interview Q&A PDF Auto-Generation:** Whenever `interview_questions.md` is updated or modified, automatically re-compile `coursera_notes/interview_questions_master.pdf` using `.venv/bin/python scratch/generate_interview_questions_pdf.py` and overwrite/remove any old versions!

## 1. The "Struggle vs. Skip" Lab Framework
Target Deadline: **July 31st** | Goal: **Interview-Ready Knowledge & Portfolio Project**

- **🧠 STRUGGLE (Must Do):** Exercises that build critical interview-ready concepts (e.g., RAG pipelines, Recursive Text Splitters, Vector Search, ReAct Agents, ParentDocumentRetriever, Pydantic Structured Outputs). The AI assistant must NOT dump solutions—let the user solve `##TODO` blocks and debug.
- **👀 SKIM:** Exercises showing code evolution (e.g., SequentialChain vs LCEL) or alternative implementations. Read for context, but do not spend time typing out boilerplate.
- **🚫 SKIP:** Basic filler exercises (e.g., model temperature tweaks, basic prompt variations, basic Flask endpoints, legacy memory classes). Skip to save time.

---

## 2. Lab Assistance Protocol
1. **Analyze First:** When a lab document is provided, immediately categorize all exercises into **SKIP**, **SKIM**, or **STRUGGLE**.
2. **No Solution Dumping:** Do NOT auto-generate solution files for labs unless explicitly requested. Guide the user through doc lookups and debugging.
3. **"No-Scrolling" Cheat Sheets:** Create condensed Markdown/PDF artifacts for complex labs so the user doesn't have to scroll through Coursera's long Jupyter notebooks.

---

## 3. Tech Stack & Architectural Rules
- **Backend Background:** The user is a Senior Java / Spring Boot developer transitioning to AI.
- **Python AI Stack:** LangChain, LangGraph, Pydantic, Gemini API, ChromaDB.
- **Production API Framework:** Use **FastAPI** (not Flask) for building production AI REST microservices.
- **Enterprise Pattern:** Hybrid Microservice Architecture (Spring Boot Backend ➔ FastAPI / LangGraph Python AI Agent).

---

## 4. Sequential Learning & Project Workflow
- **Workflow Rule:** Sequential, NOT parallel. The user will focus 100% on completing the Coursera courses (Course 2 ➔ Course 6 ➔ Course 7 ➔ Course 9) FIRST to prevent context switching.
- **Project Phase:** The `ai-engineering-lab` project codebase will be built in dedicated coding sprints AFTER course milestones are completed.
- **Workspace:** `/Users/ankitmalhotra/Developer/ai-engineering-lab/`
- **Active Project:** Financial Data / Earnings Call Extractor (Pydantic + RAG + LangGraph + FastAPI).

