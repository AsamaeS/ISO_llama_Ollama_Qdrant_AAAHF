# config.py

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "docs"
TEMP_DIR = BASE_DIR / "temp"

# Ensure temp directory exists
TEMP_DIR.mkdir(exist_ok=True)

# Qdrant settings
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "iso_rh_knowledge_base"

# Embedding model settings
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en"
EMBEDDING_DEVICE = "cpu"
EMBEDDING_ENCODE_KWARGS = {"normalize_embeddings": True}

# LLM settings
LLM_MODEL = "llama3.2"
LLM_TEMPERATURE = 0.7

# Document processing settings
SUPPORTED_EXTENSIONS = {
    'pdf': ['.pdf'],
    'excel': ['.xlsx', '.xls'],
    'word': ['.docx', '.doc']
}

ALL_SUPPORTED_EXTENSIONS = [ext for exts in SUPPORTED_EXTENSIONS.values() for ext in exts]

# Chunking settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 250

# Retrieval settings
RETRIEVAL_K = 5  # Number of documents to retrieve for context

# Document type mapping (for categorization)
DOCUMENT_TYPES = {
    'ISO': ['ISO', 'iso', 'norme', 'standard'],
    'RH': ['RH', 'formation', 'FOR-RH'],
    'Procédure': ['PCD', 'procédure', 'procedure']
}

def get_document_type(filename: str) -> str:
    """
    Determine document type based on filename.
    
    Args:
        filename: Name of the document file
        
    Returns:
        Document type category
    """
    filename_upper = filename.upper()
    
    for doc_type, keywords in DOCUMENT_TYPES.items():
        for keyword in keywords:
            if keyword.upper() in filename_upper:
                return doc_type
    
    return "Général"
