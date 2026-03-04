import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq

# --- STEP 0: CONFIGURATION ---repalce api key as required
GROQ_API_KEY = "api-key"
FILE_PATH = "data.pdf"

# --- STEP 1: LOAD & SPLIT PDF ---
print("1. Reading PDF...")
loader = PyPDFLoader(FILE_PATH)
pages = loader.load()

# Split into chunks so the AI doesn't get overwhelmed
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(pages)

# --- STEP 2: CREATE VECTOR DATABASE ---
print("2. Creating the 'Search Engine' (Embeddings)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# This creates the database in a folder called 'db_storage'
vector_db = Chroma.from_documents(
    documents=chunks, 
    embedding=embeddings, 
    persist_directory="./db_storage"
)

# --- STEP 3: SEARCH & ASK CLOUD AI ---
query = "Can I use ChatGPT for Level 3 data at ACME Corp?"
print(f"3. Searching for: {query}")

# Find the exact text in the PDF
relevant_docs = vector_db.similarity_search(query, k=1)
context = relevant_docs[0].page_content

print("4. Sending context to Cloud Llama (Groq)...")
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile", temperature=0)

prompt = f"Answer based ONLY on this text: {context}\n\nQuestion: {query}"
response = llm.invoke(prompt)

print("\n" + "="*40)
print("FINAL RESPONSE:")
print(response.content)
print("="*40)