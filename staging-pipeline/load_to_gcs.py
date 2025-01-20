import os
import pandas as pd
from google.cloud import storage
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection settings
DB_USER = os.getenv("DB_USER", "taxi_user")
DB_PASS = os.getenv("DB_PASS", "taxi_pass")
DB_HOST = os.getenv("DB_HOST", "localhost")  # Change if using a remote DB
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "nyc_taxi")

# Google Cloud Storage settings
GCS_BUCKET_NAME = "nyc-taxi-data-pipeline"  # Change to your actual bucket name
GCS_KEY_PATH = os.getenv("GCS_KEY_PATH", "config/gcs_service_account.json")

# Local storage settings
OUTPUT_DIR = "data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure directory exists

# Connect to PostgreSQL
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Define SQL query to fetch data
TABLE_NAME = "yellow_taxi_trips"
QUERY = f"SELECT * FROM {TABLE_NAME};"

# Read data from PostgreSQL
print("📥 Extracting data from PostgreSQL...")
df = pd.read_sql(QUERY, engine)

# Save data as a Parquet file
parquet_filename = f"{TABLE_NAME}.parquet"
parquet_path = os.path.join(OUTPUT_DIR, parquet_filename)
df.to_parquet(parquet_path, engine="pyarrow", index=False)

print(f"✅ Data saved locally as {parquet_path}")

# Upload file to Google Cloud Storage
def upload_to_gcs(local_file, bucket_name, destination_blob_name):
    """Uploads a file to Google Cloud Storage."""
    storage_client = storage.Client.from_service_account_json(GCS_KEY_PATH)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(local_file)
    print(f"🚀 Uploaded {local_file} to gs://{bucket_name}/{destination_blob_name}")

# Run the upload
upload_to_gcs(parquet_path, GCS_BUCKET_NAME, f"processed/{parquet_filename}")

print("✅ Data successfully uploaded to GCS!")
