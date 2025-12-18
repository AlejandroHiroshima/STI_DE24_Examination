with raw as (SELECT * FROM  {{ ref('src_cardio')}} ),
 
normalized as (
    SELECT
        workout_date_local,   -- date
        start_datetime_local,
        distance_m / 1000 AS distance_km,
        total_time_s / 60 AS total_time_min, -- total time for session in minutes, including stops/breaks 
        moving_time_s / 60 AS moving_time_min, -- time spent actually moving in minutes
        moving_time_s / 3600 AS moving_time_h, -- time spent moving in hours
        (total_time_min - moving_time_min) AS rest_time_min, -- time spent resting in minutes
        distance_km / moving_time_h AS average_speed_kmh, -- in km/h
        average_heartrate_bpm,
        max_heartrate_bpm,
        max_speed_m_per_s * 3.6 AS max_speed_kmh, -- in km/h
        CASE 
            WHEN distance_km = 0 THEN 'Spinning'
            ELSE activity_type END AS activity_type
    FROM raw
),

with_keys as (
    SELECT
        {{dbt_utils.generate_surrogate_key(['workout_date_local'])}} as workout_date_id,
        start_datetime_local,
        workout_date_local,
        activity_type,
        distance_km,
        moving_time_min,
        rest_time_min,
        average_heartrate_bpm,
        max_heartrate_bpm,
        average_speed_kmh,
        max_speed_kmh
    FROM normalized
)

SELECT * FROM with_keys