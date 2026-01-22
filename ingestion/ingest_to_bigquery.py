"""
BigQuery Data Ingestion Script

Ingests CSV data from sample_data directory into BigQuery tables.
"""

import os
import sys
import yaml
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime


class BigQueryIngestion:
    """Handle data ingestion to BigQuery."""
    
    def __init__(self, config_path='config.yaml'):
        """Initialize with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.bq_config = self.config['bigquery']
        self.data_path = self.config['data_source']['path']
        self.options = self.config['options']
        
        self.client = None
        
    def connect(self):
        """Establish connection to BigQuery."""
        print("Connecting to BigQuery...")
        
        # Load credentials
        credentials = service_account.Credentials.from_service_account_file(
            self.bq_config['credentials_path']
        )
        
        self.client = bigquery.Client(
            credentials=credentials,
            project=self.bq_config['project_id']
        )
        print("Connected successfully!")
        
    def ingest_table(self, table_name, csv_file):
        """Ingest a single CSV file into a BigQuery table."""
        print(f"\nIngesting {table_name}...")
        
        # Read CSV file
        csv_path = os.path.join(self.data_path, csv_file)
        if not os.path.exists(csv_path):
            print(f"  Warning: File {csv_path} not found. Skipping.")
            return
        
        df = pd.read_csv(csv_path)
        print(f"  Loaded {len(df)} rows from {csv_file}")
        
        # Prepare table reference
        table_id = f"{self.bq_config['project_id']}.{self.bq_config['dataset_id']}.{table_name}"
        
        # Configure load job
        job_config = bigquery.LoadJobConfig()
        
        if self.options['truncate_before_load']:
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
            print(f"  Will truncate table {table_name}")
        else:
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        
        if self.options['create_tables_if_not_exist']:
            job_config.autodetect = True
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
        
        # Load data from DataFrame
        try:
            job = self.client.load_table_from_dataframe(
                df,
                table_id,
                job_config=job_config
            )
            
            # Wait for the job to complete
            job.result()
            
            # Get the destination table
            table = self.client.get_table(table_id)
            print(f"  ✓ Successfully ingested {table.num_rows} rows into {table_name}")
            
        except Exception as e:
            print(f"  Error ingesting data: {e}")
            raise
    
    def ingest_all(self):
        """Ingest all tables."""
        tables = {
            'products': 'products.csv',
            'recipes': 'recipes.csv',
            'recipe_lines': 'recipe_lines.csv',
            'customers': 'customers.csv',
            'orders': 'orders.csv',
            'order_lines': 'order_lines.csv',
            'shipments': 'shipments.csv',
            'returns': 'returns.csv',
            'waste': 'waste.csv',
            'quality_inspections': 'quality_inspections.csv'
        }
        
        print("=" * 80)
        print("BIGQUERY DATA INGESTION")
        print("=" * 80)
        print(f"Start time: {datetime.now()}")
        print()
        
        self.connect()
        
        try:
            for table_name, csv_file in tables.items():
                self.ingest_table(table_name, csv_file)
        except Exception as e:
            print(f"\nError during ingestion: {e}")
            raise
        
        print()
        print("=" * 80)
        print("INGESTION COMPLETE!")
        print("=" * 80)
        print(f"End time: {datetime.now()}")


def main():
    """Main execution function."""
    config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.yaml'
    
    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' not found.")
        print("Please copy config_template.yaml to config.yaml and configure it.")
        sys.exit(1)
    
    ingestion = BigQueryIngestion(config_path)
    ingestion.ingest_all()


if __name__ == '__main__':
    main()
