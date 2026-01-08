import datetime
import pandas as pd
import taipy.gui.builder as tgb
from taipy.gui import navigate
from cardio_utils import on_filter_click, on_statistic_change, on_session_change, minutes_to_h_m_s

activity_types = ["All", "Run", "Ride", "Spinning"]
selected_activity = "All"
start_date = datetime.date(2025, 11, 10)
end_date = datetime.date.today()
dates = [start_date, end_date]
show_data = False
pie_figure = None
selected_statistics = "average_heartrate_bpm"
session_list = []
selected_session = None
session_avg_pulse = 0
session_total_distance = 0
session_max_heartrate = 0
session_avg_speed = 0
session_total_moving = 0
cardio_data = pd.DataFrame()
weekly_volume = pd.DataFrame()
top_exercises = pd.DataFrame()
cardio_data_agg = pd.DataFrame()
chart_y_title = ""
minutes_to_h_m = minutes_to_h_m_s

stat_labels = {
    "average_heartrate_bpm": "Average Heart Rate (bpm)",
    "average_speed_kmh": "Average Speed (km/h)",
    "max_heartrate_bpm": "Max Heart Rate (bpm)",
    "max_speed_kmh": "Max Speed (km/h)",
    "total_distance_km": "Total Distance (km)"
}
lov_keys = list(stat_labels.keys())
lov_labels = list(stat_labels.values())


def go_dashboard(state):
    navigate(state, to="dashboard")
    
    
with tgb.Page() as cardio_page:
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
                                "xaxis": {
                                    "title": "Week number",
                                    "tickangle": -45,
                                    "titlefont": {"size": 16, "family": "Arial, sans-serif", "color": "#A6FF00"},
                                    "title_standoff": 25,
                                    "tickfont": {"size": 12}
                                },
                                "yaxis": {
                                    "title": "Distance (km)",
                                    "titlefont": {"size": 16, "family": "Arial, sans-serif", "color": "#A6FF00"},
                                    "title_standoff": 25,
                                    "tickfont": {"size": 12}
                                },
                                "margin": {"t": 50, "b": 100}
                            },
                            height="400px",
                            color="#A6FF00"
                        )
                    with tgb.part(class_name= "card card-margin"):
                        tgb.text("## Volume by exercise", mode="md")
                        tgb.chart(figure="{pie_figure}", height="400px")
            
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
                                "{minutes_to_h_m(cardio_data['average_moving_time_min'].sum())}",
                                class_name="h2",
                            )

                        with tgb.part(class_name="card"):
                            tgb.text("**Average heart rate (bpm)**", mode="md")
                            tgb.text("{round(cardio_data['average_heartrate_bpm'].mean())}", class_name="h2")

                        with tgb.part(class_name="card"):
                            tgb.text("**Max heart rate (bpm)**", mode="md")
                            tgb.text("{round(cardio_data['max_heartrate_bpm'].max(), 0)}", class_name="h2")
                    
            with tgb.part(render="{show_data}"):
                tgb.text("## Statistics", mode="md")
                with tgb.part(class_name="card card-margin"):
                    tgb.selector(
                        value="{selected_statistics}",
                        lov=lov_keys,
                        lov_labels=lov_labels,
                        dropdown=True,
                        label="Choose statistic",
                        on_change=on_statistic_change
                    )
                    
                    tgb.chart(
                        "{cardio_data_agg}",
                        x="full_workout_date",
                        y="value",
                        type="line",
                        title="{stat_labels[selected_statistics] if selected_statistics in stat_labels else selected_statistics} over time",
                        layout={
                            "xaxis": {
                                "title": "Date",
                                "type": "date",
                                "tickangle": -45,
                                "titlefont": {"size": 16, "family": "Arial, sans-serif", "color": "#A6FF00"},
                                "title_standoff": 25,
                                "tickfont": {"size": 12}
                            },
                            "yaxis": {
                                "title": "Value",
                                "titlefont": {"size": 16, "family": "Arial, sans-serif", "color": "#A6FF00"},
                                "title_standoff": 25,
                                "tickfont": {"size": 12}
                            },
                            "margin": {"t": 50, "b": 100}
                        },
                        height="300px",
                        render="{selected_statistics is not None and len(cardio_data_agg) > 0}",
                        color="#A6FF00"
                    )
                    
            with tgb.part(render="{show_data}"):
                tgb.text("## Session explorer", mode="md")
                with tgb.part(class_name="card card-margin"):
                    tgb.selector(
                        value="{selected_session}",
                        lov="{session_list}",
                        dropdown=True,
                        label="Choose session",
                        on_change=on_session_change
                    )
                    with tgb.part(render="{selected_session is not None}"):
                        with tgb.layout(columns="1 1 1 1 1"):
                            with tgb.part(class_name="card"):
                                tgb.text("**Session average pulse (bpm)**", mode="md")
                                tgb.text("{session_avg_pulse}", class_name="h3")
                            with tgb.part(class_name="card"):
                                tgb.text("**Total distance (km)**", mode="md")
                                tgb.text("{session_total_distance}", class_name="h3")
                            with tgb.part(class_name="card"):
                                tgb.text("**Max heart rate (bpm)**", mode="md")
                                tgb.text("{session_max_heartrate}", class_name="h3")
                            with tgb.part(class_name="card"):
                                tgb.text("**Average speed (km/h)**", mode="md")
                                tgb.text("{session_avg_speed}", class_name="h3")
                            with tgb.part(class_name="card"):
                                tgb.text("**Total running time (00:00:00)**", mode="md")
                                tgb.text("{minutes_to_h_m(session_total_moving)}", class_name="h3")

            with tgb.part(style="text-align: center; width: 100%; margin-top: 20px;"):
                tgb.button(
                    "Back to main page",
                    on_action=go_dashboard
                )