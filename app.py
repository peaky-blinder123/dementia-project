import io
import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import gdown

app = FastAPI(title="NeuroScan AI — Oasis Dementia Classification")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define class names matching training order
CLASS_NAMES = ['Mild Dementia', 'Moderate Dementia', 'Non Demented', 'Very mild Dementia']

# Setup Device & Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 4)

MODEL_PATH = "best_model.pt"
FILE_ID = "1IR15vcwLLRoW75MYqOI57nUbTE3fwQYg"
URL = f"https://drive.google.com/uc?id={FILE_ID}"

if not os.path.exists(MODEL_PATH):
    print("Downloading model weights from Google Drive...")
    gdown.download(URL, MODEL_PATH, quiet=False)
    print("Model downloaded successfully!")

# Load best_model.pt
state_dict = torch.load(MODEL_PATH, map_location=device)
if "model_state_dict" in state_dict:
    model.load_state_dict(state_dict["model_state_dict"])
else:
    model.load_state_dict(state_dict)

model.to(device)
model.eval()

# Image Preprocessing Pipeline (matching training validation transforms)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Mount static folder
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    index_file = os.path.join("static", "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "NeuroScan AI Backend is running successfully!"}

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "model": "ResNet18",
        "classes": CLASS_NAMES,
        "device": str(device)
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

    # Preprocess image
    tensor = transform(image).unsqueeze(0).to(device)

    # Inference
    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        conf, predicted = torch.max(probabilities, 1)

    predicted_class = CLASS_NAMES[predicted.item()]
    confidence_score = conf.item()

    return {
        "prediction": predicted_class,
        "confidence": round(confidence_score * 100, 2),
        "probabilities": {CLASS_NAMES[i]: round(probabilities[0][i].item() * 100, 2) for i in range(4)}
    }
