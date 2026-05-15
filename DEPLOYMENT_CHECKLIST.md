# NutriSense Deployment Checklist

Complete checklist for deploying NutriSense to production (Streamlit Cloud frontend + HF Spaces backend).

---

## Pre-Deployment Verification

### Code & Configuration
- [ ] **main.py** — Verify `/predict/` endpoint signature matches frontend payload
  - Should accept: `{nutrition_input: list[9 floats], ingredients: list[str]}`
  - Should NOT require `params` in request body
- [ ] **model.py** — Verify NUTRITION_COLS list has exactly 9 nutrition parameters
  - Expected: `['Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent']`
- [ ] **Recipe Pydantic model** — Confirm time fields accept both str and int
  - `CookTime: str | int`
  - `PrepTime: str | int`
  - `TotalTime: str | int`
- [ ] **Generate_Recommendations.py** — Verify backend URL uses secrets
  - Line 5: `BACKEND_URL = st.secrets.get("backend_url", "http://localhost:8080")`
  - Payload only sends: `{nutrition_input, ingredients}` (no `params`)
- [ ] **Dataset** — Verify `Data/dataset.csv` is gzip-compressed and readable
  - Size should be ~91 MB
  - File format: CSV with gzip compression
  - Can test locally: `python -c "import pandas as pd; df = pd.read_csv('Data/dataset.csv', compression='gzip'); print(df.shape)"`

### Docker & Requirements
- [ ] **FastAPI_Backend/requirements.txt**
  - fastapi==0.104.1
  - uvicorn==0.24.0
  - numpy==1.24.3
  - scikit-learn==1.3.2
  - pandas==2.0.3
  - pydantic==2.4.2
- [ ] **Streamlit_Frontend/requirements.txt**
  - streamlit>=1.28.1
  - requests==2.31.0
  - streamlit-echarts==0.4.0
  - All required packages present
- [ ] **FastAPI_Backend/Dockerfile**
  - Exposes port 7860 (HF Spaces standard)
  - Multi-stage build for minimal image size
  - `CMD` runs: `uvicorn main:app --host 0.0.0.0 --port 7860 --workers 1`
- [ ] **Streamlit_Frontend/Dockerfile**
  - Exposes port 8501
  - Runs: `streamlit run --server.port=8501 Hello.py`
- [ ] **docker-compose.yml**
  - Frontend: `ports: 8501:8501`
  - Backend: `ports: 8080:7860` (host:container mapping)
  - Both services in same `project_network`
  - Volumes mounted correctly

### Local Testing
- [ ] **Docker Compose Build** — Completes without errors
  ```bash
  docker-compose up --build
  ```
- [ ] **Backend Health Check** — Returns 200 OK
  ```bash
  curl http://localhost:8080/health
  # {"status":"healthy"}
  ```
- [ ] **Backend Prediction** — Returns recipes with 200 status
  ```bash
  curl -X POST http://localhost:8080/predict/ \
    -H "Content-Type: application/json" \
    -d '{"nutrition_input":[100,5,2,0,200,15,2,5,8],"ingredients":[]}'
  ```
  - Should return ~5 recipes in ~5-10 seconds (first load) or <1 second (cached)
  - Each recipe should include: Name, CookTime, PrepTime, TotalTime, etc.
- [ ] **Frontend Locally**
  - Loads on `http://localhost:8501`
  - Can enter nutrition values
  - Can click "Get Recommendations" without errors
  - Displays recipes from backend

---

## Hugging Face Spaces Deployment

### Create & Configure Space
- [ ] **Create HF Space**
  - Name: `nutrisense-backend` (or chosen name)
  - SDK: Docker
  - Visibility: Public
- [ ] **Connect GitHub Repository**
  - Repo: `AMJ2004/NutriSense`
  - Branch: `main`
  - Dockerfile path: `FastAPI_Backend/Dockerfile`
- [ ] **Enable Auto-Sync**
  - Check that "Sync with GitHub" is enabled
  - Space will auto-rebuild on push to `main`
- [ ] **Wait for Build** — Space builds and deploys (5-10 minutes)
  - Check **Build** tab for errors
  - Once deployed, space shows **Running** status

### Test HF Space Backend
- [ ] **Get Space URL**
  - Format: `https://yourusername-spacename.hf.space`
  - Confirm URL is accessible publicly
- [ ] **Health Check** — Returns 200
  ```bash
  curl https://yourusername-spacename.hf.space/health
  ```
- [ ] **Dataset Loading** — First prediction takes 30-60s
  - Check logs for: `Loading dataset...`
  - Subsequent requests should be fast (<1s)
- [ ] **Prediction Endpoint** — Returns recipes
  ```bash
  curl -X POST https://yourusername-spacename.hf.space/predict/ \
    -H "Content-Type: application/json" \
    -d '{"nutrition_input":[100,5,2,0,200,15,2,5,8],"ingredients":[]}'
  ```

---

## Streamlit Cloud Deployment

### Update Secrets
- [ ] **Add Backend URL to Secrets**
  - Go to Streamlit Cloud app settings
  - Click **Secrets**
  - Add:
    ```
    backend_url = "https://yourusername-spacename.hf.space"
    ```
  - Save (takes ~5 minutes to propagate)
- [ ] **Verify Secrets Updated**
  - Refresh app in browser
  - Check browser console (F12) for any backend URL errors

### Test Frontend
- [ ] **Frontend Loads** — App on `https://nutrisense-health.streamlit.app` loads
- [ ] **Navigate to Diet Recommendation** — Click "1_💪_Diet_Recommendation"
- [ ] **Enter Nutrition Values** — Fill in the nutrition input fields
- [ ] **Click Get Recommendations** — App calls backend
- [ ] **Recipes Display** — 5 recipes show with images and details
  - Recipe name, prep time, cook time, ingredients, nutrition

---

## Post-Deployment Validation

### Full End-to-End Test
- [ ] User opens Streamlit app
- [ ] User enters nutrition values (e.g., 100 cal, 5g fat, etc.)
- [ ] User clicks "Get Recommendations"
- [ ] Recipes load within 10 seconds
- [ ] Each recipe shows: Name, Prep/Cook/Total Time, Ingredients, Nutrition Info

### Edge Cases
- [ ] **Empty Ingredients** — Recommendations work without ingredient filter
- [ ] **With Ingredients** — Recommendations work with ingredients (e.g., ["tomato", "basil"])
- [ ] **Invalid Nutrition Input** — App shows error if <9 values provided
- [ ] **Timeout Handling** — If backend takes >90s, Streamlit shows timeout message

### Monitoring
- [ ] **Backend Logs** — HF Space dashboard shows requests
- [ ] **Frontend Errors** — No 500 errors in Streamlit Cloud logs
- [ ] **Response Times** — Typical prediction <5 seconds (after first cold start)

---

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| HF Space stuck "Building" | Docker build error | Check Build tab logs, verify Dockerfile & requirements |
| 503 "Dataset not available" | Dataset file missing or load error | Verify `Data/dataset.csv` is in repo, 90MB gzip format |
| 422 Validation errors | Time fields receiving int not str | Update Recipe model: `CookTime: str \| int` |
| Frontend can't reach backend | Wrong backend URL | Update Streamlit secrets with exact HF Space URL |
| Slow first request (30-60s) | Dataset lazy loads on first request | Normal; subsequent requests cached in memory |
| Frontend shows "Failed to connect" | Backend URL wrong or HF Space private | Check secrets, ensure HF Space visibility is Public |

---

## Rollback Plan

If something breaks after deployment:

1. **Quick Fix** — Revert latest code push to GitHub
   ```bash
   git revert HEAD
   git push origin main
   ```
   - HF Space auto-rebuilds with reverted code (~5 min)

2. **Manual Revert** — Manually rebuild HF Space
   - Go to HF Space → **Settings** → Click **Rebuild**

3. **Downtime Prevention** — Keep old backend URL in Streamlit secrets
   - If new HF Space fails, temporarily revert `backend_url` secret to old endpoint
   - Users won't notice downtime

---

## Success Criteria

✅ **Deployment is successful when:**

- [ ] HF Space is **Running** and publicly accessible
- [ ] `/health` endpoint returns `{"status":"healthy"}`
- [ ] `/predict/` endpoint accepts requests and returns recipes
- [ ] Frontend fetches recommendations from HF Space backend
- [ ] First request after deployment completes in <60 seconds
- [ ] Subsequent requests complete in <5 seconds
- [ ] No errors in Streamlit Cloud or HF Space logs
- [ ] Full end-to-end workflow works (user → Streamlit → HF Space → recipes)

---

## Post-Deployment Checklist

After successful deployment:

- [ ] Document the HF Space URL for future reference
- [ ] Save Streamlit secrets backup
- [ ] Add deployment notes to README.md with the live URLs
- [ ] Monitor logs for 24 hours post-deployment
- [ ] Get user feedback on recommendation quality
- [ ] Plan future dataset updates (if needed)

---

**Need help?** See [HF_SPACES_DEPLOYMENT.md](HF_SPACES_DEPLOYMENT.md) for detailed instructions.
