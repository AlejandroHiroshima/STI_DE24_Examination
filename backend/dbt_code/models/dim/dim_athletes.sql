with raw as (
    select
        trim(lower(athlete_first_name)) as athlete_first_name,
        trim(lower(athlete_last_name)) as athlete_last_name,
        athlete_date_of_birth,
        body_weight_kg,
        gender,
        workout_date
    from {{ ref('src') }}
    where athlete_first_name is not null
      and athlete_date_of_birth is not null
),

ranked as (
    select
        *,
        row_number() over (
            partition by athlete_first_name, athlete_last_name, athlete_date_of_birth
            order by case when body_weight_kg is not null then workout_date else null end desc nulls last
        ) as rn
    from raw
    where body_weight_kg is not null
),

latest_weight as (
    select
        trim(lower(athlete_first_name)) as athlete_first_name,
        trim(lower(athlete_last_name)) as athlete_last_name,
        athlete_date_of_birth,
        body_weight_kg,
        gender
    from ranked
    where rn = 1
),

distinct_athletes as (
    select distinct
        trim(lower(athlete_first_name)) as athlete_first_name,
        trim(lower(athlete_last_name)) as athlete_last_name,
        athlete_date_of_birth,
        gender
    from raw
)

select
    {{ dbt_utils.generate_surrogate_key(['lower(trim(da.athlete_first_name))', 'da.athlete_date_of_birth']) }} as athlete_id,
    da.athlete_first_name,
    da.athlete_last_name,
    da.athlete_date_of_birth,
    lw.body_weight_kg,
    da.gender
from distinct_athletes da
left join latest_weight lw
    on da.athlete_first_name = lw.athlete_first_name
    and da.athlete_last_name = lw.athlete_last_name
    and da.athlete_date_of_birth = lw.athlete_date_of_birth
