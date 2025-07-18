"""
In My System CSC 470 Final Project
Test Change
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, Pack
from toga import ImageView, Image, Selection
from toga.sources import ListSource
from inmysystem.doseHandler import doseHandler
from datetime import datetime, timedelta
import asyncio

class InMySystem(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.timeFormat = "%a at %H:%M:%S"
        self.doseHandler = doseHandler(self.paths)
        self.doseHandler.getDoseInfo()

        self.activeList = ListSource( # THIS WORKS!
            accessors=("icon","title","subtitle"),
            data=[]
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
        
        self.dose_info = toga.MultilineTextInput(readonly=True,
            placeholder="Future Information",
            flex=1,
            margin=5)
        
        self.dose_list = toga.DetailedList(
            missing_value="WHAT",
            data =self.activeList     
        )
        self.main_box.add(self.add_button)
        self.main_box.add(self.dose_info)
        self.main_box.add(self.dose_list)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()
        
    def btn_testing(self, widget):
        pass

    async def doseInput(self, widget):
        dialog = doseDialog(self.doseHandler)
        dialog.show()
        result = await dialog
        #self.dose_info.value = result
        self.addNewDose(result)
        await self.checkTime()

    def addNewDose(self, nextDose):
        # TODO: Add the day? 
        detailedDose = self.doseHandler.getDetailDose()
        newDose = next(filter(lambda v: v['Name'] == nextDose, detailedDose), None)
        activeMin = (int)(newDose['ActiveTime'])
        currentTime = datetime.now()
        expireTime = currentTime + timedelta(minutes=activeMin)
        self.activeList.append({
            "icon": toga.Icon.DEFAULT_ICON,
            "title": newDose['Name'] + " - " + newDose['Dose'],
            "subtitle": expireTime.strftime(self.timeFormat)
        })
        self.doseHandler.addActiveDose(expireTime)
        #print(newDose)
        #print(self.doseHandler.getActiveDose())

    async def checkTime(self):
        interval_seconds = 20

        while True:
            print("Checking...")
            if self.doseHandler.activeTimeDose:
                currTime = datetime.now()
                if currTime > self.doseHandler.activeTimeDose[0]:
                    try:
                        timeRemove = (self.doseHandler.activeTimeDose[0]).strftime(self.timeFormat)
                        toRemove = self.activeList.find({"subtitle": timeRemove})
                        self.activeList.remove(toRemove)
                    except Exception as e:
                        raise Exception(f"Unexpected error while removing from activeList {e}")
            await asyncio.sleep(interval_seconds)

"""
Pop-up dialog for getting the dose to add!
"""
class doseDialog(toga.Window):
    def __init__(self, dosageHandler):
        super().__init__(title="Add Dose", resizable=False, size=(400, 300))
        self._doseHandler = dosageHandler

        self.selection = toga.Selection(
            items = self._doseHandler.getSimpleDose()
            on_change=self.updateList
        )

        self.infoTable = toga.Table(
            headings=["Name", "NickName", "Dose", "ActiveTime", "Notes"],
            data=[]
        )
        self.ok_button = toga.Button("OK", on_press=self.on_accept)
        self.content = toga.Box(
            style=Pack(direction=COLUMN, flex=1),
            children=[
                self.selection,
                self.infoTable,
                self.ok_button, 
                ]
            )
        self.future = self.app.loop.create_future()

    def on_accept(self, widget, **kwargs):
        self.future.set_result(self.selection.value)
        self.close()

    def __await__(self):
        return self.future.__await__()
    
    def updateList(self):
        pass

    def fillTable(self):
        full_list = self._doseHandler.getDetailDose()


def main():
    return InMySystem()
