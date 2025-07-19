import json
import pprint
import datetime
from pathlib import Path
from json import JSONEncoder

# class DateTimeEncoder(JSONEncoder):
#     def default(self, o):
#         if isinstance(o, (datetime.datetime)):
#             return o.isoformat
#         return super().default(o)

class JsonFileHandler:

    def __init__(self, app_paths):
        self._app_paths = app_paths
        self._jsonData = jsonData = ""

        # print(f"JsonFileHandler initialized with path base: {self._app_paths.app}")
        
    def read_dose_data(self, file2Read : str) -> dict:
        file_with_path = self._app_paths.app / "resources" / file2Read
        print(f"File2Read in use with file: {file2Read} and {file_with_path}")

        if not file_with_path.exists():
            raise FileNotFoundError(f"File Not Found: {file_with_path}")
        if file_with_path.stat().st_size == 0:
            print(f"File {file2Read} is empty")
            return []
        try:
            json_text = file_with_path.read_text(encoding="utf-8")
            self._jsonData = json.loads(json_text)
            return self._jsonData     
        except json.JSONDecodeError:
            raise json.JSONDecoder(f"Error with JSON decoding: {file_with_path}")
        except Exception as e:
            raise Exception(f"Unexpected error while reading {file_with_path}: {e}")

    def write_dose_history(self, dose_history, file2Write):
        file_with_path = self._app_paths.app / "resources" / file2Write

        try:
            history_json = json.dumps(dose_history, indent=4)
            print(history_json)
            file_with_path.write_text(history_json)
        except Exception as e:
            raise Exception(f"Unexpected error while writing to {file_with_path}: {e}")

    def makeJSONPretty(self, jsonData: dict) ->str:
        return pprint.pformat(jsonData, sort_dicts=False)
    