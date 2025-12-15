with src as (
    SELECT DISTINCT(TRIM(exercise_name)) AS exercise_name_raw
    FROM {{ ref('src') }}
    WHERE exercise_name IS NOT NULL
),

normalized_names as (

    select
        coalesce(e.canonical_exercise_name, s.exercise_name_raw) as canonical_exercise_name
    from src s
    left join {{ ref('exercise_name') }} e
           on s.exercise_name_raw = e.raw_exercise_name

), assigned_muscle_groups as (

    select
        nn.canonical_exercise_name,
        mg.primary_muscle_group,
        mg.secondary_muscle_group 
        from normalized_names nn
    left join {{ ref('muscle_groups') }} mg
           on nn.canonical_exercise_name = mg.canonical_exercise_name

)

select
    {{ dbt_utils.generate_surrogate_key(['canonical_exercise_name']) }} as exercise_id,
    max(canonical_exercise_name) as exercise_name,  
    primary_muscle_group,
    secondary_muscle_group
from assigned_muscle_groups
GROUP BY 
    exercise_id,
    primary_muscle_group,
    secondary_muscle_group