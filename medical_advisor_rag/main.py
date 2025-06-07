from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from medical_advisor_rag.advanced_medical_advisor import AdvancedMedicalAdvisor
from medical_advisor_rag.database import DatabaseManager
import os

app = FastAPI(
    title="Medical Advisor API",
    description="API for medical advice using RAG system",
    version="1.0.0"
)

# Récupérer l\'URL de la base de données depuis les variables d\'environnement ou utiliser la valeur par défaut
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/med_sys")
db_manager = DatabaseManager(DATABASE_URL) # Initialisation du DatabaseManager

# Initialize the medical advisor with the same key as in run_advisor.py et le db_manager
advisor = AdvancedMedicalAdvisor(api_key="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", db_manager=db_manager)

class SpecialistRecommendation(BaseModel):
    specialite: str
    raison: str
    nom_medecin: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class MedicalAdviceResponse(BaseModel):
    reassurance: str
    specialite_identifiee: Optional[str] = None
    conseils_generaux: List[str]
    specialistes_recommandes: List[SpecialistRecommendation]
    message_final: str

class MedicalAdviceRequest(BaseModel):
    symptoms: List[str]
    age: int
    is_emergency: bool
    location: str
    budget: float

@app.post("/medical-advice", response_model=MedicalAdviceResponse)
async def get_medical_advice(request: MedicalAdviceRequest):
    try:
        advice = advisor.get_medical_advice(
            symptoms=request.symptoms,
            age=request.age,
            is_emergency=request.is_emergency,
            location=request.location,
            budget=request.budget
        )
        # If the model returns an error or unexpected format, raise an exception
        if not all(k in advice for k in ("reassurance", "conseils_generaux", "specialistes_recommandes", "message_final")):
            raise ValueError("Format de réponse inattendu")
        return advice
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/consultation-history")
async def get_consultation_history():
    try:
        history = advisor.get_consultation_history()
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Nouvel endpoint pour le chat libre
class ChatRequest(BaseModel):
    user_prompt: str

@app.post("/chat", response_model=MedicalAdviceResponse)
async def chat_with_user(request: ChatRequest):
    try:
        advice = advisor.chat_with_user(request.user_prompt)
        if not all(k in advice for k in ("reassurance", "conseils_generaux", "specialistes_recommandes", "message_final")):
            raise ValueError("Format de réponse inattendu")
        return advice
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Le DatabaseManager sera automatiquement connecté/déconnecté via son contexte manager si on l'utilise globalement.
    # Pour un démarrage propre avec uvicorn, on s'assure qu'il est initialisé avant de lancer l'app.
    uvicorn.run(app, host="0.0.0.0", port=8001) 