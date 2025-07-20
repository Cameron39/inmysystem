"""
In My System CSC 470 Final Project
Test Change
TODO:
"""

from datetime import datetime, timedelta
import asyncio
from enum import Enum
import copy
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, Pack
from toga import ImageView, Image, Selection
from toga.sources import ListSource
from inmysystem.doseHandler import DoseHandler


class DoseIcons(Enum):
    """TODO:"""
    ACTIVE = 'resources/active.png'
    HISTORY = 'resources/history.png'
    ADD = 'resources/pilladd.png'


class InMySystem(toga.App):
    """TODO:"""

    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.time_format = "%a at %H:%M:%S"
        self.dose_handler = DoseHandler(self.paths)
        self.dose_handler.load_dose_file()
        self.dose_handler.load_history_file()
        
        self.dtl_cur_list_src = ListSource(
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
                direction=COLUMN
            )
        )

        self.btn_add = toga.Button(
            "Add New Dose",
            on_press= self.dose_get,
            style=Pack(
                margin_top=1, margin_bottom=20, margin_left=20, margin_right=20)
        )

        self.btn_clear = toga.Button(
            "Clear All Data",
            id="clear_all",
            on_press=self.clear_all,
            style=Pack(
                margin_top=1, margin_bottom=5, margin_left=20, margin_right=20)
        )
        
        self.dtl_dose_history = toga.DetailedList(
            missing_value="None",
            data = self.dtl_hst_list_src,
            style=Pack(margin=5)
            )
        
        self.dtl_act_dose = toga.DetailedList(
            missing_value="None",
            data =self.dtl_cur_list_src,
            style=Pack(margin=5)     
        )

        self.lbl_cur_dose = toga.Label(
            text="Current Dose(s)" + "{:>39}".format("Expiration")
        )

        self.lbl_his_dose = toga.Label(
            text="History of Dose(s)" + "{:>32}".format("Expiration"),
            style=Pack(margin_top=10)
        )

        self.divi = toga.Divider()

        self.main_box.add(self.lbl_cur_dose)
        self.main_box.add(self.dtl_act_dose)
        self.main_box.add(self.btn_add)
        self.main_box.add(self.divi)
        self.main_box.add(self.lbl_his_dose)
        self.main_box.add(self.dtl_dose_history)
        self.main_box.add(self.btn_clear)
        self.load_history_data()

        self.main_window = toga.MainWindow(
            title=self.formal_name, size=(400,300))
        self.main_window.content = self.main_box
        self.main_window.show()

    async def clear_all(self, widget):
        """TODO:"""
        user_answer = toga.ConfirmDialog("Please Confirm",
            "Please confirm you want ALL DATA removed")
        message = ""

        if await self.main_window.dialog(user_answer):
            if widget.id == "clear_all": 
                self.dose_handler.clear_file(self.dose_handler.history_file)
                message = "Completed"
                self.dtl_hst_list_src.clear()
                self.dtl_cur_list_src.clear()
        else:
            message = "Aborted"
            
        if await self.main_window.dialog(toga.InfoDialog(message, message)):
            return
        
    async def dose_get(self, widget):
        """TODO:"""
        dialog = DoseDialog(self.dose_handler)
        dialog.show()
        result = await dialog
        yes_continue = await self.check_if_dose_is_active(result)
        if yes_continue:
            self.add_new_dose(result)
            await self.check_dose_time()
            
    def listsource_add(
            self, the_list_source : ListSource, 
            the_dict : dict, type: DoseIcons):
        """TODO:"""
        try:
            if isinstance(the_dict['Expire'], datetime):
                new_time = the_dict['Expire'].strftime(self.time_format)
            else:
                new_time = datetime.fromisoformat(the_dict['Expire']).strftime(
                    self.time_format)
        except Exception as e:
            raise Exception(f"Unexpected error extracting time: {e}")
        
        the_list_source.append({
            "icon": toga.Icon(type.value),
            "title": the_dict['Name'] + " - " + the_dict['Dose'],
            "subtitle": new_time
        })

    def load_history_data(self):
        if (bool(self.dose_handler.history_dose)):
            current_time = datetime.now()
            for dose in self.dose_handler.history_dose:
                expire_time = datetime.fromisoformat(dose['Expire'])
                if current_time < expire_time:
                    self.listsource_add(self.dtl_cur_list_src, dose, 
                        DoseIcons.ACTIVE)   
                self.listsource_add(self.dtl_hst_list_src, dose, 
                        DoseIcons.HISTORY)

    async def check_if_dose_is_active(self, new_dose_name : str) -> bool:
        """ TODO: """
        temp_find = (' '.join([str(s) for s in self.dtl_cur_list_src])).find(
            new_dose_name)

        if temp_find == -1:
            return True
        else:
            user_answer = toga.ConfirmDialog(
                title="Warning!",
                message="Dose already in your system!\n" \
                "Are you SURE?"
            )
            if await self.dialog(user_answer):
                return True
            else:
                return False
    
    def add_new_dose(self, nextDose):
        """TODO:"""
        detailed_dose = copy.deepcopy(self.dose_handler.src_dose_all)
        new_dose = next(filter(
            lambda v: v['Name'] == nextDose, detailed_dose
            ), None)
        active_min = (float)(new_dose['ActiveMinutes'])
        current_time = datetime.now()
        expire_time = current_time + timedelta(minutes=active_min)

        new_dose['Expire'] = expire_time

        self.listsource_add(self.dtl_cur_list_src, new_dose, DoseIcons.ACTIVE)
        self.listsource_add(self.dtl_hst_list_src, new_dose, DoseIcons.HISTORY)

        self.dose_handler.history_dose.append({
            "Name": new_dose['Name'],
            "Dose": new_dose['Dose'],
            "Expire": expire_time.isoformat()
        })

        self.dose_handler.write_to_history()
        self.dose_handler.add_active_time_dose(expire_time)

    async def check_dose_time(self):
        """TODO:"""
        interval_seconds = 20

        while True:
            if self.dose_handler.current_dose_times:
                current_time = datetime.now()
                if current_time > self.dose_handler.current_dose_times[0]:
                    try:
                        time_remove = (
                            self.dose_handler.current_dose_times[0]).strftime(
                                self.time_format)
                        to_remove = self.dtl_cur_list_src.find(
                            {"subtitle": time_remove})
                        self.dtl_cur_list_src.remove(to_remove)
                        del self.dose_handler.current_dose_times[0]
                    except Exception as e:
                        raise Exception(
                            f"Unexpected error while removing from \
                            activeList {e}")
            await asyncio.sleep(interval_seconds)


class DoseDialog(toga.Window):
    """Pop-up dialog for getting the dose to add! TODO:"""

    def __init__(self, dosageHandler):
        super().__init__(title="Add Dose", resizable=False, size=(400, 200))
        self._dose_handler = dosageHandler
        self.add_icon = toga.Icon(DoseIcons.ADD.value)

        self.dose_info_src = ListSource( 
            accessors=("icon","title","subtitle"),
            data=[]
        )

        self.selection_dose = toga.Selection(
            style=Pack(margin=5),
            items = self._dose_handler.src_dose_names,
            on_change=self.fill_dose_info
        )

        self.dlt_dose_info = toga.DetailedList(
            style=Pack(margin=5),
            data=self.dose_info_src
            )
        
        self.lbl_add_dose = toga.Label(
            style=Pack(margin=5),
            text="Select a Dose"
        )

        self.btn_okay = toga.Button("Add Dose", on_press=self.on_accept,
            style=Pack(margin=5)
            )
        self.content = toga.Box(
            style=Pack(direction=COLUMN, flex=1, margin=5),
            children=[
                self.lbl_add_dose,
                self.selection_dose,
                self.dlt_dose_info,
                self.btn_okay 
                ]
            )
        self.future = self.app.loop.create_future()
        self.fill_dose_info(self.selection_dose)

    def on_accept(self, widget, **kwargs):
        self.future.set_result(self.selection_dose.value)
        self.close()

    def __await__(self):
        return self.future.__await__()
    
    def fill_dose_info(self, widget):
        """TODO:"""
        next_dose = self.selection_dose.value
        detailed_dose = copy.deepcopy(self._dose_handler.src_dose_all)
        new_dose = next(filter(
            lambda v: v['Name'] == next_dose, detailed_dose
            ), None)
        self.dose_info_src.clear()
        for key,item in new_dose.items():
            self.dose_info_src.append({
                "icon": self.add_icon,
                "title": key,
                "subtitle": item
            })

def main():
    return InMySystem()
