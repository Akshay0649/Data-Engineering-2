"""
Snowflake Data Ingestion Script

Ingests CSV data from sample_data directory into Snowflake tables.
"""

import os
import sys
import yaml
import pandas as pd
import snowflake.connector
from datetime import datetime


class SnowflakeIngestion:
    """Handle data ingestion to Snowflake."""
    
    def __init__(self, config_path='config.yaml'):
        """Initialize with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.db_config = self.config['snowflake']
        self.data_path = self.config['data_source']['path']
        self.options = self.config['options']
        
        self.connection = None
        
    def connect(self):
        """Establish connection to Snowflake."""
        print("Connecting to Snowflake...")
        self.connection = snowflake.connector.connect(
            user=self.db_config['user'],
            password=self.db_config['password'],
            account=self.db_config['account'],
            warehouse=self.db_config['warehouse'],
            database=self.db_config['database'],
            schema=self.db_config['schema'],
            role=self.db_config.get('role', 'SYSADMIN')
        )
        print("Connected successfully!")
        
    def disconnect(self):
        """Close connection."""
        if self.connection:
            self.connection.close()
            print("Disconnected from Snowflake")
    
    def ingest_table(self, table_name, csv_file):
        """Ingest a single CSV file into a Snowflake table."""
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
                cursor.execute(f"TRUNCATE TABLE {table_name}")
                print(f"  Truncated table {table_name}")
            except Exception as e:
                print(f"  Note: Could not truncate table: {e}")
        
        # Use Snowflake's write_pandas for efficient loading
        # This uses Snowflake's internal staging
        from snowflake.connector.pandas_tools import write_pandas
        
        try:
            success, nchunks, nrows, _ = write_pandas(
                conn=self.connection,
                df=df,
                table_name=table_name.upper(),
                database=self.db_config['database'],
                schema=self.db_config['schema'],
                auto_create_table=self.options['create_tables_if_not_exist'],
                overwrite=self.options['truncate_before_load']
            )
            
            if success:
                print(f"  ✓ Successfully ingested {nrows} rows into {table_name}")
            else:
                print(f"  ✗ Failed to ingest {table_name}")
                
        except Exception as e:
            print(f"  Error ingesting data: {e}")
            raise
        finally:
            cursor.close()
    
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
        print("SNOWFLAKE DATA INGESTION")
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
    
    ingestion = SnowflakeIngestion(config_path)
    ingestion.ingest_all()


if __name__ == '__main__':
    main()
