import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../config/.env")

# PostgreSQL connection settings
DB_USER = os.getenv("DB_USER", "taxi_user")
DB_PASS = os.getenv("DB_PASS", "taxi_pass")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "nyc_taxi")

# Local storage settings
CLEANED_DIR = "../data/cleaned"
os.makedirs(CLEANED_DIR, exist_ok=True)  # Ensure directory exists

# Connect to PostgreSQL
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Define SQL query to fetch data
TABLE_NAME = "yellow_taxi_trips"
QUERY = f"SELECT * FROM {TABLE_NAME};"

print("📥 Extracting data from PostgreSQL...")
df = pd.read_sql(QUERY, engine)

### **🔹 Data Cleaning Steps** ###

# **1️⃣ Rename columns to match BigQuery schema**
df.rename(columns={
    "vendorid": "vendor_id",
    "tpep_pickup_datetime": "pickup_datetime",
    "tpep_dropoff_datetime": "dropoff_datetime",
    "ratecodeid": "rate_code_id",
    "pulocationid": "pickup_location_id",
    "dolocationid": "dropoff_location_id",
}, inplace=True)

# **2️⃣ Drop unwanted columns**
df.drop(columns=["congestion_surcharge", "airport_fee"], inplace=True, errors="ignore")

# **3️⃣ Convert timestamps to timezone-aware UTC**
df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce", utc=True)
df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"], errors="coerce", utc=True)

# **4️⃣ Remove rows where pickup or dropoff is NaT (invalid)**
df.dropna(subset=["pickup_datetime", "dropoff_datetime"], inplace=True)

# **5️⃣ Clamp timestamps to BigQuery-compatible range** 
#    (year 0001 to 9999)
min_bq_datetime = pd.Timestamp(year=1, month=1, day=1, tz='UTC')
max_bq_datetime = pd.Timestamp(year=9999, month=12, day=31, tz='UTC')
df = df[
    (df["pickup_datetime"] >= min_bq_datetime) &
    (df["pickup_datetime"] <= max_bq_datetime) &
    (df["dropoff_datetime"] >= min_bq_datetime) &
    (df["dropoff_datetime"] <= max_bq_datetime)
]

# **6️⃣ Convert timezone-aware to naive & cast to microseconds**
#    This ensures that nanosecond timestamps won't exceed BigQuery limits.
df["pickup_datetime"] = df["pickup_datetime"].dt.tz_convert(None).astype("datetime64[us]")
df["dropoff_datetime"] = df["dropoff_datetime"].dt.tz_convert(None).astype("datetime64[us]")

# **7️⃣ Ensure correct data types**
df["passenger_count"] = df["passenger_count"].fillna(0).astype(int)
df["rate_code_id"] = df["rate_code_id"].fillna(0).astype(int)

# **8️⃣ Drop duplicates**
df.drop_duplicates(inplace=True)

# **9️⃣ Save cleaned data to Parquet**
cleaned_file_path = os.path.join(CLEANED_DIR, f"{TABLE_NAME}_cleaned.parquet")
df.to_parquet(cleaned_file_path, engine="pyarrow", index=False)

print(f"✅ Cleaned data saved to {cleaned_file_path}")