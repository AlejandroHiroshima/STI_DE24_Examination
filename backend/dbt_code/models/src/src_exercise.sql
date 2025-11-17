with staging_exercise as (select * from {{ source('strength_table', 'strength_table') }} )

select
    exercise_name,
    muscle_group_primary,
    muscle_group_secondary,
    muscle_group_tertiary,
    
from staging_exercise