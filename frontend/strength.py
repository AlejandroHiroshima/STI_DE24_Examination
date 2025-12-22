import taipy.gui.builder as tgb
from taipy.gui import navigate
from connect_duckdb import query_strength_duckdb
import datetime
import pandas as pd

people = ["Erik", "Alexander"]
selected_athlete = "Erik"
start_date = datetime.date(2025,12,1)
end_date = datetime.date.today()
dates = [start_date, end_date]
show_data = False
strength_data = pd.DataFrame()
weekly_volume = pd.DataFrame()  # Ny state-variabel för grafen

def on_filter_click(state):
    athlete = state.selected_athlete
    start_date = state.dates[0].strftime("%Y-%m-%d")
    end_date = state.dates[1].strftime("%Y-%m-%d")
    df= query_strength_duckdb(athlete, start_date, end_date)    
    state.strength_data = df
    state.show_data= True
    
    #-------------------------------------------------Beräkningar för grafen
    
    # --- Beräkna volym per rad beroende på atlet ---
    if athlete == "Erik":
        df["volume_kg"] = df["total_volume_session"] * 1000  # Konvertera ton till kg
    else:  # Alexander
        df["volume_kg"] = df["weight_kg"] * df["reps"]
    
    # --- Skapa veckokolumn ---
    df["full_workout_date"] = pd.to_datetime(df["full_workout_date"])
    df["year_week"] = df["full_workout_date"].dt.strftime("%Y-W%V")
    
    # --- Aggregera per vecka ---
    weekly = (
        df.groupby("year_week", as_index=False)["volume_kg"]
          .sum()
          .sort_values("year_week")
    )
    
    state.strength_data = df
    state.weekly_volume = weekly
    state.show_data = True
    
    #---------------------------------------------------------------------

#---Ändrar tidsformatet från pandas Timedelta till 'X h Y min'    
def format_timedelta_to_h_m(td) -> str:
    if td is None or pd.isna(td):
        return "0 h 0 min"

    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f"{hours} h {minutes} min"


# -- Toggle back to dashboard button 
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
            # --- graf för Lyft volym per vecka             
                with tgb.part(class_name="card card-margin"):
                    tgb.chart(
                        "{weekly_volume}",
                        x="year_week",
                        y="volume_kg",
                        type="linechart",
                        title="Total lifted volume per week (kg)",
                        height="400px",
                        color = "red"
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
                                "{strength_data.loc[strength_data['weight_kg'].idxmax(), 'reps']} reps, "
                                "{strength_data.loc[strength_data['weight_kg'].idxmax(), 'exercise_name']}",
                                class_name="h2"
    )
                        


                tgb.button(
                    "Back to main page",
                    on_action=go_dashboard,
                )

