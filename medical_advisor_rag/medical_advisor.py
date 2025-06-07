import json
from typing import List, Dict, Any
from pathlib import Path
from groq import Groq
import os

class MedicalAdvisor:
    def __init__(self, api_key: str = None):
        """
        Initialise le conseiller médical RAG
        
        Args:
            api_key: Clé API Groq (optionnel si configurée en variable d'environnement GROQ_API_KEY)
        """
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            self.client = Groq()
            
        self.model = "llama2-70b-4096"
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """
        Charge la base de connaissances des spécialités médicales
        """
        knowledge_path = Path(__file__).parent / "knowledge_base.json"
        if not knowledge_path.exists():
            # Créer une base de connaissances par défaut si elle n'existe pas
            default_knowledge = {
                "specialties": {
                    "generaliste": {
                        "description": "Médecin traitant pour les soins de base et le suivi général",
                        "symptomes": ["fièvre", "rhume", "grippe", "maux de tête", "fatigue générale"],
                        "urgent": False
                    },
                    "cardiologue": {
                        "description": "Spécialiste du cœur et des vaisseaux sanguins",
                        "symptomes": ["douleur thoracique", "essoufflement", "palpitations", "hypertension"],
                        "urgent": True
                    },
                    "dermatologue": {
                        "description": "Spécialiste de la peau, des cheveux et des ongles",
                        "symptomes": ["éruptions cutanées", "acné", "allergies cutanées", "chute de cheveux"],
                        "urgent": False
                    },
                    "pediatre": {
                        "description": "Spécialiste des enfants de 0 à 18 ans",
                        "symptomes": ["fièvre enfant", "troubles de croissance", "maladies infantiles"],
                        "urgent": True
                    },
                    "urgentiste": {
                        "description": "Médecin des urgences pour les cas graves",
                        "symptomes": ["traumatismes", "hémorragies", "difficultés respiratoires sévères"],
                        "urgent": True
                    }
                }
            }
            with open(knowledge_path, 'w', encoding='utf-8') as f:
                json.dump(default_knowledge, f, ensure_ascii=False, indent=2)
            return default_knowledge
        
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_medical_advice(self, symptoms: List[str], age: int = None, is_emergency: bool = False) -> Dict[str, Any]:
        """
        Fournit des conseils sur le type de médecin à consulter
        
        Args:
            symptoms: Liste des symptômes
            age: Âge du patient (optionnel)
            is_emergency: Indique si c'est une urgence
            
        Returns:
            Dictionnaire contenant les recommandations
        """
        # Préparation du prompt pour Groq
        prompt = f"""En tant qu'assistant médical, aide à déterminer le type de médecin à consulter.

Symptômes rapportés: {', '.join(symptoms)}
Âge du patient: {age if age else 'Non spécifié'}
Urgence: {'Oui' if is_emergency else 'Non'}

Base de connaissances des spécialités:
{json.dumps(self.knowledge_base, ensure_ascii=False, indent=2)}

Fournis une réponse structurée en JSON avec:
1. Le type de médecin recommandé
2. La raison de cette recommandation
3. Le niveau d'urgence (basé sur les symptômes)
4. Des conseils supplémentaires
5. Si une consultation immédiate est nécessaire

Format de réponse attendu:
{{
    "medecin_recommande": "type de médecin",
    "raison": "explication",
    "urgence": "niveau d'urgence",
    "conseils": ["liste de conseils"],
    "consultation_immediate": true/false
}}"""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1000
            )
            
            response = completion.choices[0].message.content
            
            # Extraction du JSON de la réponse
            try:
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            except json.JSONDecodeError:
                return {
                    "error": "Impossible de parser la réponse",
                    "raw_response": response
                }
                
        except Exception as e:
            return {
                "error": f"Erreur lors de la consultation: {str(e)}"
            }

    def update_knowledge_base(self, new_data: Dict[str, Any]) -> bool:
        """
        Met à jour la base de connaissances
        
        Args:
            new_data: Nouvelles données à ajouter
            
        Returns:
            True si la mise à jour a réussi
        """
        try:
            self.knowledge_base.update(new_data)
            knowledge_path = Path(__file__).parent / "knowledge_base.json"
            with open(knowledge_path, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la base de connaissances: {str(e)}")
            return False

# Exemple d'utilisation
if __name__ == "__main__":
    # Initialiser le conseiller médical
    advisor = MedicalAdvisor(api_key="votre_cle_api_groq")
    
    # Exemple de consultation
    symptoms = ["douleur thoracique", "essoufflement"]
    advice = advisor.get_medical_advice(symptoms, age=45, is_emergency=True)
    
    print("\nRecommandation médicale:")
    print(json.dumps(advice, ensure_ascii=False, indent=2)) 