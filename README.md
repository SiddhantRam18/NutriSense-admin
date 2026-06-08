# NutriSense — AI-Powered Diet Recommendation System

NutriSense is a full-stack machine learning application that generates personalized meal plans and recipe recommendations based on nutritional goals, body metrics, and ingredient preferences.

## Live Demo

> Hosted on Streamlit Community Cloud — link in repository about section.

## Features

- **Automatic Diet Recommendation** — input age, height, weight, gender, and activity level to receive a fully personalized daily meal plan with calorie breakdowns across breakfast, snacks, lunch, and dinner
- **Custom Food Search** — set specific nutritional targets and optional ingredient filters to discover matching recipes
- **BMI & Calorie Calculator** — real-time BMI classification and daily calorie estimates across seven weight-management plans
- **Nutritional Analytics** — interactive pie charts and bar charts (Apache ECharts) comparing chosen meal nutrition against daily targets
- **Recipe Details** — ingredients, step-by-step instructions, cook/prep times, and food images pulled automatically from TheMealDB and Openverse

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit, Apache ECharts |
| Backend | FastAPI, Uvicorn |
| ML Model | Scikit-learn (content-based filtering, KNN) |
| Data | ~500k recipes dataset with full nutritional values |
| Containerisation | Docker, Docker Compose |
| Deployment | Streamlit Community Cloud (frontend) |

## Architecture

```
┌─────────────────────┐        HTTP        ┌──────────────────────┐
│  Streamlit Frontend │ ──────────────────▶ │   FastAPI Backend    │
│  (port 8501)        │                     │   (port 7860/8080)   │
└─────────────────────┘                     └──────────┬───────────┘
                                                       │
                                            ┌──────────▼───────────┐
                                            │  Scikit-learn KNN    │
                                            │  Recipe Dataset      │
                                            └──────────────────────┘
```

## Running Locally

**Prerequisites:** Docker and Docker Compose installed.

```bash
git clone https://github.com/AMJ2004/NutriSense.git
cd NutriSense
docker-compose up --build
```

- Frontend: `http://localhost:8501`
- Backend API docs: `http://localhost:8080/docs`

## Project Structure

```
NutriSense/
├── FastAPI_Backend/
│   ├── main.py          # API endpoints
│   ├── model.py         # KNN recommendation model
│   └── Dockerfile
├── Streamlit_Frontend/
│   ├── Hello.py         # Landing page
│   ├── pages/
│   │   ├── 1_💪_Diet_Recommendation.py
│   │   └── 2_🔍_Custom_Food_Recommendation.py
│   ├── grainient_bg.py  # Animated background
│   ├── ImageFinder/     # Recipe image fetcher
│   └── Dockerfile
├── Data/
│   └── dataset.csv      # Recipe + nutrition dataset
└── docker-compose.yml
```

## How It Works

1. The user provides body metrics and a weight goal
2. The frontend calculates a target calorie distribution across meals
3. A request is sent to the FastAPI backend with the nutritional targets
4. The backend runs a KNN model on the recipe dataset to find the closest nutritional matches
5. Results are returned and displayed with recipe images, ingredients, and cooking instructions
