"""
Shipments Data Generator

Generates synthetic shipment and delivery tracking data.
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


def generate_shipments(num_shipments=8000):
    """Generate shipment data."""
    
    carriers = ['FedEx', 'UPS', 'DHL', 'USPS', 'Amazon Logistics']
    shipment_statuses = ['Pending', 'In Transit', 'Out for Delivery', 'Delivered', 'Failed Delivery', 'Returned']
    service_levels = ['Standard', 'Express', '2-Day', 'Overnight', 'Economy']
    
    shipments = []
    
    for i in range(num_shipments):
        order_id = f'ORD{random.randint(1, 10000):08d}'
        
        # Generate shipment date
        shipment_date = datetime.now() - timedelta(days=random.randint(1, 730))
        
        status = random.choice(shipment_statuses)
        carrier = random.choice(carriers)
        service_level = random.choice(service_levels)
        
        # Calculate delivery times based on service level
        transit_days = {
            'Standard': random.randint(5, 7),
            'Express': random.randint(3, 4),
            '2-Day': 2,
            'Overnight': 1,
            'Economy': random.randint(7, 14)
        }
        
        expected_delivery = shipment_date + timedelta(days=transit_days[service_level])
        
        # Actual delivery might be different
        if status == 'Delivered':
            actual_delivery = expected_delivery + timedelta(days=random.randint(-1, 3))
        else:
            actual_delivery = None
        
        shipment = {
            'shipment_id': f'SHP{i+1:08d}',
            'order_id': order_id,
            'tracking_number': f'{carrier[:3].upper()}{random.randint(100000000, 999999999)}',
            'carrier': carrier,
            'service_level': service_level,
            'shipment_date': shipment_date.strftime('%Y-%m-%d'),
            'expected_delivery_date': expected_delivery.strftime('%Y-%m-%d'),
            'actual_delivery_date': actual_delivery.strftime('%Y-%m-%d') if actual_delivery else None,
            'shipment_status': status,
            'origin_warehouse': f'WH-{random.choice(["NYC", "LAX", "CHI", "ATL", "DFW"])}',
            'destination_city': fake.city(),
            'destination_state': fake.state_abbr(),
            'destination_postal_code': fake.zipcode(),
            'weight_kg': round(random.uniform(0.5, 50), 2),
            'dimensions_cm': f'{random.randint(10, 100)}x{random.randint(10, 100)}x{random.randint(5, 50)}',
            'shipping_cost': round(random.uniform(5, 150), 2),
            'package_count': random.randint(1, 5),
            'is_signature_required': random.choices([True, False], weights=[0.2, 0.8])[0],
            'is_insured': random.choices([True, False], weights=[0.3, 0.7])[0],
            'insurance_value': round(random.uniform(100, 5000), 2) if random.random() > 0.7 else 0,
            'delivery_notes': fake.sentence() if random.random() > 0.8 else '',
            'created_date': shipment_date.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        shipments.append(shipment)
    
    return pd.DataFrame(shipments)


def main():
    """Main execution function."""
    print("Generating shipments data...")
    
    # Generate data
    shipments_df = generate_shipments(8000)
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('sample_data', exist_ok=True)
    
    # Save to CSV
    output_file = 'sample_data/shipments.csv'
    shipments_df.to_csv(output_file, index=False)
    
    print(f"Generated {len(shipments_df)} shipments")
    print(f"Saved to {output_file}")
    print(f"\nSample data:")
    print(shipments_df.head())
    print(f"\nShipment status distribution:")
    print(shipments_df['shipment_status'].value_counts())
    print(f"\nCarrier distribution:")
    print(shipments_df['carrier'].value_counts())


if __name__ == '__main__':
    main()
