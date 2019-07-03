import json
from pathlib import Path
calibration_folder = Path('./CalibrationFiles')


def json_write(data, namelist):
    file_to_open = Path('./CalibrationFiles') / (namelist + '.json')
    with open(file_to_open, 'w') as filehandle:
        json.dump(data, filehandle)


def initialise_thermodes():
    thermodeInfo = [{
        'name': 'thermode_v5',
        'OffSetTemp_DA': 366,
        'ScaleFactorTemp_DA': 45.8,
        'OffSetSlope_DA': -48,
        'ScaleFactorSlope_DA': 437,
        'OffSetTemp_AD': 27,
        'ScaleFactorTemp_AD': 69.1
    }, {
        'name': 'thermode_fMRI',
        'OffSetTemp_DA': 420,
        'ScaleFactorTemp_DA': 45.0,
        'OffSetSlope_DA': -66,
        'ScaleFactorSlope_DA': 437,
        'OffSetTemp_AD': 92,
        'ScaleFactorTemp_AD': 68.6
    }]
    json_write(thermodeInfo, 'thermodeInfo')


initialise_thermodes()


def initialise_vals():
    # Initial data
    startingdata = {
        'baselineTemperature': 25.,
        'Slope': 5.,
        'RestTime': 30.,
        'HoldTime': 5.,
        'tolerance': 0.4,
    }
    json_write(startingdata, 'startingdata')

    # Training data
    trainingdata = {
        'startingTemperature': 38.,
        'NoxiousTemps': (43., 46., 49.),
        'Slope': 5.,
        'RestTime': 30.,
        'HoldTime': 5.,
    }
    json_write(trainingdata, 'trainingdata')

    # PreCap data
    precapdata = {
        'startingTemperature': 38.,
        'NoxiousTemps': (43., 44., 45., 46., 47., 48., 49., 50.),
        # 'NoxiousTemps': (43., 44.),
        'Slope': 5.,
        'RestTime': 30.,
        'HoldTime': 5.,
    }
    json_write(precapdata, 'precapdata')

    # PreHeat data
    preheatdata = {
        'startingTemperature': 38.,
        'NoxiousTemp': 45.,
        'Slope': 3.,
        'RestTime': 30.,
        'HoldTime': 300.,
    }
    json_write(preheatdata, 'preheatdata')

    # Calibration data
    calibrationdata = {
        'startingTemperature': 25.,
        'FirstNoxiousTemp': 31.,
        'Slope': 5.,
        'RestTime': 30.,
        'HoldTime': 5.,
        'maxSamples': 12
    }
    json_write(calibrationdata, 'calibrationdata')


def initialise():
    initialise_thermodes()
    initialise_vals()
