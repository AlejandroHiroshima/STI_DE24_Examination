with cardio_raw as (
    select 
        *
    from {{ source('strength_table', 'staging_cardio') }}
),

normalized as (
    SELECT
        date(start_date_local) as workout_date_local,
        type as activity_type,
        distance AS distance_m,
        elapsed_time AS total_time_s,
        moving_time AS moving_time_s,
        moving_time_h,
        average_heartrate AS average_heartrate_bpm,
        max_heartrate AS max_heartrate_bpm,
        max_speed AS max_speed_m_per_s
    FROM cardio_raw
)

SELECT * FROM normalized