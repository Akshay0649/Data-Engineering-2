"""
Quality Data Generator

Generates synthetic quality control and inspection data.
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


def generate_quality(num_inspections=5000):
    """Generate quality inspection data."""
    
    inspection_types = [
        'Incoming Material', 'In-Process', 'Final Product',
        'First Article', 'Random Sample', 'Customer Return',
        'Audit', 'Regulatory Compliance'
    ]
    
    inspection_statuses = ['Pass', 'Fail', 'Conditional Pass', 'Re-inspection Required']
    
    defect_types = [
        'Dimensional', 'Visual/Cosmetic', 'Functional', 'Material',
        'Assembly', 'Packaging', 'Documentation', 'Performance',
        'Safety', 'Contamination'
    ]
    
    severity_levels = ['Critical', 'Major', 'Minor', 'Observation']
    
    quality_records = []
    
    for i in range(num_inspections):
        inspection_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        inspection_type = random.choice(inspection_types)
        status = random.choices(
            inspection_statuses,
            weights=[0.80, 0.10, 0.05, 0.05]
        )[0]
        
        # Generate defects for failed inspections
        has_defects = status in ['Fail', 'Conditional Pass', 'Re-inspection Required']
        num_defects = random.randint(1, 5) if has_defects else 0
        
        quality_record = {
            'inspection_id': f'QC{i+1:08d}',
            'inspection_date': inspection_date.strftime('%Y-%m-%d'),
            'inspection_time': inspection_date.strftime('%H:%M:%S'),
            'inspection_type': inspection_type,
            'inspection_status': status,
            'product_id': f'PRD{random.randint(1, 1000):06d}',
            'batch_id': f'BATCH{random.randint(1000, 9999)}',
            'order_id': f'ORD{random.randint(1, 10000):08d}' if inspection_type in ['Final Product', 'Customer Return'] else None,
            'facility_location': random.choice(['Plant-A', 'Plant-B', 'Plant-C']),
            'inspector_name': fake.name(),
            'inspector_id': f'EMP{random.randint(1, 100):04d}',
            'sample_size': random.randint(1, 100),
            'defect_count': num_defects,
            'defect_type': random.choice(defect_types) if has_defects else None,
            'severity_level': random.choice(severity_levels) if has_defects else None,
            'defect_description': fake.sentence() if has_defects else '',
            'measurement_1': round(random.uniform(90, 110), 2),  # Some measured value
            'measurement_2': round(random.uniform(45, 55), 2),
            'measurement_3': round(random.uniform(18, 22), 2),
            'specification_met': status == 'Pass',
            'tolerance_percentage': round(random.uniform(-5, 5), 2),
            'visual_inspection_score': round(random.uniform(1, 10), 1),
            'functional_test_result': random.choice(['Pass', 'Fail', 'N/A']),
            'compliance_standard': random.choice(['ISO-9001', 'ISO-14001', 'FDA', 'CE', 'UL', 'N/A']),
            'corrective_action_required': has_defects and random.random() > 0.3,
            'corrective_action_description': fake.sentence() if has_defects and random.random() > 0.5 else '',
            'follow_up_date': (inspection_date + timedelta(days=random.randint(7, 30))).strftime('%Y-%m-%d') if has_defects else None,
            'root_cause_analysis': fake.sentence() if status == 'Fail' else '',
            'cost_of_quality': round(random.uniform(0, 1000), 2) if has_defects else 0,
            'disposition': random.choice(['Accept', 'Reject', 'Rework', 'Use As Is', 'Scrap']) if has_defects else 'Accept',
            'notes': fake.sentence() if random.random() > 0.7 else '',
            'created_date': inspection_date.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        quality_records.append(quality_record)
    
    return pd.DataFrame(quality_records)


def main():
    """Main execution function."""
    print("Generating quality inspection data...")
    
    # Generate data
    quality_df = generate_quality(5000)
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('sample_data', exist_ok=True)
    
    # Save to CSV
    output_file = 'sample_data/quality_inspections.csv'
    quality_df.to_csv(output_file, index=False)
    
    print(f"Generated {len(quality_df)} quality inspection records")
    print(f"Saved to {output_file}")
    print(f"\nSample data:")
    print(quality_df.head())
    print(f"\nInspection status distribution:")
    print(quality_df['inspection_status'].value_counts())
    print(f"\nInspection type distribution:")
    print(quality_df['inspection_type'].value_counts())


if __name__ == '__main__':
    main()
