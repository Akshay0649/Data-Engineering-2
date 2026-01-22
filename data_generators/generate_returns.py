"""
Returns Data Generator

Generates synthetic product return and refund data.
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


def generate_returns(num_returns=1500):
    """Generate returns data."""
    
    return_reasons = [
        'Defective Product', 'Wrong Item Received', 'Not as Described',
        'Changed Mind', 'Better Price Elsewhere', 'Damaged in Shipping',
        'Size/Fit Issue', 'Quality Issues', 'Late Delivery', 'No Longer Needed'
    ]
    
    return_statuses = ['Requested', 'Approved', 'In Transit', 'Received', 'Inspected', 'Refunded', 'Rejected']
    refund_methods = ['Original Payment Method', 'Store Credit', 'Exchange', 'Bank Transfer']
    
    returns = []
    
    for i in range(num_returns):
        order_id = f'ORD{random.randint(1, 10000):08d}'
        order_line_id = f'{order_id}-{random.randint(1, 8):03d}'
        product_id = f'PRD{random.randint(1, 1000):06d}'
        
        # Generate return request date (within 90 days of order)
        order_date = datetime.now() - timedelta(days=random.randint(90, 730))
        return_request_date = order_date + timedelta(days=random.randint(1, 90))
        
        status = random.choice(return_statuses)
        reason = random.choice(return_reasons)
        
        # Calculate processing times
        if status in ['Approved', 'In Transit', 'Received', 'Inspected', 'Refunded']:
            approved_date = return_request_date + timedelta(days=random.randint(1, 3))
        else:
            approved_date = None
        
        if status in ['Received', 'Inspected', 'Refunded']:
            received_date = approved_date + timedelta(days=random.randint(3, 10))
        else:
            received_date = None
        
        if status == 'Refunded':
            refund_date = received_date + timedelta(days=random.randint(1, 5))
        else:
            refund_date = None
        
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(10, 500), 2)
        refund_amount = round(quantity * unit_price, 2)
        
        # Apply restocking fee for some returns
        restocking_fee = 0
        if reason in ['Changed Mind', 'Better Price Elsewhere', 'No Longer Needed']:
            if random.random() > 0.5:
                restocking_fee = round(refund_amount * 0.15, 2)  # 15% restocking fee
        
        return_record = {
            'return_id': f'RET{i+1:08d}',
            'order_id': order_id,
            'order_line_id': order_line_id,
            'product_id': product_id,
            'customer_id': f'CUS{random.randint(1, 5000):07d}',
            'return_request_date': return_request_date.strftime('%Y-%m-%d'),
            'return_reason': reason,
            'return_status': status,
            'quantity_returned': quantity,
            'return_condition': random.choice(['New', 'Like New', 'Used', 'Damaged']),
            'approved_date': approved_date.strftime('%Y-%m-%d') if approved_date else None,
            'received_date': received_date.strftime('%Y-%m-%d') if received_date else None,
            'refund_date': refund_date.strftime('%Y-%m-%d') if refund_date else None,
            'refund_method': random.choice(refund_methods) if status == 'Refunded' else None,
            'refund_amount': refund_amount if status == 'Refunded' else 0,
            'restocking_fee': restocking_fee,
            'shipping_label_cost': round(random.uniform(5, 15), 2),
            'is_warranty_return': random.choices([True, False], weights=[0.2, 0.8])[0],
            'inspector_notes': fake.sentence() if status in ['Inspected', 'Refunded'] else '',
            'customer_comments': fake.sentence(),
            'created_date': return_request_date.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        returns.append(return_record)
    
    return pd.DataFrame(returns)


def main():
    """Main execution function."""
    print("Generating returns data...")
    
    # Generate data
    returns_df = generate_returns(1500)
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('sample_data', exist_ok=True)
    
    # Save to CSV
    output_file = 'sample_data/returns.csv'
    returns_df.to_csv(output_file, index=False)
    
    print(f"Generated {len(returns_df)} returns")
    print(f"Saved to {output_file}")
    print(f"\nSample data:")
    print(returns_df.head())
    print(f"\nReturn reasons distribution:")
    print(returns_df['return_reason'].value_counts())
    print(f"\nReturn status distribution:")
    print(returns_df['return_status'].value_counts())


if __name__ == '__main__':
    main()
