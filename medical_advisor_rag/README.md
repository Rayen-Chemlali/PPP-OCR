# Medical Advisor RAG

Un agent RAG (Retrieval-Augmented Generation) qui aide les patients à choisir le bon médecin en fonction de leurs symptômes.

## Installation

1. Installez les dépendances requises :
```bash
pip install groq
```

2. Configurez votre clé API Groq :
```bash
export GROQ_API_KEY="votre_cle_api_groq"
```

## Utilisation

```python
from medical_advisor import MedicalAdvisor

# Initialiser le conseiller médical
advisor = MedicalAdvisor(api_key="votre_cle_api_groq")

# Exemple de consultation
symptoms = ["douleur thoracique", "essoufflement"]
advice = advisor.get_medical_advice(
    symptoms=symptoms,
    age=45,
    is_emergency=True
)

print(advice)
```

## Fonctionnalités

- Recommandation de spécialistes médicaux basée sur les symptômes
- Évaluation du niveau d'urgence
- Base de connaissances extensible
- Conseils personnalisés

## Structure de la base de connaissances

La base de connaissances (`knowledge_base.json`) contient des informations sur :
- Les différentes spécialités médicales
- Les symptômes associés à chaque spécialité
- Le niveau d'urgence par défaut
- Les descriptions détaillées

## Mise à jour de la base de connaissances

```python
new_data = {
    "specialties": {
        "nouvelle_specialite": {
            "description": "Description de la nouvelle spécialité",
            "symptomes": ["symptome1", "symptome2"],
            "urgent": False
        }
    }
}
advisor.update_knowledge_base(new_data)
```

## Avertissement

Cet agent est conçu pour fournir des conseils préliminaires et ne remplace pas une consultation médicale professionnelle. En cas d'urgence, contactez immédiatement les services d'urgence (15 en France). 