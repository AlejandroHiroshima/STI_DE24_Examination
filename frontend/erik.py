import taipy.gui.builder as tgb
from taipy.gui import navigate

with tgb.Page() as erik_page:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Erik – choose exercise type", mode="md")

    with tgb.part():
        with tgb.part(class_name="text-center card-margin"):
            with tgb.part(class_name="card card-margin"):
                with tgb.layout(columns="1 1"):
                    with tgb.part():
                        tgb.text("### Strength", mode="md")
                    with tgb.part():
                        tgb.text("### Cardio", mode="md")

                tgb.button(
                    "Tillbaka till dashboard",
                    on_action=lambda state: navigate(state, to="/")
                ) 

