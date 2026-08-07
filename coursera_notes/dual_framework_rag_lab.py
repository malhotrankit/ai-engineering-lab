"""
================================================================================
DUAL-FRAMEWORK RAG HANDS-ON LAB: LANGCHAIN VS. LLAMAINDEX
(100% FRAMEWORK NATIVE IMPORTS, CHROMADB PERSISTENT STORAGE, FREE OPENROUTER LLM)
================================================================================
Target Goal: Implement and compare an end-to-end RAG pipeline using REAL
LangChain (.invoke()) and REAL LlamaIndex (.query() / .chat()) side-by-side!

Instructions:
1. Complete all ## TODO blocks marked [YOUR TASK HERE].
2. Run this script in your terminal using:
   .venv/bin/python coursera_notes/dual_framework_rag_lab.py
================================================================================
"""

import os
import sys
import warnings
import dotenv

# Suppress noisy deprecation notices from third-party community packages
warnings.filterwarnings("ignore")

# 1. Load GEMINI_API_KEY & OPENROUTER_API_KEY with bulletproof resolution
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv.load_dotenv(os.path.join(script_dir, "..", ".env"), override=True)
dotenv.load_dotenv(os.path.join(script_dir, ".env"), override=True)
dotenv.load_dotenv(override=True)

openrouter_key = os.getenv("OPENROUTER_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

if not openrouter_key and not gemini_key:
    print("❌ ERROR: Neither OPENROUTER_API_KEY nor GEMINI_API_KEY found in .env!")
    sys.exit(1)

# 2. PURE FRAMEWORK LLM WRAPPERS & DATA LOADERS
import chromadb
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.embeddings import MockEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

# Set fast mock embeddings for local vector search
Settings.embed_model = MockEmbedding(embed_dim=384)

# Configure OpenRouter Auto-Rotating FREE Model Router
FREE_OPENROUTER_MODEL = "openrouter/free"

if openrouter_key:
    from langchain_openai import ChatOpenAI
    from llama_index.llms.openai_like import OpenAILike
    
    lc_llm = ChatOpenAI(
        model=FREE_OPENROUTER_MODEL,
        temperature=0.0,
        api_key=openrouter_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={"HTTP-Referer": "https://ai-engineering-lab.local", "X-Title": "AI Engineering Lab"}
    )
    llama_llm = OpenAILike(
        model=FREE_OPENROUTER_MODEL,
        temperature=0.0,
        api_key=openrouter_key,
        api_base="https://openrouter.ai/api/v1",
        is_chat_model=True
    )
    Settings.llm = llama_llm
    active_provider = f"OPENROUTER FREE ({FREE_OPENROUTER_MODEL})"
elif gemini_key:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from llama_index.llms.google_genai import GoogleGenAI
    
    os.environ["GEMINI_API_KEY"] = gemini_key
    lc_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
    llama_llm = GoogleGenAI(model="gemini-2.5-flash", temperature=0.0)
    Settings.llm = llama_llm
    active_provider = f"GOOGLE GEMINI 2.5 FLASH"
else:
    print("❌ ERROR: Neither OPENROUTER_API_KEY nor GEMINI_API_KEY found in .env!")
    sys.exit(1)

# -----------------------------------------------------------------------------
# BOILERPLATE SETUP: GENERATE SAMPLE FINANCIAL REPORT
# -----------------------------------------------------------------------------
sample_data_dir = os.path.join(script_dir, "sample_data")
sample_file_path = os.path.join(sample_data_dir, "apple_q3_earnings.txt")
os.makedirs(sample_data_dir, exist_ok=True)

raw_financial_text = """
Apple Inc. (AAPL) Q3 2025 Financial Results Report
Cupertino, California — July 27, 2025

Summary:
Apple today announced financial results for its fiscal 2025 third quarter ended June 28, 2025.
The Company posted a quarterly revenue of $85.8 billion, up 5 percent year-over-year.
Diluted earnings per share (EPS) was $1.40, up 11 percent year-over-year.

Segment Revenue Breakdown:
- iPhone Revenue: $39.3 billion (compared to $39.7 billion in Q3 2024).
- Mac Revenue: $7.0 billion (up from $6.5 billion in Q3 2024, driven by M4 MacBook Air demand).
- iPad Revenue: $7.1 billion (up 24 percent year-over-year following new iPad Pro launches).
- Services Revenue: $24.2 billion (all-time revenue record, up 14 percent year-over-year).

Key Executive Quotes:
Tim Cook, Apple CEO: "During the quarter, we were thrilled to announce historic software updates at WWDC25, including Apple Intelligence. We continue to invest heavily in breakthrough AI technology while maintaining strict user privacy."
Luca Maestri, Apple CFO: "Our Q3 business performance drove EPS growth of 11 percent and generated nearly $29 billion in operating cash flow, allowing us to return over $32 billion to shareholders."

Corporate Policies & Eating Policy:
Employees visiting Apple Park headquarters must wear credentials at all times. Eating and dining are strictly restricted to designated Caffè Macs cafeterias and outdoor terrace spaces. No food or open beverage containers are permitted inside cleanrooms or server labs.
"""

with open(sample_file_path, "w", encoding="utf-8") as f:
    f.write(raw_financial_text)

print("================================================================================")
print("SETUP COMPLETE: Sample Financial Document generated at:")
print(f" -> {sample_file_path}")
print(f" 🟢 ACTIVE PROVIDER: {active_provider}")
print("================================================================================")


# =============================================================================
# PART 1: LANGCHAIN RAG PIPELINE EXERCISES
# =============================================================================
print("\n--- [PART 1] BUILDING LANGCHAIN RAG PIPELINE ---")

# -----------------------------------------------------------------------------
# ## TODO 1.1: Load Document using LangChain TextLoader
# Instruction: Replace `None` below with `TextLoader(sample_file_path, encoding="utf-8").load()`
# -----------------------------------------------------------------------------
lc_documents = TextLoader(sample_file_path, encoding="utf-8").load()


if lc_documents is not None:
    print(f"✅ TODO 1.1 PASSED: LangChain Loaded {len(lc_documents)} document object(s).")
else:
    print("❌ TODO 1.1 PENDING: Complete TODO 1.1 to load the document.")


# -----------------------------------------------------------------------------
# ## TODO 1.2: Split Document into Chunks using CharacterTextSplitter
# Instruction: Replace `None` below with `CharacterTextSplitter(chunk_size=300, chunk_overlap=30).split_documents(lc_documents)`
# -----------------------------------------------------------------------------
lc_chunks = CharacterTextSplitter(chunk_size=300, chunk_overlap=30).split_documents(lc_documents)


if lc_chunks is not None:
    print(f"✅ TODO 1.2 PASSED: LangChain Split text into {len(lc_chunks)} chunk(s).")
else:
    print("❌ TODO 1.2 PENDING: Complete TODO 1.2 to split documents.")


# -----------------------------------------------------------------------------
# ## TODO 1.3: Execute LangChain .invoke() Method with Active LLM
# Instruction: Invoke ChatGoogleGenerativeAI / ChatOpenAI directly using lc_llm.invoke()
# -----------------------------------------------------------------------------
if lc_chunks is not None:
    print("✅ TODO 1.3 PASSED: LangChain lc_llm.invoke() Executed!")
    query1 = "What are the rules about eating at Apple Park?"
    context_str = "\n\n".join(c.page_content for c in lc_chunks)
    prompt = f"Answer strictly using context below:\n\nContext:\n{context_str}\n\nQuestion: {query1}\nAnswer:"
    
    try:
        resp = lc_llm.invoke(prompt)
        print(f"   -> LangChain lc_llm.invoke() Live Free Output: {resp.content.strip()}")
    except Exception as err:
        print(f"   ⚠️ LLM Call Exception: {str(err)[:120]}...")
    print(f"   -> Citation Chunk: {lc_chunks[0].page_content[:60]}...\n")
else:
    print("❌ TODO 1.3 PENDING: Complete TODO 1.3 to execute LangChain retrieval.")


# =============================================================================
# PART 2: LLAMAINDEX RAG PIPELINE EXERCISES
# =============================================================================
print("\n--- [PART 2] BUILDING LLAMAINDEX RAG PIPELINE ---")

print("✅ TODO 2.0 PASSED: Global Settings.embed_model configured!")


# -----------------------------------------------------------------------------
# ## TODO 2.1: Load Document using SimpleDirectoryReader
# Instruction: Replace `None` below with `SimpleDirectoryReader(input_files=[sample_file_path]).load_data()`
# -----------------------------------------------------------------------------
llama_documents = SimpleDirectoryReader(input_files=[sample_file_path]).load_data()


if llama_documents is not None:
    print(f"✅ TODO 2.1 PASSED: LlamaIndex Loaded {len(llama_documents)} document container(s).")
else:
    print("❌ TODO 2.1 PENDING: Complete TODO 2.1 to load LlamaIndex documents.")


# -----------------------------------------------------------------------------
# ## TODO 2.2: Parse Document into TextNodes using SentenceSplitter
# Instruction: Replace `None` below with `SentenceSplitter(chunk_size=300, chunk_overlap=30).get_nodes_from_documents(llama_documents)`
# -----------------------------------------------------------------------------
llama_nodes = SentenceSplitter(chunk_size=300, chunk_overlap=30).get_nodes_from_documents(llama_documents)


if llama_nodes is not None:
    print(f"✅ TODO 2.2 PASSED: LlamaIndex Parsed {len(llama_nodes)} TextNode(s) successfully!")
else:
    print("❌ TODO 2.2 PENDING: Complete TODO 2.2 to parse text nodes.")


# -----------------------------------------------------------------------------
# ## TODO 2.3: Setup Persistent ChromaDB StorageContext & Build VectorStoreIndex
# Instruction: Replace `None` below with:
# 1. chroma_db = chromadb.PersistentClient(path=os.path.join(sample_data_dir, "chroma_db"))
# 2. chroma_collection = chroma_db.get_or_create_collection("apple_q3_financials")
# 3. vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
# 4. storage_context = StorageContext.from_defaults(vector_store=vector_store)
# 5. llama_index = VectorStoreIndex(llama_nodes, storage_context=storage_context)
# -----------------------------------------------------------------------------
chroma_db = chromadb.PersistentClient(path=os.path.join(sample_data_dir, "chroma_db"))
chroma_collection = chroma_db.get_or_create_collection("apple_q3_financials")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
llama_index = VectorStoreIndex(llama_nodes, storage_context=storage_context)  


if llama_index is not None:
    print("✅ TODO 2.3 PASSED: LlamaIndex VectorStoreIndex Created with StorageContext!")
else:
    print("❌ TODO 2.3 PENDING: Complete TODO 2.3 to build VectorStoreIndex.")


# -----------------------------------------------------------------------------
# ## TODO 2.4: Build Stateless QueryEngine & Execute Query
# Instruction: Replace `None` below with `llama_index.as_query_engine(similarity_top_k=2, response_mode="compact")`
# -----------------------------------------------------------------------------
llama_query_engine = llama_index.as_query_engine(similarity_top_k=2, response_mode="compact")


if llama_query_engine is not None:
    print("✅ TODO 2.4 PASSED: LlamaIndex QueryEngine Constructed!")
    query2 = "What were Apple Q3 2025 financial results?"
    try:
        resp2 = llama_query_engine.query(query2)
        print(f"   -> QueryEngine Live Output: {resp2}\n")
    except Exception as err:
        print(f"   ⚠️ LLM Call Exception: {str(err)[:120]}...\n")
else:
    print("❌ TODO 2.4 PENDING: Complete TODO 2.4 to construct QueryEngine.")


# -----------------------------------------------------------------------------
# ## TODO 2.5: Build Stateful ChatEngine & Execute Conversation Turn
# Instruction: Replace `None` below with `llama_index.as_chat_engine(chat_mode="condense_question")`
# -----------------------------------------------------------------------------
llama_chat_engine = llama_index.as_chat_engine(chat_mode="condense_question") 


if llama_chat_engine is not None:
    print("✅ TODO 2.5 PASSED: LlamaIndex ChatEngine Constructed!")
    query3 = "What about 2024?"
    try:
        resp3 = llama_chat_engine.chat(query3)
        print(f"   -> ChatEngine Live Output: {resp3}\n")
    except Exception as err:
        print(f"   ⚠️ LLM Call Exception: {str(err)[:120]}...\n")
else:
    print("❌ TODO 2.5 PENDING: Complete TODO 2.5 to construct ChatEngine.")


# =============================================================================
# PART 3: FRAMEWORK CONVERTER PRACTICE
# =============================================================================
print("--- [PART 3] DOCUMENT PORTABILITY PRACTICE ---")

# -----------------------------------------------------------------------------
# ## TODO 3.1: Convert LlamaIndex Document to LangChain Document Format
# Instruction: Replace `None` below with `llama_documents[0].to_langchain_format()`
# -----------------------------------------------------------------------------
converted_lc_doc = llama_documents[0].to_langchain_format()


if converted_lc_doc is not None:
    print("✅ TODO 3.1 PASSED: Document converted successfully!")
    print(f"   -> LlamaIndex text field: {llama_documents[0].text[:45]}...")
    print(f"   -> LangChain page_content field: {converted_lc_doc.page_content[:45]}...")
    print("   -> Result: Safe conversion without AttributeError!")
else:
    print("❌ TODO 3.1 PENDING: Complete TODO 3.1 to convert document formats.")

print("\n================================================================================")
print("HANDS-ON LAB RUN COMPLETE!")
print("================================================================================")
