with raw as (
    select * from {{ ref('src') }}
),

normalized as (
    select
        r.*,
        coalesce(m.canonical_exercise_name, trim(r.exercise_name)) as canonical_exercise_name
    from raw r
    left join {{ ref('exercise_name') }} e
           on trim(r.exercise_name) = e.raw_exercise_name
),

with_muscle as (
    select
        n.*,
        d.primary_muscle_group
    from normalized n
    left join {{ ref('dim_exercises') }} d
           on n.canonical_exercise_name = d.exercise_name
),

session_enriched as (
    select
        *,
        string_agg(distinct primary_muscle_group, ', ' order by primary_muscle_group)
            over (partition by workout_date,
                             athlete_first_name,
                             athlete_date_of_birth) as primary_mg_list
    from with_muscle
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
    total_volume_session,
    concat(
        strftime(workout_date, '%d/%m'), ' ',strftime(workout_date, '%a'), ' - ',primary_mg_list
    ) as exercise_session_name
from session_enriched