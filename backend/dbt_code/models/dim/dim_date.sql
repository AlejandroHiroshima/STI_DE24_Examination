with dim_dates as (
    select distinct workout_date 
    from {{ ref('src')}} 

    union

    select distinct workout_date_local as workout_date
    from {{ ref('src_cardio')}}
    )

select
    {{ dbt_utils.generate_surrogate_key(['workout_date'])}} AS workout_date_id,
    workout_date AS full_workout_date,
    extract(year from workout_date) as year, 
    extract(quarter from workout_date) as quarter, 
    extract(month from workout_date) as month, 
    strftime(workout_date, '%b') as month_name, 
    extract(week from workout_date) as week, 
    extract(day from workout_date) as day, 
    strftime(workout_date, '%a') as day_name,
    case when extract(dayofweek from workout_date) in (0, 6) then true else false end as is_weekend
from 
    dim_dates