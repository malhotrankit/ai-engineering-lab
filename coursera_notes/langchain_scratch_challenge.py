"""
================================================================================
LANGCHAIN CODE-FROM-SCRATCH HARD CHALLENGE LAB
(100% PURE DIRECT FRAMEWORK IMPORTS & LIVE GEMINI 2.5 FLASH)
================================================================================
Target Goal: Build a complete, production-grade Enterprise Contract RAG Pipeline 
in LangChain FROM SCRATCH with direct third-party package imports!

Instructions:
1. Write your full Python solution using direct package imports:
     from langchain_community.document_loaders import TextLoader
     from langchain_text_splitters import RecursiveCharacterTextSplitter
     from langchain_core.prompts import ChatPromptTemplate
     from langchain_core.runnables import RunnablePassthrough
     from langchain_core.output_parsers import StrOutputParser
2. Run the script using:
   .venv/bin/python coursera_notes/langchain_scratch_challenge.py
================================================================================
"""

from click import prompt
from openai import embeddings
import os
import sys
import warnings
import dotenv

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
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

try:
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain
    from langchain_classic.chains import create_retrieval_chain
except ModuleNotFoundError:
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain
    from langchain_classic.chains import create_retrieval_chain
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI

if openrouter_key:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model=FREE_OPENROUTER_MODEL,
        api_key=openrouter_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={"HTTP-Referer": "https://ai-engineering-lab.local", "X-Title": "AI Engineering Lab"}
    )
    active_provider = f"OPENROUTER FREE ({FREE_OPENROUTER_MODEL})"
elif gemini_key:
    from langchain_google_genai import ChatGoogleGenerativeAI
    os.environ["GEMINI_API_KEY"] = gemini_key
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
    active_provider = "GOOGLE GEMINI 2.5 FLASH"
else:
    print("❌ ERROR: Neither OPENROUTER_API_KEY nor GEMINI_API_KEY found in .env!")
    sys.exit(1)

# -----------------------------------------------------------------------------
# AUTOMATIC TEST DATASET GENERATOR (DO NOT MODIFY THIS BLOCK)
# -----------------------------------------------------------------------------
contract_dir = os.path.join(script_dir, "sample_data")
contract_file = os.path.join(contract_dir, "enterprise_contract.txt")
os.makedirs(contract_dir, exist_ok=True)

contract_text = """
ENTERPRISE SERVICE LEVEL AGREEMENT & MASTER SOFTWARE LICENSE (SLA-2025)
Contract ID: SLA-8849-CONFIDENTIAL

1. PARTIES & TERMINATION
This Agreement is entered into between Cyberdyne Cloud Systems ("Provider") and Apex Financial Group ("Client").
Either party may terminate this agreement with ninety (90) days written notice. Early termination by Client without cause incurs an early exit fee equal to two (2) months of average recurring billing.

2. SERVICE LEVEL AGREEMENT (SLA) & UPTIME GUARANTEE
Provider guarantees a monthly service uptime SLA of 99.95%, excluding scheduled maintenance windows.
Scheduled maintenance shall occur only between 01:00 AM and 04:00 AM UTC on Sundays, with at least 48 hours prior notification.
If monthly uptime falls below 99.95%, Provider shall credit Client 10% of monthly fee. If uptime falls below 99.0%, Provider shall credit Client 30% of monthly fee.

3. DATA RETENTION & SECURITY POLICIES
All client data stored in Provider's cloud infrastructure is encrypted in transit using TLS 1.3 and at rest using AES-256 encryption.
Upon contract termination, Provider shall purge and securely sanitize all Client data within thirty (30) days and provide a certified Certificate of Data Destruction.

4. LIABILITY & INDEMNIFICATION LIMITS
Provider's total aggregate liability under this agreement shall be capped at $2,000,000 USD or the total fees paid by Client in the preceding 12 months, whichever is lower. Neither party shall be liable for indirect, punitive, or consequential damages.
"""

with open(contract_file, "w", encoding="utf-8") as f:
    f.write(contract_text)

print("================================================================================")
print("CHALLENGE LAB INITIALIZED: Dataset generated at:")
print(f" -> {contract_file}")
print(f" 🟢 LIVE GEMINI 2.5 FLASH API ENABLED (Key starts with: {gemini_key[:10]}...)")
print("================================================================================\n")


# =============================================================================
# 🎯 YOUR CHALLENGE SPECIFICATION (WRITE YOUR CODE BELOW)
# =============================================================================
"""
REQUIREMENTS TO IMPLEMENT FROM SCRATCH:

1. FUNCTION: `build_contract_rag_system(file_path)`
   - Takes `file_path` ("sample_data/enterprise_contract.txt") as input.
   - Loads document using `TextLoader(file_path, encoding="utf-8")`.
   - Splits document using `RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=40)`.
   - Returns a callable function or list of chunks.

2. FUNCTION: `query_contract(chain, question)`
   - Executes query against live Gemini API using retrieved context.
"""

# =============================================================================
# WRITE YOUR LANGCHAIN IMPLEMENTATION BELOW THIS LINE
# =============================================================================

def build_contract_rag_system(file_path):
    docs = TextLoader(file_path, encoding = 'utf-8').load()
    chunks = RecursiveCharacterTextSplitter(chunk_size = 350, chunk_overlap = 40).split_documents(docs)
    embeddings = FastEmbedEmbeddings(model = "BAAI/bge-small-en-v1.5")
    vectorstore = Chroma.from_documents(chunks, embedding = embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    prompt = ChatPromptTemplate.from_messages([
    ('system', 'Answer strictly using context below. If unknown, say NOT FOUND IN CONTEXT:\n\n{context}'),
('human', '{input}')
])

    llm = ChatOpenAI(
        model="openrouter/free",
        temperature=0.0,  # <--- Set temperature here (0.0 = 100% deterministic)
        api_key=openrouter_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={"HTTP-Referer": "https://ai-engineering-lab.local", "X-Title": "AI Engineering Lab"}
    )
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, combine_docs_chain)
    return chain


def query_contract(chain, question):
    response = chain.invoke({'input': question})
    print('response', response)
    return response['answer']


# =============================================================================
# AUTOMATED VERIFICATION TEST SUITE (DO NOT MODIFY)
# =============================================================================
if __name__ == "__main__":
    print("--- [RUNNING VERIFICATION TEST SUITE] ---")
    
    try:
        rag_chain = build_contract_rag_system(contract_file)
        if rag_chain is None:
            print("❌ TEST FAILED: `build_contract_rag_system()` returned None. Implement the function first!")
            sys.exit(1)
            
        print("✅ STAGE 1 PASSED: Contract RAG System constructed.")
        
        # Test Query 1: Factual Extraction
        q1 = "What is the guaranteed monthly uptime SLA percentage?"
        a1 = query_contract(rag_chain, q1)
        print(f"\n[Test Q1]: {q1}")
        print(f"[Your Output]: {a1}")
        
        if a1 and ("99.95" in str(a1) or "SLA" in str(a1)):
            print("✅ TEST Q1 PASSED: Correctly retrieved SLA uptime guarantee!")
        else:
            print("⚠️ TEST Q1 WARNING: Check your retriever or prompt formatting.")

        # Test Query 2: Anti-Hallucination Guardrail
        q2 = "What is the penalty fee for late payment?"
        a2 = query_contract(rag_chain, q2)
        print(f"\n[Test Q2]: {q2}")
        print(f"[Your Output]: {a2}")
        
        if a2 and "NOT FOUND" in str(a2).upper():
            print("✅ TEST Q2 PASSED: Strict anti-hallucination guardrail succeeded!")
        else:
            print("⚠️ TEST Q2 WARNING: Expected 'NOT FOUND IN CONTRACT' for missing facts.")
            
        print("\n================================================================================")
        print("CONGRATULATIONS! If all tests passed, you built a production LCEL RAG chain from scratch!")
        print("================================================================================")

    except NotImplementedError:
        print("❌ LAB INCOMPLETE: Implement `build_contract_rag_system()` and run again.")
    except Exception as e:
        print(f"❌ EXECUTION ERROR: {e}")
