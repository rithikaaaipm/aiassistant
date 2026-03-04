import streamlit as st
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq

# 1. Setup & Load Secrets
load_dotenv()
st.set_page_config(page_title="ACME Security Bot", page_icon="🤖")
st.title("🤖 ACME Policy Assistant")

# 2. Initialize RAG (Cached so it only loads once) - replace api as required
@st.cache_resource
def init_rag():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # Point to your existing database folder
    vector_db = Chroma(persist_directory="./db_storage", embedding_function=embeddings)
   # We are passing the key directly to the "Manager" (ChatGroq)
    llm = ChatGroq(
        groq_api_key="api-key", 
        model_name="llama-3.3-70b-versatile", 
        temperature=0
    )
    return vector_db, llm

vector_db, llm = init_rag()

# 3. Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. The Chat Logic
# 4. Updated Chat Logic with Sources
if prompt := st.chat_input("Ask about ABC Corp policies..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # RAG Retrieval - Get the documents
    docs = vector_db.similarity_search(prompt, k=2)
    
    # Extract context and source information
    context = "\n".join([d.page_content for d in docs])
    sources = [f"📄 {d.metadata.get('source', 'Unknown')} (Page {d.metadata.get('page', '??')})" for d in docs]
    unique_sources = list(set(sources)) # Remove duplicates

    # Generate Response
    full_prompt = f"Use ONLY this context: {context}\n\nQuestion: {prompt}"
    response = llm.invoke(full_prompt)
    answer = response.content

    # Add assistant message to UI
    with st.chat_message("assistant"):
        st.markdown(answer)
        # Display the Sources in a nice "expander" box
        with st.expander("View Sources"):
            for s in unique_sources:
                st.write(s)
                
    st.session_state.messages.append({"role": "assistant", "content": answer})