## Merchant_Analytics
Merchants interact with multiple products: they process POS transactions, sell airtime, pay bills, accept card payments, manage inventory with MonieBook, save funds, and go through KYC verification for account upgrades.

This microservice processes merchant activity data from CSV files and provides analytics through RESTful API endpoints.

### Prerequisites
- Python 3.11
- PostgreSQL (or your preferred database)
- Required Python libraries (see `requirements.txt`)

## Getting Started
1. Clone the repository
```
git clone https://github.com/Eyiza/Merchant_Analytics.git
cd Merchant_Analytics
```
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your database and update the connection settings in `config.py`
4. Import CSV data into the database (see instructions below)
5. Start the application: `python app.py`
6. Access the analytics endpoints at `http://localhost:8080/analytics`

## Test the API
Use the following commands to test the API endpoints:
```bash
curl http://localhost:8080/analytics/top-merchant
curl http://localhost:8080/analytics/monthly-active-merchants
curl http://localhost:8080/analytics/product-adoption
curl http://localhost:8080/analytics/kyc-funnel
curl http://localhost:8080/analytics/failure-rates
```