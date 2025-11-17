 with staging_athletes as (select * from {{ source('strength_table', 'strength_table') }} )

 select
    athlete_first_name, 
    athlete_last_name,
    athlete_date_of_birth,
    bodyweight_kilo,
    gender,
    created_at,
    updated_at,
    
from staging_athletes