# RAG Based LLM AI Chatbot - Assistant Intelligent ISO & RH 🤖

Assistant intelligent basé sur RAG (Retrieval-Augmented Generation) spécialisé dans les normes ISO et documents RH. Utilise une stack open source (Llama 3.2, BGE Embeddings, et Qdrant) pour fournir des réponses précises avec **citation des sources**.

![RAG Based LLM AI Chatbot](sct.png)

## 🎯 Nouveautés

Cette version améliorée offre:
- ✅ **Support Multi-Format**: PDF, Excel (.xlsx, .xls), Word (.docx, .doc)
- ✅ **Citations Précises**: Chaque réponse cite le document exact, la page/feuille, et la section
- ✅ **Traitement Automatique**: Indexe automatiquement tous les documents du dossier `data/`
- ✅ **Interface Améliorée**: Gestion de base de connaissances et affichage des sources
- ✅ **Expert ISO & RH**: Optimisé pour les normes ISO et documents de ressources humaines

## 🛠️ Fonctionnalités

- **📂 Support Multi-Format**: Traitez automatiquement vos documents PDF, Excel et Word
- **📍 Citations Précises**: Chaque réponse indique exactement d'où provient l'information
- **🧠 Indexation Automatique**: Scanne récursivement tous vos documents dans `data/docs/`
- **🤖 Chatbot Intelligent**: Répond en français avec contexte et sources
- **📊 Base de Connaissances**: Visualisez vos documents indexés avec statistiques
- **🔄 Réindexation Flexible**: Mise à jour incrémentale ou complète de votre base
- **🌟 Interface Intuitive**: Application Streamlit moderne et responsive

## 📋 Exemple de Réponse avec Sources

```
Question: "Quels sont les principes de management de la qualité selon ISO 9000?"

Réponse: Les principes de management de la qualité selon ISO 9000 incluent:
1. Orientation client
2. Leadership 
3. Implication du personnel
[...]

---

📚 Sources:

1. ISO 9000v2015.pdf (ISO Standard)
   - Localisation: Page 12, Page 13
   - Extrait: "Les sept principes de management de la qualité sont..."
```

## 🚀 Démarrage Rapide

## 🖥️ Tech Stack

The Document Buddy App leverages a combination of cutting-edge technologies to deliver a seamless and efficient user experience. Here's a breakdown of the technologies and tools used:

- **[LangChain](https://langchain.readthedocs.io/)**: Utilized as the orchestration framework to manage the flow between different components, including embeddings creation, vector storage, and chatbot interactions.
  
- **[Unstructured](https://github.com/Unstructured-IO/unstructured)**: Employed for robust PDF processing, enabling the extraction and preprocessing of text from uploaded PDF documents.
  
- **[BGE Embeddings from HuggingFace](https://huggingface.co/BAAI/bge-small-en)**: Used to generate high-quality embeddings for the processed documents, facilitating effective semantic search and retrieval.
  
- **[Qdrant](https://qdrant.tech/)**: A vector database running locally via Docker, responsible for storing and managing the generated embeddings for fast and scalable retrieval.
  
- **[LLaMA 3.2 via Ollama](https://ollama.com/)**: Integrated as the local language model to power the chatbot, providing intelligent and context-aware responses based on the document embeddings.
  
- **[Streamlit](https://streamlit.io/)**: The core framework for building the interactive web application, offering an intuitive interface for users to upload documents, create embeddings, and interact with the chatbot.

## 📁 Structure du Projet

```
RAG-Based-LLM-Chatbot/
│── config.py                 # Configuration centralisée
├── document_processor.py     # Traitement PDF/Excel/Word avec métadonnées
├── vectors.py                 # Gestion des embeddings et Qdrant
├── chatbot.py                 # Chatbot avec citations des sources
├── batch_indexer.py           # Script d'indexation par lot
├── new.py                     # Application Streamlit
├── requirements.txt           # Dépendances Python
├── GUIDE_UTILISATION.md       # Guide détaillé en français
└── data/
- `openpyxl` - Lecture/écriture de fichiers Excel (.xlsx)
- `python-docx` - Traitement de documents Word (.docx)
- `pandas` - Manipulation de données Excel
- `tqdm` - Barres de progression pour l'indexation

## ✨ Améliorations Principales

### 1. Support Multi-Format
- **PDF**: Extraction avec numéros de page
- **Excel**: Lecture de toutes les feuilles avec noms de colonnes
- **Word**: Extraction de paragraphes et tableaux

### 2. Citations des Sources
Chaque réponse inclut automatiquement:
- Nom du document source
- Localisation précise (page, feuille, section)
- Extrait pertinent du texte
- Type de document (ISO, RH, Procédure)

### 3. Interface Améliorée
- **Base de Connaissances**: Visualisation des documents indexés
- **Statistiques**: Nombre de documents par type
- **Réindexation**: Options incrémentale ou complète

### 4. Traitement Automatique
- Scan récursif de tous les sous-dossiers
- Gestion intelligente des erreurs
- Logs détaillés du processus

Contributions are welcome! Whether it’s reporting a bug, suggesting a feature, or submitting a pull request, your input is highly appreciated. Follow these steps to contribute:

1.	Fork the Repository: Click on the “Fork” button at the top-right corner of the repository page.
2.	Clone Your Fork
3.	Create a New Branch:

```
git checkout -b feature/YourFeatureName
```


4.	Make Your Changes: Implement your feature or fix.
5.	Commit Your Changes:

```
git commit -m "Add Your Feature Description"
```


6.	Push to Your Fork:

```
git push origin feature/YourFeatureName
```


7.	Create a Pull Request: Navigate to the original repository and create a pull request from your fork.


### 🔗 Useful Links


•	Streamlit Documentation: https://docs.streamlit.io/

•	LangChain Documentation: https://langchain.readthedocs.io/

•	Qdrant Documentation: https://qdrant.tech/documentation/

•	ChatOllama Documentation: https://github.com/langchain-ai/langchain-llms#ollama

Happy coding! 🚀✨

## ©️ License 🪪 

Distributed under the MIT License. See `LICENSE` for more information.

---

#### **If you like this LLM Project do drop ⭐ to this repo**
#### Follow me on [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gurpreetkaurjethra/) &nbsp; [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/GURPREETKAURJETHRA/)

---
