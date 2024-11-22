from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import torch
from torchvision import transforms
import io
from torchvision.models.resnet import ResNet
import uvicorn

# Ajouter ResNet à la liste des classes sûres
torch.serialization.add_safe_globals([ResNet])

# Initialisation de l'application FastAPI
app = FastAPI()

# Charger le modèle avec le mappage vers le CPU
model = torch.load('C:/Users/NIKIEMA Francklin/OneDrive - ESMT/Bureau/Projet_Databeez/Détection Maladies des plantes/services/get_resnext101_weighted.pth', map_location=torch.device('cpu'), weights_only=False)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()

# Définir les transformations de prétraitement
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint pour prédire la classe d'une image.

    Args:
        file: Fichier image envoyé par l'utilisateur.
    
    Returns:
        JSON contenant la probabilité et la classe prédite.
    """
    try:
        # Lire le fichier image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Appliquer les transformations
        input_tensor = preprocess(image).unsqueeze(0).to(device)  # Ajouter la dimension batch
        
        # Effectuer la prédiction
        with torch.no_grad():
            output = model(input_tensor)
            predicted_class = output.argmax(dim=1).item()
            probabilities = torch.nn.functional.softmax(output, dim=1).cpu().numpy()
        
        # Retourner les résultats
        return JSONResponse(content={
            "predicted_class": predicted_class,
            "probabilities": probabilities.tolist()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint pour vérifier l'état de l'API
@app.get("/")
def health_check():
    return {"status": "API is running"}

#if __name__ == '__main__':
 #   uvicorn.run(app,host='localhost',port=8181)

