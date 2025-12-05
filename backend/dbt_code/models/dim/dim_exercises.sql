with dim_exercise as (
    select distinct
        exercise_name,
        muscle_group_primary,
    from {{ref ('src') }})

select
    {{ dbt_utils.generate_surrogate_key(['exercise_name', 'muscle_group_primary'])}} as exercise_id,
    exercise_name,
    muscle_group_primary,
from
    dim_exercise

