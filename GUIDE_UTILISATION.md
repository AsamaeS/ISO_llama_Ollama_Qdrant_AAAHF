# Guide d'Utilisation - Assistant Intelligent ISO & RH

## 🎯 Vue d'ensemble

Votre chatbot a été amélioré pour devenir un **assistant intelligent** capable de répondre à vos questions sur les normes ISO et documents RH en **citant précisément ses sources**.

### ✨ Nouvelles Fonctionnalités

- ✅ **Support Multi-Format**: PDF, Excel (.xlsx, .xls), Word (.docx, .doc)
- ✅ **Citations Précises**: Indique le document exact, la page/feuille, et la section
- ✅ **Traitement Automatique**: Scanne tout le dossier `data/docs/` récursivement
- ✅ **Interface Améliorée**: Affichage clair des sources avec extraits pertinents

---

## 🚀 Démarrage Rapide

### 1. Installation des dépendances

Les nouvelles dépendances ont déjà été installées:
```bash
pip install openpyxl python-docx pandas tqdm
```

### 2. Préparer vos documents

Placez tous vos documents dans le dossier `data/docs/`:

```
data/docs/
├── Normes_ISO/
│   ├── ISO 9001.pdf
│   └── ISO 9000.pdf
├── Formation_RH/
│   ├── Fiche_formation.xlsx
│   └── Plan_formation.xlsx
└── Procedures/
    └── Procedure_qualite.docx
```

**Note**: Le système traite automatiquement tous les sous-dossiers.

### 3. Indexer vos documents

#### Option A: Via l'interface Streamlit (Recommandé)

```bash
streamlit run new.py
```

1. Naviguez vers "📚 Base de Connaissances"
2. Cliquez sur "🚀 Indexer les Documents"
3. Attendez la fin de l'indexation

#### Option B: Via le script de ligne de commande

```bash
python batch_indexer.py
```

Pour forcer une réindexation complète:
```bash
python batch_indexer.py --force
```

Pour indexer un dossier spécifique:
```bash
python batch_indexer.py --data-dir "chemin/vers/dossier"
```

---

## 💬 Utilisation du Chatbot

### Lancer l'application

```bash
streamlit run new.py
```

### Poser des questions

Le chatbot comprend les questions en français et cite automatiquement ses sources:

**Exemples de questions:**

1. **Sur les normes ISO:**
   - "Quels sont les principes de management de la qualité selon ISO 9000?"
   - "Quelle est la définition de la non-conformité selon ISO 9001?"
   - "Comment gérer les risques et opportunités?"

2. **Sur les documents RH:**
   - "Comment remplir la fiche d'expression des besoins en formation?"
   - "Quelle est la procédure pour organiser une formation?"
   - "Comment évaluer l'efficacité d'une formation?"

3. **Sur les procédures:**
   - "Quelle est la procédure de gestion des non-conformités?"
   - "Qui est responsable de la gestion de la formation?"

### Format des réponses

Chaque réponse inclut automatiquement:

```
[Réponse détaillée du chatbot]

---

📚 Sources:

1. ISO_9001_V_2015_Fr.pdf (ISO Standard)
   - Localisation: Page 15, Page 23
   - Extrait: "La direction doit démontrer son leadership..."

2. FOR-RH-20 Fiche d_expression des besoins en formation.xlsx (RH)
   - Localisation: Feuille: Formulaire
   - Extrait: "Nom du collaborateur: ..."
```

---

## 🔧 Configuration

### Fichier `config.py`

Vous pouvez modifier les paramètres dans `config.py`:

```python
# Qdrant settings
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "iso_rh_knowledge_base"

# Retrieval settings
RETRIEVAL_K = 5  # Nombre de documents à récupérer

# Chunking settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 250
```

**Paramètres importants:**

- `RETRIEVAL_K`: Plus élevé = plus de contexte mais réponses plus lentes
- `CHUNK_SIZE`: Taille des morceaux de texte (ajuster selon vos documents)
- `COLLECTION_NAME`: Nom de la collection Qdrant (changer pour créer une nouvelle base)

---

## 📂 Structure du Projet

```
RAG-Based-LLM-Chatbot/
├── config.py                  # Configuration centralisée
├── document_processor.py      # Traitement multi-format
├── vectors.py                 # Gestion des embeddings
├── chatbot.py                 # Chatbot avec citations
├── batch_indexer.py          # Script d'indexation
├── new.py                     # Interface Streamlit
├── requirements.txt           # Dépendances
└── data/
    └── docs/                  # VOS DOCUMENTS ICI
        ├── Normes_ISO/
        ├── Formation_RH/
        └── Procedures/
```

---

## 🐛 Dépannage

### Problème: "Qdrant connection error"

**Solution**: Assurez-vous que Qdrant est en cours d'exécution:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Si vous n'avez pas Docker, installez-le depuis [docker.com](https://www.docker.com/)

### Problème: "No module named 'openpyxl'"

**Solution**: Réinstallez les dépendances:

```bash
pip install -r requirements.txt
```

### Problème: Documents Excel mal lus

**Cause**: Fichiers Excel corrompus ou format ancien (.xls)

**Solution**: 
1. Vérifiez que le fichier s'ouvre correctement dans Excel
2. Convertissez les anciens formats .xls en .xlsx

### Problème: Réponses sans sources

**Cause**: Les documents n'ont pas été indexés correctement

**Solution**:
1. Allez dans "📚 Base de Connaissances"
2. Cochez "🔁 Forcer la réindexation complète"
3. Cliquez sur "🚀 Indexer les Documents"

### Problème: Ollama model not found

**Solution**: Assurez-vous que Llama 3.2 est installé:

```bash
ollama pull llama3.2:3b
```

---

## 📊 Performances

### Recommandations

- **Nombre de documents**: Jusqu'à 1000 documents optimaux
- **Taille des documents**: PDF jusqu'à 50 pages, Excel jusqu'à 20 feuilles
- **Temps de réponse**: 3-7 secondes selon la complexité
- **RAM requise**: 4 GB minimum, 8 GB recommandé

### Optimisation

Pour améliorer les performances:

1. **Réduire RETRIEVAL_K** dans config.py (ex: 3 au lieu de 5)
2. **Augmenter CHUNK_SIZE** pour moins de chunks totaux
3. **Utiliser un GPU** si disponible (modifier `EMBEDDING_DEVICE = "cuda"`)

---

## 🔄 Mise à Jour des Documents

### Ajouter de nouveaux documents

1. Placez les nouveaux fichiers dans `data/docs/`
2. Allez dans "📚 Base de Connaissances"
3. Cliquez sur "🚀 Indexer les Documents" (pas besoin de forcer la réindexation)

### Mettre à jour un document existant

1. Remplacez le fichier dans `data/docs/`
2. Cochez "🔁 Forcer la réindexation complète"
3. Cliquez sur "🚀 Indexer les Documents"

---

## 💡 Astuces

### Pour de meilleures réponses

1. **Soyez spécifique**: "Quelle est la clause 7.1.5 de ISO 9001?" plutôt que "Parle-moi de ISO"
2. **Posez une question à la fois**: Évitez les questions multiples
3. **Utilisez le vocabulaire des documents**: Si vos docs parlent de "procédure", utilisez ce terme

### Catégorisation automatique

Le système catégorise automatiquement vos documents:
- **ISO**: Fichiers contenant "ISO", "norme", "standard"
- **RH**: Fichiers contenant "RH", "formation", "FOR-RH"
- **Procédure**: Fichiers contenant "PCD", "procédure"

---

## 🆘 Support

Pour toute question ou problème:

1. Consultez les [Issues GitHub](https://github.com/GURPREETKAURJETHRA/RAG-Based-LLM-Chatbot/issues)
2. Créez une nouvelle issue avec:
   - Description du problème
   - Message d'erreur complet
   - Version de Python et système d'exploitation

---

## 📝 Notes Techniques

### Types de fichiers supportés

| Format | Extensions | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Extraction via UnstructuredPDFLoader |
| Excel | `.xlsx`, `.xls` | Lecture via pandas + openpyxl |
| Word | `.docx`, `.doc` | Extraction via python-docx |

### Base vectorielle

- **Système**: Qdrant (vector database)
- **Embeddings**: BAAI/bge-small-en (384 dimensions)
- **Distance**: Cosine similarity

### Modèle LLM

- **Modèle**: Llama 3.2 (3B paramètres)
- **Backend**: Ollama
- **Température**: 0.7 (équilibre créativité/précision)

---

Bon usage de votre assistant intelligent ! 🚀
