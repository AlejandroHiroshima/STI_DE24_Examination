import taipy.gui.builder as tgb
from taipy.gui import navigate

with tgb.Page() as start_page:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("Choose athlete", mode="md")

    with tgb.part():
        with tgb.part(class_name="text-center card-margin"):
            with tgb.part(class_name="card card-margin"):
                with tgb.layout(columns=("1 1")):
                    with tgb.part():
                        tgb.text('### **Erik**', mode="md")
                        tgb.image(
                            "<lägg image här>", # image
                            on_action= <länk till athletssida> #
                            class_name = "hover_color picture_style",
                            height= "150px",
                            width= "150px"      
                        )

                        tgb.text('### **Alex**', mode="md")
                        tgb.image(
                            "<lägg image här>", # image
                            on_action= <länk till athletssida> #
                            class_name = "hover_color picture_style",
                            height= "150px",
                            width= "150px"      
                        )