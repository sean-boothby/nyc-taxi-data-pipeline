# NYC Taxi Data Processing Pipeline

Welcome to the **NYC Taxi Data Processing Pipeline** project! This repository demonstrates the end-to-end creation of a modular and scalable data pipeline. The pipeline processes NYC Taxi trip data, cleanses and transforms it, and loads it into Google BigQuery for analysis. The project is structured for clarity and scalability, leveraging best practices for building production-grade data workflows.

---

## **Table of Contents**
1. [Overview](#overview)
2. [Pipeline Architecture](#pipeline-architecture)
3. [Key Features](#key-features)
4. [Pipeline Steps](#pipeline-steps)
    - [1. Data Extraction](#1-data-extraction)
    - [2. Data Staging and Cleanup](#2-data-staging-and-cleanup)
    - [3. Cloud Storage Upload](#3-cloud-storage-upload)
    - [4. BigQuery Loading](#4-bigquery-loading)
5. [Technologies Used](#technologies-used)
6. [Project Structure](#project-structure)
7. [Future Enhancements](#future-enhancements)

---

## **Overview**
The NYC Taxi Data Processing Pipeline is designed to process large-scale trip data provided by the NYC Taxi and Limousine Commission (TLC). This project demonstrates how to extract, clean, and transform raw data, and store it in a cloud-based data warehouse for querying and analytics.

This pipeline is a demonstration of building a reliable and modular data workflow, showcasing skills in data engineering, cloud computing, and pipeline orchestration.

---

## **Pipeline Architecture**
The pipeline consists of four main stages:

1. **Data Extraction**: Downloads raw NYC taxi trip data in Parquet format.
2. **Data Cleanup and Transformation**: Ensures data quality and prepares it for storage.
3. **Cloud Storage Upload**: Stores cleaned data in Google Cloud Storage (GCS).
4. **BigQuery Loading**: Loads data from GCS into a partitioned and clustered BigQuery table for efficient querying.

![Pipeline Architecture](https://via.placeholder.com/800x400)  
_Illustration of the pipeline's modular architecture._

---

## **Key Features**
- **End-to-End Data Processing**: Covers extraction, transformation, and loading (ETL) steps.
- **Modular Design**: Each stage of the pipeline is implemented as a standalone component.
- **Cloud Integration**: Utilizes Google Cloud Storage and BigQuery for scalability.
- **Data Quality Enforcement**: Ensures data consistency, correct data types, and schema compliance.
- **Partitioned and Clustered Storage**: Optimized for large-scale analytics in BigQuery.

---

## **Pipeline Steps**

### **1. Data Extraction**
- Script: `extract-pipeline/grab_taxi_data.py`
- This stage downloads raw NYC taxi trip data directly from the [NYC TLC dataset](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
- **Output**: The raw Parquet file is stored locally in `data/raw/`.

### **2. Data Staging and Cleanup**
- Script: `staging-pipeline/data_cleanup.py`
- Cleans and transforms the raw data:
  - Fixes invalid timestamps.
  - Handles missing and null values.
  - Ensures compliance with the BigQuery schema.
- **Output**: A cleaned Parquet file saved in `data/cleaned/`.

### **3. Cloud Storage Upload**
- Script: `gcs-pipeline/load_to_gcs.py`
- Uploads the cleaned Parquet file to a specified bucket in Google Cloud Storage (GCS).
- **Output**: Cleaned data stored in `gs://<bucket_name>/processed/yellow_taxi_trips.parquet`.

### **4. BigQuery Loading**
- Script: `bigquery-pipeline/load_to_bigquery.py`
- Loads data from GCS into Google BigQuery:
  - Uses partitioned and clustered tables for optimized queries.
  - Handles large-scale datasets efficiently.
- **Output**: Data is available in the `nyc_taxi_data.yellow_taxi_trips` table in BigQuery.

---

## **Technologies Used**

- **Languages**: Python
- **Data Storage**: PostgreSQL, Google Cloud Storage, Google BigQuery
- **Libraries**:
  - `pandas`: Data transformation
  - `sqlalchemy`: PostgreSQL connection
  - `google-cloud-storage`: Integration with GCS
  - `google-cloud-bigquery`: Integration with BigQuery
- **Tools**: Docker (optional for PostgreSQL setup)
- **File Formats**: Parquet

---

## **Project Structure**
```
nyc-taxi-data-pipeline/
│── data/
│   ├── cleaned/                     # Cleaned Parquet files
│   ├── raw/                         # Raw files (optional)
│── extract-pipeline/
│   ├── grab_taxi_data.py            # Extraction script
│── staging-pipeline/
│   ├── data_cleanup.py              # Data cleanup and transformation
│   ├── load_to_postgres.py          # Load raw data to PostgreSQL
│── gcs-pipeline/
│   ├── load_to_gcs.py               # Upload cleaned data to GCS
│── bigquery-pipeline/
│   ├── load_to_bigquery.py          # Load data from GCS to BigQuery
│── config/
│   ├── gcs_service_account.json     # GCS credentials (gitignored)
│   ├── .env                         # Environment variables (gitignored)
│── README.md                        # Documentation
```

---

## **Future Enhancements**
1. **Orchestration with Airflow**
   - Automate and schedule pipeline tasks.
   - Monitor and retry failed tasks.
2. **Incremental Loading**
   - Process only new or updated data.
   - Reduce processing time for recurring datasets.
3. **Data Validation**
   - Add automated checks for data consistency and completeness.
4. **Streaming Data Support**
   - Handle real-time data ingestion using tools like Kafka or Google Pub/Sub.

---

We hope this project demonstrates effective methods for building robust data pipelines. Contributions and suggestions are welcome!

