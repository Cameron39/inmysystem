"""
This is the logic layer that handles the manipulation of the core data.
It is used to separate the GUI layer and the file manipulation layer.
"""

from inmysystem.dataRead import JsonFileHandler


class DoseHandler():
    """
    Handles the core data storage, loading from file, writing to file, and data
        clearing.
    Parses the loaded data into the core data storage for dose and history.
    """

    def __init__(self, appPath):
        self._app_Path = appPath
        self.src_dose_all = []
        self.src_dose_names = []
        self.current_dose_times = []
        self.history_dose = []
        self.dose_file = "doseinfo.json"
        self.history_file = "history.json"
        self.json_handler = JsonFileHandler(self._app_Path)

    def load_dose_file(self):
        temp_data = self.json_handler.read_dose_data(self.dose_file)

        if (bool(temp_data)):
            self._parse_dose_info(temp_data)

    def load_history_file(self):
        temp_data = self.json_handler.read_dose_data(self.history_file)

        if (bool(temp_data)):
            self._parse_dose_history(temp_data)

    def _parse_dose_info(self, json_data):
        if len(json_data) == 0: return
        
        for dosage in json_data:
            self.src_dose_all.append(dosage) 
            self.src_dose_names.append(dosage["Name"])

    def _parse_dose_history(self, json_data):
        if len(json_data) == 0: return

        for dosage in json_data:
            self.history_dose.append(dosage)
    
    def add_active_time_dose(self, new_dosage):
        new_dose = new_dosage
        self.current_dose_times.append(new_dose)
        self.current_dose_times.sort()

    def write_to_history(self):
        self.json_handler.write_dose_history(self.history_dose, self.history_file)

    def clear_file(self, filename):
        self.json_handler.truncate_file(file2truncate=filename)
        