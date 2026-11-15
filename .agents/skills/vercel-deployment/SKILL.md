---
name: vercel-deployment
description: Procedures and best practices for configuring, building, and deploying the application to Vercel, including FastAPI serverless setup.
---

# Vercel Deployment Guide for FastAPI

This skill guides the agent and developers on configuring and deploying this Python/FastAPI backend to Vercel.

## 1. Project Configuration (`vercel.json`)

To run a FastAPI application on Vercel Serverless Functions:

Create or update `vercel.json` in the root directory:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

Ensure `app.py` exposes the ASGI application instance as `app`:
```python
app = FastAPI()
```

## 2. Serverless Function Limitations

- **Bundle Size**: Vercel Serverless Functions have a maximum uncompressed size limit of 250 MB.
- **Large ML Libraries**: Heavy libraries like `torch` and `torchvision` combined with large `.pth` model checkpoints may exceed serverless size limits.
  - Recommendation: Use CPU-only PyTorch wheels or host heavy inference models on Google Cloud Run, AWS Lambda with container images, or Hugging Face Spaces, and use Vercel as an API gateway / frontend host.

## 3. CLI Deployment Steps

1. Install the Vercel CLI:
   ```bash
   npm install -g vercel
   ```
2. Link or Deploy:
   ```bash
   vercel
   ```
3. Deploy to production:
   ```bash
   vercel --prod
   ```
