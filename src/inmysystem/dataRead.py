import json
import pprint
from pathlib import Path

class JsonFileHandler:
    def __init__(self, app_paths):
        self._app_paths = app_paths
        self._jsonData = jsonData = ""

        # print(f"JsonFileHandler initialized with path base: {self._app_paths.app}")
        
    def read_dose_data(self, file2Read) -> dict:
        file_with_path = self._app_paths.app / "resources" / file2Read
        # print(f"File2Read in use with file: {file2Read} and {fileWithPath}")

        if not file_with_path.exists():
            raise FileNotFoundError(f"File Not Found: {file_with_path}")
        try:
            json_text = file_with_path.read_text(encoding="utf-8")
            self._jsonData = json.loads(json_text)
            return self._jsonData     
        except json.JSONDecodeError:
            raise json.JSONDecoder(f"Error with JSON decoding: {file_with_path}")
        except Exception as e:
            raise Exception(f"Unexpected error while reading {file_with_path}")



    def makeJSONPretty(self, jsonData: dict) ->str:
        return pprint.pformat(jsonData, sort_dicts=False)
    