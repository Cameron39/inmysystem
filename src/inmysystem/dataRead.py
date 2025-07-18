import json
import pprint
from pathlib import Path
from datetime import datetime

class JsonFileHandler:

    def __init__(self, app_paths):
        self._app_paths = app_paths
        self._jsonData = jsonData = ""
        self.history_file = "history.json"

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

    def write_dose_history(self, dose_history):
        file_with_path = self._app_paths.app / "resources" / self.history_file

        try:
            history_json = json.dumps(dose_history, indent=2)
            print(history_json)
            file_with_path.write_text(history_json)
        except Exception as e:
            raise Exception(f"Unexpected error while writing to {file_with_path}: {e}")

    def makeJSONPretty(self, jsonData: dict) ->str:
        return pprint.pformat(jsonData, sort_dicts=False)
    