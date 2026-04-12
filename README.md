# RPG Assistant (RAG-based)

A RAG-based chatbot that answers questions about any tabletop RPG using its official manual in PDF format. Built and tested with the Aquelarre RPG.

## Tech Stack
- Python + Flask
- Ollama (llama3.1)
- LangChain + ChromaDB
- HuggingFace Embeddings

## Requirements
- Ollama installed with llama3.1 model
- Any RPG manual in PDF format. Rename it to match the filename in `app.py` or update the filename in the code.

## Installation

1. Create and activate a virtual environment:
```bash
py -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install flask ollama langchain langchain-community langchain-text-splitters chromadb sentence-transformers PyMuPDF
```

3. Run the app:
```bash
python app.py
```

4. Open your browser at `http://localhost:5000`

## How it works
The app reads the Aquelarre PDF, splits it into fragments and stores them in a ChromaDB vector database. When you ask a question, it searches for the most relevant fragments and passes them to the llama3.1 model to generate an answer.