{{
    config(
        materialized='table',
        schema='marts'
    )
}}

-- Fact: Waste
-- Grain: One row per waste record

with waste as (
    select * from {{ ref('stg_waste') }}
),

products as (
    select * from {{ ref('dim_products') }}
),

final as (
    select
        -- Keys
        w.waste_id,
        w.product_id,
        w.batch_id,
        w.waste_date as date_key,
        
        -- Attributes
        w.waste_type,
        w.waste_category,
        w.material_sku,
        w.facility_location,
        w.department,
        w.disposal_method,
        w.disposal_vendor,
        w.recorded_by,
        w.root_cause,
        
        -- Measurements
        w.quantity,
        w.unit_of_measure,
        
        -- Costs
        w.unit_cost,
        w.total_material_cost,
        w.disposal_cost,
        w.total_waste_cost,
        
        -- Environmental
        w.environmental_impact_score,
        w.carbon_footprint_kg,
        
        -- Flags
        w.is_preventable,
        
        -- Dates
        w.waste_date,
        w.disposal_date,
        w.waste_month,
        
        -- Product attributes
        p.category as product_category,
        p.subcategory as product_subcategory,
        p.brand as product_brand,
        
        current_timestamp() as _dbt_loaded_at
    from waste w
    left join products p on w.product_id = p.product_id
)

select * from final
