import taipy.gui.builder as tgb
from taipy.gui import Gui
from taipy.gui import navigate
from cardio import cardio_page
from strength import strength_page



with tgb.Page() as start_page:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Training dashboard", mode="md")
        tgb.image("logo.png")
        
        with tgb.part():
            tgb.text("## Choose activity:", mode="md")
            with tgb.layout(columns="1 1"):

                with tgb.part() as column_erik:
                    with tgb.part(class_name="text-center card-margin"):
                        with tgb.part(class_name="card card-margin"):
                                with tgb.part():
                                    tgb.text('#### **Strength**', mode="md")
                                    tgb.image("strength.png",
                                        on_action=lambda state: navigate(state, to="strength")
                                    )

                with tgb.part() as column_alex:
                        with tgb.part(class_name="text-center card-margin"):
                            with tgb.part(class_name="card card-margin"):
                                    with tgb.part():
                                        tgb.text('#### **Cardio**', mode="md")
                                        tgb.image("cardio.png",
                                            on_action=lambda state: navigate(state, to="cardio")
                                        )            
                        
if __name__ == "__main__":
    pages = {
        "dashboard": start_page,
        "strength": strength_page,
        "cardio": cardio_page,
    }
    
    Gui(pages=pages).run(dark_mode=True, use_reloader=False,host="0.0.0.0", port=8081)