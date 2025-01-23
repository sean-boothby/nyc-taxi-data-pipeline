import os
from google.cloud import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../config/.env")

# Google Cloud Storage settings
GCS_BUCKET_NAME = "nyc-taxi-data-pipeline"  # Change to your actual bucket name
GCS_KEY_PATH = os.getenv("GCS_KEY_PATH", "../config/gcs_service_account.json")

# Local storage settings
CLEANED_DIR = "../data/cleaned"
TABLE_NAME = "yellow_taxi_trips"
cleaned_file_path = os.path.join(CLEANED_DIR, f"{TABLE_NAME}_cleaned.parquet")

# Ensure the cleaned file exists
if not os.path.exists(cleaned_file_path):
    raise FileNotFoundError(f"❌ Cleaned data file not found: {cleaned_file_path}")

print(f"📂 Using cleaned data: {cleaned_file_path}")

# Upload file to Google Cloud Storage
def upload_to_gcs(local_file, bucket_name, destination_blob_name):
    """Uploads a file to Google Cloud Storage."""
    storage_client = storage.Client.from_service_account_json(GCS_KEY_PATH)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(local_file)
    print(f"🚀 Uploaded {local_file} to gs://{bucket_name}/{destination_blob_name}")

# Run the upload
upload_to_gcs(cleaned_file_path, GCS_BUCKET_NAME, f"processed/{TABLE_NAME}.parquet")

print("✅ Data successfully uploaded to GCS!")
