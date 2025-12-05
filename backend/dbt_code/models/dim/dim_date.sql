with dim_dates as (select distinct workout_date from {{ ref('src')}} )

select
    {{ dbt_utils.generate_surrogate_key(['workout_date'])}} AS workout_date_id,
    extract(year from workout_date) as year, 
    extract(quarter from workout_date) as quarter, 
    extract(month from workout_date) as month, 
    extract(week from workout_date) as week, 
    extract(day from workout_date) as day, 
    case when extract(dayofweek from workout_date) in (0, 6) then true else false end as is_weekend

from 
    dim_dates


