with dim_athletes as (
   select distinct
      athlete_first_name,
      athlete_last_name,
      athlete_date_of_birth,  
      body_weight_kg, 
      gender
   from {{ref('src') }})


select
   {{ dbt_utils.generate_surrogate_key(['athlete_first_name', 'athlete_date_of_birth'])}} AS athlete_id,
   athlete_first_name,
   athlete_last_name,
   athlete_date_of_birth as body_weight_kg,  
   body_weight_kg, 
   gender
from
    dim_athletes





