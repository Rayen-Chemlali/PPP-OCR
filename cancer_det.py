from transformers import pipeline
classifier = pipeline("image-classification", model="VRJBro/skin-cancer-detection")
image_path = "img.png"
result = classifier(image_path)
print(result)  # Outputs 'cancerous' or 'non-cancerous' with confidence