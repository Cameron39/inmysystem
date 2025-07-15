import json
from pathlib import Path

class JsonFileHandler:
    def __init__(self, app_paths):
        self._app_paths = app_paths

        # print(f"JsonFileHandler initialized with path base: {self._app_paths.app}")

    def readTestFile(self) -> dict:
        testFile = "testInfo.json"

        # fileName = app_path \ "resources" \ testFile
        full_path = self._app_paths.app / "resources" / testFile
        fileName = full_path

        if not fileName.exists():
            raise FileNotFoundError(f"File Not Found: {fileName}")

        try:
            json_text = fileName.read_text(encoding="utf-8")
            json_data = json.loads(json_text)
            return json_data
            
        except json.JSONDecodeError:
            raise json.JSONDecoder(f"Error with JSON decoding: {fileName}")
        except Exception as e:
            raise Exception(f"Unexpected error while reading {fileName}")
    