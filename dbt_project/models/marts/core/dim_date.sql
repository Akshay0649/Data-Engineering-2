{{
    config(
        materialized='table',
        schema='marts'
    )
}}

-- Dimension: Date
-- Standard date dimension for time-based analysis

with date_spine as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2020-01-01' as date)",
        end_date="cast('2030-12-31' as date)"
    ) }}
),

final as (
    select
        cast(date_day as date) as date_key,
        date_day,
        extract(year from date_day) as year,
        extract(quarter from date_day) as quarter,
        extract(month from date_day) as month,
        extract(day from date_day) as day,
        extract(dayofweek from date_day) as day_of_week,
        extract(dayofyear from date_day) as day_of_year,
        extract(week from date_day) as week_of_year,
        case extract(dayofweek from date_day)
            when 0 then 'Sunday'
            when 1 then 'Monday'
            when 2 then 'Tuesday'
            when 3 then 'Wednesday'
            when 4 then 'Thursday'
            when 5 then 'Friday'
            when 6 then 'Saturday'
        end as day_name,
        case extract(month from date_day)
            when 1 then 'January'
            when 2 then 'February'
            when 3 then 'March'
            when 4 then 'April'
            when 5 then 'May'
            when 6 then 'June'
            when 7 then 'July'
            when 8 then 'August'
            when 9 then 'September'
            when 10 then 'October'
            when 11 then 'November'
            when 12 then 'December'
        end as month_name,
        case when extract(dayofweek from date_day) in (0, 6) then true else false end as is_weekend,
        date_trunc('month', date_day) as first_day_of_month,
        last_day(date_day, 'month') as last_day_of_month,
        date_trunc('quarter', date_day) as first_day_of_quarter,
        date_trunc('year', date_day) as first_day_of_year
    from date_spine
)

select * from final
