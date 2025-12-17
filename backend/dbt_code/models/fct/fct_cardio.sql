with raw as (SELECT * FROM  {{ ref('src_cardio')}} ),
 
normalized as (
    SELECT
        id as activity_id,
        athlete_id,
        start_datetime_local, -- timestamp
        workout_date_local,   -- date
        activity_type,
        name_of_workout,
        distance,
        elapsed_time,
        average_heartrate,
        max_heartrate,
        average_speed,
        max_speed
    FROM raw
),

with_keys as (
    SELECT
        {{dbt.utils.dbt_utils.generate_surrogate_key(['workout_date_local'])}} as workout_date_id,
        activity_id,
        athlete_id,
        start_datetime_local,
        workout_date_local,
        activity_type,
        name_of_workout,
        distance,
        elapsed_time,
        average_heartrate,
        max_heartrate,
        average_speed,
        max_speed
    FROM normalized
)

SELECT * FROM with_keys