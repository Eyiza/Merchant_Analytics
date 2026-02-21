from fastapi import FastAPI
# from fastapi.resources import JSONResponse
from src.db import get_connection
from src.analytics import get_top_merchant

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to the Merchant Analytics API!",
        "status": "ok"
        }

@app.get("/analytics/top-merchant")
def top_merchant():
    result = get_top_merchant()
    if result is None:
        return {"message": "No successful transactions found."}
    return result

@app.get("/analytics/monthly-active-merchants")
def monthly_active_merchants():
    from src.analytics import get_monthly_active_merchants
    result = get_monthly_active_merchants()
    return result