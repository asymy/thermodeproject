import config
from pathlib import Path


def setup():
    config.participantID = input('Enter the Participant ID: ')
    config.folders['data'] = Path(
        'ParticipantFiles/Participant_' + config.participantID)
    config.folders['calibration'] = Path('E:/ThermodeProject/CalibrationFiles')
    config.folders['log'] = Path('logs')
    config.folders['data'].mkdir(parents=True, exist_ok=True)

    Thermode = input(
        '\nChoose the thermode: 0 = RegularThermode_v5, 1 = fMRI Thermode: ')
    if Thermode == '0':
        config.selectedThermode = 'RegularThermode_v5'
    elif Thermode == '1':
        config.selectedThermode = 'fMRIThermode'
    else:
        config.selectedThermode = 'RegularThermode_v5'
    print('Thermode Selected: ' + config.selectedThermode)

    Monitor = input(
        '\nChoose the Monitor: 0 = Lonovo, 1 = Dell: ')
    if Monitor == '0':
        monitorName = 'Lonovo'
    elif Monitor == '1':
        monitorName = 'Dell'
    else:
        monitorName = 'Lonovo'
    print('Monitor Selected: ' + monitorName + '\n')
