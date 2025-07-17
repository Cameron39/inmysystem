import json
import pprint
from pathlib import Path

class JsonFileHandler:
    def __init__(self, app_paths):
        self._app_paths = app_paths
        self._detailDose = _doseData = []
        self._simpleDose = _simpleDose = []
        self._jsonData = jsonData = ""

        # print(f"JsonFileHandler initialized with path base: {self._app_paths.app}")

    def readTestFile(self) -> dict:
        testFile = "testInfo.json"
        return self.readData(testFile)
        
    def readData(self, file2Read) -> dict:
        fileWithPath = self._app_paths.app / "resources" / file2Read

        # print(f"File2Read in use with file: {file2Read} and {fileWithPath}")

        if not fileWithPath.exists():
            raise FileNotFoundError(f"File Not Found: {fileWithPath}")
        try:
            jsonText = fileWithPath.read_text(encoding="utf-8")
            jsonData = json.loads(jsonText)
            #jsonData = json.loads(jsonText, object_hook=SimpleNamespace)
            print("Here1")
            self.parseData(jsonData)
            return jsonData     
        except json.JSONDecodeError:
            raise json.JSONDecoder(f"Error with JSON decoding: {fileWithPath}")
        except Exception as e:
            raise Exception(f"Unexpected error while reading {fileWithPath}")
        
    def parseData(self, jsonData):
        if len(jsonData) == 0: return
        
        for dosage in jsonData:
            self._detailDose.append(dosage) 
            self._simpleDose.append(dosage["Name"])

        # print(self._doseData)

    def getSimpleDose(self) -> dict:
        return self._simpleDose
    
    def getDetailDose(self) -> list:
        return self._detailDose

        
    def makeJSONPretty(self, jsonData: dict) ->str:
        # return json.dumps(jsonData, indent=4)
        # return pprint.pprint(jsonData, sort_dicts=False)
        return pprint.pformat(jsonData, sort_dicts=False)
    