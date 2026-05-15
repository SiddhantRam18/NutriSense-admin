from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
import pandas as pd
import os
import gc
import threading
from model import recommend, output_recommended_recipes

# Global dataset variable with lazy loading
dataset = None
dataset_lock = threading.Lock()
dataset_loaded = False

app = FastAPI(title="NutriSense API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionParams(BaseModel):
    n_neighbors: int = 5
    return_distance: bool = False

class PredictionIn(BaseModel):
    nutrition_input: Annotated[list[float], Field(min_length=9, max_length=9)]
    ingredients: list[str] = []
    params: Optional[PredictionParams] = None

class Recipe(BaseModel):
    Name: str
    CookTime: str
    PrepTime: str
    TotalTime: str
    RecipeIngredientParts: list[str]
    Calories: float
    FatContent: float
    SaturatedFatContent: float
    CholesterolContent: float
    SodiumContent: float
    CarbohydrateContent: float
    FiberContent: float
    SugarContent: float
    ProteinContent: float
    RecipeInstructions: list[str]

class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None

def load_dataset():
    """Lazy load dataset on first use"""
    global dataset, dataset_loaded
    
    if dataset_loaded:
        return dataset
    
    with dataset_lock:
        if dataset_loaded:
            return dataset
            
        try:
            data_path = '/app/Data/dataset_small.csv.gz'
            if os.path.exists(data_path):
                print("Loading dataset...")
                dataset = pd.read_csv(data_path, compression='gzip')
                dataset_loaded = True
                print(f"Dataset loaded: {dataset.shape}, memory: {dataset.memory_usage(deep=True).sum()//1024//1024} MB")
                gc.collect()
                return dataset
            else:
                print(f"Warning: Dataset not found at {data_path} — ensure dataset_small.csv.gz is in /app/Data/")
                dataset_loaded = True
                return None
        except Exception as e:
            print(f"Error loading dataset: {e}")
            dataset_loaded = True
            return None

@app.get("/")
def home():
    return {"health_check": "OK", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict/", response_model=PredictionOut)
def update_item(prediction_input: PredictionIn):
    """Load dataset on first prediction request"""
    data = load_dataset()
    
    if data is None:
        raise HTTPException(status_code=503, detail="Dataset not available")
    
    try:
        recommendation_dataframe = recommend(
            data,
            prediction_input.nutrition_input,
            prediction_input.ingredients,
            prediction_input.params.model_dump() if prediction_input.params else {'n_neighbors': 5, 'return_distance': False}
        )
        output = output_recommended_recipes(recommendation_dataframe)
        
        if output is None:
            return {"output": None}
        else:
            gc.collect()
            return {"output": output}
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

