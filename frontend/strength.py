import taipy.gui.builder as tgb
from taipy.gui import navigate
from connect_duckdb import connect_duckdb

people = ["erik", "alex"]
selected_athlete = ""

with tgb.Page() as strength_page:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Strength", mode="md")

    with tgb.part():
        with tgb.part(class_name="text-center card-margin"):
            with tgb.part(class_name="card card-margin"):
                with tgb.layout(columns="1 1"):
                    with tgb.part():
                        tgb.text("### Strength", mode="md")
                        tgb.selector(
                            value="{selected_athlete}",
                            lov=people,
                            dropdown=True,
                            label = "Choose athlete",
                            
                        )
                tgb.button(
                    "Tillbaka till dashboard",
                    on_action=lambda state: navigate(state, to="/")
                ) 

