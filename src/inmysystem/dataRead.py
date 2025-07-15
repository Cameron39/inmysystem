import json
from pathlib import Path

class JsonFileHandler:
    def __init__(self, app_paths):
        self._app_paths = app_paths

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
            return jsonData     
        except json.JSONDecodeError:
            raise json.JSONDecoder(f"Error with JSON decoding: {fileWithPath}")
        except Exception as e:
            raise Exception(f"Unexpected error while reading {fileWithPath}")
        
    def makeJSONPretty(self, jsonData: dict) ->str:
        return json.dumps(jsonData, indent=2)
    