with staging_dates as (select * from {{ source('strength_table', 'strength_table') }} )

select
    workout_date

from staging_dates


