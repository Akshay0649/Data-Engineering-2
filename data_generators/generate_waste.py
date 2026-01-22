"""
Waste Data Generator

Generates synthetic manufacturing waste and scrap tracking data.
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


def generate_waste(num_records=3000):
    """Generate waste tracking data."""
    
    waste_types = [
        'Material Scrap', 'Packaging Waste', 'Defective Product',
        'Expired Materials', 'Production Overrun', 'Trim Waste',
        'Off-spec Product', 'Contaminated Materials', 'Obsolete Inventory'
    ]
    
    disposal_methods = [
        'Recycling', 'Landfill', 'Incineration', 'Composting',
        'Hazardous Waste Disposal', 'Donation', 'Resale', 'Reprocessing'
    ]
    
    waste_categories = ['Recyclable', 'Non-Recyclable', 'Hazardous', 'Organic']
    
    waste_records = []
    
    for i in range(num_records):
        waste_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        waste_type = random.choice(waste_types)
        disposal_method = random.choice(disposal_methods)
        category = random.choice(waste_categories)
        
        # Align disposal method with category
        if category == 'Recyclable':
            disposal_method = random.choice(['Recycling', 'Reprocessing', 'Resale'])
        elif category == 'Hazardous':
            disposal_method = 'Hazardous Waste Disposal'
        elif category == 'Organic':
            disposal_method = random.choice(['Composting', 'Incineration'])
        
        quantity = round(random.uniform(1, 500), 2)
        unit_cost = round(random.uniform(5, 200), 2)
        total_cost = round(quantity * unit_cost, 2)
        
        # Calculate disposal cost
        disposal_cost_per_unit = {
            'Recycling': 2,
            'Landfill': 5,
            'Incineration': 8,
            'Composting': 3,
            'Hazardous Waste Disposal': 50,
            'Donation': 0,
            'Resale': -5,  # Revenue
            'Reprocessing': 10
        }
        
        disposal_cost = round(quantity * disposal_cost_per_unit.get(disposal_method, 5), 2)
        
        waste_record = {
            'waste_id': f'WST{i+1:08d}',
            'waste_date': waste_date.strftime('%Y-%m-%d'),
            'waste_type': waste_type,
            'waste_category': category,
            'product_id': f'PRD{random.randint(1, 1000):06d}' if random.random() > 0.3 else None,
            'material_sku': f'MAT-{random.choice(["STE", "ALU", "PLA", "CTN"])}-{random.randint(1, 999):03d}',
            'batch_id': f'BATCH{random.randint(1000, 9999)}',
            'facility_location': random.choice(['Plant-A', 'Plant-B', 'Plant-C', 'Warehouse-1', 'Warehouse-2']),
            'department': random.choice(['Production', 'Packaging', 'Quality Control', 'Warehouse', 'Shipping']),
            'quantity': quantity,
            'unit_of_measure': random.choice(['kg', 'liters', 'units', 'meters']),
            'unit_cost': unit_cost,
            'total_material_cost': total_cost,
            'disposal_method': disposal_method,
            'disposal_cost': disposal_cost,
            'disposal_date': (waste_date + timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d'),
            'disposal_vendor': fake.company() if disposal_method != 'Donation' else 'Donation Center',
            'is_preventable': random.choices([True, False], weights=[0.6, 0.4])[0],
            'root_cause': random.choice([
                'Equipment Malfunction', 'Human Error', 'Quality Failure',
                'Process Inefficiency', 'Design Issue', 'Material Defect',
                'Forecasting Error', 'Supplier Issue'
            ]) if random.random() > 0.5 else '',
            'corrective_action': fake.sentence() if random.random() > 0.7 else '',
            'environmental_impact_score': round(random.uniform(1, 10), 1),
            'carbon_footprint_kg': round(quantity * random.uniform(0.5, 5), 2),
            'recorded_by': fake.name(),
            'created_date': waste_date.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        waste_records.append(waste_record)
    
    return pd.DataFrame(waste_records)


def main():
    """Main execution function."""
    print("Generating waste data...")
    
    # Generate data
    waste_df = generate_waste(3000)
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('sample_data', exist_ok=True)
    
    # Save to CSV
    output_file = 'sample_data/waste.csv'
    waste_df.to_csv(output_file, index=False)
    
    print(f"Generated {len(waste_df)} waste records")
    print(f"Saved to {output_file}")
    print(f"\nSample data:")
    print(waste_df.head())
    print(f"\nWaste types distribution:")
    print(waste_df['waste_type'].value_counts())
    print(f"\nDisposal methods distribution:")
    print(waste_df['disposal_method'].value_counts())


if __name__ == '__main__':
    main()
