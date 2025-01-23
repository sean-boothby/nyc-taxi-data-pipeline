import os
from google.cloud import bigquery
from dotenv import load_dotenv
from google.oauth2 import service_account

# Load environment variables
load_dotenv("../config/.env")

# Google Cloud settings
GCS_BUCKET_NAME = "nyc-taxi-data-pipeline"  # Change to your actual bucket
GCS_FILE_PATH = "processed/yellow_taxi_trips.parquet"  # File in GCS
PROJECT_ID = "terraform-448018"  # Change to your Google Cloud project
DATASET_ID = "nyc_taxi_data"
TABLE_ID = "yellow_taxi_trips"
BQ_TABLE = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
GCS_URI = f"gs://{GCS_BUCKET_NAME}/{GCS_FILE_PATH}"

# Initialize BigQuery client
GCS_KEY_PATH = os.getenv("GCS_KEY_PATH", "../config/gcs_service_account.json")

# Load credentials explicitly
credentials = service_account.Credentials.from_service_account_file(GCS_KEY_PATH)

# Initialize BigQuery client with credentials
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

# Define schema (optional, can be auto-detected)
schema = [
    bigquery.SchemaField("vendor_id", "INTEGER"),
    bigquery.SchemaField("pickup_datetime", "TIMESTAMP"),
    bigquery.SchemaField("dropoff_datetime", "TIMESTAMP"),
    bigquery.SchemaField("passenger_count", "INTEGER"),
    bigquery.SchemaField("trip_distance", "FLOAT"),
    bigquery.SchemaField("rate_code_id", "INTEGER"),
    bigquery.SchemaField("store_and_fwd_flag", "STRING"),
    bigquery.SchemaField("pickup_location_id", "INTEGER"),
    bigquery.SchemaField("dropoff_location_id", "INTEGER"),
    bigquery.SchemaField("payment_type", "INTEGER"),
    bigquery.SchemaField("fare_amount", "FLOAT"),
    bigquery.SchemaField("extra", "FLOAT"),
    bigquery.SchemaField("mta_tax", "FLOAT"),
    bigquery.SchemaField("tip_amount", "FLOAT"),
    bigquery.SchemaField("tolls_amount", "FLOAT"),
    bigquery.SchemaField("improvement_surcharge", "FLOAT"),
    bigquery.SchemaField("total_amount", "FLOAT"),
]

# Define table configuration (with partitioning & clustering)
table = bigquery.Table(BQ_TABLE, schema=schema)
table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="pickup_datetime",  # Partition by pickup date
)
table.clustering_fields = ["pickup_location_id", "dropoff_location_id"]

# Create dataset if not exists
dataset_ref = client.dataset(DATASET_ID)
try:
    client.get_dataset(dataset_ref)
    print(f"✅ Dataset {DATASET_ID} already exists.")
except:
    client.create_dataset(dataset_ref)
    print(f"🚀 Created dataset {DATASET_ID}.")

# Create table if not exists
try:
    client.get_table(BQ_TABLE)
    print(f"✅ Table {TABLE_ID} already exists.")
except:
    client.create_table(table)
    print(f"🚀 Created table {TABLE_ID}.")

# Load data from GCS to BigQuery
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
)
load_job = client.load_table_from_uri(GCS_URI, BQ_TABLE, job_config=job_config)
load_job.result()  # Wait for job to complete

print(f"✅ Successfully loaded data from {GCS_URI} into BigQuery {BQ_TABLE}!")
