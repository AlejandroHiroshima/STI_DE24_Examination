import taipy.gui.builder as tgb

with tgb.Page() as alex:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Choose exercise type", mode="md")


    with tgb.part():
        with tgb.part(class_name="text-center card-margin"):
            with tgb.part(class_name="card card-margin"):
                with tgb.layout(columns=("1 1")):
                    with tgb.part():
                        tgb.text("### Strength", mode="md")
                        tgb.image(
                            "image här", # lägg till passande strength bild
                            on_action= <nästa steg>, #
                            class_name= "hover_color picture_style",
                            height="150px",
                            width="150px"
                        )
                    
                    with tgb.part():
                        tgb.text("### Cardio", mode="md")
                        tgb.image(
                            "image här", # lägg till passande cardio bild
                            on_action= <nästa steg>, #
                            class_name=" hover_color picture_style",
                            height= "150px",
                            width= "150px"
                        )
