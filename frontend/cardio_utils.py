# from connect_duckdb import query_cardio_duckdb
# import pandas as pd
# import plotly.express as px

# def on_filter_click(state):
#     activity_type = state.selected_activity
#     start_date_str = state.dates[0].strftime("%Y-%m-%d")
#     end_date_str = state.dates[1].strftime("%Y-%m-%d")
#     df = query_cardio_duckdb(activity_type, start_date_str, end_date_str)

#     df["full_workout_date"] = pd.to_datetime(df["full_workout_date"], errors="coerce")
#     df["year_week"] = df["full_workout_date"].dt.strftime("%Y week%V")


#     weekly = (
#         df.groupby("year_week", as_index=False)["total_distance_km"]
#           .sum()
#           .sort_values("year_week")
#     )

#     top_exercises = (
#         df.groupby("activity_type", as_index=False)["total_distance_km"]
#           .sum()
#           .sort_values("total_distance_km", ascending=False)
#           .head(3)
#     )

    
#     fig = px.pie(
#         top_exercises,
#         values="total_distance_km",
#         names="activity_type",
#         hole=0.5,
#         title="Share of total distance per activity"
#     )
    
#     unique_session= sorted(df['full_workout_date'].dropna().unique().tolist())
    

#     state.cardio_data = df
#     state.weekly_volume = weekly
#     state.pie_figure = fig
#     state.show_data = True
#     state.selected_session= unique_session[0]
    
    
# def agg_data(df, stat):
#     df = df.dropna(subset=["full_workout_date"])
    

#     if stat not in df.columns:
#         return pd.DataFrame(columns=["full_workout_date", "value"])

#     df_agg = (
#         df.groupby("full_workout_date", as_index=False)[stat]
#           .mean()
#           .rename(columns={stat: "value"})
#           .sort_values("full_workout_date")
#     )
#     return df_agg


# def on_statistic_change(state):
#     stat = state.selected_statistics
#     df = getattr(state, "cardio_data", pd.DataFrame())
#     if stat and not df.empty:
#         state.cardio_data_agg = agg_data(df, stat)
#     else:
#         state.cardio_data_agg = pd.DataFrame(columns=["full_workout_date", "value"])

#--------------------------------------------------------------------------

# from connect_duckdb import query_cardio_duckdb
# import pandas as pd
# import plotly.express as px

# def on_filter_click(state):
#     activity_type = state.selected_activity
#     start_date_str = state.dates[0].strftime("%Y-%m-%d")
#     end_date_str = state.dates[1].strftime("%Y-%m-%d")
#     df = query_cardio_duckdb(activity_type, start_date_str, end_date_str)

#     # säkerställ datetime
#     df["full_workout_date"] = pd.to_datetime(df["full_workout_date"], errors="coerce")
#     df["year_week"] = df["full_workout_date"].dt.strftime("%Y week%V")

#     weekly = (
#         df.groupby("year_week", as_index=False)["total_distance_km"]
#           .sum()
#           .sort_values("year_week")
#     )

#     top_exercises = (
#         df.groupby("activity_type", as_index=False)["total_distance_km"]
#           .sum()
#           .sort_values("total_distance_km", ascending=False)
#           .head(3)
#     )

#     fig = px.pie(
#         top_exercises,
#         values="total_distance_km",
#         names="activity_type",
#         hole=0.5,
#         title="Share of total distance per activity"
#     )

   
#     session_list = sorted(
#         df["full_workout_date"].dropna().dt.strftime("%Y-%m-%d").unique().tolist()
#     )

#     # sätt state
#     state.cardio_data = df
#     state.weekly_volume = weekly
#     state.pie_figure = fig
#     state.session_list = session_list
#     state.show_data = True

    
#     if session_list:
#         state.selected_session = session_list[0]
#     else:
#         state.selected_session = None

    
#     sel_stat = getattr(state, "selected_statistics", None)
#     if sel_stat:
#         state.cardio_data_agg = agg_data(df, sel_stat)
#     else:
#         state.cardio_data_agg = pd.DataFrame(columns=["full_workout_date", "value"])

   
#     on_session_change(state)


# def agg_data(df, stat):
#     df = df.dropna(subset=["full_workout_date"])
#     if not stat or stat not in df.columns:
#         return pd.DataFrame(columns=["full_workout_date", "value"])
#     df_agg = (
#         df.groupby("full_workout_date", as_index=False)[stat]
#           .mean()
#           .rename(columns={stat: "value"})
#           .sort_values("full_workout_date")
#     )
#     return df_agg


# def on_statistic_change(state):
#     stat = state.selected_statistics
#     df = getattr(state, "cardio_data", pd.DataFrame())
#     if stat and not df.empty:
#         state.cardio_data_agg = agg_data(df, stat)
#     else:
#         state.cardio_data_agg = pd.DataFrame(columns=["full_workout_date", "value"])


# def on_session_change(state):
   
#     sel = getattr(state, "selected_session", None)
#     df = getattr(state, "cardio_data", pd.DataFrame())
#     state.session_avg_pulse = 0

#     if not sel or df.empty:
#         return

#     sel_dt = pd.to_datetime(sel)
    
#     filtered = df[df["full_workout_date"].dt.normalize() == sel_dt.normalize()]

#     if filtered.empty or "average_heartrate_bpm" not in filtered.columns:
#         state.session_avg_pulse = 0
#     else:
#         state.session_avg_pulse = int(round(filtered["average_heartrate_bpm"].mean()))


# from connect_duckdb import query_cardio_duckdb
# import pandas as pd
# import plotly.express as px

# def on_filter_click(state):
#     activity_type = state.selected_activity
#     start_date_str = state.dates[0].strftime("%Y-%m-%d")
#     end_date_str = state.dates[1].strftime("%Y-%m-%d")
#     df = query_cardio_duckdb(activity_type, start_date_str, end_date_str)

#     # säkerställ datetime
#     df["full_workout_date"] = pd.to_datetime(df["full_workout_date"], errors="coerce")
#     df["year_week"] = df["full_workout_date"].dt.strftime("%Y week%V")

#     weekly = (
#         df.groupby("year_week", as_index=False)["total_distance_km"]
#           .sum()
#           .sort_values("year_week")
#     )

#     top_exercises = (
#         df.groupby("activity_type", as_index=False)["total_distance_km"]
#           .sum()
#           .sort_values("total_distance_km", ascending=False)
#           .head(3)
#     )

#     fig = px.pie(
#         top_exercises,
#         values="total_distance_km",
#         names="activity_type",
#         hole=0.5,
#         title="Share of total distance per activity"
#     )

#     # skapa LOV som strängar (YYYY-MM-DD) för selector — undvik Timestamp-LOV
#     session_list = sorted(
#         df["full_workout_date"].dropna().dt.strftime("%Y-%m-%d").unique().tolist()
#     )

#     # sätt state
#     state.cardio_data = df
#     state.weekly_volume = weekly
#     state.pie_figure = fig
#     state.session_list = session_list
#     state.show_data = True

#     # sätt ett förvalt session-val om listan inte är tom
#     if session_list:
#         state.selected_session = session_list[0]
#     else:
#         state.selected_session = None

#     # om användaren redan har vald statistik, skapa initial agg-data
#     sel_stat = getattr(state, "selected_statistics", None)
#     if sel_stat:
#         state.cardio_data_agg = agg_data(df, sel_stat)
#     else:
#         state.cardio_data_agg = pd.DataFrame(columns=["full_workout_date", "value"])

#     # uppdatera session-specifik visning direkt (valfri)
#     on_session_change(state)


# def agg_data(df, stat):
#     df = df.dropna(subset=["full_workout_date"])
#     if not stat or stat not in df.columns:
#         return pd.DataFrame(columns=["full_workout_date", "value"])
#     df_agg = (
#         df.groupby("full_workout_date", as_index=False)[stat]
#           .mean()
#           .rename(columns={stat: "value"})
#           .sort_values("full_workout_date")
#     )
#     return df_agg


# def on_statistic_change(state):
#     stat = state.selected_statistics
#     df = getattr(state, "cardio_data", pd.DataFrame())
#     if stat and not df.empty:
#         state.cardio_data_agg = agg_data(df, stat)
#     else:
#         state.cardio_data_agg = pd.DataFrame(columns=["full_workout_date", "value"])


# def on_session_change(state):
#     """
#     Callback för när selected_session ändras.
#     Förväntar sig att state.selected_session är en sträng "YYYY-MM-DD".
#     Sätter flera KPI:er i state — 0 om ingen data.
#     """
#     sel = getattr(state, "selected_session", None)
#     df = getattr(state, "cardio_data", pd.DataFrame())
#     if not sel or df.empty:
#         state.session_avg_pulse = 0
#         state.session_total_distance = 0
#         state.session_max_heartrate = 0
#         state.session_avg_speed = 0
#         return

#     sel_dt = pd.to_datetime(sel)
#     filtered = df[df["full_workout_date"].dt.normalize() == sel_dt.normalize()]

#     if filtered.empty:
#         state.session_avg_pulse = 0
#         state.session_total_distance = 0
#         state.session_max_heartrate = 0
#         state.session_avg_speed = 0
#         return

#     state.session_avg_pulse = int(round(filtered["average_heartrate_bpm"].mean())) if "average_heartrate_bpm" in filtered else 0
#     state.session_total_distance = round(filtered["total_distance_km"].sum(), 2) if "total_distance_km" in filtered else 0
#     state.session_max_heartrate = int(filtered["max_heartrate_bpm"].max()) if "max_heartrate_bpm" in filtered else 0
#     state.session_avg_speed = round(filtered["average_speed_kmh"].mean(), 2) if "average_speed_kmh" in filtered else 0

from connect_duckdb import query_cardio_duckdb
import pandas as pd
import plotly.express as px

def minutes_to_h_m(total_minutes):
    try:
        total_minutes = int(round(float(total_minutes)))
    except Exception:
        return "0 h 0 min"
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours} h {minutes} min"

def on_filter_click(state):
    try:
        activity_type = state.selected_activity
    except AttributeError:
        activity_type = "All"

    try:
        start_date_obj = state.dates[0]
        end_date_obj = state.dates[1]
    except Exception:
        end_date_obj = pd.Timestamp.now()
        start_date_obj = end_date_obj - pd.Timedelta(days=30)

    start_date_str = pd.to_datetime(start_date_obj).strftime("%Y-%m-%d")
    end_date_str = pd.to_datetime(end_date_obj).strftime("%Y-%m-%d")

    df = query_cardio_duckdb(activity_type, start_date_str, end_date_str)
    df["full_workout_date"] = pd.to_datetime(df["full_workout_date"], errors="coerce")
    df["year_week"] = df["full_workout_date"].dt.strftime("%Y week%V")

    weekly = (
        df.groupby("year_week", as_index=False)["total_distance_km"]
          .sum()
          .sort_values("year_week")
    )

    full_df = query_cardio_duckdb("All", start_date_str, end_date_str)
    full_df["full_workout_date"] = pd.to_datetime(full_df["full_workout_date"], errors="coerce")

    time_col = "average_moving_time_min"

    if time_col in full_df.columns:
        top_exercises = (
            full_df.groupby("activity_type", as_index=False)[time_col]
            .sum()
            .rename(columns={time_col: "total_minutes"})
            .sort_values("total_minutes", ascending=False)
            .reset_index(drop=True)
        )
    else:
        top_exercises = (
            full_df.groupby("activity_type", as_index=False)["total_distance_km"]
            .sum()
            .rename(columns={"total_distance_km": "total_minutes"})
            .sort_values("total_minutes", ascending=False)
            .reset_index(drop=True)
        )

    top_exercises["time_h_m"] = top_exercises["total_minutes"].apply(minutes_to_h_m)

    fig = px.pie(
        top_exercises,
        values="total_minutes",
        names="activity_type",
        hole=0.5,
        title="Share of total time per activity (minutes)",
    )

    customdata = top_exercises[["total_minutes", "time_h_m"]].values
    fig.update_traces(
        customdata=customdata,
        text=top_exercises["time_h_m"],
        textinfo="label+text",
        hovertemplate="%{label}<br>%{customdata[1]} (%{value} min)<extra></extra>",
    )

    session_list = sorted(
        df["full_workout_date"].dropna().dt.strftime("%Y-%m-%d").unique().tolist()
    )

    state.cardio_data = df
    state.weekly_volume = weekly
    state.pie_figure = fig
    state.session_list = session_list
    state.show_data = True

    state.selected_session = session_list[0] if session_list else None

    try:
        sel_stat = state.selected_statistics
    except AttributeError:
        sel_stat = None

    if sel_stat:
        state.cardio_data_agg = agg_data(df, sel_stat)
    else:
        state.cardio_data_agg = pd.DataFrame(columns=["full_workout_date", "value"])

    on_session_change(state)


def agg_data(df, stat):
    df = df.dropna(subset=["full_workout_date"])
    if not stat or stat not in df.columns:
        return pd.DataFrame(columns=["full_workout_date", "value"])
    df_agg = (
        df.groupby("full_workout_date", as_index=False)[stat]
          .mean()
          .rename(columns={stat: "value"})
          .sort_values("full_workout_date")
    )
    return df_agg


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