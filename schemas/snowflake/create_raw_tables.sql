-- Snowflake Schema Definitions
-- Raw Layer: Bronze Tables

-- Create database and schema
CREATE DATABASE IF NOT EXISTS PHYSICAL_PRODUCT_DB;
USE DATABASE PHYSICAL_PRODUCT_DB;

CREATE SCHEMA IF NOT EXISTS RAW;
USE SCHEMA RAW;

-- Products Table
CREATE OR REPLACE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    sku VARCHAR(100) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    weight_kg DECIMAL(10,2),
    dimensions_cm VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    reorder_point INTEGER,
    lead_time_days INTEGER,
    created_date DATE,
    updated_date DATE,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Recipes Table
CREATE OR REPLACE TABLE recipes (
    recipe_id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(50),
    recipe_name VARCHAR(255),
    version VARCHAR(20),
    yield_quantity INTEGER,
    batch_size INTEGER,
    production_time_minutes INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_date DATE,
    updated_date DATE,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Recipe Lines Table
CREATE OR REPLACE TABLE recipe_lines (
    recipe_line_id VARCHAR(50) PRIMARY KEY,
    recipe_id VARCHAR(50),
    material_name VARCHAR(255),
    material_sku VARCHAR(100),
    quantity_required DECIMAL(10,2),
    unit_of_measure VARCHAR(20),
    cost_per_unit DECIMAL(10,2),
    sequence_number INTEGER,
    is_critical BOOLEAN,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Customers Table
CREATE OR REPLACE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_type VARCHAR(50),
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    customer_segment VARCHAR(50),
    lifetime_value DECIMAL(12,2),
    total_orders INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    credit_limit DECIMAL(12,2),
    payment_terms_days INTEGER,
    account_created_date DATE,
    last_order_date DATE,
    updated_date DATE,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Orders Table
CREATE OR REPLACE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_date DATE,
    order_time TIME,
    order_status VARCHAR(50),
    payment_method VARCHAR(50),
    shipping_address VARCHAR(255),
    shipping_city VARCHAR(100),
    shipping_state VARCHAR(50),
    shipping_postal_code VARCHAR(20),
    billing_address VARCHAR(255),
    billing_city VARCHAR(100),
    billing_state VARCHAR(50),
    billing_postal_code VARCHAR(20),
    subtotal DECIMAL(12,2),
    tax_amount DECIMAL(12,2),
    shipping_cost DECIMAL(12,2),
    discount_amount DECIMAL(12,2),
    total_amount DECIMAL(12,2),
    notes TEXT,
    created_date TIMESTAMP_NTZ,
    updated_date TIMESTAMP_NTZ,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Order Lines Table
CREATE OR REPLACE TABLE order_lines (
    order_line_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    discount_percent DECIMAL(5,2),
    line_total DECIMAL(12,2),
    line_status VARCHAR(50),
    notes TEXT,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Shipments Table
CREATE OR REPLACE TABLE shipments (
    shipment_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    tracking_number VARCHAR(100) UNIQUE,
    carrier VARCHAR(50),
    service_level VARCHAR(50),
    shipment_date DATE,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    shipment_status VARCHAR(50),
    origin_warehouse VARCHAR(50),
    destination_city VARCHAR(100),
    destination_state VARCHAR(50),
    destination_postal_code VARCHAR(20),
    weight_kg DECIMAL(10,2),
    dimensions_cm VARCHAR(50),
    shipping_cost DECIMAL(10,2),
    package_count INTEGER,
    is_signature_required BOOLEAN,
    is_insured BOOLEAN,
    insurance_value DECIMAL(10,2),
    delivery_notes TEXT,
    created_date TIMESTAMP_NTZ,
    updated_date TIMESTAMP_NTZ,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Returns Table
CREATE OR REPLACE TABLE returns (
    return_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    order_line_id VARCHAR(50),
    product_id VARCHAR(50),
    customer_id VARCHAR(50),
    return_request_date DATE,
    return_reason VARCHAR(255),
    return_status VARCHAR(50),
    quantity_returned INTEGER,
    return_condition VARCHAR(50),
    approved_date DATE,
    received_date DATE,
    refund_date DATE,
    refund_method VARCHAR(50),
    refund_amount DECIMAL(12,2),
    restocking_fee DECIMAL(12,2),
    shipping_label_cost DECIMAL(10,2),
    is_warranty_return BOOLEAN,
    inspector_notes TEXT,
    customer_comments TEXT,
    created_date TIMESTAMP_NTZ,
    updated_date TIMESTAMP_NTZ,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Waste Table
CREATE OR REPLACE TABLE waste (
    waste_id VARCHAR(50) PRIMARY KEY,
    waste_date DATE,
    waste_type VARCHAR(100),
    waste_category VARCHAR(50),
    product_id VARCHAR(50),
    material_sku VARCHAR(100),
    batch_id VARCHAR(50),
    facility_location VARCHAR(50),
    department VARCHAR(50),
    quantity DECIMAL(10,2),
    unit_of_measure VARCHAR(20),
    unit_cost DECIMAL(10,2),
    total_material_cost DECIMAL(12,2),
    disposal_method VARCHAR(100),
    disposal_cost DECIMAL(12,2),
    disposal_date DATE,
    disposal_vendor VARCHAR(255),
    is_preventable BOOLEAN,
    root_cause VARCHAR(255),
    corrective_action TEXT,
    environmental_impact_score DECIMAL(3,1),
    carbon_footprint_kg DECIMAL(10,2),
    recorded_by VARCHAR(100),
    created_date TIMESTAMP_NTZ,
    updated_date TIMESTAMP_NTZ,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Quality Inspections Table
CREATE OR REPLACE TABLE quality_inspections (
    inspection_id VARCHAR(50) PRIMARY KEY,
    inspection_date DATE,
    inspection_time TIME,
    inspection_type VARCHAR(100),
    inspection_status VARCHAR(50),
    product_id VARCHAR(50),
    batch_id VARCHAR(50),
    order_id VARCHAR(50),
    facility_location VARCHAR(50),
    inspector_name VARCHAR(100),
    inspector_id VARCHAR(50),
    sample_size INTEGER,
    defect_count INTEGER,
    defect_type VARCHAR(100),
    severity_level VARCHAR(50),
    defect_description TEXT,
    measurement_1 DECIMAL(10,2),
    measurement_2 DECIMAL(10,2),
    measurement_3 DECIMAL(10,2),
    specification_met BOOLEAN,
    tolerance_percentage DECIMAL(5,2),
    visual_inspection_score DECIMAL(3,1),
    functional_test_result VARCHAR(50),
    compliance_standard VARCHAR(50),
    corrective_action_required BOOLEAN,
    corrective_action_description TEXT,
    follow_up_date DATE,
    root_cause_analysis TEXT,
    cost_of_quality DECIMAL(10,2),
    disposition VARCHAR(50),
    notes TEXT,
    created_date TIMESTAMP_NTZ,
    updated_date TIMESTAMP_NTZ,
    _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Create foreign key relationships (optional, for data integrity)
-- Note: These are informational in Snowflake and don't enforce referential integrity
ALTER TABLE recipes ADD CONSTRAINT fk_recipes_product 
    FOREIGN KEY (product_id) REFERENCES products(product_id) NOT ENFORCED;

ALTER TABLE recipe_lines ADD CONSTRAINT fk_recipe_lines_recipe 
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) NOT ENFORCED;

ALTER TABLE orders ADD CONSTRAINT fk_orders_customer 
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) NOT ENFORCED;

ALTER TABLE order_lines ADD CONSTRAINT fk_order_lines_order 
    FOREIGN KEY (order_id) REFERENCES orders(order_id) NOT ENFORCED;

ALTER TABLE order_lines ADD CONSTRAINT fk_order_lines_product 
    FOREIGN KEY (product_id) REFERENCES products(product_id) NOT ENFORCED;

ALTER TABLE shipments ADD CONSTRAINT fk_shipments_order 
    FOREIGN KEY (order_id) REFERENCES orders(order_id) NOT ENFORCED;

ALTER TABLE returns ADD CONSTRAINT fk_returns_order 
    FOREIGN KEY (order_id) REFERENCES orders(order_id) NOT ENFORCED;
