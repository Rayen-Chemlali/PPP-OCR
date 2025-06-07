# Medical Advisor RAG System

## Description
Le Medical Advisor RAG (Retrieval-Augmented Generation) est un système avancé d'assistance médicale qui combine l'intelligence artificielle avec une base de connaissances médicales structurée. Le système fournit des conseils médicaux personnalisés, des recommandations de spécialistes et une assistance médicale en temps réel.

## Fonctionnalités Principales

### 1. Assistant Médical Intelligent
- Analyse des symptômes et recommandations personnalisées
- Identification automatique des spécialités médicales pertinentes
- Conseils généraux et rassurants
- Gestion des urgences médicales
- Support multilingue

### 2. Système de Recommandation de Spécialistes
- Recherche intelligente de médecins par spécialité
- Filtrage basé sur la localisation
- Prise en compte du budget
- Historique des consultations
- Évaluation de la pertinence des recommandations

### 3. Interface API RESTful
- Endpoints pour les conseils médicaux
- Gestion des consultations
- Historique des interactions
- Chat en temps réel
- Documentation Swagger/OpenAPI

## Architecture Technique

### Backend
- **Framework**: FastAPI
- **Base de données**: PostgreSQL
- **ORM**: Prisma
- **LLM**: Groq (Llama 4 Scout 17B)
- **API Documentation**: Swagger/OpenAPI

### Modèles de Données
- Patients
- Médecins
- Consultations
- Prescriptions
- Documents médicaux
- Résultats d'analyses
- RDVs

### Sécurité
- Authentification JWT
- Gestion des rôles (Patient, Doctor, Admin, etc.)
- Validation des données
- Protection des informations sensibles

## Installation

### Prérequis
- Python 3.8+
- PostgreSQL 12+
- Node.js 16+ (pour Prisma)

### Configuration
1. Cloner le repository
```bash
git clone [repository-url]
cd medical_advisor_rag
```

2. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

3. Configurer la base de données
```bash
# Créer un fichier .env
DATABASE_URL="postgresql://user:password@localhost:5432/med_sys"
GROQ_API_KEY="votre_cle_api_groq"
```

4. Initialiser la base de données
```bash
npx prisma generate
npx prisma db push
```

5. Lancer le serveur
```bash
python -m medical_advisor_rag.main
```

## Utilisation

### API Endpoints

#### 1. Conseils Médicaux
```http
POST /medical-advice
{
    "symptoms": ["symptom1", "symptom2"],
    "age": 30,
    "is_emergency": false,
    "location": "Paris",
    "budget": 100
}
```

#### 2. Chat Médical
```http
POST /chat
{
    "user_prompt": "J'ai mal à la tête"
}
```

#### 3. Historique des Consultations
```http
GET /consultation-history
```

## Technologies Utilisées

### Intelligence Artificielle
- **LLM**: Groq (Llama 4 Scout 17B)
- **RAG**: Système de récupération augmentée
- **NLP**: Traitement du langage naturel

### Base de Données
- **SGBD**: PostgreSQL
- **ORM**: Prisma
- **Schéma**: Modèles relationnels complexes

### Backend
- **Framework**: FastAPI
- **Validation**: Pydantic
- **Documentation**: Swagger/OpenAPI
- **Tests**: Pytest

### Sécurité
- **Authentification**: JWT
- **Validation**: Pydantic
- **Hachage**: Bcrypt
- **CORS**: Configuration sécurisée

## Structure du Projet
```
medical_advisor_rag/
├── main.py                 # Point d'entrée FastAPI
├── advanced_medical_advisor.py  # Logique RAG
├── database.py            # Gestion de la base de données
├── models/               # Modèles Pydantic
├── schemas/             # Schémas Prisma
├── tests/              # Tests unitaires
└── requirements.txt    # Dépendances Python
```

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

## Détails Techniques Avancés

### Prompt Engineering
Le système utilise plusieurs techniques avancées de prompt engineering pour optimiser les interactions avec le LLM :

1. **Chain-of-Thought (CoT)**
   - Décomposition des problèmes médicaux complexes en étapes logiques
   - Raisonnement pas à pas pour le diagnostic
   - Explication des décisions médicales

2. **Few-Shot Learning**
   - Exemples de cas médicaux similaires
   - Patterns de réponse pour différents types de questions
   - Templates pour les recommandations spécialisées

3. **Retrieval-Augmented Generation (RAG)**
   - Indexation vectorielle des documents médicaux
   - Recherche sémantique contextuelle
   - Fusion des informations pertinentes

4. **Prompt Templates**
   - Structure standardisée pour les questions médicales
   - Format spécifique pour les recommandations
   - Templates pour l'extraction d'informations

5. **Context Management**
   - Gestion de l'historique des conversations
   - Maintien du contexte médical
   - Adaptation dynamique du contexte

### Architecture LLM

#### Modèle Principal
- **Provider**: Groq
- **Modèle**: Llama 2 70B
- **Configuration**:
  - Temperature: 0.7
  - Top P: 0.9
  - Max Tokens: 2048
  - Stop Sequences: Personnalisées

#### Optimisations
- **Quantization**: 4-bit pour optimiser la mémoire
- **Batching**: Traitement par lots des requêtes
- **Caching**: Mise en cache des réponses fréquentes
- **Streaming**: Réponses en temps réel

### Base de Connaissances

#### Structure des Données
- **Embeddings**: 
  - Modèle: all-MiniLM-L6-v2
  - Dimension: 384
  - Métrique: Cosine Similarity

#### Indexation
- **Type**: HNSW (Hierarchical Navigable Small World)
- **Paramètres**:
  - M: 16 (nombre de connexions)
  - efConstruction: 100
  - efSearch: 50

#### Mise à Jour
- **Incremental Updates**: Mise à jour en temps réel
- **Versioning**: Gestion des versions des documents
- **Validation**: Vérification de la cohérence

### API et Intégration

#### Endpoints Principaux
```python
# Exemple de structure de prompt
{
    "system_prompt": "Vous êtes un assistant médical expert...",
    "user_prompt": "Question du patient",
    "context": {
        "medical_history": [...],
        "current_symptoms": [...],
        "previous_diagnoses": [...]
    },
    "constraints": {
        "max_length": 500,
        "format": "structured",
        "language": "fr"
    }
}
```

#### Gestion des Erreurs
- **Retry Logic**: 3 tentatives avec backoff exponentiel
- **Fallback**: Réponses de secours en cas d'échec
- **Monitoring**: Suivi des performances et erreurs

### Performance et Monitoring

#### Métriques Clés
- **Latence**: < 200ms pour les réponses
- **Précision**: > 95% sur les cas de test
- **Disponibilité**: 99.9%

#### Monitoring
- **Logging**: Structured logging avec correlation IDs
- **Tracing**: Distributed tracing avec OpenTelemetry
- **Alerting**: Alertes en temps réel sur les anomalies 