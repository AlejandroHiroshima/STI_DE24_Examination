with fct_strength as (select * from {{ref ('src') }})

select
    {{ dbt_utils.generate_surrogate_key(['workout_date'])}} AS workout_date_id,
    {{ dbt_utils.generate_surrogate_key(['athlete_first_name', 'athlete_date_of_birth'])}} AS athlete_id,
    {{ dbt_utils.generate_surrogate_key(['exercise_name', 'muscle_group_primary'])}} as exercise_id,
    set_number,
    reps,
    weight_kg,
    extra_weight_kg,
    time_session,
    total_volume_session
from fct_strength