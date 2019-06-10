from pathlib import Path
import json
import sys


def init():

    global participantID, folders, defaultVals, thermodeInfo, monitorInfo
    global startTime, selectedThermode
    global currentTemp, ratingCollected, currentRating, progStatus
    global targetTemp, changeProg
    global buttonState, cancelProg, text
    global buttonColour, buttonArray
    global monitor, vEEG, vThermode
    global availaleCOMportsThermode, availaleCOMportsEEG

    cancelProg, changeProg, ratingCollected = False, False, False

    startTime, currentTemp, targetTemp = [], [], []
    participantID, currentRating, defaultVals = [], [], []
    vEEG, vThermode = [], []

    text = ''
    monitor = ''
    if sys.platform == 'win32':
        availaleCOMportsThermode = {
            'none': False,
            'COM1': False,
            'COM4': False,
            'COM5': False,
            'COM6': False
        }
    elif sys.platform == 'linux':
        availaleCOMportsThermode = {
            'none': False,
            '/dev/ttyUSB0': False,
            '/dev/ttyUSB1': False
        }

    availaleCOMportsEEG = {
        'none': False,
        'COM1': False,
        'COM4': False,
        'COM5': False,
        'COM6': False
    }

    folders = {
        'calibration': [],
        'data': [],
        'logs': []
    }
    buttonState = {
        'PracticeRun': False,
        'CalibrationRun': False,
        'HPEEGRun': False,
        'HPEEGRand1Run': False,
        'HPEEGRand2Run': False,
        'PreCapRun': False,
        'TrainingRun': False,
        'PreHeatRun': False
    }
    buttonColour = {
        'preClick': ['mediumorchid', 'plum'],
        'postClick': ['darkgray', 'darkgray'],
        'postRun': ['thistle', 'thistle'],
    }
    buttonArray = {}
    progStatus = {
        'name': '',
        'prevTemp': [],
        'nextTemp': [],
        'timeLeft': []
    }
    thermodeInfo = json_read(Path('CalibrationFiles'), 'thermodeinfo')
    monitorInfo = json_read(Path('CalibrationFiles'), 'monitorinfo')


def json_read(data_folder, fileName):
    DataFile = Path(data_folder / (fileName + '.json'))
    with open(DataFile, 'r') as filehandle:
        data = json.load(filehandle)
    return data
