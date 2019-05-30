from psychopy import monitors
import json
from pathlib import Path


def json_write(data_folder, data, namelist):
    file_to_open = Path(data_folder / (namelist + '.json'))
    with open(file_to_open, 'w') as filehandle:
        json.dump(data, filehandle)
# Main Dell 4k monitor


my_monitor = monitors.Monitor(name='my_monitor_name')
my_monitor.setSizePix((1280, 800))
my_monitor.setWidth(20)
my_monitor.setDistance(100)
my_monitor.saveMon()

mon1 = monitors.Monitor(name='Dell')
mon1.setWidth(52.5)
mon1.setDistance(50)
mon1.setSizePix((3840, 2160))
mon1.saveMon()

# Secondary Dell Monitor

mon2 = monitors.Monitor(name='Dell2')
mon2.setWidth(47.8)
mon2.setDistance(50)
mon2.setSizePix((1680, 1050))
mon2.saveMon()

# Lenovo Monitor

mon3 = monitors.Monitor(name='Lonovo')
mon3.setWidth(52)
mon3.setDistance(50)
mon3.setSizePix((1920, 1200))
mon3.saveMon()

# viewpix Monitor

mon4 = monitors.Monitor(name='viewpix')
mon4.setWidth(51)
mon4.setDistance(50)
mon4.setSizePix((1920, 1080))
mon4.saveMon()


monitorInfo = [mon4.name, mon3.name, mon2.name, mon1.name]

json_write(Path('CalibrationFiles'), monitorInfo, 'monitorinfo')
