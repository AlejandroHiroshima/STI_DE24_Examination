import taipy.gui.builder as tgb
from taipy.gui import navigate
from connect_duckdb import query_strength_duckdb
import datetime
import pandas as pd

people = ["Erik", "alexander"]
selected_athlete = "Erik"
start_date = datetime.date(2014,1,6)
end_date = datetime.date.today()
dates = [start_date, end_date]
show_data = False
strength_data = pd.DataFrame()

def on_filter_click(state):
    athlete = state.selected_athlete
    start_date = state.dates[0].strftime("%Y-%m-%d")
    end_date = state.dates[1].strftime("%Y-%m-%d")
    df= query_strength_duckdb(athlete, start_date, end_date)
    state.strength_data = df
    state.show_data= True


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
                with tgb.part(class_name="card card-margin"):
                    tgb.text("## KPI's", mode="md")

                    with tgb.layout(columns="1 1 1"):
                        with tgb.part(class_name="card"):
                            tgb.text("**Total gym sessions**", mode="md")
                            tgb.text("{len(strength_data['full_workout_date'].unique())}", class_name="h2")
                
                        with tgb.part(class_name="card"):
                            tgb.text("**Total volume (kg)**", mode="md")
                            if selected_athlete == 'Erik':
                                tgb.text("{strength_data['total_volume_session'].sum()}", class_name="h2")
                            else:
                                tgb.text("{strength_data['weight_kg'].sum()}", class_name="h2")

                        with tgb.part(class_name="card"):
                            tgb.text("**Total amount of sets**", mode="md")
                            tgb.text("{len(strength_data)}", class_name="h2")

                    with tgb.layout(columns="1 1 1"):
                        with tgb.part(class_name="card"):
                            tgb.text("**Total time spent**", mode="md")
                            tgb.text("{(strength_data['time_session'].sum())}", class_name="h2")
                
                        with tgb.part(class_name="card"):
                            tgb.text("**Total number repetitions**", mode="md")
                            tgb.text("{strength_data['reps'].sum()}", class_name="h2")
                    
                        with tgb.part(class_name="card"):
                            tgb.text("**Heaviest set**", mode="md")
                            tgb.text("{strength_data['weight_kg'].max()}", class_name="h2")
                        


                tgb.button(
                    "Tillbaka till dashboard",
                    on_action=lambda state: navigate(state, to="dashboard")
                ) 

