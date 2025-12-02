# 📁 Répertoire des Documents ISO

## 📥 Comment ajouter vos documents

1. **Téléchargez les PDFs depuis le Drive du prof** (dossier "norme standard")
2. **Placez tous les fichiers PDF ici** dans ce dossier `data/pdfs/`

## 📚 Exemples de fichiers attendus

```
ml_core/data/pdfs/
├── ISO_9001.pdf
├── ISO_14001.pdf
├── ISO_45001.pdf
└── ... (autres normes ISO)
```

## 🚀 Ensuite pour les traiter

Une fois que vous avez placé vos PDFs ici, vous pouvez :

### Option 1 : Via le script de démo
```bash
cd ml_core
python example_usage.py
```

### Option 2 : Ingestion manuelle
```bash
python -m ml_core.ingest.ingest_pipeline ./data/pdfs/ISO_9001.pdf ./data/chunks
```

### Option 3 : Via l'API
```bash
# Démarrer l'API
uvicorn ml_core.api.api:app --reload

# Puis utiliser l'endpoint /ingest
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_path": "d:/iso-doc-navigator-main/ml_core/data/pdfs/ISO_9001.pdf",
    "document_name": "ISO 9001",
    "rebuild_index": true
  }'
```

## 📋 Structure complète des données

```
ml_core/data/
├── pdfs/           ← VOS PDFs ICI
│   └── *.pdf
├── chunks/         ← Chunks générés automatiquement
│   ├── ISO_9001_chunks.json
│   └── ISO_9001_metadata.json
└── index/          ← Index FAISS généré automatiquement
    ├── faiss_index.bin
    ├── faiss_index_metadata.json
    └── faiss_index_config.json
```

## ⚠️ Important

- Les PDFs peuvent être **en français ou anglais** (le système gère les deux)
- Les PDFs **scannés sont supportés** (OCR avec Tesseract + PaddleOCR)
- Formats acceptés : **PDF uniquement**

## 🔧 Accès au Drive

Lien Drive fourni : https://drive.google.com/drive/folders/1K-MKriXizybzJPkqAm7Uy8CakFgOjxiY

Cherchez le dossier **"norme standard"** et téléchargez les PDFs ISO.
