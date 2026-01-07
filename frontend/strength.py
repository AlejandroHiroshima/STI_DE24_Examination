import taipy.gui.builder as tgb
from taipy.gui import navigate
from strength_utils import on_filter_click
import datetime
import pandas as pd
import plotly.graph_objects as go

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
weekly_figure = go.Figure()
exercise_line_figure = go.Figure()
    
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
    with tgb.part(class_name="text-center"):
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
                            label="Choose athlete"
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
                            figure="{weekly_figure}",
                            height="400px",
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
                            class_name="h2")
            
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
                            "-{strength_data.loc[strength_data['weight_kg'].idxmax(), 'year']}"
                            , class_name="h5"
                        )
                tgb.text("## Exercise focus", mode="md")
                with tgb.part(class_name="card card-margin"):
                    with tgb.layout(columns= "2 1 1 1"):
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
                        with tgb.part(render= "{selected_exercise is not None}"):    
                            tgb.text("**Total sets**", mode="md")
                            tgb.text("{len(strength_data[strength_data['exercise_name'] == selected_exercise])}", class_name="h3")
                        with tgb.part(render= "{selected_exercise is not None}"):    
                            tgb.text("**Max weight**", mode="md")
                            tgb.text("{strength_data[strength_data['exercise_name'] == selected_exercise]['weight_kg'].max()} kg",
                                     class_name="h3")
                    with tgb.part():
                        tgb.chart(
                            figure="{exercise_line_figure}",
                            height="300px"
                        )
                tgb.text("## Session explorer", mode="md")
                with tgb.part(class_name="card card-margin"):
                    tgb.selector("{selected_session}",
                                lov="{sorted(strength_data['exercise_session_name'].dropna().unique().tolist())}",
                                dropdown=True,
                                label="Choose session")
                    with tgb.part(render="{selected_session is not None}"):
                        with tgb.layout(columns="1 1 1"):
                            with tgb.part(class_name="card"):
                                tgb.text("**Session volume (kg)**", mode="md")
                                tgb.text("{round(strength_data[strength_data['exercise_session_name'] == selected_session]['volume_kg'].sum(), 1)}", class_name="h3")
                            with tgb.part(class_name="card"):
                                tgb.text("**Exercises**", mode="md")    
                                tgb.text("{len(strength_data[strength_data['exercise_session_name'] == selected_session]['exercise_name'].unique())}", class_name="h3")
                            with tgb.part(class_name="card"):
                                tgb.text("**Total sets**", mode="md")    
                                tgb.text("{len(strength_data[strength_data['exercise_session_name'] == selected_session])}", class_name="h3")
                        tgb.table("{strength_data[strength_data['exercise_session_name'] == selected_session][['exercise_name','set_number','reps','weight_kg']].sort_values(['exercise_name','set_number']).rename(columns=lambda c: c.replace('_',' ').title()).reset_index(drop=True)}")

                tgb.button(
                    "Back to main page",
                    on_action=go_dashboard,
                )