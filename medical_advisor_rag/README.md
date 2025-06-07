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

### Techniques RAG Utilisées

#### 1. Prompt Engineering Avancé
- **Système de Prompt Structuré**: Utilisation d'un prompt système détaillé qui guide le LLM dans sa prise de décision
- **Liste de Spécialités Contrôlée**: Intégration d'une liste exhaustive des spécialités médicales disponibles dans le prompt
- **Format de Réponse Standardisé**: Structure JSON stricte pour assurer la cohérence des réponses

#### 2. Gestion des Connaissances
- **Base de Données Relationnelle**: Stockage structuré des informations sur les médecins et leurs spécialités
- **Mapping Intelligent**: Conversion automatique des spécialités en format standardisé
- **Validation des Données**: Vérification systématique des spécialités recommandées

#### 3. Techniques de Récupération
- **Recherche Contextuelle**: Utilisation du contexte de la conversation pour affiner les recommandations
- **Filtrage Dynamique**: Adaptation des résultats en fonction des symptômes et du profil du patient
- **Fallback Intelligent**: Système de repli pour assurer des recommandations pertinentes même en cas d'incertitude

#### 4. Génération Augmentée
- **Contexte Enrichi**: Intégration des informations de la base de données dans les réponses du LLM
- **Validation en Temps Réel**: Vérification immédiate de la pertinence des recommandations
- **Personnalisation Dynamique**: Adaptation des réponses en fonction du profil et des besoins du patient

#### 5. Gestion des Erreurs et Robustesse
- **Validation des Spécialités**: Vérification que les spécialités recommandées existent dans la base
- **Gestion des Cas Limites**: Traitement approprié des questions non médicales
- **Système de Fallback**: Mécanismes de secours pour assurer une réponse même en cas d'erreur

#### 6. Construction des Requêtes
- **Requêtes Contextuelles**: Construction dynamique des requêtes basée sur le contexte de la conversation
- **Paramètres de Recherche**: Utilisation intelligente des paramètres (symptômes, âge, localisation, budget)
- **Optimisation des Requêtes**: Construction efficace des requêtes SQL pour la recherche de médecins
- **Filtrage Multi-critères**: Combinaison de plusieurs critères pour affiner les résultats
- **Requêtes Adaptatives**: Ajustement des requêtes en fonction des résultats précédents

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