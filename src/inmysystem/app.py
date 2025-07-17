"""
In My System CSC 470 Final Project
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, Pack
from toga import ImageView, Image, Selection
from toga.sources import ListSource, Listener
from inmysystem.dataRead import JsonFileHandler


class InMySystem(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.jsonHandler = JsonFileHandler(self.paths)
        # jsonData = self.jsonFileHanlder.readData("testInfo.json")
        jsonData = self.jsonHandler.readTestFile()

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
            on_press= self.doseInput,
            margin=5,
        )
        
        # print(f"Value: {item}")
        self.dose_info = toga.MultilineTextInput(readonly=True,
            placeholder="Future Information",
            value=jsonData,
            flex=1,
            margin=5)
        
        self.dose_list = toga.DetailedList(
            missing_value="WHAT",
            data =self.initialData
            
        )
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

    async def doseInput(self, widget):
        dialog = doseDialog(self.jsonHandler)
        dialog.show()
        result = await dialog
        self.dose_info.value = result
        self.addNewDose(result)

    def addNewDose(self, nextDose):
        detailedDose = self.jsonHandler.getDetailDose()
        newDose = next(filter(lambda v: v['Name'] == nextDose, detailedDose), None)
        self.initialData.append({
            "icon": toga.Icon.DEFAULT_ICON,
            "title": newDose['Name'],
            "subtitle": newDose['Dose']
        })
        print(newDose)

"""
Pop-up dialog for getting the dose to add!
"""
class doseDialog(toga.Window):
    def __init__(self, JsonFileHandler):
        super().__init__(title="Add Dose", resizable=False, size=(400, 300))
        self.jsonDataHandler = JsonFileHandler

        print(self.jsonDataHandler.getSimpleDose())

        self.textinput = toga.TextInput()
        self.selection = toga.Selection(
            #items=["Test1", "Test2"]
            items = self.jsonDataHandler.getSimpleDose()
        )
        self.ok_button = toga.Button("OK", on_press=self.on_accept)
        self.content = toga.Box(children=[self.textinput, self.ok_button, self.selection])
        self.future = self.app.loop.create_future()

    def on_accept(self, widget, **kwargs):
        self.future.set_result(self.selection.value)
        self.close()

    def __await__(self):
        return self.future.__await__()


def main():
    return InMySystem()
