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
        self.time_format = "%a at %H:%M:%S"
        self.dose_handler = doseHandler(self.paths)
        self.dose_handler.loadDoseInfo()

        self.dtl_cur_list_src = ListSource( # THIS WORKS!
            accessors=("icon","title","subtitle"),
            data=[]
        )

        self.dtl_hst_list_src = ListSource(
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
        
        self.dose_history = toga.DetailedList(
            missing_value="None",
            data = self.dtl_hst_list_src
            )
        
        self.dose_list = toga.DetailedList(
            missing_value="WHAT",
            data =self.dtl_cur_list_src     
        )
        self.main_box.add(self.add_button)
        self.main_box.add(self.dose_list)
        self.main_box.add(self.dose_history)
        

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()
        
    def btn_testing(self, widget):
        pass

    async def doseInput(self, widget):
        dialog = doseDialog(self.dose_handler)
        dialog.show()
        result = await dialog
        #self.dose_info.value = result
        self.addNewDose(result)
        await self.checkTime()

    def addNewDose(self, nextDose):
        detailedDose = self.dose_handler.src_dose_all
        newDose = next(filter(lambda v: v['Name'] == nextDose, detailedDose), None)
        activeMin = (int)(newDose['ActiveTime'])
        currentTime = datetime.now()
        expireTime = currentTime + timedelta(minutes=activeMin)
        # self.activeList.append({
        #     "icon": toga.Icon.DEFAULT_ICON,
        #     "title": newDose['Name'] + " - " + newDose['Dose'],
        #     "subtitle": expireTime.strftime(self.timeFormat)
        # })

        tempDict = {
            "icon": toga.Icon.DEFAULT_ICON,
            "title": newDose['Name'] + " - " + newDose['Dose'],
            "subtitle": expireTime.strftime(self.time_format)
        }

        
        self.dose_handler.addActiveTimeDose(expireTime)
        #print(newDose)
        #print(self.doseHandler.getActiveDose())

    async def checkTime(self):
        interval_seconds = 20

        while True:
            print("Checking...")
            if self.dose_handler.current_dose_times:
                currTime = datetime.now()
                if currTime > self.dose_handler.current_dose_times[0]:
                    try:
                        timeRemove = (self.dose_handler.current_dose_times[0]).strftime(self.time_format)
                        toRemove = self.dtl_cur_list_src.find({"subtitle": timeRemove})
                        
                        self.dtl_cur_list_src.remove(toRemove)
                        # self.historyList.append({
                        #     "icon": toRemove["icon"],
                        #     "title": toRemove["title"],
                        #     "subtitle": toRemove["subtitle"]
                        # })
                        # self.historyList.append(toRemove)
                        del self.dose_handler.current_dose_times[0]
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

        self.doseInfo = ListSource( 
            accessors=("icon","title","subtitle"),
            data=[

            ]
        )

        self.selection = toga.Selection(
            style=Pack(margin=5),
            items = self._doseHandler.src_dose_names,
            on_change=self.updateList,
        )

        self.doseInfoDtlList = toga.DetailedList(
            style=Pack(margin=5),
            data=self.doseInfo
            )

        self.ok_button = toga.Button("Add Dose", on_press=self.on_accept,
            style=Pack(margin=5)
            )
        self.content = toga.Box(
            style=Pack(direction=COLUMN, flex=1, margin=5),
            children=[
                self.selection,
                self.doseInfoDtlList,
                self.ok_button, 
                ]
            )
        self.future = self.app.loop.create_future()
        self.updateList(self.selection)

    def on_accept(self, widget, **kwargs):
        self.future.set_result(self.selection.value)
        self.close()

    def __await__(self):
        return self.future.__await__()
    
    def updateList(self, widget):
        nextDose = self.selection.value
        detailedDose = self._doseHandler.src_dose_all
        newDose = next(filter(lambda v: v['Name'] == nextDose, detailedDose), None)
        self.doseInfo.clear()
        for key,item in newDose.items():
            self.doseInfo.append({
                "icon": toga.Icon.DEFAULT_ICON,
                "title": key,
                "subtitle": item
            })



def main():
    return InMySystem()
