"""
In My System CSC 470 Final Project
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, Pack
from toga import ImageView, Image
from toga.sources import ListSource, Listener
from inmysystem.dataRead import JsonFileHandler


class InMySystem(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.jsonFileHanlder = JsonFileHandler(self.paths)
        # jsonData = self.jsonFileHanlder.readData("testInfo.json")
        jsonData = self.jsonFileHanlder.readTestFile()

        self.initialData = ListSource( # THIS WORKS!
            data=[
                {
                    "icon": toga.Icon.DEFAULT_ICON,
                    "title": "Arthur Dent",
                    "subtitle": "Where's the tea?"
                },
                {
                    "icon": toga.Icon.DEFAULT_ICON,
                    "title": "Ford Prefect",
                    "subtitle": "Do you know where my towel is?"
                },
                {
                    "icon": toga.Icon.DEFAULT_ICON,
                    "title": "Tricia McMillan",
                    "subtitle": "What planet are you from?"
                },
            ],
            accessors=["icon","title","subtitle"]
        )

        self.main_box = toga.Box(
            style=Pack(
                margin=20,
                align_items=CENTER,
                direction=COLUMN,
                # width = 435,
                # height = 640,
            )
        )

        self.add_button = toga.Button(
            "Add Dose",
            on_press= self.add_dose,
            margin=5,
        )
        
        # print(f"Value: {item}")
        self.dose_info = toga.MultilineTextInput(readonly=True,
            # placeholder="Future Information",
            value=self.initialData,
            flex=1,
            margin=5)
        
        self.dose_list = toga.DetailedList(
            missing_value="WHAT",
            data =self.initialData
            
        )
        
    #     self.dose_list = toga.DetailedList(
    #         accessors=("Name", "Nickname", "Dose", "ActiveTime", "Notes"),
    #         data=self.jsonFileHanlder.makeJSONPretty(jsonData),
    #         missing_value="MISSING",
    # #         [
    # #     {
    # #         "icon": toga.Icon.DEFAULT_ICON,
    # #         "title": "Arthur Dent",
    # #         "subtitle": "Where's the tea?"
    # #     },
    # #     {
    # #         "icon": toga.Icon.DEFAULT_ICON,
    # #         "title": "Ford Prefect",
    # #         "subtitle": "Do you know where my towel is?"
    # #     },
    # #     {
    # #         "icon": toga.Icon.DEFAULT_ICON,
    # #         "title": "Tricia McMillan",
    # #         "subtitle": "What planet are you from?"
    # #     },
    # # ]
    #     )

        # self.doseTable = toga.Table(
        #     headings=["Name", "Nickname", "Dose", "ActiveTime", "Notes"],
        #     accessors={"Name", "Nickname", "Dose", "ActiveTime", "Notes"},
        #     data=self.jsonFileHanlder.makeJSONPretty(jsonData),
        #     missing_value="NONE",
        # )

        # self.dose_info.value = jsonData
        # bck_image = toga.ImageView(toga.Image('./resources/background2.png'),
        #                            style=Pack(flex=1,
        #                            align_items=CENTER,
        #                            width = 435,
        #                            height = 640,)
        #                            )
        # main_box.add(bck_image)
        self.main_box.add(self.add_button)
        self.main_box.add(self.dose_info)
        self.main_box.add(self.dose_list)
        # self.main_box.add(self.doseTable)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()


    def add_dose(self, widget):
        toRemove = self.initialData.find({"title": "Ford Prefect"})
        self.initialData.remove(toRemove)
    


def main():
    return InMySystem()
