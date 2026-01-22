{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('raw', 'returns') }}
),

renamed as (
    select
        return_id,
        order_id,
        order_line_id,
        product_id,
        customer_id,
        return_request_date,
        return_reason,
        return_status,
        quantity_returned,
        return_condition,
        approved_date,
        received_date,
        refund_date,
        refund_method,
        refund_amount,
        restocking_fee,
        shipping_label_cost,
        is_warranty_return,
        inspector_notes,
        customer_comments,
        created_date,
        updated_date,
        -- Derived metrics
        datediff('day', return_request_date, approved_date) as days_to_approval,
        datediff('day', return_request_date, refund_date) as days_to_refund,
        round(refund_amount - restocking_fee - shipping_label_cost, 2) as net_refund_amount
    from source
)

select * from renamed
