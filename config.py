def init():
    global cancelProg
    global startTime
    global currentTemp
    global targetTemp
    global slope
    global changeProg
    global folders
    global selectedThermode
    global participantID
    global currentRating
    global buttonState
    global ratingCollected
    global defaultVals

    cancelProg = False
    changeProg = False
    ratingCollected = False

    startTime = []
    currentTemp = []
    targetTemp = 25.
    slope = []
    participantID = []
    currentRating = []
    defaultVals = []

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
