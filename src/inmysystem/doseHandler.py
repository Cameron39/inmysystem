"""
Structure of Dosage

Handling of Dose

Put ALL data here!
"""

from inmysystem.dataRead import JsonFileHandler
from datetime import datetime, timedelta

class doseHandler():
    def __init__(self, appPath):
        self._appPath = appPath
        self.detailDose = []
        self.simpleDose = []
        self.activeTimeDose = []
        self.dataFile = "testInfo.json"

    def getDoseInfo(self):
        JHandler = JsonFileHandler(self._appPath)
        tempdata = JHandler.readData(self.dataFile)

        if (bool(tempdata)):
            self.parseDoseInfo(tempdata)

    def parseDoseInfo(self, jsonData):
        if len(jsonData) == 0: return
        
        for dosage in jsonData:
            self.detailDose.append(dosage) 
            self.simpleDose.append(dosage["Name"])

    def getSimpleDose(self) -> dict:
        return self.simpleDose

    def getDetailDose(self) -> list:
        return self.detailDose
    
    def addActiveDose(self, newDosage):
        newDose = newDosage
        self.activeTimeDose.append(newDose)
        self.activeTimeDose.sort()
        #print(f"Added Dose {newDose}")

    def getActiveDose(self) -> list:
        return self.activeTimeDose

