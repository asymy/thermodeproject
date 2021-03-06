import numpy as np
import time

# Personal
from EEGControl import EEGControl
from generalfunc import general
from CalibrationPlot import CalibratedPlot_Participant
from stopThreadclass import StoppableThread
import vals
import config


config.init()
gen = general()
vals.initialise()
EEGControl = EEGControl()


class MyHeatPainProgramme(StoppableThread):

    def __init__(self):
        config.buttonState = {
            'PracticeRun': False,
            'CalibrationRun': False,
            'HPEEGRun': False,
            'HPEEGRand1Run': False,
            'HPEEGRand2Run': False,
            'PreCapRun': False,
            'TrainingRun': False,
            'PreHeatRun': False
        }
        StoppableThread.__init__(self)

        startingVals = gen.json_read(
            config.folders['calibration'], 'startingdata')
        config.defaultVals = startingVals
        config.targetTemp = config.defaultVals['baselineTemperature']
        config.changeProg = True

        self.allRatings = []
        self.EEG = False

    def run(self):
        while not self.stopped():
            if config.buttonState['PracticeRun']:
                self.Practice()
            elif config.buttonState['TrainingRun']:
                self.Training()
            elif config.buttonState['CalibrationRun']:
                self.Calibration()
            elif config.buttonState['HPEEGRun']:
                self.EEGAscend()
            elif config.buttonState['HPEEGRand1Run']:
                self.EEGRand(1)
            elif config.buttonState['HPEEGRand2Run']:
                self.EEGRand(2)
            elif config.buttonState['PreCapRun']:
                self.PreCapHP()
            elif config.buttonState['PreHeatRun']:
                self.PreHeat()
            else:
                time.sleep(0.1)

    def HeatPainRun(self, baselineTemp, noxioustemps, holdTimes):
        self.allRatings = []
        gen.wait(2)
        config.text = '+'
        gen.wait(2)
        # Set temperature to baseline temp, check it has reached this, send
        # EEG trigger, hold for rest period.
        # set temperature to noxious temp, send EEG trigger, check it as
        # reached temp, send another EEG trigger
        # wait for hold period, send another EEG trigger, set temp back to
        # baseline, check it has reached, send another EEG trigger
        # loop back to begining, and do for all noxious temps
        self.setandcheck(baselineTemp)
        T = time.time()
        EEGControl.EEGTrigger(11)
        config.progStatus['nextTemp'] = noxioustemps[0]
        gen.wait(5)
        gen.timer(T, config.defaultVals['RestTime'])
        EEGControl.EEGTrigger(12)
        for x in range(len(noxioustemps)):
            self.setandcheck(noxioustemps[x])
            T = time.time()
            EEGControl.EEGTrigger(13)
            gen.timer(T, holdTimes[x])
            EEGControl.EEGTrigger(14)
            self.setandcheck(baselineTemp)
            T = time.time()
            EEGControl.EEGTrigger(11)
            gen.wait(5)
            EEGControl.EEGTrigger(15)
            config.ratingCollected = False
            config.text = 'rt'
            while (config.ratingCollected is False and
                   config.cancelProg is False):
                gen.wait(0.05)
            gen.wait(.5)
            config.progStatus['prevTemp'] = noxioustemps[x]
            if x < len(noxioustemps)-1:
                config.progStatus['nextTemp'] = noxioustemps[x+1]
            else:
                config.progStatus['nextTemp'] = 'NaN'
            gen.timer(T, config.defaultVals['RestTime'])
            if not config.cancelProg:
                self.allRatings = np.append(
                    self.allRatings, config.currentRating)
                EEGControl.EEGTrigger(12)
            else:
                break
            if not self.EEG:
                if config.currentRating >= 8:
                    break
            elif self.EEG:
                if config.currentRating > 8:
                    break

    def Practice(self):
        config.progStatus['name'] = 'Practice'
        messages = (('During the stimulation a fixation cross will appear on '
                     'the screen.\nPlease relax, and focus on the cross when '
                     'it is on the screen.\nAn example of the cross is on the '
                     'next screen.'),
                    ('After the Heat Stimulus, a rating scale will appear on '
                     'the screen.\nClick on the line with the mouse, and drag '
                     'the marker to change your selection.\nClick on the '
                     'button to confirm your answer.'),
                    ('You are now experiencing no pain, '
                     'please use the scale to indicate this.'),
                    ('You are now experiencing mild pain, '
                     'please use the scale to indicate this.'),
                    ('You are now experiencing extreme pain, '
                     'please use the scale to indicate this.'))
        stim = ('+', 'rt', 'rt', 'rt', 'rt')
        for x in range(len(messages)):
            if not config.cancelProg:
                config.text = messages[x]
                gen.wait(10)
                config.text = stim[x]
                if x == 0:
                    gen.wait(2)
                else:
                    while (config.ratingCollected is False and
                           config.cancelProg is False):
                        gen.wait(0.05)
                    config.ratingCollected = False
                    gen.wait(2)
        config.text = ''
        config.buttonArray['Practice'].color = (
            config.buttonColour['postRun'][0])
        config.buttonArray['Practice'].hovercolor = (
            config.buttonColour['postRun'][1])
        self.SetButtonFalse()

    def Training(self):
        config.progStatus['name'] = 'Training'
        trainingData = gen.json_read(
            config.folders['calibration'], 'trainingdata')
        startingTemperature = trainingData['startingTemperature']
        noxioustemps = trainingData['NoxiousTemps']

        holdTimes = np.ones_like(noxioustemps)*trainingData['HoldTime']
        config.text = "Starting Training Session"
        self.HeatPainRun(startingTemperature, noxioustemps, holdTimes)
        config.buttonArray['Training'].color = (
            config.buttonColour['postRun'][0])
        config.buttonArray['Training'].hovercolor = (
            config.buttonColour['postRun'][1])
        self.SetButtonFalse()

    def PreCapHP(self):
        config.progStatus['name'] = 'Pre-Capsaicin'
        preCapData = gen.json_read(config.folders['calibration'], 'precapdata')
        startingTemperature = preCapData['startingTemperature']
        noxioustemps = preCapData['NoxiousTemps']
        holdTimes = np.ones_like(noxioustemps)*preCapData['HoldTime']
        config.text = "Starting Pre-Treatment Session"
        self.HeatPainRun(startingTemperature, noxioustemps, holdTimes)
        if len(self.allRatings) is not 0:
            data = {
                'noxioustemps': noxioustemps,
                'painRatings': self.allRatings.tolist()
            }
            fileName = ('PreCapPainRatings' + '_Participant' +
                        config.participantID)
            gen.json_write(config.folders['data'], data, fileName)
        config.buttonArray['PreCap'].color = (
            config.buttonColour['postRun'][0])
        config.buttonArray['PreCap'].hovercolor = (
            config.buttonColour['postRun'][1])
        self.SetButtonFalse()

    def PreHeat(self):
        config.progStatus['name'] = 'Pre-Heat'
        preHeatData = gen.json_read(
            config.folders['calibration'], 'preheatdata')
        noxioustemps = preHeatData['NoxiousTemp']
        startingTemp = preHeatData['startingTemperature']
        holdTimes = preHeatData['HoldTime']
        # restTime = preHeatData['RestTime']
        # slope = preHeatData['Slope']
        sample = 60
        self.allRatings = []

        config.text = "Starting Pre-Heat Session"
        self.setandcheck(startingTemp)
        T = time.time()
        config.progStatus['nextTemp'] = noxioustemps
        gen.timer(T, 10)
        config.text = '+'
        gen.wait(10)
        self.setandcheck(noxioustemps)
        T = time.time()
        endTime = T + holdTimes
        time_in_s = holdTimes+2
        currentTime = time.time()
        startTime = currentTime
        endTime = startTime + time_in_s
        config.progStatus['prevTemp'] = noxioustemps
        config.progStatus['nextTemp'] = startingTemp
        config.progStatus['timeLeft'] = endTime - currentTime
        while currentTime < endTime and config.cancelProg is False:
            if np.around(
                    config.progStatus['timeLeft']-1, decimals=0) % sample == 0:
                config.ratingCollected = False
                config.text = 'rt'
                while (config.ratingCollected is False and
                       config.cancelProg is False):
                    gen.wait(0.05)
                    currentTime = time.time()
                    config.progStatus['timeLeft'] = np.around(
                        endTime - currentTime, decimals=1)
                gen.wait(.5)

                self.allRatings = np.append(
                    self.allRatings, config.currentRating)
            else:
                gen.wait(0.05)
                currentTime = time.time()

                config.progStatus['timeLeft'] = np.around(
                    endTime - currentTime, decimals=1)
        print('Apply Capsaicin')
        self.setandcheck(startingTemp)
        if len(self.allRatings) is not 0:
            data = {
                'painRating': self.allRatings.tolist()
            }
            fileName = ('PreHeatRatings_Participant' +
                        config.participantID)
            gen.json_write(config.folders['data'], data, fileName)
        gen.wait(20)
        config.buttonArray['preHeat'].color = (
            config.buttonColour['postRun'][0])
        config.buttonArray['preHeat'].hovercolor = (
            config.buttonColour['postRun'][1])
        self.SetButtonFalse()

    def Calibration(self):
        config.progStatus['name'] = 'Calibration'
        caliData = gen.json_read(
            config.folders['calibration'], 'calibrationdata')
        nextTemp = caliData['FirstNoxiousTemp']
        noxioustemps = []
        startingTemp = caliData['startingTemperature']
        # holdTimes = caliData['HoldTime']
        # restTime = caliData['RestTime']
        # slope = caliData['Slope']
        max_samples = caliData['maxSamples']
        sequence = True
        self.allRatings = []
        config.text = "Now Begining the Calibration Procedure."
        gen.wait(2)
        config.text = '+'
        self.setandcheck(startingTemp)
        Tr = time.time()
        for sample in range(max_samples):
            if not config.cancelProg:
                noxioustemps = np.append(noxioustemps, nextTemp)
                config.progStatus['prevTemp'] = noxioustemps[sample-1]
                config.progStatus['nextTemp'] = nextTemp
                gen.timer(Tr, config.defaultVals['RestTime'])
                self.setandcheck(noxioustemps[sample])
                Tn = time.time()
                gen.timer(Tn, config.defaultVals['HoldTime'])
            if not config.cancelProg:
                self.setandcheck(startingTemp)
                Tr = time.time()
                gen.wait(3)
                config.text = 'rt'
                config.ratingCollected = False
            while (config.ratingCollected is False and
                   config.cancelProg is False):
                gen.wait(0.5)
            if not config.cancelProg:
                self.allRatings = np.append(
                    self.allRatings, config.currentRating)
                # not enough samples to perform linear regression
                if len(self.allRatings) < 3.:  # sample < 2 or
                    if config.currentRating < 1.:
                        nextTemp = noxioustemps[sample] + 3
                    elif config.currentRating <= 3.:
                        nextTemp = noxioustemps[sample] + 1
                    elif (config.currentRating >= 3. and
                          config.currentRating < 8.):
                        nextTemp = noxioustemps[sample] + .5
                    elif config.currentRating >= 8.:
                        nextTemp = noxioustemps[sample] - 2
                else:
                    if config.currentRating < 8. and sequence:
                        targetRating = config.currentRating+1
                        if targetRating > 8:
                            targetRating = 8.
                        nextTemp = gen.predict_val(
                            self.allRatings, noxioustemps, targetRating)
                        print('\ttarget rating: ' + str(targetRating))
                    else:
                        nextRating = gen.findmissingvals(self.allRatings)
                        sequence = False
                        if nextRating == 9:
                            break
                        else:
                            nextTemp = gen.predict_val(
                                self.allRatings, noxioustemps, nextRating)

                nextTemp = np.around(nextTemp, decimals=1)
                gen.wait(1)
                if nextTemp > 50.0:
                    nextTemp = 50.0
        if len(self.allRatings) is not 0:
            data = {
                'noxioustemps': noxioustemps.tolist(),
                'painRatings': self.allRatings.tolist()
            }
            fileName = ('CalibratedResults_Participant' +
                        config.participantID)
            gen.json_write(config.folders['data'], data, fileName)

            targetRating = np.array([1, 2, 3, 4, 5, 6, 7, 8])
            newTempsAscend = np.around(gen.make_model(
                self.allRatings, noxioustemps, targetRating), decimals=1)
            i = np.where(newTempsAscend > 50.)
            newTempsAscend[i[0]] = 50.

            targetRating = np.array(
                [1., 2., 3., 4., 5., 6., 6.5, 7., 7.5, 8., 8.])
            newTempsRand = np.around(gen.make_model(
                self.allRatings, noxioustemps, targetRating), decimals=1)
            i = np.where(newTempsRand > 50.)
            newTempsRand[i[0]] = 50.

            data = {
                'EEGAscendTemps': newTempsAscend.tolist(),
                'EEGRandTemps': newTempsRand.tolist()
            }
            fileName = ('EEGTemps_Participant' +
                        config.participantID)
            gen.json_write(config.folders['data'], data, fileName)

        gen.timer(Tr, config.defaultVals['RestTime'])
        config.buttonArray['Calibration'].color = (
            config.buttonColour['postRun'][0])
        config.buttonArray['Calibration'].hovercolor = (
            config.buttonColour['postRun'][1])
        try:
            CalibratedPlot_Participant(config.participantID)
        except FileNotFoundError:
            print('Unable to plot Calibration graph.')
        self.SetButtonFalse()

    def EEGAscend(self):
        config.progStatus['name'] = 'EEG Ascend'
        try:
            data_folder = config.folders['data']
            fileName = ('EEGTemps_Participant' +
                        config.participantID)
            EEGtemps = gen.json_read(data_folder, fileName)
            noxioustemps = EEGtemps['EEGAscendTemps']
            # noxioustemps = [31.0, 32.0, 32.5, 33.0, 33.5, 34, 34.5, 35.0]
            baselineTemp = 25
            holdTimes = np.linspace(10, 10, len(noxioustemps))
            config.text = "Starting EEG Run 1"

            preheattemp = noxioustemps[3]  # should be pain rating of 4
            config.text = '+'
            gen.wait(5)
            self.setandcheck(preheattemp)
            T = time.time()
            config.progStatus['nextTemp'] = noxioustemps[0]
            gen.timer(T, 60)  # pre-heat period of one minute
            self.setandcheck(baselineTemp)

            self.EEG = True
            self.HeatPainRun(baselineTemp, noxioustemps, holdTimes)
            if len(self.allRatings) is not 0:
                fileName = ('EEGRun1PainRatings_Participant' +
                            config.participantID)
                file_to_open = config.folders['data']
                gen.json_write(
                    file_to_open,
                    self.allRatings.tolist(),
                    fileName
                    )
            self.SetButtonFalse()
        except FileNotFoundError as fnf_error:
            print(fnf_error)
        config.buttonArray['EEGAscend'].color = (
            config.buttonColour['postRun'][0])
        config.buttonArray['EEGAscend'].hovercolor = (
            config.buttonColour['postRun'][1])
        self.SetButtonFalse()

    def EEGRand(self, num):
        data_folder = config.folders['data']
        fileName = ('EEGTemps_Participant' +
                    config.participantID)
        EEGtemps = gen.json_read(data_folder, fileName)
        temps = EEGtemps['EEGRandTemps']
        baselineTemp = 25
        Times = np.linspace(10, 10, len(temps))
        if num == 1:
            index = [4, 7, 8, 0, 6, 10, 3, 1, 5, 9, 2]
            config.text = "Starting EEG Run 2"
            config.progStatus['name'] = 'EEG Rand 1'
        elif num == 2:
            index = [5, 8, 10, 0, 4, 6, 9, 2, 1, 3, 7]
            config.text = "Starting EEG Run 3"
            config.progStatus['name'] = 'EEG Rand 2'
        noxioustemps = np.zeros_like(index, dtype=float)
        holdTimes = np.zeros_like(index)
        for x in range(len(index)):
            i = index[x]
            noxioustemps[x] = np.around(temps[i], decimals=1)
            holdTimes[x] = Times[i]

        preheattemp = temps[3]  # should be pain rating of 4
        config.text = '+'
        gen.wait(5)
        self.setandcheck(preheattemp)
        T = time.time()
        config.progStatus['nextTemp'] = noxioustemps[0]
        gen.timer(T, 60)  # pre-heat period of one minute
        self.setandcheck(baselineTemp)

        self.EEG = True
        self.HeatPainRun(baselineTemp, noxioustemps, holdTimes)
        if num == 1:
            if len(self.allRatings) is not 0:
                fileName = ('EEGRand1PainRatings_Participant' +
                            config.participantID)
                file_to_open = config.folders['data']
                gen.json_write(
                    file_to_open,
                    self.allRatings.tolist(),
                    fileName
                    )
            config.buttonArray['EEGRand1'].color = (
                config.buttonColour['postRun'][0])
            config.buttonArray['EEGRand1'].hovercolor = (
                config.buttonColour['postRun'][1])
        elif num == 2:
            if len(self.allRatings) is not 0:
                fileName = ('EEGRand2PainRatings_Participant' +
                            config.participantID)
                file_to_open = config.folders['data']
                gen.json_write(
                    file_to_open,
                    self.allRatings.tolist(),
                    fileName
                    )
            config.buttonArray['EEGRand2'].color = (
                config.buttonColour['postRun'][0])
            config.buttonArray['EEGRand2'].hovercolor = (
                config.buttonColour['postRun'][1])
        self.SetButtonFalse()

    def SetButtonFalse(self):
        config.text = 'Session Finished'
        config.targetTemp = config.defaultVals['baselineTemperature']
        config.changeProg = True
        config.text = ''
        config.currentRating = []
        self.allRatings = []
        config.buttonState = {
            'PracticeRun': False,
            'CalibrationRun': False,
            'HPEEGRun': False,
            'HPEEGRand1Run': False,
            'HPEEGRand2Run': False,
            'PreCapRun': False,
            'TrainingRun': False,
            'PreHeatRun': False

        }
        config.progStatus = {
            'name': '',
            'prevTemp': [],
            'nextTemp': [],
            'timeLeft': []
        }
        config.cancelProg = False

    def setandcheck(self, temp):
        if not config.cancelProg:
            config.targetTemp = temp
            config.changeProg = True
            while (config.currentTemp >=
                   (config.targetTemp + config.defaultVals['tolerance']) or
                   config.currentTemp <=
                   (config.targetTemp - config.defaultVals['tolerance'])):
                gen.wait(0.1)
