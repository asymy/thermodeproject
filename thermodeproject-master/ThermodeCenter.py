import json

# Normal Thermode
OffSetTemp_DA = 366
ScaleFactorTemp_DA = 458
OffSetSlope_DA = -48
ScaleFactorSlope_DA = 437
OffSetTemp_AD = 27
ScaleFactorTemp_AD = 691

List = OffSetTemp_DA, ScaleFactorTemp_DA, OffSetSlope_DA, ScaleFactorSlope_DA, OffSetTemp_AD, ScaleFactorTemp_AD

file_to_open = 'RegularThermode_v5.json'
with open(file_to_open, 'w') as filehandle:
    json.dump(List, filehandle)

# fMRI Thermode
OffSetTemp_DA = 420
ScaleFactorTemp_DA = 450
OffSetSlope_DA = -66
ScaleFactorSlope_DA = 437
OffSetTemp_AD = 92
ScaleFactorTemp_AD = 686

List = OffSetTemp_DA, ScaleFactorTemp_DA, OffSetSlope_DA, ScaleFactorSlope_DA, OffSetTemp_AD, ScaleFactorTemp_AD

file_to_open = 'fMRIThermode.json'
with open(file_to_open, 'w') as filehandle:
    json.dump(List, filehandle)
