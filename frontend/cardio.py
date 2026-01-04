import datetime
import pandas as pd
import taipy.gui.builder as tgb
from taipy.gui import navigate
from cardio_utils import on_filter_click

activity_types = ["All", "Run", "Ride", "Spinning"]
selected_activity = "All"
start_date = datetime.date(2025, 11, 10)
end_date = datetime.date.today()
dates = [start_date, end_date]
show_data = False
pie_figure= None
cardio_data = pd.DataFrame()
weekly_volume = pd.DataFrame()


def format_minutes_to_h_m(total_minutes: float) -> str:
    if total_minutes is None or pd.isna(total_minutes):
        return "0 h 0 min"
    total_minutes = int(round(total_minutes))
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours} h {minutes}"

def go_dashboard(state):
    navigate(state, to="dashboard")
    
with tgb.Page() as cardio_page:
    tgb.toggle(theme=True)

    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Cardio", mode="md")

    with tgb.part():
        with tgb.part(class_name="text-center card-margin"):
            with tgb.part(class_name="card card-margin"):
                with tgb.layout(columns="1 1"):
                    with tgb.part():
                        tgb.selector(
                            value="{selected_activity}",
                            lov=activity_types,
                            dropdown=True,
                            label="Choose activity type",
                        )
                    with tgb.part():
                        tgb.date_range("{dates}", with_time=False, format="yyyy-MM-dd")

                with tgb.part():
                    tgb.button("Filter", on_action=on_filter_click)
                    
            with tgb.part(render="{show_data}"):
                with tgb.layout(columns="2 1"): 
                    with tgb.part(class_name="card card-margin"):
                        tgb.chart(
                            "{weekly_volume}",
                            x="year_week",
                            y="total_distance_km",
                            type="linechart",
                            title="Total distance (km)",
                            layout= {
                                "xaxis": {"title": "Week number",
                                        "tickangle": -45},
                                "yaxis": {"title": "Distance (km)"}
                            },
                            height="400px",
                            color = "red"
                        )
                    with tgb.part(class_name= "card card-margin"):
                        tgb.text("## Volume by exercise", mode="md")
                        tgb.chart(figure= "{pie_figure}", height="400px")
            

            with tgb.part(render="{show_data}"):
                with tgb.part(class_name="card card-margin"):
                    tgb.text("## KPI's", mode="md")

                    with tgb.layout(columns="1 1 1"):
                        with tgb.part(class_name="card"):
                            tgb.text("**Total sessions**", mode="md")
                            tgb.text("{len(cardio_data)}", class_name="h2")

                        with tgb.part(class_name="card"):
                            tgb.text("**Total distance (km)**", mode="md")
                            tgb.text("{round(cardio_data['total_distance_km'].sum(), 1)}", class_name="h2")

                        with tgb.part(class_name="card"):
                            tgb.text("**Average speed (km/h)**", mode="md")
                            tgb.text("{round(cardio_data['average_speed_kmh'].mean(), 1)}", class_name="h2")

                        with tgb.part(class_name="card"):
                            tgb.text("**Total time**", mode="md")
                            tgb.text(
                                "{format_minutes_to_h_m(cardio_data['average_moving_time_min'].sum())}",
                                class_name="h2",
                            )
                        with tgb.part(class_name="card"):
                            tgb.text("**Average heart rate (bpm)**", mode="md")
                            tgb.text("{round(cardio_data['average_heartrate_bpm'].mean())}", class_name="h2")

                        with tgb.part(class_name="card"):
                            tgb.text("**Max heart rate (bpm)**", mode="md")
                            tgb.text("{round(cardio_data['max_heartrate_bpm'].max(), 0)}", class_name="h2")

                tgb.button(
                    "Back to main page",
                    on_action=go_dashboard,
                )