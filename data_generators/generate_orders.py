"""
Orders Data Generator

Generates synthetic sales order data including order headers and line items.
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


def generate_orders(num_orders=10000):
    """Generate order data."""
    
    order_statuses = ['Pending', 'Confirmed', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery']
    
    orders = []
    order_lines = []
    
    for i in range(num_orders):
        order_id = f'ORD{i+1:08d}'
        customer_id = f'CUS{random.randint(1, 5000):07d}'
        
        # Generate order date within last 2 years
        order_date = datetime.now() - timedelta(days=random.randint(1, 730))
        
        status = random.choice(order_statuses)
        
        order = {
            'order_id': order_id,
            'customer_id': customer_id,
            'order_date': order_date.strftime('%Y-%m-%d'),
            'order_time': order_date.strftime('%H:%M:%S'),
            'order_status': status,
            'payment_method': random.choice(payment_methods),
            'shipping_address': fake.street_address(),
            'shipping_city': fake.city(),
            'shipping_state': fake.state_abbr(),
            'shipping_postal_code': fake.zipcode(),
            'billing_address': fake.street_address(),
            'billing_city': fake.city(),
            'billing_state': fake.state_abbr(),
            'billing_postal_code': fake.zipcode(),
            'subtotal': 0,  # Will calculate from order lines
            'tax_amount': 0,
            'shipping_cost': round(random.uniform(0, 50), 2),
            'discount_amount': round(random.uniform(0, 100), 2) if random.random() > 0.7 else 0,
            'total_amount': 0,  # Will calculate
            'notes': fake.sentence() if random.random() > 0.8 else '',
            'created_date': order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        orders.append(order)
        
        # Generate 1-8 order lines per order
        num_lines = random.randint(1, 8)
        subtotal = 0
        
        for j in range(num_lines):
            product_id = f'PRD{random.randint(1, 1000):06d}'
            quantity = random.randint(1, 20)
            unit_price = round(random.uniform(10, 500), 2)
            line_total = round(quantity * unit_price, 2)
            subtotal += line_total
            
            order_line = {
                'order_line_id': f'{order_id}-{j+1:03d}',
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'discount_percent': round(random.uniform(0, 20), 2) if random.random() > 0.8 else 0,
                'line_total': line_total,
                'line_status': status,
                'notes': ''
            }
            order_lines.append(order_line)
        
        # Update order totals
        order['subtotal'] = round(subtotal, 2)
        order['tax_amount'] = round(subtotal * 0.08, 2)  # 8% tax
        order['total_amount'] = round(subtotal + order['tax_amount'] + order['shipping_cost'] - order['discount_amount'], 2)
    
    return pd.DataFrame(orders), pd.DataFrame(order_lines)


def main():
    """Main execution function."""
    print("Generating orders data...")
    
    # Generate data
    orders_df, order_lines_df = generate_orders(10000)
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('sample_data', exist_ok=True)
    
    # Save to CSV
    orders_file = 'sample_data/orders.csv'
    order_lines_file = 'sample_data/order_lines.csv'
    
    orders_df.to_csv(orders_file, index=False)
    order_lines_df.to_csv(order_lines_file, index=False)
    
    print(f"Generated {len(orders_df)} orders")
    print(f"Generated {len(order_lines_df)} order lines")
    print(f"Saved to {orders_file} and {order_lines_file}")
    print(f"\nSample orders:")
    print(orders_df.head())
    print(f"\nOrder status distribution:")
    print(orders_df['order_status'].value_counts())


if __name__ == '__main__':
    main()
