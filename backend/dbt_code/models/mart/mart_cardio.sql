with cardio as (
    SELECT 
        workout_date_id,
        workout_date_local,
        COUNT(*) AS total_cardio_sessions,
        SUM(distance_km) AS total_distance_km,
        SUM(moving_time_min) AS total_moving_time_min,
        SUM(rest_time_min) AS total_rest_time_min,
        AVG(average_heartrate_bpm) AS average_heartrate_bpm,
        MAX(max_heartrate_bpm) AS max_heartrate_bpm,
        AVG(average_speed_kmh) AS average_speed_kmh,
        MAX(max_speed_kmh) AS max_speed_kmh,
        AVG(moving_time_min) AS average_moving_time_min
    FROM {{ ref('fct_cardio') }}
    GROUP BY 
        workout_date_id,
        workout_date_local,
)

SELECT 
    c.*,
    dd.full_workout_date,
    dd.year,
    dd.quarter,
    dd.month,
    dd.month_name,
    dd.week,
    dd.day,
    dd.day_name,
    dd.is_weekend
FROM cardio c
LEFT JOIN {{ ref('dim_date') }} dd
    ON c.workout_date_id = dd.workout_date_id