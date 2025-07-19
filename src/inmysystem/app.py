"""
In My System CSC 470 Final Project
Test Change
"""

import toga
# import toga.icons
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
        # icon_path = self.paths.app / "icons" / "active_dose.ico"
        print(self.paths.app.absolute)
        print(self.paths)
        self.time_format = "%a at %H:%M:%S"
        self.dose_handler = doseHandler(self.paths)
        # self.default_icon = toga.Icon('resource/history.png')
        self.active_icon = toga.Icon('resources/active.png')
        self.history_icon = toga.Icon('resources/history.png')
        self.dose_handler.loadDoseFile()
        self.dose_handler.loadHistoryFile()
        

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
            ),
        )

        self.add_button = toga.Button(
            "Add New Dose",
            on_press= self.doseInput,
            style=Pack(margin_top=1, margin_bottom=20, margin_left=20, margin_right=20),
        )

        self.clear_history = toga.Button(
            "Clear All History",
            id="clear_history",
            on_press=self.clear_file,
            style=Pack(margin_top=1, margin_bottom=5, margin_left=20, margin_right=20)
        )
        
        self.dose_history = toga.DetailedList(
            missing_value="None",
            data = self.dtl_hst_list_src,
            style=Pack(margin=5)
            )
        
        self.dose_list = toga.DetailedList(
            missing_value="None",
            data =self.dtl_cur_list_src,
            style=Pack(margin=5)     
        )

        self.lbl_cur_dose = toga.Label(
            text="Current Dose(s)"
        )

        self.lbl_his_dose = toga.Label(
            text="History of Dose(s)",
            style=Pack(margin_top=10)
        )

        self.divi = toga.Divider()

        self.main_box.add(self.lbl_cur_dose)
        self.main_box.add(self.dose_list)
        self.main_box.add(self.add_button)
        self.main_box.add(self.divi)
        self.main_box.add(self.lbl_his_dose)
        self.main_box.add(self.dose_history)
        self.main_box.add(self.clear_history)
        self.loadHistoryData()

        self.main_window = toga.MainWindow(title=self.formal_name, size=(400,300))
        self.main_window.content = self.main_box
        self.main_window.show()
        
    def btn_testing(self, widget):
        pass

    async def clear_file(self, widget):
        user_answer = toga.ConfirmDialog("Please Confirm","Please confirm you want the history file emptied")
        message = ""

        if await self.main_window.dialog(user_answer):
            #print("Confirmed")
            if widget.id == "clear_history": 
                self.dose_handler.clearFile(self.dose_handler.history_file)
                message = "Completed"
                self.dtl_hst_list_src.clear()
        else:
            #print("Denied")
            message = "Aborted"
            
        if await self.main_window.dialog(toga.InfoDialog(message, message)):
            return
        

    async def doseInput(self, widget):
        dialog = doseDialog(self.dose_handler)
        dialog.show()
        result = await dialog
        self.addNewDose(result)
        await self.checkTime()

    def addToListSource(self, the_list_source : ListSource, the_dict : dict):
            the_list_source.append({
                "icon": self.active_icon,
                "title": the_dict['Name'] + " - " + the_dict['Dose'],
                "subtitle": datetime.fromisoformat(the_dict['Expire']).strftime(self.time_format)
            })

    def loadHistoryData(self):
        if (bool(self.dose_handler.history_dose)):
            current_time = datetime.now()
            for dose in self.dose_handler.history_dose:
                expire_time = datetime.fromisoformat(dose['Expire'])
                if current_time > expire_time:
                    self.addToListSource(self.dtl_hst_list_src, dose)
                else:
                    self.addToListSource(self.dtl_cur_list_src, dose)

    def addNewDose(self, nextDose):
        detailedDose = self.dose_handler.src_dose_all
        newDose = next(filter(lambda v: v['Name'] == nextDose, detailedDose), None)
        activeMin = (int)(newDose['ActiveTime'])
        currentTime = datetime.now()
        expireTime = currentTime + timedelta(minutes=activeMin)

        self.dtl_cur_list_src.append({
            "icon": self.active_icon,
            "title": newDose['Name'] + " - " + newDose['Dose'],
            "subtitle": expireTime.strftime(self.time_format)
        })

        self.dtl_hst_list_src.append({
            "icon": self.history_icon,
            "title": newDose['Name'] + " - " + newDose['Dose'],
            "subtitle": expireTime.strftime(self.time_format)
        })

        self.dose_handler.history_dose.append({
            "Name": newDose['Name'],
            "Dose": newDose['Dose'],
            "Expire": expireTime.isoformat()
        })
        self.dose_handler.writeHistory()
        self.dose_handler.addActiveTimeDose(expireTime)

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
                        toRemInd = self.dtl_cur_list_src.index(toRemove)
                        to_history = self.dtl_cur_list_src.__getitem__(toRemInd)
                        self.dtl_cur_list_src.remove(toRemove)
                        del self.dose_handler.current_dose_times[0]
                    except Exception as e:
                        raise Exception(f"Unexpected error while removing from activeList {e}")
            await asyncio.sleep(interval_seconds)

"""
Pop-up dialog for getting the dose to add!
"""
class doseDialog(toga.Window):
    def __init__(self, dosageHandler):
        super().__init__(title="Add Dose", resizable=False, size=(400, 200))
        self._doseHandler = dosageHandler
        self.active_icon = toga.Icon('resources/pilladd.png')

        self.doseInfo = ListSource( 
            accessors=("icon","title","subtitle"),
            data=[]
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
                "icon": self.active_icon,
                "title": key,
                "subtitle": item
            })

def main():
    return InMySystem()
