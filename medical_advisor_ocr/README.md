# Medical Advisor OCR System

## Description
Le Medical Advisor OCR (Optical Character Recognition) est un système avancé de traitement de documents médicaux qui permet l'extraction, l'analyse et la structuration automatique des informations à partir de documents médicaux scannés ou photographiés. Le système utilise des techniques avancées d'OCR et de traitement d'image pour fournir des résultats précis et fiables.

## Fonctionnalités Principales

### 1. Traitement de Documents Médicaux
- Reconnaissance de texte sur documents médicaux
- Extraction de données structurées
- Support multilingue
- Traitement de différents formats (PDF, images, scans)
- Détection automatique de la langue

### 2. Analyse de Documents Spécifiques
- Ordonnances médicales
- Résultats d'analyses
- Certificats médicaux
- Factures médicales
- Radiographies et imagerie médicale

### 3. Intégration avec le Système RAG
- Enrichissement de la base de connaissances
- Mise à jour automatique des dossiers patients
- Extraction de données pour l'analyse médicale
- Historique des documents traités

## Architecture Technique

### Backend
- **Framework**: FastAPI
- **Base de données**: PostgreSQL
- **ORM**: Prisma
- **OCR Engine**: Tesseract
- **Image Processing**: OpenCV
- **ML Models**: PyTorch/TensorFlow

### Modèles de Données
- Documents médicaux
- Résultats d'analyses
- Images médicales
- Métadonnées des documents
- Historique de traitement

### Sécurité
- Chiffrement des documents
- Gestion des accès
- Validation des données
- Protection des informations sensibles

## Installation

### Prérequis
- Python 3.8+
- PostgreSQL 12+
- Tesseract OCR
- Node.js 16+ (pour Prisma)

### Configuration
1. Cloner le repository
```bash
git clone [repository-url]
cd medical_advisor_ocr
```

2. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

3. Installer Tesseract OCR
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Télécharger l'installateur depuis GitHub
```

4. Configurer la base de données
```bash
# Créer un fichier .env
DATABASE_URL="postgresql://user:password@localhost:5432/med_sys"
```

5. Initialiser la base de données
```bash
npx prisma generate
npx prisma db push
```

6. Lancer le serveur
```bash
python -m medical_advisor_ocr.main
```

## Utilisation

### API Endpoints

#### 1. Traitement de Document
```http
POST /process-document
Content-Type: multipart/form-data
{
    "file": [fichier],
    "document_type": "prescription",
    "language": "fr"
}
```

#### 2. Extraction de Données
```http
POST /extract-data
{
    "document_id": "uuid",
    "extraction_type": "medical_data"
}
```

#### 3. Historique des Documents
```http
GET /document-history
```

## Technologies Utilisées

### OCR et Traitement d'Image
- **OCR Engine**: Tesseract
- **Image Processing**: OpenCV
- **Preprocessing**: PIL/Pillow
- **PDF Processing**: PyPDF2

### Machine Learning
- **Framework**: PyTorch/TensorFlow
- **Computer Vision**: OpenCV
- **NLP**: spaCy/NLTK
- **Document Classification**: Custom CNN

### Backend
- **Framework**: FastAPI
- **Validation**: Pydantic
- **Documentation**: Swagger/OpenAPI
- **Tests**: Pytest

### Base de Données
- **SGBD**: PostgreSQL
- **ORM**: Prisma
- **Schéma**: Modèles relationnels complexes

### Sécurité
- **Authentification**: JWT
- **Validation**: Pydantic
- **Chiffrement**: AES-256
- **CORS**: Configuration sécurisée

## Structure du Projet
```
medical_advisor_ocr/
├── main.py                 # Point d'entrée FastAPI
├── ocr_processor.py        # Logique OCR
├── image_processor.py      # Traitement d'images
├── document_classifier.py  # Classification de documents
├── database.py            # Gestion de la base de données
├── models/               # Modèles Pydantic
├── schemas/             # Schémas Prisma
├── ml_models/          # Modèles ML
├── tests/              # Tests unitaires
└── requirements.txt    # Dépendances Python
```

## Fonctionnalités Avancées

### 1. Prétraitement d'Images
- Correction de l'orientation
- Amélioration de la qualité
- Réduction du bruit
- Normalisation des couleurs
- Détection des zones de texte

### 2. Post-traitement OCR
- Correction orthographique
- Structuration des données
- Validation des informations
- Extraction de métadonnées
- Classification des documents

### 3. Intégration avec le Système RAG
- Enrichissement de la base de connaissances
- Mise à jour des dossiers patients
- Analyse automatique des documents
- Historique des traitements

## Contribution
Les contributions sont les bienvenues ! Veuillez suivre ces étapes :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence
[Type de licence]

## Contact
[Informations de contact] 