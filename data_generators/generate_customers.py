"""
Customer Data Generator

Generates synthetic customer demographic and account data.
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)


def generate_customers(num_customers=5000):
    """Generate customer data."""
    
    customer_segments = ['Premium', 'Standard', 'Basic', 'Enterprise']
    customer_types = ['Individual', 'Business']
    
    customers = []
    
    for i in range(num_customers):
        customer_type = random.choice(customer_types)
        segment = random.choice(customer_segments)
        
        # Generate account age
        account_age_days = random.randint(1, 1825)  # Up to 5 years
        created_date = datetime.now() - timedelta(days=account_age_days)
        
        customer = {
            'customer_id': f'CUS{i+1:07d}',
            'customer_type': customer_type,
            'customer_name': fake.company() if customer_type == 'Business' else fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address_line1': fake.street_address(),
            'address_line2': fake.secondary_address() if random.random() > 0.7 else '',
            'city': fake.city(),
            'state': fake.state_abbr(),
            'postal_code': fake.zipcode(),
            'country': 'USA',
            'customer_segment': segment,
            'lifetime_value': round(random.uniform(100, 50000), 2),
            'total_orders': random.randint(0, 150),
            'is_active': random.choices([True, False], weights=[0.85, 0.15])[0],
            'credit_limit': round(random.uniform(1000, 100000), 2) if customer_type == 'Business' else 0,
            'payment_terms_days': random.choice([0, 15, 30, 45, 60]) if customer_type == 'Business' else 0,
            'account_created_date': created_date.strftime('%Y-%m-%d'),
            'last_order_date': (datetime.now() - timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d') if random.random() > 0.2 else None,
            'updated_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        customers.append(customer)
    
    return pd.DataFrame(customers)


def main():
    """Main execution function."""
    print("Generating customers data...")
    
    # Generate data
    customers_df = generate_customers(5000)
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('sample_data', exist_ok=True)
    
    # Save to CSV
    output_file = 'sample_data/customers.csv'
    customers_df.to_csv(output_file, index=False)
    
    print(f"Generated {len(customers_df)} customers")
    print(f"Saved to {output_file}")
    print(f"\nSample data:")
    print(customers_df.head())
    print(f"\nCustomer segments distribution:")
    print(customers_df['customer_segment'].value_counts())
    print(f"\nCustomer types distribution:")
    print(customers_df['customer_type'].value_counts())


if __name__ == '__main__':
    main()
