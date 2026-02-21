## Merchant_Analytics
Merchants interact with multiple products: they process POS transactions, sell airtime, pay bills, accept card payments, manage inventory with MonieBook, save funds, and go through KYC verification for account upgrades.

This microservice processes merchant activity data from CSV files and provides analytics through RESTful API endpoints.

### Prerequisites
- Python 3.11
- PostgreSQL (or your preferred database)
- Required Python libraries (see `requirements.txt`)

## Getting Started
1. **Clone the repository**
``` bash
git clone https://github.com/Eyiza/Merchant_Analytics.git
cd Merchant_Analytics
```

2. **Virtual Environment** - This keeps your dependencies for your project separate and organized. 
Initialize and activate a virtualenv using:
``` bash
python -m venv env
source env/bin/activate
```
Note - In Windows, the `env` does not have a `bin` directory. Use the analogous command shown below:
``` bash
env/Scripts/activate
```

3. **PIP Dependencies** - Once the virtual environment is setup and running, install the required dependencies by navigating to the repo's directory on the terminal and running:
``` bash
pip install -r requirements.txt
```
All required packages are included in the requirements file. 

4. **Set up the Database**
With Postgres running, create a `merchant_analytics_db` database:
``` bash
createdb merchant_analytics_db
```
<!-- Populate the database with the neccessary relations using:

``` bash
psql -U postgres -d merchant_analytics_db -f src/db_init.sql
```
Replace `postgres` with your database user if different. This will create the necessary tables and relations for the application to function properly. -->

5. **Environment Variables setup**
Create a `.env` and set up the necessary environment variables:
```bash
DATABASE_NAME="your_db_name"
DATABASE_USER="your_db_user"
DATABASE_PASSWORD="your_db_password"
DATABASE_HOST="your_db_host"
DATABASE_PORT="your_db_port"
```

6. **Data Ingestion**
The application expects CSV files containing merchant activity data. Each file should be named in the format `activities_YYYYMMDD.csv` and placed in a `data/` directory within the repository.

6. **Create Tables and Import CSV data into the database**
Create the necesary tables and import the CSV data into the database using the `config.py` script:
``` bash   
python src/config.py
```
This will create the necessary tables and import the data from the CSV files into the database. The script reads all CSV files in the `data/` directory, parses the data, and inserts it into the `activities` table in batches for efficiency.

7. **Run the application**
``` bash
uvicorn src.app:app --reload --port 8080
```
Access the API at `http://localhost:8080/`



## Project Structure
```
Merchant_Analytics/
├── src/
│   ├── app.py
│   ├── config.py
│   ├── db.py
│   ├── analytics.py
│   └── db_init.sql
├── data/
│   ├── activities_20240101.csv
│   ├── activities_20240102.csv
│   └── ...
├── requirements.txt
├── README.md
└── .env
```

## Test the API
Use the following commands to test the API endpoints:
```bash
curl http://localhost:8080/analytics/top-merchant
curl http://localhost:8080/analytics/monthly-active-merchants
curl http://localhost:8080/analytics/product-adoption
curl http://localhost:8080/analytics/kyc-funnel
curl http://localhost:8080/analytics/failure-rates
```

### Endpoints
The application provides the following analytics endpoints:
#### GET /analytics/top-merchant
- Sample URL: `curl http://127.0.0.1:5000/analytics/top-merchant`
- Request Arguments: None
- Response body:
  - Returns the merchant with the highest total successful transaction amount across ALL products.
``` {
    "merchant_id": "MRC-009405",
    "total_volume": 181479333.57
}
```

#### GET /analytics/monthly-active-merchants
- Sample URL: `curl http://localhost:8080/analytics/monthly-active-merchants`
- Request Arguments: None
- Response body:
  - Returns the count of unique merchants with at least one successful event per month.
``` {
    "2024-01": 8234, 
    "2024-02": 8456
}
```

#### GET /analytics/product-adoption
- Sample URL: `curl http://localhost:8080/analytics/product-adoption`
- Request Arguments: None
- Response body:
  - Returns a list of products with the count of unique merchants that have used each product.
``` {
    "BILLS": 4379,
    "SAVINGS": 4368,
    "POS": 4348,
    "AIRTIME": 4277,
    "MONIEBOOK": 4267,
    "CARD_PAYMENT": 4233,
    "KYC": 4167
}
```
