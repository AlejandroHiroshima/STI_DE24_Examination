import taipy.gui.builder as tgb
from taipy.gui import Gui
from taipy.gui import navigate
from alex import alex_page
from erik import erik_page

with tgb.Page() as start_page:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Training dashboard", mode="md")
        tgb.image("../files/logo.jpg")
        
        with tgb.part():
            tgb.text("## Choose athlete:", mode="md")
            with tgb.layout(columns="1 1"):

                with tgb.part() as column_erik:
                    with tgb.part(class_name="text-center card-margin"):
                        with tgb.part(class_name="card card-margin"):
                                with tgb.part():
                                    tgb.text('#### **Erik**', mode="md")
                                    tgb.image("../files/erik_profile.jpg",
                                        on_action=lambda state: navigate(state, to="erik")
                                    )

                with tgb.part() as column_alex:
                        with tgb.part(class_name="text-center card-margin"):
                            with tgb.part(class_name="card card-margin"):
                                    with tgb.part():
                                        tgb.text('#### **Alexander**', mode="md")
                                        tgb.image("../files/erik_profile.jpg",
                                            on_action=lambda state: navigate(state, to="alex")
                                        )            
                        
if __name__ == "__main__":
    


    pages = {
            "dashboard": start_page,
            "erik": erik_page,
            "alex": alex_page,
        }
        
        
    Gui(pages=pages).run(dark_mode=True, use_reloader=True, port=8081)