import pickle
from pathlib import Path
calibration_folder = Path('E:/ThermodeProject/CalibrationFiles')


def pkl_save(var, file_Name):
    fileObject = open((calibration_folder / file_Name), 'wb')
    pickle.dump(var, fileObject)
    fileObject.close()


def initialise_thermodes():
    thermode_v5 = {
        'OffSetTemp_DA': 366,
        'ScaleFactorTemp_DA': 45.8,
        'OffSetSlope_DA': -48,
        'ScaleFactorSlope_DA': 437,
        'OffSetTemp_AD': 27,
        'ScaleFactorTemp_AD': 69.1
    }
    pkl_save(thermode_v5, 'RegularThermode_v5')

    thermode_fMRI = {
        'OffSetTemp_DA': 420,
        'ScaleFactorTemp_DA': 45.0,
        'OffSetSlope_DA': -66,
        'ScaleFactorSlope_DA': 437,
        'OffSetTemp_AD': 92,
        'ScaleFactorTemp_AD': 68.6
    }
    pkl_save(thermode_fMRI, 'fMRIThermode')

def initialise_vals():
    # Initial data
    startingdata = {
        'baselineTemperature': 25.,
        'Slope': 5.,
        'RestTime': 30.,
        'HoldTime': 5.,
        'tolerance': 0.4,
    }
    pkl_save(startingdata, 'startingdata')

    # Training data
    trainingdata = {
        'startingTemperature': 38.,
        'NoxiousTemps': (43., 46., 49.),
        'Slope': 5.,
        'RestTime': 30.,
        'HoldTime': 5.,
    }
    pkl_save(trainingdata, 'trainingdata')

    # PreCap data
    precapdata = {
        'startingTemperature': 38.,
        'NoxiousTemps': (43., 44., 45., 46., 47., 48., 49., 50.),
        'Slope': 5.,
        'RestTime': 30.,
        'HoldTime': 5.,
    }
    pkl_save(precapdata, 'precapdata')

    # PreHeat data
    preheatdata = {
        'startingTemperature': 38.,
        'NoxiousTemp': 45.,
        'Slope': 3.,
        'RestTime': 30.,
        'HoldTime': 300.,
    }
    pkl_save(preheatdata, 'preheatdata')

    # Calibration data
    calibrationdata = {
        'startingTemperature': 25.,
        'FirstNoxiousTemp': 31.,
        'Slope': 5.,
        'RestTime': 30.,
        'HoldTime': 5.,
        'maxSamples': 12
    }
    pkl_save(calibrationdata, 'calibrationdata')