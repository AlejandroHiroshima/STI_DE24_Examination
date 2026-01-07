import taipy.gui.builder as tgb
from taipy.gui import Gui
from taipy.gui import navigate
from cardio import cardio_page
from strength import strength_page

pic_width= "400px"
pic_height= "350px"

with tgb.Page() as start_page:
    with tgb.part(class_name="text-center"):
        tgb.text("# Training dashboard", mode="md")
        tgb.image("logo.png")
        
        with tgb.part():
            tgb.text("## Choose activity:", mode="md")
            with tgb.layout(columns="1 1"):

                with tgb.part() as strength:
                    with tgb.part(class_name="text-center"):
                            with tgb.part():
                                tgb.text('#### **Strength**', mode="md")
                                tgb.image("strength.png",
                                    width=pic_width,
                                    height=pic_height,
                                    on_action=lambda state: navigate(state, to="strength")
                                )

                with tgb.part() as cardio:
                    with tgb.part(class_name="text-center"):
                            with tgb.part():
                                tgb.text('#### **Cardio**', mode="md")
                                tgb.image("cardio.png",
                                    width=pic_width,
                                    height=pic_height,
                                    on_action=lambda state: navigate(state, to="cardio")
                                )            
                        
if __name__ == "__main__":
    pages = {
        "dashboard": start_page,
        "strength": strength_page,
        "cardio": cardio_page,
    }
    
    Gui(pages=pages, css_file="style.css").run(dark_mode=True, 
                                               use_reloader=True,
                                               host="0.0.0.0", 
                                               port=8081, 
                                               title= "Training Dashboard", 
                                               watermark="Training Dashboard")