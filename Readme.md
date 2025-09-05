# 📄 Agent PDF Intelligent avec Mistral et LangChain

Ce projet permet de poser des **questions directement à un PDF** en utilisant un agent intelligent.  
Il combine la puissance de **LangChain**, **FAISS**, **MistralChat via Agno**, et **Rich** pour créer une interface interactive dans le terminal.

---

## ⚙️ Fonctionnalités

- Charger un fichier PDF et extraire son texte  
- Découper le texte en **chunks** pour un traitement efficace  
- Créer un **vector store** avec embeddings pour la recherche sémantique  
- Poser des questions au PDF et obtenir des réponses contextualisées  
- Interface console **colorée et interactive** grâce à **Rich**

---

## 🛠 Technologies utilisées

- **Python 3.11+**  
- **PyPDF2** pour lire les fichiers PDF  
- **LangChain** pour la découpe et vectorisation du texte  
- **FAISS** pour la recherche sémantique  
- **HuggingFace Embeddings** (`sentence-transformers/all-mpnet-base-v2`)  
- **Agno + MistralChat** pour l’agent intelligent  
- **Rich** pour l’affichage interactif dans le terminal  
- **python-dotenv** pour gérer les variables d’environnement (clé API Mistral)

---

## 🔧 Installation et utilisation

1. **Cloner le dépôt :**  
```bash
git clone https://github.com/ton-utilisateur/Nouridouine.mt.git
cd Nouridouine.mt
