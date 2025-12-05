with fct_strength_raw as (
    select * from {{ ref('src') }}
),

normalized_exercise as (
    select
        f.*,
        coalesce(nm.canonical_exercise_name, trim(f.exercise_name)) as canonical_exercise_name
    from fct_strength_raw f
    left join {{ ref('exercise_name') }} nm
           on trim(f.exercise_name) = nm.raw_exercise_name
)

select
    {{ dbt_utils.generate_surrogate_key(['workout_date']) }} as workout_date_id,
    {{ dbt_utils.generate_surrogate_key(['athlete_first_name', 'athlete_date_of_birth']) }} as athlete_id,
    {{ dbt_utils.generate_surrogate_key(['canonical_exercise_name']) }} as exercise_id,
    set_number,
    reps,
    weight_kg,
    extra_weight_kg,
    time_session,
    total_volume_session
from normalized_exercise