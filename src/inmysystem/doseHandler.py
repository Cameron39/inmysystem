"""
Structure of Dosage

Handling of Dose

Put ALL data here!
"""

from inmysystem.dataRead import JsonFileHandler

class doseHandler():
    def __init__(self, appPath):
        self._appPath = appPath
        self.detailDose = detailDose = []
        self.simpleDose = simpleDose = []
        self.activeDose = activeDose = []
        self.dataFile = "testInfo.json"

    def getDoseInfo(self):
        pass

    def parseDoseInfo(self, jsonData):
        if len(jsonData) == 0: return
        
        for dosage in jsonData:
            self.detailDose.append(dosage) 
            self.simpleDose.append(dosage["Name"])

    def getSimpleDose(self):
        pass

    def getDetailDose(self):
        pass
    
    async def checkActiveDose(self):
        pass

