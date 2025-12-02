# new.py

"""
Enhanced Streamlit app for RAG-based ISO & RH intelligent assistant.
Supports automatic document processing from data directory with source citations.
"""

import streamlit as st
from streamlit import session_state
import time
import os
from pathlib import Path
import config
from vectors import EmbeddingsManager
from chatbot import ChatbotManager
from qdrant_client import QdrantClient


# Initialize session_state variables if not already present
if 'chatbot_manager' not in st.session_state:
    st.session_state['chatbot_manager'] = None

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'documents_indexed' not in st.session_state:
    st.session_state['documents_indexed'] = False

# Set the page configuration
st.set_page_config(
    page_title="Assistant Intelligent ISO & RH",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.write("DEBUG: App is loading...")
print("DEBUG: App script started")


# Sidebar
print("DEBUG: Sidebar starting")
with st.sidebar:
    st.image("logo.png", use_column_width=True) if os.path.exists("logo.png") else st.markdown("# 📚")
    st.markdown("### Assistant Intelligent ISO & RH")
    st.markdown("Expert en normes ISO et documents RH")
    st.markdown("---")
    
    # Navigation Menu
    menu = ["🏠 Accueil", "📚 Base de Connaissances", "💬 Chatbot", "📧 Contact"]
    choice = st.selectbox("Navigation", menu)

# Helper function to check if documents are indexed
def check_documents_indexed():
    """Check if there are documents in the Qdrant collection."""
    try:
        client = QdrantClient(url=config.QDRANT_URL, prefer_grpc=False)
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]
        return config.COLLECTION_NAME in collection_names
    except:
        return False

# Home Page
if choice == "🏠 Accueil":
    st.title("📚 Assistant Intelligent ISO & RH")
    st.markdown("""
    Bienvenue dans votre assistant intelligent spécialisé en normes ISO et documents RH ! 🚀

    **Fonctionnalités:**
    - 📄 **Support Multi-Format**: Traite automatiquement vos documents PDF, Excel et Word
    - 🤖 **Réponses Précises**: Répond à vos questions avec des citations exactes des sources
    - 📍 **Localisation**: Indique précisément la page, feuille ou section d'où provient l'information
    - 🔍 **Base de Connaissances**: Indexe automatiquement tous vos documents
    
    **Documents Supportés:**
    - 📑 Normes ISO (PDF)
    - 📊 Formulaires et tableaux RH (Excel)
    - 📝 Procédures et documents (Word)

    ---
    
    ### 🚀 Démarrage Rapide
    
    1. Placez vos documents dans le dossier `data/docs/`
    2. Allez dans "📚 Base de Connaissances" pour indexer vos documents
    3. Utilisez le "💬 Chatbot" pour poser vos questions
    
    L'assistant citera automatiquement ses sources avec précision ! 😊
    """)

# Knowledge Base Page
elif choice == "📚 Base de Connaissances":
    st.title("📚 Base de Connaissances")
    st.markdown("---")
    
    # Check if documents are already indexed
    is_indexed = check_documents_indexed()
    
    if is_indexed:
        st.success("✅ Des documents sont déjà indexés dans la base de connaissances")
    else:
        st.info("ℹ️ Aucun document indexé. Cliquez sur 'Indexer les Documents' ci-dessous.")
    
    # Display data directory info
    st.subheader("📁 Répertoire de Documents")
    st.code(str(config.DATA_DIR))
    
    if config.DATA_DIR.exists():
        # Count files by type
        pdf_files = list(config.DATA_DIR.rglob("*.pdf"))
        excel_files = list(config.DATA_DIR.rglob("*.xlsx")) + list(config.DATA_DIR.rglob("*.xls"))
        word_files = list(config.DATA_DIR.rglob("*.docx")) + list(config.DATA_DIR.rglob("*.doc"))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 PDF", len(pdf_files))
        with col2:
            st.metric("📊 Excel", len(excel_files))
        with col3:
            st.metric("📝 Word", len(word_files))
        
        total_files = len(pdf_files) + len(excel_files) + len(word_files)
        
        if total_files > 0:
            st.markdown("---")
            st.subheader("📋 Documents Disponibles")
            
            # Display files in an expander
            with st.expander(f"Voir les {total_files} documents"):
                if pdf_files:
                    st.markdown("**📄 Fichiers PDF:**")
                    for f in pdf_files:
                        st.markdown(f"- {f.name}")
                
                if excel_files:
                    st.markdown("**📊 Fichiers Excel:**")
                    for f in excel_files:
                        st.markdown(f"- {f.name}")
                
                if word_files:
                    st.markdown("**📝 Fichiers Word:**")
                    for f in word_files:
                        st.markdown(f"- {f.name}")
    else:
        st.warning(f"⚠️ Le répertoire {config.DATA_DIR} n'existe pas.")
        total_files = 0
    
    # Indexing section
    st.markdown("---")
    st.subheader("🔄 Indexation des Documents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        force_reindex = st.checkbox("🔁 Forcer la réindexation complète", 
                                     help="Supprime l'index existant et réindexe tous les documents")
    
    with col2:
        if st.button("🚀 Indexer les Documents", type="primary"):
            if total_files == 0:
                st.error("❌ Aucun document trouvé à indexer")
            else:
                with st.spinner(f"🔄 Indexation de {total_files} documents en cours..."):
                    try:
                        # Create embeddings manager
                        embeddings_manager = EmbeddingsManager()
                        
                        # Load and index documents
                        result = embeddings_manager.load_directory_and_embed(
                            str(config.DATA_DIR),
                            force_recreate=force_reindex
                        )
                        
                        st.success(result)
                        st.session_state['documents_indexed'] = True
                        
                        # Initialize chatbot if not already done
                        if st.session_state['chatbot_manager'] is None:
                            st.session_state['chatbot_manager'] = ChatbotManager()
                            st.info("✅ Chatbot initialisé et prêt à répondre à vos questions!")
                        
                        time.sleep(1)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de l'indexation: {e}")
                        import traceback
                        with st.expander("voir les détails de l'erreur"):
                            st.code(traceback.format_exc())

# Chatbot Page
elif choice == "💬 Chatbot":
    st.title("💬 Assistant Intelligent")
    st.markdown("Posez vos questions sur les normes ISO et documents RH")
    st.markdown("---")
    
    # Check if documents are indexed
    if not check_documents_indexed():
        st.warning("⚠️ Aucun document indexé. Veuillez d'abord indexer vos documents dans la section '📚 Base de Connaissances'.")
        if st.button("Aller à la Base de Connaissances"):
            st.session_state['nav_choice'] = "📚 Base de Connaissances"
            st.rerun()
    else:
        # Initialize chatbot if not already done
        if st.session_state['chatbot_manager'] is None:
            with st.spinner("🔄 Initialisation du chatbot..."):
                try:
                    st.session_state['chatbot_manager'] = ChatbotManager()
                    st.success("✅ Chatbot initialisé!")
                    time.sleep(0.5)
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'initialisation: {e}")
        
        if st.session_state['chatbot_manager'] is not None:
            # Display existing messages
            for msg in st.session_state['messages']:
                st.chat_message(msg['role']).markdown(msg['content'])

            # User input
            if user_input := st.chat_input("Posez votre question ici..."):
                # Display user message
                st.chat_message("user").markdown(user_input)
                st.session_state['messages'].append({"role": "user", "content": user_input})

                with st.spinner("🤖 Recherche et analyse en cours..."):
                    try:
                        # Get the chatbot response
                        response = st.session_state['chatbot_manager'].get_response(user_input)
                        answer = response['answer']
                        
                    except Exception as e:
                        answer = f"⚠️ Une erreur s'est produite: {e}"
                        import traceback
                        answer += f"\n\n```\n{traceback.format_exc()}\n```"
                
                # Display chatbot message
                st.chat_message("assistant").markdown(answer)
                st.session_state['messages'].append({"role": "assistant", "content": answer})

# Contact Page
elif choice == "📧 Contact":
    st.title("📬 Contact")
    st.markdown("""
    Pour toute question ou suggestion concernant cet assistant intelligent:

    - **GitHub:** [RAG-Based-LLM-Chatbot](https://github.com/GURPREETKAURJETHRA/RAG-Based-LLM-Chatbot) 🛠️
    
    Si vous souhaitez proposer une amélioration ou signaler un bug, n'hésitez pas à ouvrir une issue sur GitHub. 
    Vos contributions sont les bienvenues ! 🙌
    """)

# Footer
st.markdown("---")
st.markdown("© 2024 Assistant Intelligent ISO & RH - Propulsé par Llama 3.2 & RAG 🚀")
