# Hugging Face Spaces Deployment Guide for NutriSense Backend

This guide walks through deploying the FastAPI backend to Hugging Face Spaces, making it production-ready for the Streamlit frontend on Streamlit Cloud.

---

## Prerequisites
- Hugging Face account (free tier works; CPU Basic space is 16 GB RAM, more than enough)
- GitHub access to AMJ2004/NutriSense repository
- Streamlit Cloud secrets management access

---

## Step 1: Create a Hugging Face Space

1. **Go to [huggingface.co/spaces](https://huggingface.co/spaces)** and click **"Create new Space"**
2. **Fill in the details:**
   - **Space name:** `nutrisense-backend` (or similar)
   - **License:** Choose any (e.g., MIT or Apache 2.0)
   - **Space SDK:** Select **Docker**
   - **Visibility:** Public (needed for frontend to access)
3. **Click "Create Space"**

---

## Step 2: Connect to GitHub Repository

1. Once the space is created, go to **Settings** → **Repository details**
2. **Enable persistent storage** (optional, but recommended for logging)
3. **Connect GitHub repo:**
   - Under "Repository sync," select **GitHub**
   - Authorize HF to access GitHub
   - Select repo: `AMJ2004/NutriSense`
   - Select branch: `main`
4. **Set Dockerfile path:** `FastAPI_Backend/Dockerfile`
5. **Click "Save"**

HF Spaces will now:
- Auto-pull from GitHub on every push to `main`
- Build the Dockerfile
- Deploy to `https://yourusername-nutrisense-backend.hf.space`

---

## Step 3: Get Your Space URL

Once deployed (takes ~5-10 minutes), your space URL will be:
```
https://yourusername-nutrisense-backend.hf.space
```

Test it with:
```bash
curl https://yourusername-nutrisense-backend.hf.space/health
# Should return: {"status":"healthy"}
```

---

## Step 4: Update Streamlit Cloud Secrets

1. Go to **[streamlit.io/cloud](https://streamlit.io/cloud)** and open your app settings
2. Click **Secrets** (or the gear icon)
3. Add/update the secret:
   ```
   backend_url = "https://yourusername-nutrisense-backend.hf.space"
   ```
4. **Save**

The frontend will now connect to your HF Space backend.

---

## Step 5: End-to-End Testing

### Test the Backend Directly
```bash
# Health check
curl https://yourusername-nutrisense-backend.hf.space/health

# Test prediction endpoint
curl -X POST https://yourusername-nutrisense-backend.hf.space/predict/ \
  -H "Content-Type: application/json" \
  -d '{"nutrition_input":[100,5,2,0,200,15,2,5,8], "ingredients":[]}'
# Should return a list of 5 recommended recipes
```

### Test the Full Frontend
1. Go to **[nutrisense-health.streamlit.app](https://nutrisense-health.streamlit.app)**
2. Navigate to **"1_💪_Diet_Recommendation"**
3. Enter nutrition values and click **"Get Recommendations"**
4. Verify recipes load successfully

---

## Troubleshooting

### Space shows "Building" or "Running" forever
- Check the **Build** tab in the space settings for errors
- Common issues:
  - Missing `Data/dataset.csv` (verify file is in repo)
  - Wrong Dockerfile path (should be `FastAPI_Backend/Dockerfile`)
  - Python package install failure (check `requirements.txt`)

### 503 "Dataset not available"
- The backend needs ~30 seconds for cold start (first request loads 375K recipes)
- Wait 30s after space starts before testing
- Check logs in HF Space dashboard for "Loading dataset..." message

### 422 Validation errors
- Ensure `Generate_Recommendations.py` is not sending `params` dict
- Payload should only have `nutrition_input` and `ingredients`

### Frontend can't reach backend
- Check Streamlit secrets: `backend_url` must be exact HF Space URL
- Ensure HF Space is **Public** (Settings → Visibility)
- Wait 5 minutes after updating secrets for Streamlit Cloud to sync

---

## How Deployment Works

```
Streamlit Cloud                HF Spaces (Docker)
┌─────────────────┐            ┌──────────────────────────┐
│  Frontend App   │            │  FastAPI Backend        │
│  (Hello.py)     │────HTTP──→ │  (main.py)              │
│  Streamlit Cloud│ backend_url│  Port: 7860             │
└─────────────────┘            │  Lazy-loads dataset.csv │
                                │  (~375K recipes, 90MB)  │
                                └──────────────────────────┘
```

1. User opens Streamlit app → requests recommendations
2. Frontend sends POST to HF Space `/predict/` endpoint
3. Backend loads dataset (first request only, then cached)
4. Backend runs KNN algorithm on nutrition input
5. Backend returns 5 closest recipe matches
6. Frontend displays recipes with images

---

## Environment Configuration

The Dockerfile sets these for optimal performance:

```dockerfile
# Memory optimization for HF Spaces (16 GB CPU Basic)
ENV MALLOC_TRIM_THRESHOLD_=64000
ENV MALLOC_MMAP_THRESHOLD_=131072
ENV MALLOC_MMAP_MAX_=65536

# Keep-alive and timeout
--timeout-keep-alive 5

# Workers (1 worker for shared HF resources)
--workers 1
```

---

## Maintenance & Updates

**To update the backend:**
1. Make changes to `FastAPI_Backend/` or `Data/dataset.csv`
2. Push to GitHub `main` branch
3. HF Spaces auto-triggers rebuild (~5 min)
4. No manual intervention needed

**To check logs:**
- HF Space dashboard → **Logs** tab
- Shows build & runtime output

---

## Important Notes

- **Data privacy:** The dataset.csv is public and included in the Docker image
- **Cold starts:** First request after deployment takes 30-60s (dataset loads)
- **Memory:** Full dataset uses ~2-3GB RAM in container (well under 16GB limit)
- **Concurrent requests:** Single worker handles 1 request at a time; others queue
- **Dataset updates:** Rebuild space to pick up new dataset.csv

For questions or issues, check the [NutriSense GitHub repo](https://github.com/AMJ2004/NutriSense).
