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
6. **Import CSV data into the database**
Create the necesary tables and import the CSV data into the database using the `config.py` script:
``` bash   
python src/config.py
```

6. Import CSV data into the database 
7. **Run the application**
``` bash
uvicorn src.app:app --reload --port 8080
```
8. Access the analytics endpoints at `http://localhost:8080/analytics`

## Test the API
Use the following commands to test the API endpoints:
```bash
curl http://localhost:8080/analytics/top-merchant
curl http://localhost:8080/analytics/monthly-active-merchants
curl http://localhost:8080/analytics/product-adoption
curl http://localhost:8080/analytics/kyc-funnel
curl http://localhost:8080/analytics/failure-rates
```