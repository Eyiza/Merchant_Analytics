from fastapi import FastAPI
# from fastapi.resources import JSONResponse
from src.db import get_connection

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to the Merchant Analytics API!",
        "status": "ok"
        }