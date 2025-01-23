import os
import requests
from datetime import datetime

print(os.getcwd())

# Base URL for NYC Taxi Data
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{}-{}.parquet"

# Define the output directory
OUTPUT_DIR = "../data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure directory exists

# Specify the year and month for the data you want to fetch
year = datetime.now().year  # Defaults to current year
month = datetime.now().month - 2  # Defaults to previous month
if month == 0 or month == -1:
    year = year - 1
    if month == 0:
        month = 12
    elif month == -1:
        month = 11

# Format month as two digits
month_str = f"{month:02d}"

# Define file name and URL
file_name = f"yellow_tripdata_{year}-{month_str}.parquet"
file_url = BASE_URL.format(year, month_str)

# Path to save the file locally
output_path = os.path.join(OUTPUT_DIR, file_name)

def download_file(url, output_path):
    """Downloads a file from a URL and saves it locally."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise error for failed request
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded {file_name} successfully.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {file_name}: {e}")

# Run the download
download_file(file_url, output_path)