from advanced_medical_advisor import AdvancedMedicalAdvisor
import json

def main():
    # Initialiser le conseiller médical avec la clé API Groq
    advisor = AdvancedMedicalAdvisor(api_key="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")
    
    # Exemple 1: Consultation pour des symptômes cardiaques
    print("\n=== Exemple 1: Consultation cardiaque ===")
    symptoms_cardio = ["douleur thoracique", "essoufflement"]
    advice_cardio = advisor.get_medical_advice(
        symptoms=symptoms_cardio,
        age=45,
        is_emergency=True,
        location="Paris",
        budget=100
    )
    print(json.dumps(advice_cardio, ensure_ascii=False, indent=2))
    
    # Exemple 2: Consultation pour des problèmes de peau
    print("\n=== Exemple 2: Consultation dermatologique ===")
    symptoms_dermato = ["éruption cutanée", "démangeaisons"]
    advice_dermato = advisor.get_medical_advice(
        symptoms=symptoms_dermato,
        age=30,
        is_emergency=False,
        location="Lyon",
        budget=50
    )
    print(json.dumps(advice_dermato, ensure_ascii=False, indent=2))
    
    # Exemple 3: Consultation pédiatrique
    print("\n=== Exemple 3: Consultation pédiatrique ===")
    symptoms_pediatrie = ["fièvre", "toux"]
    advice_pediatrie = advisor.get_medical_advice(
        symptoms=symptoms_pediatrie,
        age=5,
        is_emergency=False,
        location="Marseille",
        budget=40
    )
    print(json.dumps(advice_pediatrie, ensure_ascii=False, indent=2))
    
    # Afficher l'historique des consultations
    print("\n=== Historique des consultations ===")
    history = advisor.get_consultation_history()
    print(json.dumps(history, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 