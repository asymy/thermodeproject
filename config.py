def init():
    global participantID, folders, defaultVals
    global startTime, selectedThermode
    global currentTemp, ratingCollected, currentRating
    global targetTemp, changeProg
    global buttonState, cancelProg, text
    global buttonColour, buttonArray

    cancelProg, changeProg, ratingCollected = False, False, False

    startTime, currentTemp, targetTemp = [], [], []
    participantID, currentRating, defaultVals = [], [], []

    text = ''

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
        'postClick': [[1, 0, 0, 0.9], [1, 0, 0, 0.6]],
        'postRun': [[0, 1, 0, 0.9], [0, 1, 0, 0.6]]
    }
    buttonArray = {}
