import os
import csv 
from datetime import datetime
import glob 
from uuid import UUID
from db import get_connection
from psycopg2.extras import execute_batch

def parse_uuid(value: str):
    try:
        return str(UUID(value))
    except Exception:
        return None

def parse_timestamp(value: str):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None

def parse_amount(value: str):
    if value is None or value == "":
        return 0.0
    try:
        return float(value)
    except Exception:
        return 0.0

def create_tables():
    """Create the necessary tables in the PostgreSQL database."""
    conn = get_connection()
    if conn is None:
        print("Failed to connect to the database. Cannot create tables.")
        return
    
    cur = conn.cursor()
    try:
        cur.execute(open("src/db_init.sql", "r").read())
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error creating tables: {e}")
    finally:
        conn.close()
        cur.close()

DATA_DIR = 'data'  # Directory where CSV files are stored

def load_csv_to_db():
    """Load data from a CSV file into the PostgreSQL database."""
    conn = get_connection()
    if conn is None:
        print("Failed to connect to the database. Cannot load data.")
        return
    
    cur = conn.cursor()
    try:
        files = glob.glob(os.path.join(DATA_DIR, "activities_*.csv"))
        print(f"Found {len(files)} files to load. This may take a few minutes...")

        batch = []
        batch_size = 5000

        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # try:
                    event_id = parse_uuid(row["event_id"])
                    # event_id = str(UUID(row["event_id"]))
                    merchant_id = row["merchant_id"]
                    # event_timestamp = datetime.fromisoformat(row["event_timestamp"])
                    event_timestamp = parse_timestamp(row["event_timestamp"])
                    product = row["product"]
                    event_type = row["event_type"]
                    # amount = float(row["amount"] or 0)
                    amount = parse_amount(row["amount"])
                    status = row["status"]
                    channel = row["channel"]
                    region = row.get("region")
                    merchant_tier = row.get("merchant_tier")

                    if not event_id or not merchant_id or not event_timestamp:
                        continue

                    batch.append((
                        event_id,
                        merchant_id,
                        event_timestamp,
                        product,
                        event_type,
                        amount,
                        status,
                        channel,
                        region,
                        merchant_tier
                    ))

                    if len(batch) >= batch_size:
                        execute_batch(cur, """
                            INSERT INTO activities (
                                event_id, merchant_id, event_timestamp, product, event_type,
                                amount, status, channel, region, merchant_tier
                            ) VALUES (
                                %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s
                            )
                            ON CONFLICT (event_id) DO NOTHING
                            """, batch)
                        batch.clear()
                    
                    
                          
                    # except Exception as e:
                    #     # print(f"Skipping row due to error: {e}")
                    #     continue
        # Insert remaining rows
        if batch:
            execute_batch(
                cur,
                """
                INSERT INTO activities (
                    event_id, merchant_id, event_timestamp,
                    product, event_type, amount,
                    status, channel, region, merchant_tier
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (event_id) DO NOTHING
                """,
                batch
            )

        conn.commit()
        print("CSV loading completed.")
    except Exception as e:
        conn.rollback()
        print(f"Error loading CSV: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    create_tables()
    load_csv_to_db()