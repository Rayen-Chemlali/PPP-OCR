from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import tempfile
from pathlib import Path
from typing import Dict, Any
import uvicorn

# Import de votre classe MedicalOCR
from OCR.groq_client import MedicalOCR

# Initialisation de FastAPI
app = FastAPI(
    title="Medical OCR API",
    description="API pour l'extraction OCR de documents médicaux (ordonnances et analyses de laboratoire)",
    version="1.0.0"
)

# Initialisation du client OCR
ocr = MedicalOCR(
    api_key="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",
    seed=1234
)


# Modèles Pydantic pour les requêtes
class ImagePathRequest(BaseModel):
    image_path: str


# Route de base
@app.get("/")
async def root():
    return {"message": "Medical OCR API", "version": "1.0.0", "status": "active"}


# Endpoint pour l'extraction complète d'ordonnance
@app.post("/extract-prescription", response_model=Dict[str, Any])
async def extract_prescription_endpoint(request: ImagePathRequest):
    """
    Extrait les informations complètes d'une ordonnance manuscrite

    Args:
        request: Objet contenant le chemin vers l'image

    Returns:
        Dictionnaire JSON avec les informations extraites de l'ordonnance
    """
    try:
        # Vérifier que le fichier existe
        if not Path(request.image_path).exists():
            raise HTTPException(status_code=404, detail=f"Le fichier {request.image_path} n'existe pas")

        # Extraction des données
        result = ocr.extract_prescription(request.image_path)
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction: {str(e)}")


# Endpoint pour l'extraction simplifiée d'ordonnance
@app.post("/extract-prescription-simple", response_model=Dict[str, str])
async def extract_prescription_simple_endpoint(request: ImagePathRequest):
    """
    Extrait les informations essentielles d'une ordonnance de manière simplifiée

    Args:
        request: Objet contenant le chemin vers l'image

    Returns:
        Dictionnaire JSON simplifié avec les informations extraites
    """
    try:
        # Vérifier que le fichier existe
        if not Path(request.image_path).exists():
            raise HTTPException(status_code=404, detail=f"Le fichier {request.image_path} n'existe pas")

        # Extraction des données
        result = ocr.extract_prescription_simple(request.image_path)
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction: {str(e)}")


# Endpoint pour l'extraction de rapport d'analyse de laboratoire
@app.post("/extract-lab-report", response_model=Dict[str, Any])
async def extract_lab_report_endpoint(request: ImagePathRequest):
    """
    Extrait et structure les informations d'un rapport d'analyse de laboratoire

    Args:
        request: Objet contenant le chemin vers l'image

    Returns:
        Dictionnaire structuré avec les informations du rapport
    """
    try:
        # Vérifier que le fichier existe
        if not Path(request.image_path).exists():
            raise HTTPException(status_code=404, detail=f"Le fichier {request.image_path} n'existe pas")

        # Extraction des données
        result = ocr.extract_lab_report(request.image_path)
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction: {str(e)}")


# Endpoints avec upload de fichier (alternative)
@app.post("/upload-prescription")
async def upload_and_extract_prescription(file: UploadFile = File(...)):
    """
    Upload d'une image d'ordonnance et extraction des informations complètes
    """
    try:
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        try:
            # Extraction des données
            result = ocr.extract_prescription(temp_path)
            return JSONResponse(content=result)
        finally:
            # Nettoyer le fichier temporaire
            os.unlink(temp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction: {str(e)}")


@app.post("/upload-prescription-simple")
async def upload_and_extract_prescription_simple(file: UploadFile = File(...)):
    """
    Upload d'une image d'ordonnance et extraction simplifiée
    """
    try:
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        try:
            # Extraction des données
            result = ocr.extract_prescription_simple(temp_path)
            return JSONResponse(content=result)
        finally:
            # Nettoyer le fichier temporaire
            os.unlink(temp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction: {str(e)}")


@app.post("/upload-lab-report")
async def upload_and_extract_lab_report(file: UploadFile = File(...)):
    """
    Upload d'une image de rapport de laboratoire et extraction des informations
    """
    try:
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        try:
            # Extraction des données
            result = ocr.extract_lab_report(temp_path)
            return JSONResponse(content=result)
        finally:
            # Nettoyer le fichier temporaire
            os.unlink(temp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction: {str(e)}")


# Endpoint pour tester les trois fonctions (comme votre code original)
@app.post("/test-all")
async def test_all_functions():
    """
    Teste les trois fonctions OCR avec des fichiers par défaut
    (nécessite ord.png et hema.png dans le répertoire courant)
    """
    try:
        results = {}

        # Vérifier les fichiers de test
        if Path("ord.png").exists():
            results["prescription"] = ocr.extract_prescription("ord.png")
            results["prescription_simple"] = ocr.extract_prescription_simple("ord.png")
        else:
            results["prescription"] = "Fichier ord.png non trouvé"
            results["prescription_simple"] = "Fichier ord.png non trouvé"

        if Path("hema.png").exists():
            results["lab_report"] = ocr.extract_lab_report("hema.png")
        else:
            results["lab_report"] = "Fichier hema.png non trouvé"

        return JSONResponse(content=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du test: {str(e)}")


# Point d'entrée principal
if __name__ == "__main__":
    print("🚀 Démarrage du serveur Medical OCR API...")
    print("📋 Endpoints disponibles:")
    print("  - POST /extract-prescription")
    print("  - POST /extract-prescription-simple")
    print("  - POST /extract-lab-report")
    print("  - POST /upload-prescription")
    print("  - POST /upload-prescription-simple")
    print("  - POST /upload-lab-report")
    print("  - POST /test-all")
    print("📖 Documentation: http://localhost:8000/docs")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")