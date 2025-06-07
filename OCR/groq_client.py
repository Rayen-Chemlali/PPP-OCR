import json
import base64
import os
from groq import Groq
from typing import Dict, Any, Optional
from pathlib import Path


class MedicalOCR:
    def __init__(self, api_key: Optional[str] = None, seed: int = 42):
        """
        Initialise le client Groq pour l'OCR médical

        Args:
            api_key: Clé API Groq (optionnel si configurée en variable d'environnement GROQ_API_KEY)
            seed: Seed pour la reproductibilité des résultats (défaut: 42)
        """
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            # Utilise la variable d'environnement GROQ_API_KEY
            self.client = Groq()

        # Modèle Llama 4 Vision disponible sur Groq (2025)
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"

        # Seed fixe pour reproductibilité
        self.seed = seed

    def _encode_image(self, image_path: str) -> str:
        """
        Encode une image en base64

        Args:
            image_path: Chemin vers l'image

        Returns:
            String base64 de l'image
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _make_completion_json(self, messages: list) -> str:
        """
        Effectue une requête à l'API Groq avec mode JSON

        Args:
            messages: Liste des messages pour la conversation

        Returns:
            Réponse complète du modèle
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.0,  # Température 0 pour reproductibilité maximale
                max_completion_tokens=2048,
                top_p=1.0,  # Pas de sampling probabiliste
                stream=False,  # Pas de streaming pour récupérer la réponse complète
                response_format={"type": "json_object"},  # Mode JSON pour ordonnances
                stop=None,
                seed=self.seed,  # Seed fixe pour reproductibilité
            )
            return completion.choices[0].message.content
        except Exception as e:
            # Fallback sans JSON mode si erreur
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.0,  # Température 0 pour reproductibilité maximale
                    max_completion_tokens=2048,
                    top_p=1.0,  # Pas de sampling probabiliste
                    stream=False,
                    stop=None,
                    seed=self.seed,  # Seed fixe pour reproductibilité
                )
                return completion.choices[0].message.content
            except Exception as e2:
                raise Exception(f"Erreur lors de l'appel à l'API Groq: {str(e2)}")

    def _make_completion(self, messages: list) -> str:
        """
        Effectue une requête à l'API Groq

        Args:
            messages: Liste des messages pour la conversation

        Returns:
            Réponse complète du modèle
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.0,  # Température 0 pour reproductibilité maximale
                max_completion_tokens=2048,
                top_p=1.0,  # Pas de sampling probabiliste
                stream=False,  # Pas de streaming pour récupérer la réponse complète
                stop=None,
                seed=self.seed,  # Seed fixe pour reproductibilité
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Erreur lors de l'appel à l'API Groq: {str(e)}")

    def extract_prescription_simple(self, image_path: str) -> Dict[str, str]:
        """
        Extrait les informations essentielles d'une ordonnance de manière simplifiée

        Args:
            image_path: Chemin vers l'image de l'ordonnance

        Returns:
            Dictionnaire JSON simplifié avec les informations extraites
        """
        # Vérifier que le fichier existe
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Le fichier {image_path} n'existe pas")

        base64_image = self._encode_image(image_path)

        prompt = """Tu es un expert en OCR médical. Extrais les informations essentielles de cette ordonnance.

INSTRUCTIONS:
- Lis attentivement le document médical
- Identifie les informations clés demandées
- Si une information n'est pas visible, mets "Non spécifié"
- Sois précis et concis

RÉPONSE REQUISE: JSON strict avec cette structure exacte:
{
    "nom_docteur": "[Nom complet du médecin avec titre Dr.]",
    "specialite": "[Spécialité médicale si mentionnée, sinon 'Non spécifié']",
    "date": "[Date de l'ordonnance au format JJ/MM/AAAA]",
    "institut": "[Nom de la clinique/hôpital/cabinet, sinon 'Non spécifié']",
    "contenu": "[Ce qui est  ecrit dans l'ordonnance par le docteur par sa main hors la date et la signature]",
}

Fournis UNIQUEMENT le JSON, sans texte additionnel."""

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]

        response = self._make_completion_json(messages)

        try:
            # Nettoyer la réponse pour extraire uniquement le JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_text = response[json_start:json_end]
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            raise Exception(f"Erreur de parsing JSON: {str(e)}\nRéponse brute: {response}")

    def extract_prescription(self, image_path: str) -> Dict[str, Any]:
        """
        Extrait les informations complètes d'une ordonnance manuscrite

        Args:
            image_path: Chemin vers l'image de l'ordonnance

        Returns:
            Dictionnaire JSON avec les informations extraites
        """

        # Vérifier que le fichier existe
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Le fichier {image_path} n'existe pas")

        base64_image = self._encode_image(image_path)

        prompt = """Tu es un expert en OCR médical spécialisé dans l'extraction d'ordonnances manuscrites.

TÂCHE: Extrais TOUT le texte visible de cette ordonnance manuscrite avec une précision maximale.

INSTRUCTIONS CRITIQUES:
- Lis attentivement chaque mot, même s'il est difficile à déchiffrer
- Pour les mots illisibles, indique [ILLISIBLE] mais essaie de deviner le contexte
- Respecte l'orthographe exacte, même les erreurs du médecin
- Inclus TOUS les détails: posologies, durées, instructions spéciales
- Garde la structure et l'ordre original du document

RÉPONSE REQUISE: JSON strict avec cette structure exacte:
{
    "docteur": {
        "nom": "Dr. [Nom du médecin]",
        "specialite": "[Spécialité si mentionnée]",
        "adresse": "[Adresse complète du cabinet]",
        "telephone": "[Numéro si présent]"
    },
    "patient": {
        "nom": "[Nom du patient]",
        "age": "[Âge si mentionné]",
        "autres_infos": "[Autres informations patient]"
    },
    "date": "[Date de l'ordonnance format JJ/MM/AAAA]",
    "medicaments": [
        {
            "nom": "[Nom exact du médicament]",
            "dosage": "[Dosage/concentration]",
            "forme": "[Comprimé/sirop/etc.]",
            "posologie": "[Instructions de prise complètes]",
            "duree": "[Durée du traitement]",
            "quantite": "[Nombre de boîtes/unités]"
        }
    ],
    "instructions_generales": "[Instructions additionnelles du médecin]",
    "texte_brut_complet": "[Transcription exacte de TOUT le texte visible]"
}

Fournis UNIQUEMENT le JSON, sans texte additionnel."""

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]

        response = self._make_completion_json(messages)

        try:
            # Nettoyer la réponse pour extraire uniquement le JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_text = response[json_start:json_end]
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            raise Exception(f"Erreur de parsing JSON: {str(e)}\nRéponse brute: {response}")

    def extract_lab_report(self, image_path: str) -> Dict[str, Any]:
        """
        Extrait et structure les informations d'un rapport d'analyse de laboratoire

        Args:
            image_path: Chemin vers l'image du rapport d'analyse

        Returns:
            Dictionnaire structuré avec les informations du rapport
        """

        # Vérifier que le fichier existe
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Le fichier {image_path} n'existe pas")

        base64_image = self._encode_image(image_path)

        prompt = """Tu es un expert en OCR médical spécialisé dans l'analyse de rapports de laboratoire.

TÂCHE: Extrais et structure TOUTES les informations de ce rapport d'analyse avec une précision parfaite.

INSTRUCTIONS CRITIQUES:
- Identifie chaque section du rapport (hématologie, chimie, etc.)
- Extrais chaque paramètre avec sa valeur exacte et son unité
- Inclus les valeurs de référence (normales) pour chaque paramètre
- Respecte la hiérarchie et l'organisation du document
- Pour les valeurs illisibles, marque [ILLISIBLE]
- Inclus toutes les informations d'en-tête et de pied de page

RÉPONSE REQUISE: JSON structuré avec cette organisation:
{
    "informations_laboratoire": {
        "nom": "[Nom du laboratoire]",
        "adresse": "[Adresse complète]",
        "telephone": "[Numéro de téléphone]",
        "autres_infos": "[Autres informations du labo]"
    },
    "informations_patient": {
        "nom": "[Nom du patient]",
        "age": "[Âge si mentionné]",
        "sexe": "[Sexe si mentionné]",
        "date_naissance": "[Date de naissance si mentionnée]",
        "autres_infos": "[Autres informations patient]"
    },
    "informations_analyse": {
        "date_prelevement": "[Date et heure de prélèvement]",
        "date_rapport": "[Date du rapport]",
        "medecin_prescripteur": "[Nom du médecin prescripteur]",
        "type_analyse": "[Type d'analyse demandée]"
    },
    "resultats_par_section": {
        "[NOM_SECTION]": {
            "titre": "[Titre exact de la section]",
            "methode": "[Méthode d'analyse si mentionnée]",
            "parametres": [
                {
                    "nom": "[Nom du paramètre]",
                    "valeur": "[Valeur mesurée]",
                    "unite": "[Unité de mesure]",
                    "valeur_reference": "[Valeurs normales]",
                    "statut": "[Normal/Anormal/Élevé/Bas si déterminable]"
                }
            ]
        }
    },
    "commentaires_biologiste": "[Commentaires ou observations du biologiste]",
    "signatures_cachets": "[Description des signatures et cachets visibles]",
    "texte_brut_complet": "[Transcription exacte de TOUT le texte visible, conservant la mise en forme]"
}

Fournis UNIQUEMENT le JSON structuré, sans commentaires additionnels."""

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]

        response = self._make_completion_json(messages)

        try:
            # Nettoyer la réponse pour extraire uniquement le JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_text = response[json_start:json_end]
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            # Fallback: retourner le texte brut si le JSON échoue
            print(f"Erreur JSON, retour du texte brut: {str(e)}")
            return {"erreur": "Parsing JSON échoué", "texte_brut": response}

    def save_results(self, data: Any, output_path: str, format_type: str = "json"):
        """
        Sauvegarde les résultats dans un fichier

        Args:
            data: Données à sauvegarder
            output_path: Chemin de sortie
            format_type: Type de format ("json" ou "txt")
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                if format_type == "json":
                    json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    f.write(str(data))
            print(f"Résultats sauvegardés dans: {output_path}")
        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde: {str(e)}")

