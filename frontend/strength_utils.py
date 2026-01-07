from connect_duckdb import query_strength_duckdb
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

colors = [
    "#A6FF00",  
    "#FF6F61", 
    "#4B9CD3",  
    "#FFD700",
    "#6A5ACD", 
    "#FF8C00",  
]

def on_filter_click(state):
    athlete = state.selected_athlete
    start_date = state.dates[0].strftime("%Y-%m-%d")
    end_date = state.dates[1].strftime("%Y-%m-%d")
    df = query_strength_duckdb(athlete, start_date, end_date)    

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
        names="exercise_name",
        hole=0.5,
        title="Share of total volume per exercise",
        color_discrete_sequence=colors
    )
    fig.update_traces(textinfo='percent+label')

    unique_exercises = sorted(df['exercise_name'].dropna().unique().tolist())
    unique_sessions = sorted(df['exercise_session_name'].dropna().unique().tolist())

    # Sätt förvalda val om de inte redan finns
    if not state.selected_exercise and unique_exercises:
        state.selected_exercise = unique_exercises[0]

    if not state.selected_session and unique_sessions:
        state.selected_session = unique_sessions[0]

    line_fig = px.line(
        weekly,
        x="year_week",
        y="volume_kg",
        title="Total lifted volume per week (kg)",
        markers=False,
        color_discrete_sequence=["#A6FF00"]
    )
    line_fig.update_traces(line=dict(width=3))

    sel_ex = state.selected_exercise if state.selected_exercise else None

    if sel_ex:
        exercise_data = df[df['exercise_name'] == sel_ex]
        exercise_volume = exercise_data.groupby('full_workout_date', as_index=False)['volume_kg'].sum()
        exercise_line_fig = px.line(
            exercise_volume,
            x='full_workout_date',
            y='volume_kg',
            title=f"Volume over time for selected exercise: {sel_ex}",
            color_discrete_sequence=["#A6FF00"]
        )
        exercise_line_fig.update_traces(line=dict(width=3))
        state.exercise_line_figure = exercise_line_fig
    else:
        state.exercise_line_figure = None

    state.weekly_figure = line_fig
    state.strength_data = df
    state.top_exercises = top_exercises
    state.weekly_volume = weekly
    state.pie_figure = fig
    state.show_data = True