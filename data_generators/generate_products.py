"""
Product Data Generator

Generates synthetic product data including SKUs, categories, pricing, and attributes.
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


def generate_products(num_products=1000):
    """Generate product catalog data."""
    
    categories = [
        'Electronics', 'Furniture', 'Clothing', 'Food & Beverage',
        'Home & Garden', 'Sports & Outdoors', 'Toys & Games',
        'Health & Beauty', 'Automotive', 'Books & Media'
    ]
    
    subcategories = {
        'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Accessories'],
        'Furniture': ['Chairs', 'Tables', 'Sofas', 'Storage'],
        'Clothing': ['Shirts', 'Pants', 'Dresses', 'Shoes'],
        'Food & Beverage': ['Snacks', 'Beverages', 'Fresh Produce', 'Packaged Foods'],
        'Home & Garden': ['Kitchen', 'Bath', 'Garden Tools', 'Decor'],
        'Sports & Outdoors': ['Fitness', 'Camping', 'Team Sports', 'Water Sports'],
        'Toys & Games': ['Action Figures', 'Board Games', 'Puzzles', 'Educational'],
        'Health & Beauty': ['Skincare', 'Makeup', 'Hair Care', 'Wellness'],
        'Automotive': ['Parts', 'Accessories', 'Tools', 'Fluids'],
        'Books & Media': ['Fiction', 'Non-Fiction', 'Movies', 'Music']
    }
    
    products = []
    
    for i in range(num_products):
        category = random.choice(categories)
        subcategory = random.choice(subcategories[category])
        
        product = {
            'product_id': f'PRD{i+1:06d}',
            'sku': f'{category[:3].upper()}-{subcategory[:3].upper()}-{i+1:05d}',
            'product_name': fake.catch_phrase() + ' ' + subcategory,
            'category': category,
            'subcategory': subcategory,
            'brand': fake.company(),
            'unit_cost': round(random.uniform(5, 500), 2),
            'unit_price': 0,  # Will calculate with markup
            'weight_kg': round(random.uniform(0.1, 50), 2),
            'dimensions_cm': f'{random.randint(10, 100)}x{random.randint(10, 100)}x{random.randint(5, 50)}',
            'is_active': random.choices([True, False], weights=[0.95, 0.05])[0],
            'reorder_point': random.randint(10, 100),
            'lead_time_days': random.randint(7, 45),
            'created_date': (datetime.now() - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d'),
            'updated_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Calculate price with markup
        markup = random.uniform(1.3, 2.5)
        product['unit_price'] = round(product['unit_cost'] * markup, 2)
        
        products.append(product)
    
    return pd.DataFrame(products)


def main():
    """Main execution function."""
    print("Generating products data...")
    
    # Generate data
    products_df = generate_products(1000)
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('sample_data', exist_ok=True)
    
    # Save to CSV
    output_file = 'sample_data/products.csv'
    products_df.to_csv(output_file, index=False)
    
    print(f"Generated {len(products_df)} products")
    print(f"Saved to {output_file}")
    print(f"\nSample data:")
    print(products_df.head())
    print(f"\nData shape: {products_df.shape}")
    print(f"\nCategories: {products_df['category'].nunique()}")


if __name__ == '__main__':
    main()
