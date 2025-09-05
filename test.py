import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from agno.agent import Agent
from agno.models.mistral import MistralChat
from rich.console import Console
from rich.panel import Panel

# ----------------------------
# 1️⃣ Initialisation
# ----------------------------
load_dotenv()  # Assure-toi que .env contient MISTRAL_API_KEY
console = Console()

# ----------------------------
# 2️⃣ Charger le PDF
# ----------------------------
def load_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# ----------------------------
# 3️⃣ Découper le texte en chunks
# ----------------------------
def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return [chunk for chunk in splitter.split_text(text) if chunk.strip()]

# ----------------------------
# 4️⃣ Créer le vector store avec embeddingswg
# ----------------------------
def create_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore

# ----------------------------
# 5️⃣ Créer l'agent et lui donner accès au vector store
# ----------------------------
def create_agent(vectorstore):
    model = MistralChat()
    agent = Agent(model=model)
    agent.add_to_knowledge(query="PDF", result={"vectorstore": vectorstore})
    return agent

# ----------------------------
# 6️⃣ Fonction principale
# ----------------------------
def main():
    pdf_path = "a.pdf"  # Remplace par ton PDF
    text = load_pdf(pdf_path)
    console.print(f"[green][DEBUG][/green] PDF loaded, total characters: {len(text)}")

    chunks = split_text(text)
    console.print(f"[green][DEBUG][/green] PDF split into {len(chunks)} chunks")

    vectorstore = create_vectorstore(chunks)
    agent = create_agent(vectorstore)

    console.print("[bold green]Agent prêt ! Pose tes questions (tape 'exit' pour quitter)[/bold green]\n")

    while True:
        query = console.input("[bold yellow]Question:[/bold yellow] ")
        if query.lower() == "exit":
            break

        # Récupérer les chunks pertinents depuis FAISS
        docs = vectorstore.similarity_search(query, k=3)
        context_text = " ".join([doc.page_content for doc in docs])

        # Lancer l'agent avec le contexte
        response = agent.run(
            f"Using the following text from the PDF, answer the question:\n{context_text}\nQuestion: {query}"
        )

        # Affichage formaté avec Rich
        if hasattr(response, "content") and response.content:
            console.print(Panel(response.content, title="Réponse", border_style="cyan", expand=False))
        else:
            console.print(Panel(str(response), title="Réponse", border_style="red", expand=False))

# ----------------------------
# 7️⃣ Lancer le script
# ----------------------------
if __name__ == "__main__":
    main()
