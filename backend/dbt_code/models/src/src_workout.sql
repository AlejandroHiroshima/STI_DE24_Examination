with staging_workout as (select * from {{ source('strength_table', 'strength_table') }} )

select
    workoutgym_name,
    athlete_id,
    workout_date,
    total_volume_session
    
from staging_workout