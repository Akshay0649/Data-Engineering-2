{{
    config(
        materialized='table',
        schema='marts'
    )
}}

-- Fact: Quality Inspections
-- Grain: One row per inspection

with inspections as (
    select * from {{ ref('stg_quality_inspections') }}
),

products as (
    select * from {{ ref('dim_products') }}
),

final as (
    select
        -- Keys
        i.inspection_id,
        i.product_id,
        i.batch_id,
        i.order_id,
        i.inspection_date as date_key,
        
        -- Attributes
        i.inspection_type,
        i.inspection_status,
        i.facility_location,
        i.inspector_id,
        i.inspector_name,
        i.defect_type,
        i.severity_level,
        i.compliance_standard,
        i.disposition,
        
        -- Measurements
        i.sample_size,
        i.defect_count,
        i.defect_rate,
        i.measurement_1,
        i.measurement_2,
        i.measurement_3,
        i.tolerance_percentage,
        i.visual_inspection_score,
        
        -- Flags
        i.specification_met,
        i.corrective_action_required,
        i.is_passed,
        
        -- Costs
        i.cost_of_quality,
        
        -- Dates
        i.inspection_date,
        i.follow_up_date,
        i.inspection_month,
        
        -- Product attributes
        p.category as product_category,
        p.subcategory as product_subcategory,
        p.brand as product_brand,
        
        current_timestamp() as _dbt_loaded_at
    from inspections i
    left join products p on i.product_id = p.product_id
)

select * from final
