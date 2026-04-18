# RPG Assistant (RAG-based)

A RAG-based chatbot that answers questions about any document in PDF format.

## Features
- Upload any PDF directly from the web interface
- Ask questions about the document content
- Conversational chat with context memory
- Medieval dark theme UI

## Tech Stack
- Python + Flask
- Ollama (llama3.1)
- LangChain + ChromaDB
- HuggingFace Embeddings

## Requirements
- Ollama installed with llama3.1 model (`ollama pull llama3.1`)
- Python 3.10+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tuusuario/pdf-assistant.git
cd pdf-assistant
```

2. Create and activate a virtual environment:
```bash
py -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask ollama langchain langchain-community langchain-text-splitters chromadb sentence-transformers PyMuPDF
```

4. Run the app:
```bash
python app.py
```

5. Open your browser at `http://localhost:5000`

## How it works
Upload any PDF using the interface. The app splits it into fragments, stores them
in a ChromaDB vector database, and uses llama3.1 to answer questions based on
the document content. Each new PDF upload replaces the previous database.