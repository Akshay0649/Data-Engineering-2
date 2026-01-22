"""
Databricks Data Ingestion Script

Ingests CSV data from sample_data directory into Databricks tables.
"""

import os
import sys
import yaml
import pandas as pd
from databricks import sql
from datetime import datetime


class DatabricksIngestion:
    """Handle data ingestion to Databricks."""
    
    def __init__(self, config_path='config.yaml'):
        """Initialize with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.db_config = self.config['databricks']
        self.data_path = self.config['data_source']['path']
        self.options = self.config['options']
        
        self.connection = None
        
    def connect(self):
        """Establish connection to Databricks."""
        print("Connecting to Databricks...")
        self.connection = sql.connect(
            server_hostname=self.db_config['server_hostname'],
            http_path=self.db_config['http_path'],
            access_token=self.db_config['access_token']
        )
        print("Connected successfully!")
        
    def disconnect(self):
        """Close connection."""
        if self.connection:
            self.connection.close()
            print("Disconnected from Databricks")
    
    def ingest_table(self, table_name, csv_file):
        """Ingest a single CSV file into a Databricks table."""
        print(f"\nIngesting {table_name}...")
        
        # Read CSV file
        csv_path = os.path.join(self.data_path, csv_file)
        if not os.path.exists(csv_path):
            print(f"  Warning: File {csv_path} not found. Skipping.")
            return
        
        df = pd.read_csv(csv_path)
        print(f"  Loaded {len(df)} rows from {csv_file}")
        
        # Create cursor
        cursor = self.connection.cursor()
        
        # Optionally truncate table
        if self.options['truncate_before_load']:
            try:
                cursor.execute(f"TRUNCATE TABLE {self.db_config['catalog']}.{table_name}")
                print(f"  Truncated table {table_name}")
            except Exception as e:
                print(f"  Note: Could not truncate table: {e}")
        
        # Prepare INSERT statement
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['?' for _ in df.columns])
        insert_sql = f"""
            INSERT INTO {self.db_config['catalog']}.{table_name} 
            ({columns})
            VALUES ({placeholders})
        """
        
        # Insert data in batches
        batch_size = self.options['batch_size']
        total_rows = len(df)
        
        for i in range(0, total_rows, batch_size):
            batch = df.iloc[i:i+batch_size]
            rows = [tuple(x) for x in batch.values]
            
            try:
                cursor.executemany(insert_sql, rows)
                print(f"  Inserted {min(i+batch_size, total_rows)}/{total_rows} rows")
            except Exception as e:
                print(f"  Error inserting batch: {e}")
                raise
        
        cursor.close()
        print(f"  ✓ Successfully ingested {total_rows} rows into {table_name}")
    
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
        print("DATABRICKS DATA INGESTION")
        print("=" * 80)
        print(f"Start time: {datetime.now()}")
        print()
        
        self.connect()
        
        try:
            for table_name, csv_file in tables.items():
                self.ingest_table(table_name, csv_file)
        finally:
            self.disconnect()
        
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
    
    ingestion = DatabricksIngestion(config_path)
    ingestion.ingest_all()


if __name__ == '__main__':
    main()
