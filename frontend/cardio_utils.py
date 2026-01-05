from connect_duckdb import query_cardio_duckdb
import pandas as pd
import plotly.express as px

def on_filter_click(state):
    activity_type = state.selected_activity
    start_date_str = state.dates[0].strftime("%Y-%m-%d")
    end_date_str = state.dates[1].strftime("%Y-%m-%d")
    df = query_cardio_duckdb(activity_type, start_date_str, end_date_str)

    df["full_workout_date"] = pd.to_datetime(df["full_workout_date"], errors="coerce")
    df["year_week"] = df["full_workout_date"].dt.strftime("%Y week%V")


    weekly = (
        df.groupby("year_week", as_index=False)["total_distance_km"]
          .sum()
          .sort_values("year_week")
    )

    top_exercises = (
        df.groupby("activity_type", as_index=False)["total_distance_km"]
          .sum()
          .sort_values("total_distance_km", ascending=False)
          .head(3)
    )

    
    fig = px.pie(
        top_exercises,
        values="total_distance_km",
        names="activity_type",
        hole=0.5,
        title="Share of total distance per activity"
    )

    state.cardio_data = df
    state.weekly_volume = weekly
    state.pie_figure = fig
    state.show_data = True
    
    
def agg_data(df, stat):
    df = df.dropna(subset=["full_workout_date"])
    

    if stat not in df.columns:
        return pd.DataFrame(columns=["full_workout_date", "value"])

    df_agg = (
        df.groupby("full_workout_date", as_index=False)[stat]
          .mean()
          .rename(columns={stat: "value"})
          .sort_values("full_workout_date")
    )
    return df_agg


def on_statistic_change(state):
    stat = state.selected_statistics
    df = getattr(state, "cardio_data", pd.DataFrame())
    if stat and not df.empty:
        state.cardio_data_agg = agg_data(df, stat)
    else:
        state.cardio_data_agg = pd.DataFrame(columns=["full_workout_date", "value"])