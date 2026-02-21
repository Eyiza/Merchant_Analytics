import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration
DATABASE_NAME = os.environ.get("DATABASE_NAME", "merchant_analytics_db")
DATABASE_USER = os.environ.get("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "password")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_PORT = os.environ.get("DATABASE_PORT", "5432")

def get_connection():
    """Establish a connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            # minconn = 1,
            # maxconn = 10,
            dbname=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            cursor_factory=RealDictCursor
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None