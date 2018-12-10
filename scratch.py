import vals
import pickle
from pathlib import Path
calibration_folder = Path('E:/ThermodeProject/CalibrationFiles')

vals.initialise_thermodes()

Thermode = calibration_folder / ('RegularThermode_v5')
fileObject = open(Thermode,'rb')  
# load the object from the file into var b
Thermode = pickle.load(fileObject) 
fileObject.close()


