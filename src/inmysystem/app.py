"""
In My System CSC 470 Final Project
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, Pack
from toga import ImageView, Image


class InMySystem(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(
            style=Pack(
                margin=5,
                align_items=CENTER,
                direction=COLUMN,
                width = 435,
                height = 640,
            )
        )

        add_button = toga.Button(
            "Add Dose",
            on_press= self.add_dose,
            margin=5,
        )
        

        # bck_image = toga.ImageView(toga.Image('./resources/background2.png'),
        #                            style=Pack(flex=1,
        #                            align_items=CENTER,
        #                            width = 435,
        #                            height = 640,)
        #                            )
        # main_box.add(bck_image)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def add_dose(self):
        pass

def main():
    return InMySystem()
