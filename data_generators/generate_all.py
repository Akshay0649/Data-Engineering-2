"""
Generate All Data

Master script to generate all sample data for the analytics engineering project.
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_products import generate_products
from generate_recipes import generate_recipes
from generate_customers import generate_customers
from generate_orders import generate_orders
from generate_shipments import generate_shipments
from generate_returns import generate_returns
from generate_waste import generate_waste
from generate_quality import generate_quality


def main():
    """Generate all sample data."""
    print("=" * 80)
    print("GENERATING ALL SAMPLE DATA FOR ANALYTICS ENGINEERING PROJECT")
    print("=" * 80)
    print()
    
    # Create output directory
    os.makedirs('sample_data', exist_ok=True)
    
    # Generate all datasets
    print("1. Generating Products...")
    products_df = generate_products(1000)
    products_df.to_csv('sample_data/products.csv', index=False)
    print(f"   ✓ Generated {len(products_df)} products")
    print()
    
    print("2. Generating Recipes...")
    recipes_df, recipe_lines_df = generate_recipes(500)
    recipes_df.to_csv('sample_data/recipes.csv', index=False)
    recipe_lines_df.to_csv('sample_data/recipe_lines.csv', index=False)
    print(f"   ✓ Generated {len(recipes_df)} recipes with {len(recipe_lines_df)} recipe lines")
    print()
    
    print("3. Generating Customers...")
    customers_df = generate_customers(5000)
    customers_df.to_csv('sample_data/customers.csv', index=False)
    print(f"   ✓ Generated {len(customers_df)} customers")
    print()
    
    print("4. Generating Orders...")
    orders_df, order_lines_df = generate_orders(10000)
    orders_df.to_csv('sample_data/orders.csv', index=False)
    order_lines_df.to_csv('sample_data/order_lines.csv', index=False)
    print(f"   ✓ Generated {len(orders_df)} orders with {len(order_lines_df)} order lines")
    print()
    
    print("5. Generating Shipments...")
    shipments_df = generate_shipments(8000)
    shipments_df.to_csv('sample_data/shipments.csv', index=False)
    print(f"   ✓ Generated {len(shipments_df)} shipments")
    print()
    
    print("6. Generating Returns...")
    returns_df = generate_returns(1500)
    returns_df.to_csv('sample_data/returns.csv', index=False)
    print(f"   ✓ Generated {len(returns_df)} returns")
    print()
    
    print("7. Generating Waste Tracking...")
    waste_df = generate_waste(3000)
    waste_df.to_csv('sample_data/waste.csv', index=False)
    print(f"   ✓ Generated {len(waste_df)} waste records")
    print()
    
    print("8. Generating Quality Inspections...")
    quality_df = generate_quality(5000)
    quality_df.to_csv('sample_data/quality_inspections.csv', index=False)
    print(f"   ✓ Generated {len(quality_df)} quality inspection records")
    print()
    
    print("=" * 80)
    print("DATA GENERATION COMPLETE!")
    print("=" * 80)
    print()
    print("Summary:")
    print(f"  - Products: {len(products_df)}")
    print(f"  - Recipes: {len(recipes_df)} (with {len(recipe_lines_df)} lines)")
    print(f"  - Customers: {len(customers_df)}")
    print(f"  - Orders: {len(orders_df)} (with {len(order_lines_df)} lines)")
    print(f"  - Shipments: {len(shipments_df)}")
    print(f"  - Returns: {len(returns_df)}")
    print(f"  - Waste Records: {len(waste_df)}")
    print(f"  - Quality Inspections: {len(quality_df)}")
    print()
    print("All data saved to 'sample_data/' directory")
    print()


if __name__ == '__main__':
    main()
