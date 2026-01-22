-- BigQuery Schema Definitions
-- Raw Layer: Bronze Tables

-- Create dataset
-- Run this in BigQuery console or via bq CLI:
-- bq mk --dataset --location=US physical_product_raw

-- Products Table
CREATE OR REPLACE TABLE `physical_product_raw.products` (
    product_id STRING NOT NULL,
    sku STRING NOT NULL,
    product_name STRING NOT NULL,
    category STRING,
    subcategory STRING,
    brand STRING,
    unit_cost NUMERIC(10,2),
    unit_price NUMERIC(10,2),
    weight_kg NUMERIC(10,2),
    dimensions_cm STRING,
    is_active BOOL,
    reorder_point INT64,
    lead_time_days INT64,
    created_date DATE,
    updated_date DATE,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
OPTIONS(
    description="Product catalog with SKUs, pricing, and attributes"
);

-- Recipes Table
CREATE OR REPLACE TABLE `physical_product_raw.recipes` (
    recipe_id STRING NOT NULL,
    product_id STRING,
    recipe_name STRING,
    version STRING,
    yield_quantity INT64,
    batch_size INT64,
    production_time_minutes INT64,
    is_active BOOL,
    created_date DATE,
    updated_date DATE,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
OPTIONS(
    description="Manufacturing recipes and bill of materials"
);

-- Recipe Lines Table
CREATE OR REPLACE TABLE `physical_product_raw.recipe_lines` (
    recipe_line_id STRING NOT NULL,
    recipe_id STRING,
    material_name STRING,
    material_sku STRING,
    quantity_required NUMERIC(10,2),
    unit_of_measure STRING,
    cost_per_unit NUMERIC(10,2),
    sequence_number INT64,
    is_critical BOOL,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
OPTIONS(
    description="Recipe line items with material requirements"
);

-- Customers Table
CREATE OR REPLACE TABLE `physical_product_raw.customers` (
    customer_id STRING NOT NULL,
    customer_type STRING,
    customer_name STRING NOT NULL,
    email STRING,
    phone STRING,
    address_line1 STRING,
    address_line2 STRING,
    city STRING,
    state STRING,
    postal_code STRING,
    country STRING,
    customer_segment STRING,
    lifetime_value NUMERIC(12,2),
    total_orders INT64,
    is_active BOOL,
    credit_limit NUMERIC(12,2),
    payment_terms_days INT64,
    account_created_date DATE,
    last_order_date DATE,
    updated_date DATE,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
OPTIONS(
    description="Customer demographics and account information"
);

-- Orders Table
CREATE OR REPLACE TABLE `physical_product_raw.orders` (
    order_id STRING NOT NULL,
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
    subtotal NUMERIC(12,2),
    tax_amount NUMERIC(12,2),
    shipping_cost NUMERIC(12,2),
    discount_amount NUMERIC(12,2),
    total_amount NUMERIC(12,2),
    notes STRING,
    created_date TIMESTAMP,
    updated_date TIMESTAMP,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(order_date)
CLUSTER BY customer_id, order_status
OPTIONS(
    description="Sales order headers",
    partition_expiration_days=1825  -- 5 years
);

-- Order Lines Table
CREATE OR REPLACE TABLE `physical_product_raw.order_lines` (
    order_line_id STRING NOT NULL,
    order_id STRING,
    product_id STRING,
    quantity INT64,
    unit_price NUMERIC(10,2),
    discount_percent NUMERIC(5,2),
    line_total NUMERIC(12,2),
    line_status STRING,
    notes STRING,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
OPTIONS(
    description="Sales order line items"
);

-- Shipments Table
CREATE OR REPLACE TABLE `physical_product_raw.shipments` (
    shipment_id STRING NOT NULL,
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
    weight_kg NUMERIC(10,2),
    dimensions_cm STRING,
    shipping_cost NUMERIC(10,2),
    package_count INT64,
    is_signature_required BOOL,
    is_insured BOOL,
    insurance_value NUMERIC(10,2),
    delivery_notes STRING,
    created_date TIMESTAMP,
    updated_date TIMESTAMP,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(shipment_date)
CLUSTER BY carrier, shipment_status
OPTIONS(
    description="Shipment and delivery tracking",
    partition_expiration_days=1825  -- 5 years
);

-- Returns Table
CREATE OR REPLACE TABLE `physical_product_raw.returns` (
    return_id STRING NOT NULL,
    order_id STRING,
    order_line_id STRING,
    product_id STRING,
    customer_id STRING,
    return_request_date DATE,
    return_reason STRING,
    return_status STRING,
    quantity_returned INT64,
    return_condition STRING,
    approved_date DATE,
    received_date DATE,
    refund_date DATE,
    refund_method STRING,
    refund_amount NUMERIC(12,2),
    restocking_fee NUMERIC(12,2),
    shipping_label_cost NUMERIC(10,2),
    is_warranty_return BOOL,
    inspector_notes STRING,
    customer_comments STRING,
    created_date TIMESTAMP,
    updated_date TIMESTAMP,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(return_request_date)
CLUSTER BY return_status, return_reason
OPTIONS(
    description="Product returns and refunds",
    partition_expiration_days=1825  -- 5 years
);

-- Waste Table
CREATE OR REPLACE TABLE `physical_product_raw.waste` (
    waste_id STRING NOT NULL,
    waste_date DATE,
    waste_type STRING,
    waste_category STRING,
    product_id STRING,
    material_sku STRING,
    batch_id STRING,
    facility_location STRING,
    department STRING,
    quantity NUMERIC(10,2),
    unit_of_measure STRING,
    unit_cost NUMERIC(10,2),
    total_material_cost NUMERIC(12,2),
    disposal_method STRING,
    disposal_cost NUMERIC(12,2),
    disposal_date DATE,
    disposal_vendor STRING,
    is_preventable BOOL,
    root_cause STRING,
    corrective_action STRING,
    environmental_impact_score NUMERIC(3,1),
    carbon_footprint_kg NUMERIC(10,2),
    recorded_by STRING,
    created_date TIMESTAMP,
    updated_date TIMESTAMP,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(waste_date)
CLUSTER BY waste_category, facility_location
OPTIONS(
    description="Manufacturing waste and scrap tracking",
    partition_expiration_days=1825  -- 5 years
);

-- Quality Inspections Table
CREATE OR REPLACE TABLE `physical_product_raw.quality_inspections` (
    inspection_id STRING NOT NULL,
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
    sample_size INT64,
    defect_count INT64,
    defect_type STRING,
    severity_level STRING,
    defect_description STRING,
    measurement_1 NUMERIC(10,2),
    measurement_2 NUMERIC(10,2),
    measurement_3 NUMERIC(10,2),
    specification_met BOOL,
    tolerance_percentage NUMERIC(5,2),
    visual_inspection_score NUMERIC(3,1),
    functional_test_result STRING,
    compliance_standard STRING,
    corrective_action_required BOOL,
    corrective_action_description STRING,
    follow_up_date DATE,
    root_cause_analysis STRING,
    cost_of_quality NUMERIC(10,2),
    disposition STRING,
    notes STRING,
    created_date TIMESTAMP,
    updated_date TIMESTAMP,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(inspection_date)
CLUSTER BY inspection_status, facility_location
OPTIONS(
    description="Quality control and inspection records",
    partition_expiration_days=1825  -- 5 years
);
