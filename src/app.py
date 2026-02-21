from fastapi import FastAPI
# from fastapi.resources import JSONResponse
from src.db import get_connection
from src.analytics import get_top_merchant
from src.analytics import get_monthly_active_merchants
from src.analytics import get_product_adoption
from src.analytics import get_kyc_funnel

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
    return get_monthly_active_merchants()

@app.get("/analytics/product-adoption")
def product_adoption():
    return get_product_adoption()

@app.get("/analytics/kyc-funnel")
def kyc_funnel():
    return get_kyc_funnel()