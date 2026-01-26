{{ config(materialized="view") }}

select
    -- bases
    dispatching_base_num,
    affiliated_base_number as affiliated_base_num,

    -- identifiers
    cast(pulocationid as integer) as pickup_locationid,
    cast(dolocationid as integer) as dropoff_locationid,

    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,

    -- shared trips flag
    cast(sr_flag as integer) as sr_flag

from {{ source("staging", "fhv_tripdata") }}

where dispatching_base_num is not null and extract(year from pickup_datetime) = 2019
