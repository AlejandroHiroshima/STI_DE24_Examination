with dim_athletes as (select * from {{ref('src_athletes') }})


select
   {{ dbt_utils.generate_surrogate_key(['athlete_first_name', 'athlete_date_of_birth'])}} AS athlete_id,
   split_part(athlete_name, ' ' , 1) as athlete_first_name,
   split_part(athlete_name, ' ' , 2) as athlete_last_name,
   cast(athlete_date_of_birth as date) as athlete_date_of_birth,  
   cast(body_weight_kg as float) as body_weight_kg, 
   gender,
   current_timestamp as created_at,
   current_timestamp as updated_at,
from
    dim_athletes





