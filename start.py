import pickle
from pathlib import Path
calibration_folder = Path('E:/ThermodeProject/CalibrationFiles')
def pkl_save(var, file_Name):
    fileObject = open((calibration_folder / file_Name), 'wb')
    pickle.dump(var, fileObject)
    fileObject.close()

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
        'HoldTime': 5.,
    }
    pkl_save(preheatdata, 'preheatdata')

    # Calibration data
    calibrationdata = {
        'startingTemperature': 25.,
        'FirstNoxiousTemp': 30.,
        'Slope': 5.,
        'RestTime': 30.,
        'HoldTime': 5.,
    }
    pkl_save(calibrationdata, 'calibrationdata')