{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('raw', 'quality_inspections') }}
),

renamed as (
    select
        inspection_id,
        inspection_date,
        inspection_time,
        inspection_type,
        inspection_status,
        product_id,
        batch_id,
        order_id,
        facility_location,
        inspector_name,
        inspector_id,
        sample_size,
        defect_count,
        defect_type,
        severity_level,
        defect_description,
        measurement_1,
        measurement_2,
        measurement_3,
        specification_met,
        tolerance_percentage,
        visual_inspection_score,
        functional_test_result,
        compliance_standard,
        corrective_action_required,
        corrective_action_description,
        follow_up_date,
        root_cause_analysis,
        cost_of_quality,
        disposition,
        notes,
        created_date,
        updated_date,
        -- Derived metrics
        case when defect_count > 0 then round(defect_count * 100.0 / sample_size, 2) else 0 end as defect_rate,
        case when inspection_status = 'Pass' then 1 else 0 end as is_passed,
        date_trunc('month', inspection_date) as inspection_month
    from source
)

select * from renamed
