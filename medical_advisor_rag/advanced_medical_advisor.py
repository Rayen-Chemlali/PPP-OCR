import json
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from groq import Groq
import os
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from medical_advisor_rag.database import DatabaseManager

class AdvancedMedicalAdvisor:
    def __init__(self, api_key: str, db_manager: DatabaseManager):
        self.client = Groq(api_key=api_key)
        self.consultation_history = []
        self.db_manager = db_manager
        
    def _create_system_prompt(self) -> str:
        return """Tu es un assistant médical rassurant et professionnel. Ton rôle est de :
1. Toujours rassurer le patient en restant positif et optimiste
2. Ne jamais entrer dans les détails techniques ou médicaux complexes
3. Toujours recommander des spécialistes appropriés. Si une spécialité est clairement identifiable à partir des symptômes, **identifie-la et inclus-la dans le champ `specialite_identifiee`**. Sinon, ce champ doit être null.
4. Donner des conseils généraux simples et rassurants
5. Insister sur le fait que la situation est gérable et que tout ira bien
6. Tu ne réponds qu'aux questions en lien avec la santé ou la médecine. Si la question n'est pas médicale, tu réponds poliment : 'Je suis un assistant médical et je ne peux répondre qu'aux questions de santé.'

Règles strictes :
- Ne jamais mentionner de complications possibles
- Ne jamais donner de diagnostic précis
- Toujours rester positif et rassurant
- Toujours recommander au moins 2 spécialistes (même si des noms spécifiques ne sont pas trouvés)
- Utiliser un ton chaleureux et empathique
- Se concentrer sur les solutions plutôt que les problèmes
- Refuser poliment toute question hors du domaine médical

Format de réponse :
{
    "reassurance": "Message rassurant et positif ou message de refus si hors sujet médical",
    "specialite_identifiee": "Nom de la spécialité détectée, ex: cardiologue, ou null",
    "conseils_generaux": ["Conseil 1", "Conseil 2"],
    "specialistes_recommandes": [
        {
            "specialite": "Spécialité (ex: généraliste, dermatologue)",
            "raison": "Raison simple et rassurante",
            "nom_medecin": "Nom du médecin (optionnel, si trouvé en base)",
            "email": "Email du médecin (optionnel)",
            "phone": "Téléphone du médecin (optionnel)",
            "address": "Adresse du médecin (optionnel)"
        }
    ],
    "message_final": "Message positif de conclusion ou de refus"
}
"""

    def _process_llm_response(self, response_content: str, user_prompt_context: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            advice = json.loads(response_content)

            # If the response indicates this is not a medical question, format it properly
            if advice.get("reassurance") == "Je suis un assistant médical et je ne peux répondre qu'aux questions de santé.":
                return {
                    "reassurance": "",
                    "specialite_identifiee": None,
                    "conseils_generaux": [],
                    "specialistes_recommandes": [],
                    "message_final": advice["reassurance"]
                }

            # Vérifier si une spécialité a été identifiée par le LLM
            identified_specialty = advice.get("specialite_identifiee")

            if identified_specialty:
                print(f"Spécialité identifiée par le LLM: {identified_specialty}")
                try:
                    # Tenter de récupérer des médecins de la base de données
                    db_doctors = self.db_manager.get_doctors_by_specialty(identified_specialty)
                    if db_doctors:
                        print(f"Médecins trouvés en base pour {identified_specialty}: {len(db_doctors)}")
                        # Remplacer les suggestions génériques par les médecins de la BDD
                        advice["specialistes_recommandes"] = []
                        for doc in db_doctors:
                            advice["specialistes_recommandes"].append({
                                "specialite": doc["specialty"],
                                "raison": f"Médecin recommandé pour vos symptômes.",
                                "nom_medecin": f"{doc["first_name"]} {doc["last_name"]}",
                                "email": doc["email"],
                                "phone": doc["phone"],
                                "address": doc["address"]
                            })
                    else:
                        print(f"Aucun médecin spécifique trouvé en base pour {identified_specialty}. Retour aux suggestions générales du LLM.")
                except Exception as db_error:
                    print(f"Erreur lors de la recherche en base de données pour {identified_specialty}: {db_error}. Retour aux suggestions générales du LLM.")
                    # L'erreur est catchée, le système ne s'arrête pas, et la réponse LLM initiale est utilisée

            # S'assurer qu'il y a toujours au moins 2 recommandations si c'est une réponse médicale valide
            if len(advice.get("specialistes_recommandes", [])) < 2 and advice.get("reassurance") != "Je suis un assistant médical et je ne peux répondre qu'aux questions de santé.":
                # Si le LLM n'a pas fourni assez de spécialistes ou si la BDD n'a rien trouvé, assurez des suggestions génériques
                if not advice.get("specialistes_recommandes") or not identified_specialty:
                    # Exemple de fallback, à affiner si nécessaire avec des spécialités par défaut
                    advice["specialistes_recommandes"] = advice.get("specialistes_recommandes", [])
                    if {"specialite": "Médecin généraliste", "raison": "Pour une première évaluation et un suivi global"} not in advice["specialistes_recommandes"]:
                        advice["specialistes_recommandes"].append({"specialite": "Médecin généraliste", "raison": "Pour une première évaluation et un suivi global"})
                    if len(advice["specialistes_recommandes"]) < 2:
                        # Ajouter une autre spécialité générique si nécessaire, basée sur le contexte ou un défaut
                        if "douleur thoracique" in user_prompt_context.get("symptoms", []):
                             if {"specialite": "Cardiologue", "raison": "Pour un avis spécialisé concernant des symptômes cardiaques"} not in advice["specialistes_recommandes"]:
                                advice["specialistes_recommandes"].append({"specialite": "Cardiologue", "raison": "Pour un avis spécialisé concernant des symptômes cardiaques"})
                        elif "éruption cutanée" in user_prompt_context.get("symptoms", []):
                             if {"specialite": "Dermatologue", "raison": "Pour un diagnostic précis de l'éruption cutanée"} not in advice["specialistes_recommandes"]:
                                advice["specialistes_recommandes"].append({"specialite": "Dermatologue", "raison": "Pour un diagnostic précis de l'éruption cutanée"})
                        else:
                            # Fallback générique si aucune spécialité spécifique n'est déterminable
                            if {"specialite": "Spécialiste approprié", "raison": "Pour un examen plus approfondi de vos symptômes"} not in advice["specialistes_recommandes"]:
                                advice["specialistes_recommandes"].append({"specialite": "Spécialiste approprié", "raison": "Pour un examen plus approfondi de vos symptômes"})


            if user_prompt_context:
                self.consultation_history.append({
                    "symptoms": user_prompt_context.get("symptoms"),
                    "age": user_prompt_context.get("age"),
                    "location": user_prompt_context.get("location"),
                    "user_prompt": user_prompt_context.get("user_prompt"),
                    "advice": advice
                })
            return advice
        except json.JSONDecodeError:
            print(f"Erreur de décodage JSON de la réponse du LLM: {response_content}")
            return {
                "error": "Erreur dans le format de la réponse",
                "raw_response": response_content
            }
        except Exception as e:
            print(f"Erreur inattendue dans _process_llm_response: {e}")
            return {"error": f"Erreur de traitement: {str(e)}"}

    def get_medical_advice(self, symptoms: List[str], age: int, is_emergency: bool, location: str, budget: float) -> Dict[str, Any]:
        user_prompt = f"""Patient de {age} ans à {location}.
Symptômes: {', '.join(symptoms)}
Urgence: {'Oui' if is_emergency else 'Non'}
Budget: {budget}€

Donne des conseils rassurants et recommande des spécialistes appropriés. Identifie la spécialité principale si possible."""

        messages = [
            {"role": "system", "content": self._create_system_prompt()},
            {"role": "user", "content": user_prompt}
        ]

        response = self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            temperature=0.0,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stream=False
        )

        user_prompt_context = {
            "symptoms": symptoms,
            "age": age,
            "location": location,
            "is_emergency": is_emergency,
            "budget": budget,
            "user_prompt": user_prompt
        }
        return self._process_llm_response(response.choices[0].message.content, user_prompt_context)

    def chat_with_user(self, user_prompt: str) -> Dict[str, Any]:
        """
        Prend un prompt utilisateur libre et répond dans le style rassurant et orienté recommandation. Ignore poliment les questions hors santé.
        Identifie la spécialité principale si possible.
        """
        messages = [
            {"role": "system", "content": self._create_system_prompt()},
            {"role": "user", "content": user_prompt}
        ]
        response = self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            temperature=0.0,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stream=False
        )
        
        # If the response is not in JSON format, create a proper JSON response
        response_content = response.choices[0].message.content
        if not response_content.strip().startswith('{'):
            return {
                "reassurance": "",
                "specialite_identifiee": None,
                "conseils_generaux": [],
                "specialistes_recommandes": [],
                "message_final": "Je suis un assistant médical et je ne peux répondre qu'aux questions de santé."
            }
            
        user_prompt_context = {"user_prompt": user_prompt}
        return self._process_llm_response(response_content, user_prompt_context)

    def get_consultation_history(self) -> List[Dict[str, Any]]:
        return self.consultation_history

# Exemple d'utilisation
if __name__ == "__main__":
    # Initialiser le conseiller médical avancé
    db_manager = DatabaseManager()
    advisor = AdvancedMedicalAdvisor(api_key="votre_cle_api_groq", db_manager=db_manager)
    
    # Exemple de consultation avancée
    symptoms = ["douleur thoracique", "essoufflement"]
    advice = advisor.get_medical_advice(
        symptoms=symptoms,
        age=45,
        is_emergency=True,
        location="Paris",
        budget=100
    )
    
    print("\nRecommandation médicale avancée:")
    print(json.dumps(advice, ensure_ascii=False, indent=2)) 