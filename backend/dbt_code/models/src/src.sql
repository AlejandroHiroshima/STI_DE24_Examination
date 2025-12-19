with alex_raw_data as (select * from {{ source('strength_table', 'stg_alex') }}),
 erik_raw_data as (select * from {{ source('strength_table', 'stg_erik') }}),

alex_normalized as(
    select
    {# trim(lower(athlete_first_name)) as athlete_first_name,
    trim(lower(athlete_last_name)) as athlete_last_name, #}
    'alexander' as athlete_first_name,
    'hrachovina' as athlete_last_name,
    cast('1985-06-24' as date) as athlete_date_of_birth,
    'male' as gender,
    cast(athlete_weight_kg as double) as body_weight_kg,
    cast(workout_date as date) as workout_date,
    exercise_name,
    cast(set_number as integer) as set_number,
    cast(reps as integer) as reps,
    cast(weight_kg as double) as weight_kg,
    cast(extra_weight_kg as double) as extra_weight_kg,
    cast(time_session as interval) as time_session,
    {# 'set' as log_type, #}
    0.0 as total_volume_session
from alex_raw_data
),

erik_normalized as(
    select
    {# trim(lower(athlete_first_name)) as athlete_first_name,
    trim(lower(athlete_last_name)) as athlete_last_name, #}
    'erik' as athlete_first_name,
    'unevik' as athlete_last_name,
    cast('1988-03-22' as date) as athlete_date_of_birth,
    'male' AS gender,
    cast(athlete_weight_kg as double) as body_weight_kg,
    cast(workout_date as date) as workout_date,
    exercise_name,
    cast(set_number as integer) as set_number,
    cast(reps as integer) as reps,
    cast(weight_kg as double) as weight_kg,
    cast(extra_weight_kg as double) as extra_weight_kg,
    cast(time_session as interval) as time_session,
    cast(total_volume_session as double) as total_volume_session,
    {# case when total_volume_session is not null then 'session'
    else 'set'
    end as log_type #}
from erik_raw_data
),

combined as (select * from alex_normalized
              union all
              select * from erik_normalized
)

select * from combined