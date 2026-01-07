# from connect_duckdb import query_cardio_duckdb
# import pandas as pd
# import plotly.express as px

# colors = [
#     "#A6FF00",  
#     "#FF6F61", 
#     "#4B9CD3",  
#     "#FFD700",
#     "#6A5ACD", 
#     "#FF8C00",  
# ]
# lime_color = "#A6FF00"

# def minutes_to_h_m(total_minutes):
#     try:
#         total_minutes = int(round(float(total_minutes)))
#     except Exception:
#         return "0 h 0 min"
#     hours = total_minutes // 60
#     minutes = total_minutes % 60
#     return f"{hours} h {minutes} min"

# def on_filter_click(state):
#     try:
#         activity_type = state.selected_activity
#     except AttributeError:
#         activity_type = "All"

#     try:
#         start_date_obj = state.dates[0]
#         end_date_obj = state.dates[1]
#     except Exception:
#         end_date_obj = pd.Timestamp.now()
#         start_date_obj = end_date_obj - pd.Timedelta(days=30)

#     start_date_str = pd.to_datetime(start_date_obj).strftime("%Y-%m-%d")
#     end_date_str = pd.to_datetime(end_date_obj).strftime("%Y-%m-%d")

#     df = query_cardio_duckdb(activity_type, start_date_str, end_date_str)
#     df["full_workout_date"] = pd.to_datetime(df["full_workout_date"], errors="coerce")
#     df["year_week"] = df["full_workout_date"].dt.strftime("%Y week%V")

#     weekly = (
#         df.groupby("year_week", as_index=False)["total_distance_km"]
#           .sum()
#           .sort_values("year_week")
#     )

#     full_df = query_cardio_duckdb("All", start_date_str, end_date_str)
#     full_df["full_workout_date"] = pd.to_datetime(full_df["full_workout_date"], errors="coerce")

#     time_col = "average_moving_time_min"

#     if time_col in full_df.columns:
#         top_exercises = (
#             full_df.groupby("activity_type", as_index=False)[time_col]
#             .sum()
#             .rename(columns={time_col: "total_minutes"})
#             .sort_values("total_minutes", ascending=False)
#             .reset_index(drop=True)
#         )
#     else:
#         top_exercises = (
#             full_df.groupby("activity_type", as_index=False)["total_distance_km"]
#             .sum()
#             .rename(columns={"total_distance_km": "total_minutes"})
#             .sort_values("total_minutes", ascending=False)
#             .reset_index(drop=True)
#         )

#     top_exercises["time_h_m"] = top_exercises["total_minutes"].apply(minutes_to_h_m)

#     fig = px.pie(
#         top_exercises,
#         values="total_minutes",
#         names="activity_type",
#         hole=0.5,
#         title="Share of total time per activity",
#         color_discrete_sequence=colors
#     )

#     customdata = top_exercises[["total_minutes", "time_h_m"]].values
#     fig.update_traces(
#         customdata=customdata,
#         text=top_exercises["time_h_m"],
#         textinfo="label+text",
#         hovertemplate="%{label}<br>%{customdata[1]} (%{value} min)<extra></extra>",
#     )

#     session_list = sorted(
#         df["full_workout_date"].dropna().dt.strftime("%Y-%m-%d").unique().tolist()
#     )

#     state.cardio_data = df
#     state.weekly_volume = weekly
#     state.pie_figure = fig
#     state.session_list = session_list
#     state.show_data = True

#     state.selected_session = session_list[0] if session_list else None

#     try:
#         sel_stat = state.selected_statistics
#     except AttributeError:
#         sel_stat = None

#     if sel_stat:
#         state.cardio_data_agg = agg_data(df, sel_stat)
#     else:
#         state.cardio_data_agg = pd.DataFrame(columns=["full_workout_date", "value"])

#     on_session_change(state)


# def agg_data(df, stat):
#     df = df.dropna(subset=["full_workout_date"])
#     if not stat or stat not in df.columns:
#         return pd.DataFrame(columns=["full_workout_date", "value"])

#     df = df.copy()
#     df[stat] = pd.to_numeric(df[stat], errors="coerce")   
#     df_agg = (
#         df.groupby("full_workout_date", as_index=False)[stat]
#           .mean()
#           .rename(columns={stat: "value"})
#           .sort_values("full_workout_date")
#     )
#     return df_agg


# def on_statistic_change(state):
#     try:
#         stat = state.selected_statistics
#     except AttributeError:
#         stat = None

#     try:
#         df = state.cardio_data if state.cardio_data is not None else pd.DataFrame()
#     except AttributeError:
#         df = pd.DataFrame()

#     if stat and not df.empty:
#         state.cardio_data_agg = agg_data(df, stat)
#     else:
#         state.cardio_data_agg = pd.DataFrame(columns=["full_workout_date", "value"])

# def on_session_change(state):
#     try:
#         sel = state.selected_session
#     except AttributeError:
#         sel = None

#     try:
#         df = state.cardio_data if state.cardio_data is not None else pd.DataFrame()
#     except AttributeError:
#         df = pd.DataFrame()

#     state.session_avg_pulse = 0
#     state.session_total_distance = 0
#     state.session_max_heartrate = 0
#     state.session_avg_speed = 0
#     state.session_total_moving = 0

#     if not sel or df.empty:
#         return

#     sel_dt = pd.to_datetime(sel)
#     filtered = df[df["full_workout_date"].dt.normalize() == sel_dt.normalize()]

#     if filtered.empty:
#         return

#     if "average_heartrate_bpm" in filtered:
#         state.session_avg_pulse = int(round(filtered["average_heartrate_bpm"].mean()))
#     if "total_distance_km" in filtered:
#         state.session_total_distance = round(filtered["total_distance_km"].sum(), 2)
#     if "max_heartrate_bpm" in filtered:
#         state.session_max_heartrate = int(filtered["max_heartrate_bpm"].max())
#     if "average_speed_kmh" in filtered:
#         state.session_avg_speed = round(filtered["average_speed_kmh"].mean(), 2)
#     if "total_moving_time_min" in filtered:
#         state.session_total_moving = round(filtered["total_moving_time_min"].sum(), 2)
        
# def minutes_to_h_m_s(total_minutes):
#     try:
#         total_seconds = int(round(float(total_minutes) * 60))
#     except Exception:
#         return "00:00:00"
#     hours = total_seconds // 3600
#     minutes = (total_seconds % 3600) // 60
#     seconds = total_seconds % 60
#     return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


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

lime_color = "#A6FF00"


def on_filter_click(state):
    athlete = state.selected_athlete
    # state.dates kommer från UI, anta list [start_date, end_date]
    start_date = state.dates[0].strftime("%Y-%m-%d")
    end_date = state.dates[1].strftime("%Y-%m-%d")

    df = query_strength_duckdb(athlete, start_date, end_date)

    # Hantera tomt resultat
    if df is None or df.empty:
        state.strength_data = pd.DataFrame()
        state.top_exercises = pd.DataFrame()
        state.weekly_volume = pd.DataFrame()
        state.pie_figure = None
        state.weekly_figure = go.Figure()
        state.exercise_line_figure = go.Figure()
        state.selected_exercise = None
        state.selected_session = None
        state.show_data = False
        return

    # Säkerställ numeriska kolumner
    for col in ("weight_kg", "reps"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        else:
            df[col] = 0

    # Volym per rad
    df["volume_kg"] = df["weight_kg"] * df["reps"]

    # Datumhantering
    df["full_workout_date"] = pd.to_datetime(df["full_workout_date"], errors="coerce")

    # Filtrera säkerställning (redundant om query redan filtrerat men tryggt)
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    df = df[(df["full_workout_date"] >= start_dt) & (df["full_workout_date"] <= end_dt)]

    # Skapa veckans start (måndag) för kronologisk gruppering
    df = df.dropna(subset=["full_workout_date"])
    if not df.empty:
        df["week_start_date"] = df["full_workout_date"] - pd.to_timedelta(df["full_workout_date"].dt.weekday, unit="d")
    else:
        df["week_start_date"] = pd.NaT

    # Aggregation per vecka med verklig datum som index
    weekly = (
        df.groupby("week_start_date", as_index=False)["volume_kg"]
          .sum()
          .sort_values("week_start_date")
    )

    # Lägg till en label för visning (valfritt)
    weekly["year_week"] = weekly["week_start_date"].dt.strftime("%Y week%V")

    # Top exercises
    top_exercises = (
        df.groupby("exercise_name", as_index=False)["volume_kg"]
          .sum()
          .sort_values("volume_kg", ascending=False)
          .head(5)
    )

    # Pie chart
    fig = px.pie(
        top_exercises,
        values="volume_kg",
        names="exercise_name",
        hole=0.5,
        title="Share of total volume per exercise",
        color_discrete_sequence=colors
    )
    fig.update_traces(textinfo="percent+label")

    # Defaults för selectors
    unique_exercises = sorted(df["exercise_name"].dropna().unique().tolist())
    unique_sessions = sorted(df["exercise_session_name"].dropna().unique().tolist())

    if not getattr(state, "selected_exercise", None) and unique_exercises:
        state.selected_exercise = unique_exercises[0]

    if not getattr(state, "selected_session", None) and unique_sessions:
        state.selected_session = unique_sessions[0]

    # Line plot per vecka — använd week_start_date som x
    if not weekly.empty:
        line_fig = px.line(
            weekly,
            x="week_start_date",
            y="volume_kg",
            title="Total lifted volume per week (kg)",
            markers=False,
            color_discrete_sequence=[lime_color]
        )
        line_fig.update_traces(line=dict(width=3))
        line_fig.update_xaxes(tickangle=-45, tickformat="%Y-%W")
        line_fig.update_layout(
            xaxis_title="Week number",
            yaxis_title="Volume (kg)",
            margin=dict(t=50, b=100)
        )
    else:
        line_fig = go.Figure()

    # Exercise-specific line (per date)
    sel_ex = state.selected_exercise if state.selected_exercise else None
    if sel_ex:
        exercise_data = df[df["exercise_name"] == sel_ex]
        if not exercise_data.empty:
            exercise_volume = exercise_data.groupby("full_workout_date", as_index=False)["volume_kg"].sum().sort_values("full_workout_date")
            exercise_line_fig = px.line(
                exercise_volume,
                x="full_workout_date",
                y="volume_kg",
                title=f"Volume over time for selected exercise: {sel_ex}",
                color_discrete_sequence=[lime_color]
            )
            exercise_line_fig.update_traces(line=dict(width=3))
            exercise_line_fig.update_xaxes(tickangle=-45)
            exercise_line_fig.update_layout(
                xaxis_title="Workout date",
                yaxis_title="Volume (kg)",
                margin=dict(t=50, b=100)
            )
        else:
            exercise_line_fig = go.Figure()
    else:
        exercise_line_fig = go.Figure()

    # Spara i state
    state.weekly_figure = line_fig
    state.strength_data = df
    state.top_exercises = top_exercises
    state.weekly_volume = weekly
    state.pie_figure = fig
    state.show_data = True
    state.exercise_line_figure = exercise_line_fig


def on_exercise_change(state):
   
    try:
        df = state.strength_data
    except AttributeError:
        df = pd.DataFrame()

    sel_ex = state.selected_exercise if state.selected_exercise else None

    if df is None or df.empty or not sel_ex:
        state.exercise_line_figure = go.Figure()
        return

    exercise_data = df[df["exercise_name"] == sel_ex]
    if exercise_data.empty:
        state.exercise_line_figure = go.Figure()
        return

    exercise_volume = exercise_data.groupby("full_workout_date", as_index=False)["volume_kg"].sum().sort_values("full_workout_date")
    exercise_line_fig = px.line(
        exercise_volume,
        x="full_workout_date",
        y="volume_kg",
        title=f"Volume over time for selected exercise: {sel_ex}",
        color_discrete_sequence=[lime_color]
    )
    exercise_line_fig.update_traces(line=dict(width=3))
    exercise_line_fig.update_xaxes(tickangle=-45)
    exercise_line_fig.update_layout(
        xaxis_title="Workout date",
        yaxis_title="Volume (kg)",
        margin=dict(t=50, b=100)
    )
    state.exercise_line_figure = exercise_line_fig

def on_statistic_change(state):
    try:
        stat = state.selected_statistics
    except AttributeError:
        stat = None

    try:
        df = state.cardio_data if state.cardio_data is not None else pd.DataFrame()
    except AttributeError:
        df = pd.DataFrame()

    if stat and not df.empty:
        state.cardio_data_agg = agg_data(df, stat)
    else:
        state.cardio_data_agg = pd.DataFrame(columns=["full_workout_date", "value"])

def on_session_change(state):
    try:
        sel = state.selected_session
    except AttributeError:
        sel = None

    try:
        df = state.cardio_data if state.cardio_data is not None else pd.DataFrame()
    except AttributeError:
        df = pd.DataFrame()

    state.session_avg_pulse = 0
    state.session_total_distance = 0
    state.session_max_heartrate = 0
    state.session_avg_speed = 0
    state.session_total_moving = 0

    if not sel or df.empty:
        return

    sel_dt = pd.to_datetime(sel)
    filtered = df[df["full_workout_date"].dt.normalize() == sel_dt.normalize()]

    if filtered.empty:
        return

    if "average_heartrate_bpm" in filtered:
        state.session_avg_pulse = int(round(filtered["average_heartrate_bpm"].mean()))
    if "total_distance_km" in filtered:
        state.session_total_distance = round(filtered["total_distance_km"].sum(), 2)
    if "max_heartrate_bpm" in filtered:
        state.session_max_heartrate = int(filtered["max_heartrate_bpm"].max())
    if "average_speed_kmh" in filtered:
        state.session_avg_speed = round(filtered["average_speed_kmh"].mean(), 2)
    if "total_moving_time_min" in filtered:
        state.session_total_moving = round(filtered["total_moving_time_min"].sum(), 2)
        
def minutes_to_h_m_s(total_minutes):
    try:
        total_seconds = int(round(float(total_minutes) * 60))
    except Exception:
        return "00:00:00"
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
