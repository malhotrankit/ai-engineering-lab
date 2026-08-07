"""
===============================================================================
LLAMAINDEX ICEBREAKER BOT: CLEAN ANNOTATED IMPLEMENTATION
===============================================================================
This file demonstrates the core business logic of Course 2 Module 3 Lab:
"Build an AI Icebreaker Bot with LlamaIndex & IBM Granite".

It strips out the clunky Gradio UI boilerplate (Part 8) and CLI loop (Part 7)
to focus 100% on the core LlamaIndex RAG pipeline:
  1. Loading profile documents via SimpleDirectoryReader.
  2. Building a VectorStoreIndex.
  3. Configuring custom PromptTemplates for Icebreaker generation.
  4. Executing queries using QueryEngine.
===============================================================================
"""

import os
import warnings

# Suppress transformer / deprecation warnings
warnings.filterwarnings('ignore')

from llama_index.core import (
    SimpleDirectoryReader, 
    VectorStoreIndex, 
    PromptTemplate, 
    Settings
)
from llama_index.core.node_parser import SentenceSplitter

# -----------------------------------------------------------------------------
# STEP 1: CREATE MOCK LINKEDIN PROFILE DATA
# -----------------------------------------------------------------------------
# In the lab, a text file containing a person's resume or LinkedIn profile is loaded.
profile_filename = "linkedin_profile_sample.txt"

sample_profile_text = """
Name: Sarah Connor
Current Role: Lead AI Engineer at Cyberdyne Systems (San Francisco, CA)
Summary: Experienced software engineer specializing in autonomous agent workflows, distributed systems, and modern RAG architectures.
Background: 
 - 8+ years building enterprise microservices in Python and Java.
 - Spoke at PyCon 2025 on 'Scaling Vector Databases with Hybrid Search'.
 - Passionate about open-source LLM evaluation, marathon running, and espresso brewing.
Recent Projects:
 - Built a real-time earnings call extractor processing 10,000+ SEC filings daily.
 - Contributed to LlamaIndex core node parser modules.
"""

if not os.path.exists(profile_filename):
    with open(profile_filename, "w", encoding="utf-8") as f:
        f.write(sample_profile_text)
    print(f"Created sample profile: {profile_filename}")


# -----------------------------------------------------------------------------
# STEP 2: LOAD & CHUNK DOCUMENT USING LLAMAINDEX
# -----------------------------------------------------------------------------
# SimpleDirectoryReader automatically reads the text file into a LlamaIndex Document object.
reader = SimpleDirectoryReader(input_files=[profile_filename])
documents = reader.load_data()
print(f"Loaded {len(documents)} document container.")

# SentenceSplitter chops the text into TextNode instances.
node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
nodes = node_parser.get_nodes_from_documents(documents)
print(f"Generated {len(nodes)} TextNode chunks.")


# -----------------------------------------------------------------------------
# STEP 3: BUILD VECTORSTOREINDEX
# -----------------------------------------------------------------------------
# VectorStoreIndex handles embedding generation and vector store indexing.
# (In the lab, IBM Granite LLM & Watsonx Embeddings are set globally via Settings.llm & Settings.embed_model)
index = VectorStoreIndex(nodes)
print("VectorStoreIndex constructed successfully.")


# -----------------------------------------------------------------------------
# STEP 4: CUSTOM ICEBREAKER PROMPT TEMPLATE
# -----------------------------------------------------------------------------
# Custom prompt instructing the LLM to synthesize icebreakers from retrieved profile context.
icebreaker_prompt_str = """
You are an expert networking assistant preparing a senior executive for a meeting.
Using ONLY the candidate profile information below, generate:
  1. A 2-sentence summary of the candidate's core background.
  2. Two interesting facts about the candidate.
  3. One personalized, highly engaging icebreaker conversation starter for a meeting.

Candidate Profile Context:
-------------------------
{context_str}
-------------------------

User Instruction: {query_str}
Response:
"""

custom_prompt = PromptTemplate(icebreaker_prompt_str)


# -----------------------------------------------------------------------------
# STEP 5: QUERY ENGINE CREATION & EXECUTION
# -----------------------------------------------------------------------------
# `as_query_engine` combines retrieval, prompt injection, and LLM generation into 1 line!
query_engine = index.as_query_engine(
    text_qa_template=custom_prompt,
    similarity_top_k=3
)

print("\n--- EXECUTING ICEBREAKER GENERATION QUERY ---")
response = query_engine.query("Generate meeting icebreakers for Sarah Connor.")

print("\nAI ICEBREAKER BOT RESPONSE:")
print(response)

print("\n===============================================================================")
print("ICEBREAKER RAG PIPELINE COMPLETE!")
print("===============================================================================")
