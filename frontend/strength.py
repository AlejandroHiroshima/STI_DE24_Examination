import taipy.gui.builder as tgb
from taipy.gui import navigate
from connect_duckdb import query_strength_duckdb
import datetime
import pandas as pd
import plotly.express as px

people = ["Erik", "Alexander"]
selected_athlete = "Erik"
start_date = datetime.date(2025,12,1)
end_date = datetime.date.today()
dates = [start_date, end_date]
show_data = False
pie_figure= None
selected_exercise = None
selected_session = None
strength_data = pd.DataFrame()
weekly_volume = pd.DataFrame()
top_exercises = pd.DataFrame()

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
    
def format_timedelta_to_h_m(td) -> str:
    if td is None or pd.isna(td):
        return "0 h 0 min"

    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f"{hours} h {minutes} min"

def go_dashboard(state):
    navigate(state, to="dashboard")
    
with tgb.Page() as strength_page:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Strength", mode="md")

    with tgb.part():
        with tgb.part(class_name="text-center card-margin"):
            with tgb.part(class_name="card card-margin"):
                with tgb.layout(columns="1 1"):
                    with tgb.part():
                        tgb.selector(
                            value="{selected_athlete}",
                            lov=people,
                            dropdown=True,
                            label = "Choose athlete"
                        )
                    with tgb.part():
                        tgb.date_range("{dates}", with_time=False, format="yyyy-MM-dd")

                with tgb.part():
                    tgb.button(
                        "Filter",
                        on_action= on_filter_click
                    )  
                
            with tgb.part(render="{show_data}"):
                with tgb.layout(columns="2 1"): 
                    with tgb.part(class_name="card card-margin"):
                        tgb.chart(
                            "{weekly_volume}",
                            x="year_week",
                            y="volume_kg",
                            type="linechart",
                            title="Total lifted volume per week (kg)",
                            layout= {
                                "xaxis": {"title": "Week number",
                                        "tickangle": -45},
                                "yaxis": {"title": "Volume (kg)"}
                            },
                            height="400px",
                            color = "red"
                        )
                    with tgb.part(class_name= "card card-margin"):
                        tgb.text("## Volume by exercise", mode="md")
                        tgb.chart(figure= "{pie_figure}", height="400px")
                tgb.text("## KPI's", mode="md") 
                with tgb.layout(columns="1 1 1"): 
                    with tgb.part(class_name="card"):
                        tgb.text("**Total gym sessions**", mode="md") 
                        tgb.text("{len(strength_data['full_workout_date'].unique())}", class_name="h2")
            
                    with tgb.part(class_name="card"):
                        tgb.text("**Total volume (kg)**", mode="md")
                        with tgb.part(render="{selected_athlete == 'Erik'}"):
                            tgb.text("{round(strength_data['total_volume_session'].sum()*1000, 1)}", class_name="h2")
                        with tgb.part(render="{selected_athlete == 'Alexander'}"):
                            tgb.text("{round((strength_data['weight_kg'] * strength_data['reps']).sum(), 1)}", class_name="h2")
                            
                    with tgb.part(class_name="card"):
                        tgb.text("**Total amount of sets**", mode="md")
                        tgb.text("{len(strength_data)}", class_name="h2")

            
                    with tgb.part(class_name="card"):
                        tgb.text("**Total time**", mode="md")
                        tgb.text(
                            "{format_timedelta_to_h_m(strength_data['time_session'].sum())}",
                            class_name="h2"
                        )
            
                    with tgb.part(class_name="card"):
                        tgb.text("**Total number repetitions**", mode="md")
                        tgb.text("{strength_data['reps'].sum()}", class_name="h2")
                
                    with tgb.part(class_name="card"):
                        tgb.text("**Heaviest set**", mode="md")
                        tgb.text(
                            "{strength_data.loc[strength_data['weight_kg'].idxmax(), 'weight_kg']} kg × "
                            "{strength_data.loc[strength_data['weight_kg'].idxmax(), 'reps']} reps "
                            "{strength_data.loc[strength_data['weight_kg'].idxmax(), 'exercise_name']}",
                            class_name="h2")
                        tgb.text(
                            " on {strength_data.loc[strength_data['weight_kg'].idxmax(), 'day_name']}"
                            " {strength_data.loc[strength_data['weight_kg'].idxmax(), 'day']}"
                            "/{strength_data.loc[strength_data['weight_kg'].idxmax(), 'month']}"
                            , class_name="h5"
                        )
                tgb.text("## Exercise focus", mode="md")
                with tgb.part(class_name="card card-margin"):
                    with tgb.layout(columns= "1 2"):
                        with tgb.part():
                            tgb.selector(
                                value= "{selected_exercise}",
                                lov="{sorted(strength_data['exercise_name'].dropna().unique().tolist())}",
                                dropdown=True, 
                                label="Choose exercise")
                        with tgb.part(render= "{selected_exercise is not None}"):
                            tgb.text("**Total volume (kg)**", mode= "md")
                            tgb.text("{round(strength_data[strength_data['exercise_name'] == selected_exercise]['volume_kg'].sum(), 1)}", 
                                    class_name="h3")
                            tgb.text("**Total sets**", mode="md")
                            tgb.text("{len(strength_data[strength_data['exercise_name'] == selected_exercise])}", class_name="h3")
                            tgb.text("**Max weight**", mode="md")
                            tgb.text("{strength_data[strength_data['exercise_name'] == selected_exercise]['weight_kg'].max()} kg",
                                     class_name="h3")
                    with tgb.part():
                        tgb.chart(
                            "{strength_data[strength_data['exercise_name'] == selected_exercise]}",
                            x= "full_workout_date",
                            y="volume_kg",
                            type="line",
                            title="Volume over time for selected exercise: {selected_exercise}",
                            height="300px"
                        )
                with tgb.part(class_name="card card-margin")

                tgb.button(
                    "Back to main page",
                    on_action=go_dashboard,
                )