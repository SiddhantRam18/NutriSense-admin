import requests
import streamlit as st
import json

BACKEND_URL = st.secrets.get("backend_url", "http://localhost:8080")

class Generator:
    def __init__(self,nutrition_input:list,ingredients:list=[],params:dict={'n_neighbors':5,'return_distance':False}):
        self.nutrition_input=nutrition_input
        self.ingredients=ingredients
        self.params=params

    def set_request(self,nutrition_input:list,ingredients:list,params:dict):
        self.nutrition_input=nutrition_input
        self.ingredients=ingredients
        self.params=params

    def generate(self,):
        try:
            payload={
                'nutrition_input':self.nutrition_input,
                'ingredients':self.ingredients,
                'params':self.params
            }
            response=requests.post(
                f"{BACKEND_URL}/predict/",
                json=payload,
                timeout=90
            )
            if response.status_code == 200:
                return response
            else:
                st.error(f"Backend error: {response.status_code} — {response.text}")
                return None
        except Exception as e:
            st.error(f"Failed to connect to backend: {str(e)}")
            return None
