"""
================================================================================
LLAMAINDEX CODE-FROM-SCRATCH HARD CHALLENGE LAB
(100% PURE DIRECT FRAMEWORK IMPORTS & LIVE GEMINI 2.5 FLASH)
================================================================================
Target Goal: Build a complete, production-grade Technical Support RAG System
in LlamaIndex FROM SCRATCH with direct third-party package imports!

Instructions:
1. Write your full Python solution using direct package imports:
     from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, PromptTemplate, Settings
     from llama_index.core.node_parser import SentenceSplitter
2. Run the script using:
   .venv/bin/python coursera_notes/llamaindex_scratch_challenge.py
================================================================================
"""

from llama_index.embeddings.fastembed import FastEmbedEmbedding
import os
import sys
import warnings
import dotenv

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

FREE_OPENROUTER_MODEL = "openrouter/free"

# 2. Pure Direct Production Package Imports
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, PromptTemplate, Settings
from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter

if openrouter_key:
    from llama_index.llms.openai_like import OpenAILike
    llm = OpenAILike(
        model=FREE_OPENROUTER_MODEL,
        temperature=0.0,
        api_key=openrouter_key,
        api_base="https://openrouter.ai/api/v1",
        is_chat_model=True
    )
    Settings.llm = llm
    active_provider = f"OPENROUTER FREE ({FREE_OPENROUTER_MODEL})"
elif gemini_key:
    from llama_index.llms.google_genai import GoogleGenAI
    os.environ["GEMINI_API_KEY"] = gemini_key
    llm = GoogleGenAI(model="gemini-2.5-flash", temperature=0.0)
    Settings.llm = llm
    active_provider = "GOOGLE GEMINI 2.5 FLASH"
else:
    print("❌ ERROR: Neither OPENROUTER_API_KEY nor GEMINI_API_KEY found in .env!")
    sys.exit(1)

# -----------------------------------------------------------------------------
# AUTOMATIC TEST DATASET GENERATOR (DO NOT MODIFY THIS BLOCK)
# -----------------------------------------------------------------------------
docs_dir = os.path.join(script_dir, "sample_data", "tech_support")
doc_file = os.path.join(docs_dir, "api_support_guide.txt")
os.makedirs(docs_dir, exist_ok=True)

technical_doc_text = """
APEX CLOUD PLATFORM TECHNICAL SUPPORT & API RATE LIMIT SPECIFICATION (v3.4)
Document ID: TECH-SUP-2025-REVISION-A

1. API RATE LIMITS & THROTTLING
The Apex Cloud Platform enforces tiered rate limiting across all REST endpoints:
- Developer Tier: 60 requests per minute per IP address. Burst limit: 10 requests per second.
- Enterprise Tier: 5,000 requests per minute per tenant API key. Burst limit: 500 requests per second.
Exceeding rate limits triggers an HTTP 429 Too Many Requests response with a Retry-After header.

2. AUTHENTICATION & TOKEN EXPIRATION
All API requests must pass a Bearer JSON Web Token (JWT) in the Authorization header.
Tokens expire after exactly two (2) hours. Refresh tokens are valid for fourteen (14) days.
Failed authentication returns HTTP 401 Unauthorized.

3. TECHNICAL SUPPORT INCIDENT SEVERITY & SLA RESPONSE TIMES
- Severity 1 (Critical Outage): Core API service down for all tenants. Target SLA Response Time: 15 minutes.
- Severity 2 (Major Impairment): Key features degraded with no workaround. Target SLA Response Time: 1 hour.
- Severity 3 (Minor Issue): General bugs or documentation inquiries. Target SLA Response Time: 24 hours.

4. SYSTEM MAINTENANCE & LOG RETENTION
Application access logs and audit trails are retained in cloud cold storage for three hundred sixty-five (365) days before permanent automated purging.
"""

with open(doc_file, "w", encoding="utf-8") as f:
    f.write(technical_doc_text)

print("================================================================================")
print("CHALLENGE LAB INITIALIZED: Dataset generated at:")
print(f" -> {doc_file}")
print(f" 🟢 LIVE GEMINI 2.5 FLASH API ENABLED (Key starts with: {gemini_key[:10]}...)")
print("================================================================================\n")


# =============================================================================
# 🎯 YOUR CHALLENGE SPECIFICATION (WRITE YOUR CODE BELOW)
# =============================================================================
"""
REQUIREMENTS TO IMPLEMENT FROM SCRATCH:

1. FUNCTION: `build_llamaindex_rag_system(data_dir)`
   - Takes `data_dir` ("sample_data/tech_support") as input.
   - Loads documents using `SimpleDirectoryReader(input_dir=data_dir)`.
   - Parses text using `SentenceSplitter(chunk_size=300, chunk_overlap=30)`.
   - Returns a tuple `(query_engine, chat_engine)` or list of nodes.

2. FUNCTION: `query_tech_docs(query_engine, question)`
   - Executes query and returns string output.

3. FUNCTION: `chat_tech_docs(chat_engine, question)`
   - Executes chat and returns string output.
"""

# =============================================================================
# WRITE YOUR LLAMAINDEX IMPLEMENTATION BELOW THIS LINE
# =============================================================================

def build_llamaindex_rag_system(data_dir):
    qa_prompt_str = (
        "Context information is below:\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, answer the query.\n"
        "If the answer is not mentioned in the context, respond strictly with 'NOT FOUND IN TECHNICAL DOCS'.\n\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt = PromptTemplate(qa_prompt_str)
    Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
    docs = SimpleDirectoryReader(input_dir=data_dir).load_data()
    nodes = SentenceSplitter(chunk_size=300, chunk_overlap=30).get_nodes_from_documents(docs)
    index = VectorStoreIndex(nodes)
    query_engine = index.as_query_engine(similarity_top_k=3, text_qa_template=qa_prompt)
    chat_engine = index.as_chat_engine(chat_mode="condense_question",similarity_top_k=3,text_qa_template=qa_prompt)
    
    return query_engine, chat_engine


def query_tech_docs(query_engine, question):
    response = query_engine.query(question)
    return response.response


def chat_tech_docs(chat_engine, question):
    response = chat_engine.chat(question)
    return response.response


# =============================================================================
# AUTOMATED VERIFICATION TEST SUITE (DO NOT MODIFY)
# =============================================================================
if __name__ == "__main__":
    print("--- [RUNNING LLAMAINDEX VERIFICATION TEST SUITE] ---")
    
    try:
        result = build_llamaindex_rag_system(docs_dir)
        if result is None or len(result) != 2:
            print("❌ TEST FAILED: `build_llamaindex_rag_system()` must return tuple `(query_engine, chat_engine)`. Implement the function first!")
            sys.exit(1)
            
        q_engine, c_engine = result
        print("✅ STAGE 1 PASSED: LlamaIndex QueryEngine & ChatEngine constructed.")
        
        # Test Query 1: Factual Extraction via QueryEngine
        q1 = "What is the target SLA response time for Severity 1 Critical Outages?"
        a1 = query_tech_docs(q_engine, q1)
        print(f"\n[Test Q1]: {q1}")
        print(f"[Your Output]: {a1}")
        
        if a1 and ("15 minutes" in str(a1) or "15 min" in str(a1)):
            print("✅ TEST Q1 PASSED: QueryEngine correctly retrieved SLA response time!")
        else:
            print("⚠️ TEST Q1 WARNING: Check your retriever, chunking, or prompt template.")

        # Test Query 2: Anti-Hallucination Guardrail
        q2 = "What is the penalty fee for database query timeout?"
        a2 = query_tech_docs(q_engine, q2)
        print(f"\n[Test Q2]: {q2}")
        print(f"[Your Output]: {a2}")
        
        if a2 and "NOT FOUND" in str(a2).upper():
            print("✅ TEST Q2 PASSED: Strict anti-hallucination guardrail succeeded!")
        else:
            print("⚠️ TEST Q2 WARNING: Expected 'NOT FOUND IN TECHNICAL DOCS' for missing facts.")

        # Test Query 3: Multi-Turn Conversation via ChatEngine
        q3_turn1 = "What is the JWT token expiration time for Developer Tier?"
        a3_t1 = chat_tech_docs(c_engine, q3_turn1)
        print(f"\n[Test Q3 Turn 1]: {q3_turn1}")
        print(f"[Your Output]: {a3_t1}")

        q3_turn2 = "What about refresh tokens?"
        a3_t2 = chat_tech_docs(c_engine, q3_turn2)
        print(f"\n[Test Q3 Turn 2 (Follow-up)]: {q3_turn2}")
        print(f"[Your Output]: {a3_t2}")

        if a3_t2 and ("14 days" in str(a3_t2) or "fourteen" in str(a3_t2).lower()):
            print("✅ TEST Q3 PASSED: ChatEngine successfully resolved multi-turn follow-up question!")
        else:
            print("⚠️ TEST Q3 WARNING: ChatEngine should rewrite follow-up query using chat history.")

        print("\n================================================================================")
        print("CONGRATULATIONS! If all tests passed, you built a production LlamaIndex RAG system from scratch!")
        print("================================================================================")

    except NotImplementedError:
        print("❌ LAB INCOMPLETE: Implement `build_llamaindex_rag_system()` and run again.")
    except Exception as e:
        print(f"❌ EXECUTION ERROR: {e}")
