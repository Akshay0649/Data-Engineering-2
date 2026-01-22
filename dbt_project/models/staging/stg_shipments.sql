{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('raw', 'shipments') }}
),

renamed as (
    select
        shipment_id,
        order_id,
        tracking_number,
        carrier,
        service_level,
        shipment_date,
        expected_delivery_date,
        actual_delivery_date,
        shipment_status,
        origin_warehouse,
        destination_city,
        destination_state,
        destination_postal_code,
        weight_kg,
        dimensions_cm,
        shipping_cost,
        package_count,
        is_signature_required,
        is_insured,
        insurance_value,
        delivery_notes,
        created_date,
        updated_date,
        -- Derived metrics
        datediff('day', shipment_date, expected_delivery_date) as expected_transit_days,
        datediff('day', shipment_date, actual_delivery_date) as actual_transit_days,
        case 
            when actual_delivery_date <= expected_delivery_date then 1 
            else 0 
        end as is_on_time_delivery,
        case 
            when actual_delivery_date > expected_delivery_date 
            then datediff('day', expected_delivery_date, actual_delivery_date)
            else 0 
        end as days_delayed
    from source
)

select * from renamed
