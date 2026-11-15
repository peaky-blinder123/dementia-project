# NeuroScan AI — Dementia & Alzheimer's MRI Stage Classifier

NeuroScan AI is a deep-learning-powered clinical screening system designed to classify brain MRI scans into dementia progression stages based on the OASIS (Open Access Series of Imaging Studies) dataset.

---

## 🧠 Key Features

- **ResNet18 Deep Learning Backbone**: Trained and evaluated on OASIS brain MRI axial slices.
- **4-Stage Cognitive Classification**:
  - `Non Demented` (Normal Controls)
  - `Very mild Dementia` (Early impairment / CDR 0.5)
  - `Mild Dementia` (Mild atrophy / CDR 1.0)
  - `Moderate Dementia` (Advanced atrophy / CDR 2.0)
- **Unified Full-Stack Architecture**: Single lightweight FastAPI application serving both the modern medical UI and prediction API.
- **Interactive Clinical Dashboard**:
  - Drag-and-drop axial brain MRI upload with real-time scan animation.
  - **1-Click OASIS Sample Scans** for immediate demonstration without requiring external image files.
  - Softmax class probability distribution bars.
  - Clinical interpretations and typical CDR stage descriptions.
  - One-click formatted **Printable / PDF Clinical Summary Report**.
- **Containerized & Production-Ready**: Preconfigured `Dockerfile` with CPU-optimized PyTorch wheels for instant deployment to Hugging Face Spaces, Render, Railway, or any cloud host.

---

## 🚀 Quick Start (Run Locally)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
uvicorn app:app --reload --port 8000
```

### 3. Open in Browser
Navigate to:
```
http://127.0.0.1:8000
```

---

## 📡 REST API Reference

### Health Check
- **`GET /api/health`**
- Returns backend operational status, model backbone, and active device (`cpu` / `cuda`).

### Predict Stage
- **`POST /predict`**
- **Payload**: `multipart/form-data` with `file: <binary image>`
- **Sample Response**:
  ```json
  {
    "prediction": "Mild Dementia",
    "confidence": 90.95,
    "probabilities": {
      "Mild Dementia": 90.95,
      "Moderate Dementia": 0.0,
      "Non Demented": 2.18,
      "Very mild Dementia": 6.87
    }
  }
  ```

---

## ☁️ 1-Click Deployment Options

### Option 1: Hugging Face Spaces (Recommended for ML Apps)
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **"Create new Space"**.
2. Select **Docker** as the Space SDK (Blank).
3. Push this repository to your Hugging Face Space git remote:
   ```bash
   git remote add space https://huggingface.co/spaces/<your-username>/<your-space-name>
   git push space main
   ```
4. Hugging Face builds and deploys the app with dedicated free CPU resources and zero cold-start limits.

### Option 2: Render.com
1. Create a new **Web Service** on [render.com](https://render.com).
2. Connect your GitHub repository.
3. Choose **Docker** as the Environment.
4. Render automatically detects the `Dockerfile` and deploys the unified application.

### Option 3: Local Docker Container
```bash
docker build -t neuroscan-ai .
docker run -p 7860:7860 neuroscan-ai
```
Open `http://localhost:7860`.

---

## ⚖️ Clinical & Research Disclaimer
*NeuroScan AI is built strictly for scientific research, benchmarking, and demonstration purposes. Output probabilities should not be used as an independent medical diagnosis. Radiological evaluations must be performed by certified clinical neurologists.*
