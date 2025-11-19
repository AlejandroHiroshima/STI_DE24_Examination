with staging_strength as (select * from {{ source('strength_table', 'strength_table') }} )

select
    set_number,
    reps,
    weight_kg,
    extra_weight_kg,
    time_minute,
    
from staging_strength
    
