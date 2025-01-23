import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from dotenv import load_dotenv
import logging

# Load environment variables (database credentials)
load_dotenv("../config/.env")

# PostgreSQL connection settings
DB_USER = os.getenv("DB_USER", "taxi_user")
DB_PASS = os.getenv("DB_PASS", "taxi_pass")
DB_HOST = os.getenv("DB_HOST", "postgres")  # Change to cloud IP if using remote DB
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "nyc_taxi")

# Directory where Parquet files are stored
DATA_DIR = "../data/raw"

# Get the latest Parquet file
parquet_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".parquet")], reverse=True)
if not parquet_files:
    print("❌ No Parquet files found in the data directory.")
    exit(1)

latest_file = os.path.join(DATA_DIR, parquet_files[0])
print(f"📂 Using file: {latest_file}")

# Create PostgreSQL connection
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Define table schema (adjust based on actual dataset)
TABLE_NAME = "yellow_taxi_trips"

CREATE_TABLE_QUERY = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    vendor_id INTEGER,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count INTEGER,
    trip_distance FLOAT,
    rate_code_id INTEGER,
    store_and_fwd_flag VARCHAR(1),
    pickup_location_id INTEGER,
    dropoff_location_id INTEGER,
    payment_type INTEGER,
    fare_amount FLOAT,
    extra FLOAT,
    mta_tax FLOAT,
    tip_amount FLOAT,
    tolls_amount FLOAT,
    improvement_surcharge FLOAT,
    total_amount FLOAT
);
"""

# Read the Parquet file
df = pd.read_parquet(latest_file)

# Rename columns to match PostgreSQL schema
df.columns = [col.lower() for col in df.columns]

# Connect to DB and create table if not exists
with engine.begin() as conn:
    conn.execute(text(CREATE_TABLE_QUERY))  # Adjusted for SQLAlchemy 2.0  # Ensure changes are saved
    print(f"✅ Table `{TABLE_NAME}` is ready.")

# Insert data into PostgreSQL
df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False, method=None, chunksize=5000)
print(f"✅ Loaded {len(df)} records into `{TABLE_NAME}`.")
