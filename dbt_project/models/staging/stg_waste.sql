{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('raw', 'waste') }}
),

renamed as (
    select
        waste_id,
        waste_date,
        waste_type,
        waste_category,
        product_id,
        material_sku,
        batch_id,
        facility_location,
        department,
        quantity,
        unit_of_measure,
        unit_cost,
        total_material_cost,
        disposal_method,
        disposal_cost,
        disposal_date,
        disposal_vendor,
        is_preventable,
        root_cause,
        corrective_action,
        environmental_impact_score,
        carbon_footprint_kg,
        recorded_by,
        created_date,
        updated_date,
        -- Derived metrics
        round(total_material_cost + disposal_cost, 2) as total_waste_cost,
        date_trunc('month', waste_date) as waste_month
    from source
)

select * from renamed
