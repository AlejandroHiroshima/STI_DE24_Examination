from connect_duckdb import query_strength_duckdb
import plotly.express as px
import pandas as pd

def on_filter_click(state):
    athlete = state.selected_athlete
    start_date = state.dates[0].strftime("%Y-%m-%d")
    end_date = state.dates[1].strftime("%Y-%m-%d")
    df= query_strength_duckdb(athlete, start_date, end_date)    
    
    if athlete == "Erik":
        df["volume_kg"] = df["total_volume_session"] * 1000
    else:
        df["volume_kg"] = df["weight_kg"] * df["reps"]
    
    df["full_workout_date"] = pd.to_datetime(df["full_workout_date"])
    df["year_week"] = df["full_workout_date"].dt.strftime("%Y week%V")
    
    weekly = (
        df.groupby("year_week", as_index=False)["volume_kg"]
          .sum()
          .sort_values("year_week")
    )
    top_exercises = (
        df.groupby("exercise_name", as_index=False)['volume_kg']
        .sum()
        .sort_values("volume_kg", ascending=False)
        .head(5)
    )
    fig = px.pie(
        top_exercises,
        values="volume_kg",
        names= "exercise_name",
        hole=0.5,
        title="Share of total volume per exercise"
    )
    unique_exercises = sorted(df['exercise_name'].dropna().unique().tolist())
    unique_sessions= sorted(df['exercise_session_name'].dropna().unique().tolist())
    
    state.strength_data = df
    state.top_exercises = top_exercises
    state.weekly_volume = weekly
    state.pie_figure = fig
    state.selected_exercise = unique_exercises[0] 
    state.selected_session = unique_sessions[0] 
    state.show_data = True
    
    

