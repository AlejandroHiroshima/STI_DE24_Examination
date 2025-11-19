with staging_exercise as (select * from {{ source('strength_table', 'strength_table') }} )

select
    exercise_name,
    muscle_group_primary,
    muscle_group_secondary,
    
from staging_exercise