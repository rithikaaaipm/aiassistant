# 🤖 ABC Corp - Employee AI Assistant (RAG)

An intelligent Retrieval-Augmented Generation (RAG) system designed to reduce corporate compliance risks. This tool allows employees to query complex internal policies and receive instant, source-cited answers.

### 🌟 Key Features
* **Zero-Hallucination Guardrails:** Responses are strictly grounded in provided PDF context.
* **Source Transparency:** Every answer includes citations citing the exact document and page number.
* **Sub-second Inference:** Powered by Llama 3.3 via Groq for near-instant user experience.
* **Enterprise Security:** Built with environment variable protection (.env) and .gitignore protocols to prevent data/API leaks.

### 🛠️ Tech Stack
* **LLM:** Llama 3.3 (70B) via Groq Cloud
* **Orchestration:** LangChain
* **Vector Store:** ChromaDB
* **Interface:** Streamlit
