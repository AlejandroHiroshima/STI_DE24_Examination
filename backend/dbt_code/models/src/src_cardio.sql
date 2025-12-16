with cardio_raw as (
    select 
        *,
        'Erik' as athlete_first_name,
        'Unevik' as athlete_last_name
    from {{ source('strength_table', 'staging_cardio') }}
),

normalized as (
    SELECT
        id as activity_id,
        athlete_id,
        cast(start_date as timestamp) as start_datetime,
        cast(start_date_local as timestamp) as start_datetime_local,
        date(start_date_local) as workout_date_local,
        timezone,
        type as activity_type,
        name as name_of_workout,
        distance,
        elapsed_time,
        average_heartrate,
        max_heartrate,
        average_speed,
        max_speed
    FROM cardio_raw
)

SELECT * FROM normalized