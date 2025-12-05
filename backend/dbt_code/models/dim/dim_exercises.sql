with src as (
    SELECT DISTINCT(TRIM(exercise_name)) AS exercise_name_raw,
        muscle_group_primary
    FROM {{ ref('src') }}
),

cleaned as (
    SELECT
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                LOWER(REPLACE(exercise_name_raw, '-', ' ')),
                ' {2,}', ' ', 'g'
            ),
            ' $', '', 'g'
        ) AS exercise_name,
        muscle_group_primary

    FROM src
), normalized AS (
    SELECT
        CASE 
            WHEN exercise_name IS 'bench press' THEN 'benchpress'
            WHEN exercise_name IS 'chinup' THEN 'chin-up'
            ELSE exercise_name
        END AS exercise_name,
        muscle_group_primary
    FROM cleaned
),

select
    {{ dbt_utils.generate_surrogate_key(['exercise_name', 'muscle_group_primary'])}} as exercise_id,
    exercise_name,
    muscle_group_primary,
from
    cleaned

