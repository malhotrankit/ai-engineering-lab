# Course 2 Master Revision Guide: Building RAG Applications

---

## 1. Fundamentals of Retrieval-Augmented Generation (RAG)

### Core Problems Solved by RAG
1. **Out-of-Date Knowledge:** LLMs are frozen at training time. RAG updates knowledge continuously by retrieving fresh data without model retraining.
2. **Hallucinations & Attribution:** Base LLMs generate text without citations. RAG forces responses grounded strictly in retrieved context with source attribution.
3. **Data Privacy:** Private enterprise data can be stored securely in vector databases and retrieved based on access permissions.

### The 4-Step Vector Operations Flow
```
[Raw File] ➔ [1. Split into Chunks] ➔ [2. Embed into Vectors] ➔ [3. Store in VectorDB] ➔ [4. Top-K Similarity Search] ➔ [LLM Generation]
```

### The 3-Part Augmented Prompt Structure
Every RAG prompt payload sent to the LLM contains:
1. **System Instruction:** *"Answer strictly using the provided context below. If unknown, say 'I don't know'."*
2. **Retrieved Context:** The concatenated text chunks fetched from the vector database.
3. **User Question:** The user's query.

---

## 2. Vector Operations, Distance Metrics & Inference Parameters

### Distance Metrics Comparison (Interview Core)
- **Cosine Similarity:** Measures the *angle* between vectors. Best when text chunk lengths vary.
- **Dot Product:** Measures *angle + magnitude*. Faster to compute; mathematically equal to Cosine Similarity when vectors are L2-normalized.
- **Euclidean (L2) Distance:** Geometric distance between vector endpoints. Smaller distance = higher similarity.

### LLM Decoding Methods & Hyperparameters
- **Greedy Decoding:** Always selects the #1 highest-probability token. 100% deterministic (same prompt = same output every time). Ideal for factual RAG, data extraction, and code generation.
- **Sampling Decoding:** Randomly samples tokens based on a probability curve. Unlocks `Temperature`, `Top-P`, and `Top-K`.
  - **Temperature (0.0 - 2.0):** Low temperature (0.1–0.3) keeps responses factual; high temperature (0.8–1.5) increases randomness/creativity.
  - **Top-P (Nucleus Sampling):** Restricts choices to the top cumulative probability (e.g. top 90%).
  - **Top-K:** Restricts choices to the top K most likely words.

---

## 3. Document Combination & Memory Strategies

### The 4 Combination Strategies (`chain_type`)
1. **`stuff` (Industry Standard - 95%+ Production):** Stuffs all retrieved chunks into a single prompt payload.
   - *Why it dominates:* Modern LLMs have huge context windows (128k+ tokens). It requires only **1 API call** (fastest & cheapest).
2. **`map_reduce`:** Runs an LLM call for *each* chunk to extract mini-answers, then runs a final LLM call to synthesize them. (Used for offline 500-page book summarization).
3. **`refine`:** Loops sequentially through chunks, refining the answer step-by-step.
4. **`map_rerank`:** Scores each chunk's answer from 0 to 100 and returns the top-scored answer.

### Grounding Verification & Citations
- Setting `return_source_documents=True` in LangChain ensures the chain returns the exact `Document` chunks retrieved from ChromaDB alongside the LLM's answer.
- **Legacy Callbacks vs Modern LCEL:**
  - *Legacy:* `ConversationalRetrievalChain` used clunky identity callbacks like `get_chat_history=lambda h: h`.
  - *Modern LCEL:* Uses `ChatPromptTemplate` with `MessagesPlaceholder(variable_name="chat_history")`.

---

## 4. LangChain vs. LlamaIndex Deep Architecture & Abstractions

### 1. Framework Data Model & Attribute Mapping
| Data Abstraction | LangChain Framework | LlamaIndex Framework | Deep Technical Difference & Attributes |
| :--- | :--- | :--- | :--- |
| **Document Container** | `Document(page_content, metadata)` | `Document(text, metadata, relationships, id_)` | LlamaIndex `Document` includes built-in unique `id_` hashes and `relationships` dictionary pointers out-of-the-box. LangChain uses plain string `page_content`. |
| **Text Chunk** | `Document` chunk | `TextNode` (or `Node`) | `TextNode` extends `Document` and adds `node_id`, `start_char_idx`, `end_char_idx`, and exact pointers to `PREVIOUS`, `NEXT`, and `PARENT` nodes. |
| **Directory Ingestion** | `DirectoryLoader` (Wraps single-file loaders) | `SimpleDirectoryReader` | `SimpleDirectoryReader` auto-detects file extensions (PDF, CSV, TXT, HTML, Markdown, Docx) natively without installing extra loader wrapper classes. |
| **Text Splitting** | `RecursiveCharacterTextSplitter` | `SentenceSplitter` (NodeParser) | `SentenceSplitter` splits recursively on character lists `["\n\n", "\n", " ", ""]` while enforcing token limits (default `chunk_size=1024`, `chunk_overlap=200`). Returns `list[TextNode]`. |
| **Vector Storage Ingestion** | 2-Step Ingestion (`embeddings.embed_documents()` ➔ `Chroma.from_documents()`) | 1-Step Ingestion (`VectorStoreIndex.from_documents(docs)`) | LlamaIndex combines embedding generation and vector DB indexing into a single constructor call. |
| **RAG Execution Engine** | `RetrievalQA` or LCEL (`create_retrieval_chain`) | `index.as_query_engine()` (`query_engine.query()`) | `as_query_engine()` encapsulates query embedding, vector search, prompt injection, and LLM call into 1 line. |
| **Conversational RAG** | `ConversationalRetrievalChain` + `ConversationBufferMemory` | `index.as_chat_engine()` (`chat_engine.chat()`) | LlamaIndex `chat_engine` manages memory history and question condensing automatically. |

### 2. Deep Dive: LlamaIndex `TextNode` Relationship Graph
Unlike LangChain where chunk relationships are lost unless stored in custom metadata dictionaries, LlamaIndex `TextNode` objects preserve the document topology directly inside `node.relationships`:
- `NodeRelationship.PARENT`: Points to the source `Document` ID.
- `NodeRelationship.PREVIOUS`: Points to the preceding `TextNode` chunk ID.
- `NodeRelationship.NEXT`: Points to the succeeding `TextNode` chunk ID.
- `NodeRelationship.CHILD`: Points to child sub-nodes (used in hierarchical chunking).

### 3. Deep Dive: Response Synthesis Strategies (`response_mode`)
When initializing `index.as_query_engine(response_mode=...)`, LlamaIndex provides 5 distinct combination modes:
1. **`compact` (Default / Stuffed):** Stuffs as many node chunks into the prompt window as possible. If context limits are approached, it pre-merges chunks to prevent token overflow crashes.
2. **`tree_summarize` (Map-Reduce):** Recursively builds a tree of LLM responses from chunks and synthesizes a final root summary response. (Best for multi-document summaries).
3. **`refine`:** Sequentially passes Chunk 1 to the LLM to form Answer 1, then passes (Answer 1 + Chunk 2) to refine the answer. (Best for detailed, exhaustive answers; high latency).
4. **`simple_summarize`:** Truncates all retrieved nodes to fit a single prompt and executes 1 LLM call.
5. **`accumulate`:** Applies the query prompt to each node chunk independently and returns a concatenated string of all individual answers.

### 4. Deep Dive: Chat Engine Memory Modes (`chat_mode`)
When initializing `index.as_chat_engine(chat_mode=...)`, LlamaIndex supports:
- **`condense_question` (Standard RAG Chat):** Uses LLM + chat history to rewrite follow-up questions into standalone queries before vector retrieval.
- **`context` (Context-Augmented Chat):** Retrieves context nodes for every turn and injects chat history directly into the system prompt.
- **`react` (Agentic Chat):** Wraps the index inside a ReAct agent loop capable of reasoning and deciding when to query the index versus answering directly.

### 5. Document Class Portability & Format Converters
Attempting to pass a LlamaIndex `Document` to a LangChain chain throws an `AttributeError` because LangChain code expects `doc.page_content` while LlamaIndex code expects `doc.text`.
- **LlamaIndex ➔ LangChain:** `lc_doc = llama_doc.to_langchain_format()`
- **LangChain ➔ LlamaIndex:** `llama_doc = LlamaDocument.from_langchain_format(lc_doc)`

### 6. StorageContext Architecture (Persistent Vector Storage)
LlamaIndex decouples index logic from storage via `StorageContext`:
- `VectorStore`: Stores vector embeddings (e.g. `ChromaVectorStore`, `PineconeVectorStore`).
- `DocStore`: Stores original raw text nodes (`KVDocumentStore`).
- `IndexStore`: Stores index metadata (`KVIndexStore`).
```python
# StorageContext allows swapping vector databases without altering downstream RAG code!
storage_context = StorageContext.from_defaults(vector_store=chroma_vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

---

## 5. Exhaustively Annotated Code Implementations

### Code Block 1: Production-Grade LangChain RAG Pipeline (Modern LCEL Standard)

```python
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# =============================================================================
# PRODUCTION LANGCHAIN LCEL RAG PIPELINE
# (Standard modern implementation using official create_retrieval_chain helpers)
# =============================================================================

# STEP 1: Load raw document into LangChain Document container
# Reads file into memory and returns a list containing 1 Document object (page_content + metadata)
loader = TextLoader("company_policies.txt", encoding="utf-8")
documents = loader.load()

# STEP 2: Recursive Character Text Splitting
# Recursively splits documents into 500-character chunks with 50-character overlap for context continuity
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# STEP 3: Dense Vector Embedding & Vector Database Ingestion (ChromaDB)
# Converts text chunks into 1536-dimensional dense vectors and stores them in ChromaDB
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # Fetches top 3 most relevant chunks

# STEP 4: Construct Augmented System Prompt Template
# IMPORTANT: Prompt MUST define `{context}` for document stuffing and `{input}` for the user query
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer strictly using the provided context below. If unknown, say 'NOT FOUND IN CONTEXT':\n\n{context}"),
    ("human", "{input}")
])

# STEP 5: Assemble Production LCEL RAG Chain
# 1. `create_stuff_documents_chain`: Concatenates retrieved Document chunks into `{context}` & invokes LLM
# 2. `create_retrieval_chain`: Connects vector store `retriever` to the stuff documents chain
llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
production_rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

# STEP 6: Execute Production Chain
# Input key is standardized to {"input": "..."}. Output dictionary contains ["input", "context", "answer"]
response = production_rag_chain.invoke({"input": "What is the eating policy?"})

print("🤖 LLM Answer:", response["answer"])
print("📚 Retrieved Citation Chunks Count:", len(response["context"]))
```

---

### Code Block 2: Complete LlamaIndex Pipeline (ChromaDB + QueryEngine + ChatEngine)
```python
import chromadb
from llama_index.core import (
    SimpleDirectoryReader, 
    VectorStoreIndex, 
    StorageContext, 
    PromptTemplate, 
    Settings
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# STEP 1: Global Settings Configuration (Replaces deprecated ServiceContext)
# Sets the global default LLM and Embedding models for all downstream LlamaIndex operations.
Settings.llm = OpenAI(model="gpt-4o", temperature=0.0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# STEP 2: Load Documents & Parse Nodes
# `SimpleDirectoryReader` auto-detects file types. `SentenceSplitter` returns `list[TextNode]`.
documents = SimpleDirectoryReader(input_dir="./data", recursive=True).load_data()
node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
nodes = node_parser.get_nodes_from_documents(documents) # Explicit TextNode list!

# STEP 3: Setup Persistent ChromaDB Vector Storage via StorageContext
# Decouples vector storage logic from index logic.
db = chromadb.PersistentClient(path="./chroma_db_storage")
chroma_collection = db.get_or_create_collection("enterprise_rag")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# STEP 4: Build VectorStoreIndex (Handles Embedding + Storage in 1 Step)
index = VectorStoreIndex(nodes, storage_context=storage_context)

# STEP 5A: All-in-One Stateless QueryEngine Execution
# Custom QA Prompt Template overriding defaults
custom_qa_prompt = PromptTemplate(
    "Context Information is below:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information, answer the question: {query_str}\n"
    "Answer in professional bullet points:"
)

query_engine = index.as_query_engine(
    text_qa_template=custom_qa_prompt,
    similarity_top_k=3,
    response_mode="compact" # Stuffs text safely without context window overflow
)
query_response = query_engine.query("What was Apple's Q3 revenue?")
print("Stateless QueryEngine Output:\n", query_response)

# STEP 5B: Stateful ChatEngine Execution (Conversational Memory)
# Automatically handles past history and query rewriting across turns.
chat_engine = index.as_chat_engine(
    chat_mode="compact", # Stuffs context + chat history; handles follow-up questions reliably
    similarity_top_k=3
)
chat_response_turn1 = chat_engine.chat("What was Q3 revenue?")
print("Chat Turn 1:", chat_response_turn1)

chat_response_turn2 = chat_engine.chat("What about Services revenue?") # Uses history!
print("Chat Turn 2 (Follow-up):", chat_response_turn2)
```

---

### Code Block 3: Framework Portability & Document Conversion
```python
from llama_index.core import Document as LlamaDocument
from langchain_core.documents import Document as LCDocument

# 1. Instantiate a LlamaIndex Document object
llama_doc = LlamaDocument(
    text="Apple Q3 2025 revenue was $85.8 billion.",
    metadata={"author": "Finance Team", "year": 2025},
    id_="llama_doc_999"
)

# 2. Convert LlamaIndex Document -> LangChain Document
# Calling `.to_langchain_format()` maps `llama_doc.text` -> `lc_doc.page_content`
lc_doc = llama_doc.to_langchain_format()

print("Original LlamaIndex text:", llama_doc.text)
print("Converted LangChain page_content:", lc_doc.page_content)
print("Preserved Metadata:", lc_doc.metadata)

# 3. Convert LangChain Document -> LlamaIndex Document
# Calling `LlamaDocument.from_langchain_format()` maps `lc_doc.page_content` -> `new_llama_doc.text`
new_llama_doc = LlamaDocument.from_langchain_format(lc_doc)
print("Re-converted LlamaIndex text:", new_llama_doc.text)
```

---

## 6. Production System Design & LLMOps

### Prototyping vs. Production (Gradio vs. FastAPI)
- **Gradio (`gr.Interface().launch()`):** Designed for 5-minute Python demos and internal previews. Lacks security, state persistence, and scalability.
- **FastAPI (Production Standard):** Used to serve LLM agents via REST microservices. Supports `async/await`, Pydantic validation, and **token streaming** (`StreamingResponse` / Server-Sent Events).

### LLM Serving Runtime (`vLLM`)
- Open-source serving engine for hosting Llama 3 / Mistral on GPUs.
- Uses **PagedAttention** (virtual memory management for KV-cache) to eliminate memory fragmentation.
- Boosts serving throughput by **2x–4x** and lowers latency.

### Caching Strategies
- **Prompt Caching (API-level):** Caches static system prompt prefixes or large RAG context documents on LLM provider servers (Anthropic/OpenAI), cutting input token costs by 50–90%.
- **Semantic Caching (Application-level):** Stores query-answer pairs in a vector cache (Redis VL / GPTCache). If a new query is $>95\%$ semantically similar to a past query, returns the cached answer instantly with **0ms LLM latency and $0 cost**.

---

## 7. Hands-On Practice Lab References

> **API Key Setup:** All labs load keys from `.env` (git-ignored). Copy `.env.example` to `.env` and fill in your keys before running.

### Lab 1: Dual-Framework RAG Pipeline
- **File:** `coursera_notes/dual_framework_rag_lab.py`
- **Data Source:** Apple Q3 Financial Results & Corporate Policies (`sample_data/apple_q3_earnings.txt`).
- **Exercises:**
  - **Part 1 (LangChain):** `TextLoader` ➔ `CharacterTextSplitter` ➔ `Chroma` ➔ `RetrievalQA.from_chain_type`.
  - **Part 2 (LlamaIndex):** `SimpleDirectoryReader` ➔ `VectorStoreIndex` ➔ `as_query_engine(response_mode="compact")` & `as_chat_engine()`.
  - **Part 3 (Portability):** `llama_doc.to_langchain_format()` format converter.
- **Execution:** `.venv/bin/python coursera_notes/dual_framework_rag_lab.py`

### Lab 2: LangChain Scratch Challenge
- **File:** `coursera_notes/langchain_scratch_challenge.py`
- **Data Source:** Enterprise Service Level Agreement (`sample_data/enterprise_contract.txt`).
- **Live LLM:** **OpenRouter Free Router** (`openrouter/free`) via `OPENROUTER_API_KEY` from `.env`.
- **Goal:** Implement `build_contract_rag_system()` using `create_retrieval_chain` from scratch.
- **Execution:** `.venv/bin/python coursera_notes/langchain_scratch_challenge.py`

### Lab 3: LlamaIndex Scratch Challenge
- **File:** `coursera_notes/llamaindex_scratch_challenge.py`
- **Data Source:** Apex Cloud Technical Support SLA (`sample_data/tech_support/api_support_guide.txt`).
- **Live LLM:** **OpenRouter Free Router** (`openrouter/free`) via `OPENROUTER_API_KEY` from `.env`.
- **Goal:** Implement `build_llamaindex_rag_system()` returning a `(query_engine, chat_engine)` tuple.
- **Features:** Stateless `QueryEngine` with strict `PromptTemplate` guardrails & stateful `ChatEngine` with multi-turn memory.
- **Execution:** `.venv/bin/python coursera_notes/llamaindex_scratch_challenge.py`
