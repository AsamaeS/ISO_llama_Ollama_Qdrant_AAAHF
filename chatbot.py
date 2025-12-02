# chatbot.py

"""
Enhanced chatbot manager with source citation capabilities.
Returns answers with precise references to source documents.
"""

import os
from typing import Dict, List, Any
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_ollama import ChatOllama
from qdrant_client import QdrantClient
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.documents import Document
import streamlit as st
import config


class ChatbotManager:
    def __init__(
        self,
        model_name: str = None,
        device: str = None,
        encode_kwargs: dict = None,
        llm_model: str = None,
        llm_temperature: float = None,
        qdrant_url: str = None,
        collection_name: str = None,
    ):
        """
        Initializes the ChatbotManager with embedding models, LLM, and vector store.

        Args:
            model_name (str): The HuggingFace model name for embeddings.
            device (str): The device to run the model on ('cpu' or 'cuda').
            encode_kwargs (dict): Additional keyword arguments for encoding.
            llm_model (str): The local LLM model name for ChatOllama.
            llm_temperature (float): Temperature setting for the LLM.
            qdrant_url (str): The URL for the Qdrant instance.
            collection_name (str): The name of the Qdrant collection.
        """
        # Use config defaults if not provided
        self.model_name = model_name or config.EMBEDDING_MODEL_NAME
        self.device = device or config.EMBEDDING_DEVICE
        self.encode_kwargs = encode_kwargs or config.EMBEDDING_ENCODE_KWARGS
        self.llm_model = llm_model or config.LLM_MODEL
        self.llm_temperature = llm_temperature or config.LLM_TEMPERATURE
        self.qdrant_url = qdrant_url or config.QDRANT_URL
        self.collection_name = collection_name or config.COLLECTION_NAME

        # Initialize Embeddings
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs=self.encode_kwargs,
        )

        # Initialize Local LLM
        self.llm = ChatOllama(
            model=self.llm_model,
            temperature=self.llm_temperature,
        )

        # Define the enhanced prompt template with source citation instructions
        self.prompt_template = """Tu es un assistant expert en normes ISO et documents RH.
Utilise les informations suivantes pour répondre à la question de l'utilisateur.

INSTRUCTIONS IMPORTANTES:
- Réponds de manière détaillée et professionnelle
- Base-toi UNIQUEMENT sur les informations fournies dans le contexte
- Si tu ne trouves pas l'information dans le contexte, dis-le clairement
- Sois précis et cite des éléments spécifiques du contexte quand c'est pertinent

Context: {context}

Question: {question}

Réponds de manière claire et structurée. À la fin de ta réponse, ajoute une section "📚 Sources:" pour lister les documents utilisés.

Réponse:
"""

        # Initialize Qdrant client
        self.client = QdrantClient(
            url=self.qdrant_url, prefer_grpc=False
        )

        # Initialize the Qdrant vector store
        self.db = Qdrant(
            client=self.client,
            embeddings=self.embeddings,
            collection_name=self.collection_name
        )

        # Initialize the prompt
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=['context', 'question']
        )

        # Initialize the retriever with more documents for better context
        self.retriever = self.db.as_retriever(
            search_kwargs={"k": config.RETRIEVAL_K}
        )

        # Define chain type kwargs
        self.chain_type_kwargs = {"prompt": self.prompt}

        # Initialize the RetrievalQA chain with return_source_documents=True
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,  # IMPORTANT: Enable source document return
            chain_type_kwargs=self.chain_type_kwargs,
            verbose=False
        )

    def format_sources(self, source_documents: List[Document]) -> str:
        """
        Format source documents into a readable citation list.
        
        Args:
            source_documents: List of source Document objects
            
        Returns:
            Formatted string with source citations
        """
        if not source_documents:
            return "\n\n📚 **Sources:** Aucune source spécifique trouvée."
        
        sources_text = "\n\n---\n\n### 📚 Sources:\n\n"
        
        # Group sources by document
        sources_by_doc = {}
        for doc in source_documents:
            source_name = doc.metadata.get('source', 'Document inconnu')
            if source_name not in sources_by_doc:
                sources_by_doc[source_name] = []
            sources_by_doc[source_name].append(doc)
        
        # Format each document's citations
        for idx, (source_name, docs) in enumerate(sources_by_doc.items(), 1):
            doc_type = docs[0].metadata.get('document_type', 'Document')
            source_type = docs[0].metadata.get('source_type', 'Fichier')
            
            sources_text += f"**{idx}. {source_name}** ({doc_type})\n"
            
            # Add location information based on source type
            locations = set()
            for doc in docs:
                if source_type == 'PDF':
                    page = doc.metadata.get('page', 'N/A')
                    locations.add(f"Page {page}")
                elif source_type == 'Excel':
                    sheet = doc.metadata.get('sheet', 'N/A')
                    locations.add(f"Feuille: {sheet}")
                elif source_type == 'Word':
                    section = doc.metadata.get('section', 'N/A')
                    locations.add(f"{section}")
            
            if locations:
                sources_text += f"   - Localisation: {', '.join(sorted(locations))}\n"
            
            # Add a short excerpt from the first relevant chunk
            if docs:
                excerpt = docs[0].page_content[:200].strip()
                if len(docs[0].page_content) > 200:
                    excerpt += "..."
                sources_text += f"   - Extrait: *\"{excerpt}\"*\n"
            
            sources_text += "\n"
        
        return sources_text

    def get_response(self, query: str) -> Dict[str, Any]:
        """
        Processes the user's query and returns the chatbot's response with sources.

        Args:
            query (str): The user's input question.

        Returns:
            Dict containing 'answer' and 'sources' keys
        """
        try:
            # Get response with source documents
            response = self.qa({"query": query})
            
            # Extract answer and source documents
            answer = response.get('result', '')
            source_documents = response.get('source_documents', [])
            
            # Format sources
            sources_formatted = self.format_sources(source_documents)
            
            # Combine answer with sources
            full_response = answer + sources_formatted
            
            return {
                'answer': full_response,
                'source_documents': source_documents,
                'sources_formatted': sources_formatted
            }
            
        except Exception as e:
            error_msg = f"⚠️ Une erreur s'est produite lors du traitement de votre demande: {e}"
            return {
                'answer': error_msg,
                'source_documents': [],
                'sources_formatted': ''
            }
    
    def get_simple_response(self, query: str) -> str:
        """
        Simplified method that returns only the formatted answer string.
        For backward compatibility.
        
        Args:
            query (str): The user's input question.
            
        Returns:
            str: The complete formatted response
        """
        response_dict = self.get_response(query)
        return response_dict['answer']
