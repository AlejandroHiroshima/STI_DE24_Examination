with cardio_raw as (
    select 
        *
    from {{ source('strength_table', 'staging_cardio') }}
),

normalized as (
    SELECT
        cast(start_date_local as timestamp) as start_datetime_local,
        date(start_date_local) as workout_date_local,
        type as activity_type,
        cast(distance as float) AS distance_m,
        elapsed_time AS total_time_s,
        moving_time AS moving_time_s,
        cast(average_heartrate as float) AS average_heartrate_bpm,
        cast(max_heartrate as float) AS max_heartrate_bpm,
        cast(max_speed as float) AS max_speed_m_per_s
    FROM cardio_raw
)

SELECT * FROM normalized