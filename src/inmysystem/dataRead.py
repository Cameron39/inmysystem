import json
import pprint
from pathlib import Path

class JsonFileHandler:
    def __init__(self, app_paths):
        self._app_paths = app_paths
        self._jsonData = jsonData = ""

        # print(f"JsonFileHandler initialized with path base: {self._app_paths.app}")
        
    def readData(self, file2Read) -> dict:
        fileWithPath = self._app_paths.app / "resources" / file2Read
        # print(f"File2Read in use with file: {file2Read} and {fileWithPath}")

        if not fileWithPath.exists():
            raise FileNotFoundError(f"File Not Found: {fileWithPath}")
        try:
            jsonText = fileWithPath.read_text(encoding="utf-8")
            self._jsonData = json.loads(jsonText)
            return self._jsonData     
        except json.JSONDecodeError:
            raise json.JSONDecoder(f"Error with JSON decoding: {fileWithPath}")
        except Exception as e:
            raise Exception(f"Unexpected error while reading {fileWithPath}")
        finally:
            pass #TODO: CLOSE reference to file?

    def makeJSONPretty(self, jsonData: dict) ->str:
        return pprint.pformat(jsonData, sort_dicts=False)
    