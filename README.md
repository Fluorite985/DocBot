
# DocBot 🤖  
*A fully local, free, and private AI chatbot that answers questions based on your own documents.*

---

## 📘 Overview  
**DocBot** is a locally-run Retrieval-Augmented Generation (RAG) chatbot built using **LangChain**, **Ollama**, **ChromaDB**, and **Streamlit**. It allows you to ingest documents, generate embeddings, and query them via a **chat interface** through a **web UI**. No internet, no API keys, no cost.

---

## 🧩 Features  
- 🧠 **LLM-powered** question answering with local models via **Ollama**  
- 🗃️ Document chunking, indexing, and retrieval with **LangChain** and **ChromaDB**  
- 💬 Interactive chat via **Streamlit** web interface or terminal  
- 🔒 100% local — no external API calls, private by design  
- 🛠️ Modular, lightweight, and easy to extend  

---

## 🔧 Built With  
- [LangChain](https://github.com/langchain-ai/langchain)  
- [Ollama](https://ollama.com/) – for running open-source LLMs locally  
- [ChromaDB](https://www.trychroma.com/) – vector DB for embeddings  
- [Streamlit](https://streamlit.io/) – simple, fast web UI  
- Python 3.10+

---

## ⚙️ Getting Started  

### ✅ Prerequisites  
- Python 3.10+  
- [Ollama installed](https://ollama.com/download) and a model pulled (e.g. `mistral`)  
- Streamlit installed (`pip install streamlit`)  
- All Python dependencies (`pip install -r requirements.txt`)

---

### 🔧 Installation  
```bash
git clone https://github.com/Fluorite985/DocBot.git
cd DocBot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Ensure Ollama is running:
```bash
ollama run mistral
```

---

## 🚀 Usage

### 🧱 1. Prepare your documents:
```bash
python dataprep.py --input data/*.txt --output chunks/
```

### 🧠 2. Start the backend (retriever + LLM wrapper):
```bash
python chat_backend.py
```

### 💬 3.Load up the interface:

#### Terminal Chat  
```bash
python interface.py
```

## 🖥 Project Structure  
```
DocBot/
├── dataprep.py            # Document splitting & cleaning(Make sure to create a seperate folder)
├── embedding_function.py  # Function to import Ollama Embeddings
├── chat_backend.py        # Loads retriever & connects to Ollama
├── interface.py           # Web-based chat interface using StreamLit 
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## 📎 Example Use Cases  
- 📚 Query summaries or answers from technical documentation  
- 🧾 Search through meeting transcripts or legal docs  
- 🎓 Use as a local AI study assistant

---

## 🔒 Privacy & Cost  
- ✅ No cloud usage  
- ✅ No OpenAI API key needed  
- ✅ No fees, fully offline after setup

---

## 🤝 Contributing  
Feel free to open issues, suggest features, or submit pull requests to improve the UI, add PDF/document support, or enhance LLM interaction.

---
