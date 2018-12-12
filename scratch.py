import json
from pathlib import Path


def json_read(calibration_folder, fileName):
    DataFile = calibration_folder / (fileName)
    with open(DataFile, 'r') as filehandle:
        output = json.load(filehandle)
    return output


out = json_read(Path('./logs'), '20181210-161712_Participant_0.json')
print(out)
