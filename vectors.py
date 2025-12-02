# vectors.py

"""
Enhanced embeddings manager with support for multiple document formats
and batch document processing.
"""

import os
from typing import List
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
import config
from document_processor import DocumentProcessor


class EmbeddingsManager:
    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en",
        device: str = "cpu",
        encode_kwargs: dict = {"normalize_embeddings": True},
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "vector_db",
    ):
        """
        Initializes the EmbeddingsManager with the specified model and Qdrant settings.

        Args:
            model_name (str): The HuggingFace model name for embeddings.
            device (str): The device to run the model on ('cpu' or 'cuda').
            encode_kwargs (dict): Additional keyword arguments for encoding.
            qdrant_url (str): The URL for the Qdrant instance.
            collection_name (str): The name of the Qdrant collection.
        """
        self.model_name = model_name
        self.device = device
        self.encode_kwargs = encode_kwargs
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name

        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs=self.encode_kwargs,
        )
        
        self.document_processor = DocumentProcessor()

    def create_embeddings(self, file_path: str):
        """
        Processes a single file, creates embeddings, and stores them in Qdrant.
        (Legacy method for backward compatibility)

        Args:
            file_path (str): The file path to the document.

        Returns:
            str: Success message upon completion.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Load document using the new document processor
        documents = self.document_processor.load_document(file_path)
        
        if not documents:
            raise ValueError("No documents were loaded from the file.")

        # Create and store embeddings in Qdrant
        return self.store_embeddings(documents)
    
    def store_embeddings(self, documents: List[Document], force_recreate: bool = False):
        """
        Store pre-loaded documents with embeddings in Qdrant.
        
        Args:
            documents: List of Document objects to store
            force_recreate: If True, delete existing collection and recreate
            
        Returns:
            str: Success message upon completion
        """
        if not documents:
            raise ValueError("No documents provided for embedding storage.")
        
        try:
            if force_recreate:
                # Delete existing collection if it exists
                try:
                    client = QdrantClient(url=self.qdrant_url, prefer_grpc=False)
                    client.delete_collection(collection_name=self.collection_name)
                    print(f"🗑️ Deleted existing collection: {self.collection_name}")
                except Exception:
                    pass  # Collection doesn't exist, that's fine
            
            # Create and store embeddings in Qdrant
            qdrant = Qdrant.from_documents(
                documents,
                self.embeddings,
                url=self.qdrant_url,
                prefer_grpc=False,
                collection_name=self.collection_name,
            )
            
            return f"✅ {len(documents)} documents successfully embedded and stored in Qdrant collection '{self.collection_name}'!"
            
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Qdrant or store embeddings: {e}")
    
    def load_directory_and_embed(self, directory_path: str, force_recreate: bool = False):
        """
        Load all documents from a directory and create embeddings.
        
        Args:
            directory_path: Path to directory containing documents
            force_recreate: If True, delete existing collection and recreate
            
        Returns:
            str: Success message with statistics
        """
        print(f"📂 Loading documents from: {directory_path}")
        documents = self.document_processor.load_directory(directory_path)
        
        if not documents:
            return "⚠️ No documents found to process."
        
        return self.store_embeddings(documents, force_recreate=force_recreate)
