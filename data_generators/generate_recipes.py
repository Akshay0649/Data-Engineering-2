"""
Recipe Data Generator

Generates synthetic recipe/bill-of-materials data for manufacturing products.
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


def generate_recipes(num_recipes=500):
    """Generate recipe/BOM data."""
    
    raw_materials = [
        'Steel Alloy', 'Aluminum', 'Copper Wire', 'Plastic Resin',
        'Cotton Fabric', 'Polyester Fabric', 'Leather', 'Rubber',
        'Glass', 'Wood', 'Cardboard', 'Foam', 'Silicon',
        'Paint', 'Adhesive', 'Fasteners', 'Electronic Components',
        'Packaging Materials', 'Labels', 'Ink'
    ]
    
    recipes = []
    recipe_lines = []
    
    for i in range(num_recipes):
        recipe_id = f'RCP{i+1:06d}'
        product_id = f'PRD{random.randint(1, 1000):06d}'
        
        recipe = {
            'recipe_id': recipe_id,
            'product_id': product_id,
            'recipe_name': f'Recipe for {fake.catch_phrase()}',
            'version': f'{random.randint(1, 5)}.{random.randint(0, 9)}',
            'yield_quantity': random.randint(1, 100),
            'batch_size': random.randint(10, 1000),
            'production_time_minutes': random.randint(30, 480),
            'is_active': random.choices([True, False], weights=[0.9, 0.1])[0],
            'created_date': (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
            'updated_date': datetime.now().strftime('%Y-%m-%d')
        }
        recipes.append(recipe)
        
        # Generate 3-10 ingredients per recipe
        num_ingredients = random.randint(3, 10)
        selected_materials = random.sample(raw_materials, min(num_ingredients, len(raw_materials)))
        
        for j, material in enumerate(selected_materials):
            recipe_line = {
                'recipe_line_id': f'{recipe_id}-{j+1:03d}',
                'recipe_id': recipe_id,
                'material_name': material,
                'material_sku': f'MAT-{material[:3].upper()}-{random.randint(1, 999):03d}',
                'quantity_required': round(random.uniform(0.1, 100), 2),
                'unit_of_measure': random.choice(['kg', 'liters', 'meters', 'units', 'grams']),
                'cost_per_unit': round(random.uniform(0.5, 50), 2),
                'sequence_number': j + 1,
                'is_critical': random.choices([True, False], weights=[0.3, 0.7])[0]
            }
            recipe_lines.append(recipe_line)
    
    return pd.DataFrame(recipes), pd.DataFrame(recipe_lines)


def main():
    """Main execution function."""
    print("Generating recipes data...")
    
    # Generate data
    recipes_df, recipe_lines_df = generate_recipes(500)
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('sample_data', exist_ok=True)
    
    # Save to CSV
    recipes_file = 'sample_data/recipes.csv'
    recipe_lines_file = 'sample_data/recipe_lines.csv'
    
    recipes_df.to_csv(recipes_file, index=False)
    recipe_lines_df.to_csv(recipe_lines_file, index=False)
    
    print(f"Generated {len(recipes_df)} recipes")
    print(f"Generated {len(recipe_lines_df)} recipe lines")
    print(f"Saved to {recipes_file} and {recipe_lines_file}")
    print(f"\nSample recipes:")
    print(recipes_df.head())
    print(f"\nSample recipe lines:")
    print(recipe_lines_df.head())


if __name__ == '__main__':
    main()
