import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "true"  # Désactiver l'avertissement de symlinks

from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch
import time

# Vérifier CUDA et la configuration
print("CUDA disponible :", torch.cuda.is_available())
print("Version de PyTorch :", torch.__version__)
print("Version CUDA de PyTorch :", torch.version.cuda)
if torch.cuda.is_available():
    print("Nom du GPU :", torch.cuda.get_device_name(0))

# Charger le processeur et le modèle
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten", use_fast=True)
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

# Déplacer le modèle vers le GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()  # Mode évaluation pour optimiser

# Optimisation avec torch.compile (si PyTorch >= 2.0)
if torch.__version__.startswith("2"):
    try:
        model = torch.compile(model)
        print("Modèle optimisé avec torch.compile")
    except Exception as e:
        print("Erreur lors de l'optimisation avec torch.compile :", e)

def ocr_image(image_path):
    # Charger et redimensionner l'image
    image = Image.open(image_path).convert("RGB").resize((512, 512))

    # Prétraiter l'image
    pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)

    # Générer le texte sans calcul de gradients
    with torch.no_grad():
        generated_ids = model.generate(pixel_values, max_length=120)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return generated_text

# Exemple d'utilisation
if __name__ == "__main__":
    image_path = "OCR/ord.png"  # Vérifie que ce chemin est correct
    try:
        start_time = time.time()
        texte = ocr_image(image_path)
        print("Texte extrait :", texte)
        print(f"Temps d'exécution : {time.time() - start_time} secondes")

        # Sauvegarder le texte dans un fichier
        with open("resultat_ocr.txt", "w", encoding="utf-8") as f:
            f.write(texte)
    except Exception as e:
        print("Erreur lors du traitement de l'image :", e)