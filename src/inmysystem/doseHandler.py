"""
Structure of Dosage

Handling of Dose

Put ALL data here!
"""

from inmysystem.dataRead import JsonFileHandler
from datetime import datetime, timedelta

class doseHandler():
    def __init__(self, appPath):
        self._app_Path = appPath
        self.src_dose_all = []
        self.src_dose_names = []
        self.current_dose_times = []
        self.history_dose = []
        self.data_file = "testInfo.json"
        self.JHandler = JsonFileHandler(self._app_Path)

    def loadDoseInfo(self):
        temp_data = self.JHandler.read_dose_data(self.data_file)

        if (bool(temp_data)):
            self._parseDoseInfo(temp_data)

    def _parseDoseInfo(self, jsonData):
        if len(jsonData) == 0: return
        
        for dosage in jsonData:
            self.src_dose_all.append(dosage) 
            self.src_dose_names.append(dosage["Name"])

    # def getSimpleDose(self) -> dict:
    #     return self.src_dose_names

    def getDetailDose(self) -> list:
        return self.src_dose_all
    
    def addActiveTimeDose(self, new_dosage):
        new_dose = new_dosage
        self.current_dose_times.append(new_dose)
        self.current_dose_times.sort()
        #print(f"Added Dose {newDose}")

    def getActiveDose(self) -> list:
        return self.current_dose_times

    def writeHistory(self):
        self.JHandler.write_dose_history(self.history_dose)