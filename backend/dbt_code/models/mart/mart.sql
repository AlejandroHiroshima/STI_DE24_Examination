with
    fct_strength as (select * from {{ref('fct_strength')}} ),
    dim_athletes as (select * from {{ref('dim_athletes')}} ),
    dim_date as (select * from {{ref('dim_date')}} ),
    dim_exercise as (select * from {{ref('dim_exercise')}} )

select
    *
from
    fct_strength f
left join dim_athletes da on f.athlete_id = da.athlete_id    
left join dim_date dd on f.workout_date_id = dd.workout_date_id
left join dim_exercise de on f.exercise_id = de.exercise_id

