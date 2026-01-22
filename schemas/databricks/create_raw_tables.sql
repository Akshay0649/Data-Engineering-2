-- Databricks Schema Definitions
-- Raw Layer: Bronze Tables

-- Create database
CREATE DATABASE IF NOT EXISTS physical_product_raw;
USE physical_product_raw;

-- Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id STRING,
    sku STRING,
    product_name STRING,
    category STRING,
    subcategory STRING,
    brand STRING,
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    weight_kg DECIMAL(10,2),
    dimensions_cm STRING,
    is_active BOOLEAN,
    reorder_point INT,
    lead_time_days INT,
    created_date DATE,
    updated_date DATE
)
USING DELTA
LOCATION '/mnt/datalake/raw/products';

-- Recipes Table
CREATE TABLE IF NOT EXISTS recipes (
    recipe_id STRING,
    product_id STRING,
    recipe_name STRING,
    version STRING,
    yield_quantity INT,
    batch_size INT,
    production_time_minutes INT,
    is_active BOOLEAN,
    created_date DATE,
    updated_date DATE
)
USING DELTA
LOCATION '/mnt/datalake/raw/recipes';

-- Recipe Lines Table
CREATE TABLE IF NOT EXISTS recipe_lines (
    recipe_line_id STRING,
    recipe_id STRING,
    material_name STRING,
    material_sku STRING,
    quantity_required DECIMAL(10,2),
    unit_of_measure STRING,
    cost_per_unit DECIMAL(10,2),
    sequence_number INT,
    is_critical BOOLEAN
)
USING DELTA
LOCATION '/mnt/datalake/raw/recipe_lines';

-- Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id STRING,
    customer_type STRING,
    customer_name STRING,
    email STRING,
    phone STRING,
    address_line1 STRING,
    address_line2 STRING,
    city STRING,
    state STRING,
    postal_code STRING,
    country STRING,
    customer_segment STRING,
    lifetime_value DECIMAL(12,2),
    total_orders INT,
    is_active BOOLEAN,
    credit_limit DECIMAL(12,2),
    payment_terms_days INT,
    account_created_date DATE,
    last_order_date DATE,
    updated_date DATE
)
USING DELTA
LOCATION '/mnt/datalake/raw/customers';

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id STRING,
    customer_id STRING,
    order_date DATE,
    order_time TIME,
    order_status STRING,
    payment_method STRING,
    shipping_address STRING,
    shipping_city STRING,
    shipping_state STRING,
    shipping_postal_code STRING,
    billing_address STRING,
    billing_city STRING,
    billing_state STRING,
    billing_postal_code STRING,
    subtotal DECIMAL(12,2),
    tax_amount DECIMAL(12,2),
    shipping_cost DECIMAL(12,2),
    discount_amount DECIMAL(12,2),
    total_amount DECIMAL(12,2),
    notes STRING,
    created_date TIMESTAMP,
    updated_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/datalake/raw/orders';

-- Order Lines Table
CREATE TABLE IF NOT EXISTS order_lines (
    order_line_id STRING,
    order_id STRING,
    product_id STRING,
    quantity INT,
    unit_price DECIMAL(10,2),
    discount_percent DECIMAL(5,2),
    line_total DECIMAL(12,2),
    line_status STRING,
    notes STRING
)
USING DELTA
LOCATION '/mnt/datalake/raw/order_lines';

-- Shipments Table
CREATE TABLE IF NOT EXISTS shipments (
    shipment_id STRING,
    order_id STRING,
    tracking_number STRING,
    carrier STRING,
    service_level STRING,
    shipment_date DATE,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    shipment_status STRING,
    origin_warehouse STRING,
    destination_city STRING,
    destination_state STRING,
    destination_postal_code STRING,
    weight_kg DECIMAL(10,2),
    dimensions_cm STRING,
    shipping_cost DECIMAL(10,2),
    package_count INT,
    is_signature_required BOOLEAN,
    is_insured BOOLEAN,
    insurance_value DECIMAL(10,2),
    delivery_notes STRING,
    created_date TIMESTAMP,
    updated_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/datalake/raw/shipments';

-- Returns Table
CREATE TABLE IF NOT EXISTS returns (
    return_id STRING,
    order_id STRING,
    order_line_id STRING,
    product_id STRING,
    customer_id STRING,
    return_request_date DATE,
    return_reason STRING,
    return_status STRING,
    quantity_returned INT,
    return_condition STRING,
    approved_date DATE,
    received_date DATE,
    refund_date DATE,
    refund_method STRING,
    refund_amount DECIMAL(12,2),
    restocking_fee DECIMAL(12,2),
    shipping_label_cost DECIMAL(10,2),
    is_warranty_return BOOLEAN,
    inspector_notes STRING,
    customer_comments STRING,
    created_date TIMESTAMP,
    updated_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/datalake/raw/returns';

-- Waste Table
CREATE TABLE IF NOT EXISTS waste (
    waste_id STRING,
    waste_date DATE,
    waste_type STRING,
    waste_category STRING,
    product_id STRING,
    material_sku STRING,
    batch_id STRING,
    facility_location STRING,
    department STRING,
    quantity DECIMAL(10,2),
    unit_of_measure STRING,
    unit_cost DECIMAL(10,2),
    total_material_cost DECIMAL(12,2),
    disposal_method STRING,
    disposal_cost DECIMAL(12,2),
    disposal_date DATE,
    disposal_vendor STRING,
    is_preventable BOOLEAN,
    root_cause STRING,
    corrective_action STRING,
    environmental_impact_score DECIMAL(3,1),
    carbon_footprint_kg DECIMAL(10,2),
    recorded_by STRING,
    created_date TIMESTAMP,
    updated_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/datalake/raw/waste';

-- Quality Inspections Table
CREATE TABLE IF NOT EXISTS quality_inspections (
    inspection_id STRING,
    inspection_date DATE,
    inspection_time TIME,
    inspection_type STRING,
    inspection_status STRING,
    product_id STRING,
    batch_id STRING,
    order_id STRING,
    facility_location STRING,
    inspector_name STRING,
    inspector_id STRING,
    sample_size INT,
    defect_count INT,
    defect_type STRING,
    severity_level STRING,
    defect_description STRING,
    measurement_1 DECIMAL(10,2),
    measurement_2 DECIMAL(10,2),
    measurement_3 DECIMAL(10,2),
    specification_met BOOLEAN,
    tolerance_percentage DECIMAL(5,2),
    visual_inspection_score DECIMAL(3,1),
    functional_test_result STRING,
    compliance_standard STRING,
    corrective_action_required BOOLEAN,
    corrective_action_description STRING,
    follow_up_date DATE,
    root_cause_analysis STRING,
    cost_of_quality DECIMAL(10,2),
    disposition STRING,
    notes STRING,
    created_date TIMESTAMP,
    updated_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/datalake/raw/quality_inspections';
