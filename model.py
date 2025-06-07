from huggingface_hub import hf_hub_download
import os

# Download the .h5 model file
model_path = hf_hub_download(repo_id="VRJBro/skin-cancer-detection", filename="skin_cancer_model.h5")
print(f"Model downloaded to: {model_path}")