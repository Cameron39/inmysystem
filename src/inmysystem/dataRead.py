import json

def readTestFile():
    testFile = "testInfo.json"

    try:
        pass
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass
    except Exception as e:
        pass
    