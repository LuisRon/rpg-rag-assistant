from flask import Flask, render_template, request, jsonify
import ollama
import os
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

app = Flask(__name__)

# Load or create the vector database
print("Starting...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

if os.path.exists("./chroma_db"):
    print("Loading existing database...")
    db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
else:
    print("Reading PDF...")
    doc = fitz.open("AQUELARRE_EDICION_DEFINITIVA.pdf")
    texto_completo = ""
    for pagina in doc:
        texto_completo += pagina.get_text()

    print("Splitting text...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    fragmentos = splitter.create_documents([texto_completo])

    print("Creating vector database...")
    db = Chroma.from_documents(fragmentos, embeddings, persist_directory="./chroma_db")

print("Ready!\n")

# Chat history with system prompt
historial = [{"role": "system", "content": """You are an expert assistant for the Aquelarre tabletop RPG.
Answer based on the information provided from the manual.
Always respond in Spanish."""}]

def is_conversational(pregunta):
    """Check if the message is a casual greeting or conversational message."""
    keywords = ["hola", "buenos días", "buenas", "gracias", "adios", "hasta luego", "cómo estás"]
    return any(keyword in pregunta.lower() for keyword in keywords)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    pregunta = request.json.get("pregunta")

    if is_conversational(pregunta):
        # No need to search the manual for casual messages
        pregunta_con_contexto = f"{pregunta}\n\nResponde de forma natural y amigable como asistente de Aquelarre."
    else:
        # Search for relevant fragments in the manual
        resultados = db.similarity_search(pregunta, k=6)
        contexto = "\n\n".join([r.page_content for r in resultados])
        pregunta_con_contexto = f"""Context from the manual:\n{contexto}\n\nQuestion: {pregunta}"""

    historial.append({"role": "user", "content": pregunta_con_contexto})

    response = ollama.chat(model="llama3.1", messages=historial)
    respuesta = response.message.content

    historial.append({"role": "assistant", "content": respuesta})

    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(debug=True)