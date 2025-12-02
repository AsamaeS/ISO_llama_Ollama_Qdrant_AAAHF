# batch_indexer.py

"""
Batch indexer script to process all documents in the data directory
and create embeddings in Qdrant vector database.
"""

import argparse
from pathlib import Path
from tqdm import tqdm
import config
from document_processor import DocumentProcessor
from vectors import EmbeddingsManager


def main(data_dir: str = None, force_reindex: bool = False):
    """
    Index all documents from the data directory.
    
    Args:
        data_dir: Directory containing documents (default: config.DATA_DIR)
        force_reindex: If True, delete existing collection and reindex all
    """
    data_path = Path(data_dir) if data_dir else config.DATA_DIR
    
    if not data_path.exists():
        print(f"❌ Error: Directory not found: {data_path}")
        return
    
    print("=" * 60)
    print("📚 Indexation des Documents ISO & RH")
    print("=" * 60)
    print(f"📁 Répertoire source: {data_path}")
    print(f"🔄 Réindexation forcée: {'Oui' if force_reindex else 'Non'}")
    print()
    
    # Initialize document processor
    print("🔧 Initialisation du processeur de documents...")
    doc_processor = DocumentProcessor()
    
    # Load all documents
    print(f"\n📖 Chargement des documents depuis {data_path}...")
    print("-" * 60)
    
    try:
        documents = doc_processor.load_directory(str(data_path))
    except Exception as e:
        print(f"\n❌ Erreur lors du chargement des documents: {e}")
        return
    
    if not documents:
        print("\n⚠️ Aucun document trouvé à indexer.")
        return
    
    print("\n" + "=" * 60)
    print(f"✅ {len(documents)} chunks chargés avec succès")
    print("=" * 60)
    
    # Create embeddings
    print(f"\n🧠 Création des embeddings et stockage dans Qdrant...")
    print(f"📊 Collection: {config.COLLECTION_NAME}")
    print(f"🔗 URL Qdrant: {config.QDRANT_URL}")
    print()
    
    try:
        embeddings_manager = EmbeddingsManager(
            model_name=config.EMBEDDING_MODEL_NAME,
            device=config.EMBEDDING_DEVICE,
            encode_kwargs=config.EMBEDDING_ENCODE_KWARGS,
            qdrant_url=config.QDRANT_URL,
            collection_name=config.COLLECTION_NAME
        )
        
        # Store embeddings
        result = embeddings_manager.store_embeddings(
            documents=documents,
            force_recreate=force_reindex
        )
        
        print(f"\n{result}")
        print("\n" + "=" * 60)
        print("✅ Indexation terminée avec succès!")
        print("=" * 60)
        print("\n💡 Vous pouvez maintenant lancer l'application:")
        print("   streamlit run new.py")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la création des embeddings: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Index documents for the ISO & RH intelligent assistant"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help=f"Directory containing documents (default: {config.DATA_DIR})"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force complete reindexing (delete existing collection)"
    )
    
    args = parser.parse_args()
    main(data_dir=args.data_dir, force_reindex=args.force)
