from pathlib import Path
import os
import dlt
import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from backend.load_strength_historical_data import strength_source
from backend.load_strava_data import strava_source

DUCKDB_PATH = os.getenv("DUCKDB_PATH")
DBT_PROFILES_DIR = os.getenv("DBT_PROFILES_DIR")

if not DUCKDB_PATH:
    raise RuntimeError("DUCKDB_PATH is not set in environment variables")

if not DBT_PROFILES_DIR:
    raise RuntimeError("DBT_PROFILES_DIR is not set in environment variables")
dlt_resource = DagsterDltResource()

@dlt_assets(
    dlt_source=strength_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="strength_training",
        dataset_name="staging",
        destination=dlt.destinations.duckdb(DUCKDB_PATH),
    ),
)
def dlt_strength_load(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


@dg.asset(
    name="dlt_strava_load",
    group_name="strava",
    compute_kind="dlt",
)
def dlt_strava_load(context: dg.AssetExecutionContext):
    duckdb_path = os.getenv("DUCKDB_PATH")
    if not duckdb_path:
        raise RuntimeError("DUCKDB_PATH is not set in environment variables")

    context.log.info(f"Creating dlt pipeline to {duckdb_path}")

    pipeline = dlt.pipeline(
        pipeline_name="strava_pipeline",
        destination="duckdb",
        dataset_name="staging",
    )

    os.environ["DESTINATION__DUCKDB__CREDENTIALS"] = duckdb_path

    source = strava_source()

    context.log.info("Running dlt pipeline for Strava...")
    load_info = pipeline.run(source)

    context.log.info(f"Load info: {load_info}")

    if pipeline.last_trace and pipeline.last_trace.last_normalize_info:
        row_counts = pipeline.last_trace.last_normalize_info.row_counts
        context.log.info(f"Row counts: {row_counts}")
        
        return dg.Output(
            value=None,
            metadata={
                "rows_loaded": row_counts.get("stg_strava_activities", 0),
                "load_id": load_info.loads_ids[0] if load_info.loads_ids else "N/A",
            }
        )
    else:
        context.log.warning("No normalize info available (0 rows loaded?)")
        return dg.Output(value=None, metadata={"rows_loaded": 0})

dbt_project_directory = Path(__file__).parent / "backend" / "dbt_code"

dbt_project = DbtProject(
    project_dir=dbt_project_directory,
    profiles_dir=DBT_PROFILES_DIR,
)

dbt_resource = DbtCliResource(project_dir=dbt_project)
dbt_project.prepare_if_dev()

@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    """
    Alla dbt-modeller (strength + cardio).
    """
    yield from dbt.cli(["build"], context=context).stream()

job_dlt_strength = dg.define_asset_job(
    "job_dlt_strength",
    selection=dg.AssetSelection.assets(dlt_strength_load)
)

job_dlt_strava = dg.define_asset_job(
    "job_dlt_strava",
    selection=dg.AssetSelection.assets(dlt_strava_load)
)

job_dbt = dg.define_asset_job(
    "job_dbt",
    selection=dg.AssetSelection.assets(dbt_models)
)

schedule_dlt_strength = dg.ScheduleDefinition(
    name="job_dlt_strength_schedule",
    job=job_dlt_strength,
    cron_schedule="00 08 * * *",
    execution_timezone="Europe/Stockholm",
)

schedule_dlt_strava = dg.ScheduleDefinition(
    name="job_dlt_strava_schedule",
    job=job_dlt_strava,
    cron_schedule="05 08 * * *",
    execution_timezone="Europe/Stockholm",
)

@dg.multi_asset_sensor(
    monitored_assets=[
        dg.AssetKey("dlt_strength_source_historical_strength_data_alex"),
        dg.AssetKey("dlt_strength_source_historical_strength_data_erik"),
        dg.AssetKey("dlt_strava_load"),
    ],
    job_name="job_dbt",
)
def dlt_strength_sensor(context: dg.MultiAssetSensorEvaluationContext):
    """
    Trigga dbt-jobbet när ALLA övervakade dlt-assets har materialiserats
    sedan senaste sensor-tick.
    """
    records = context.latest_materialization_records_by_key()

    if all(records.get(key) for key in context.asset_keys):
        context.advance_all_cursors()
        yield dg.RunRequest()

defs = dg.Definitions(
    assets=[dlt_strength_load, dlt_strava_load, dbt_models],
    resources={
        "dlt": dlt_resource,
        "dbt": dbt_resource,
    },
    jobs=[job_dlt_strength, job_dlt_strava, job_dbt],
    schedules=[schedule_dlt_strength, schedule_dlt_strava],
    sensors=[dlt_strength_sensor],
)